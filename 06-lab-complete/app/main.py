"""
Production AI Agent — Final Project Part 6
Combines: Config, Docker, Auth, Rate Limiting, Cost Guard, Scaling & Reliability.
"""
import os
import time
import signal
import logging
import json
import uuid
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from app.config import settings
from app.auth import verify_api_key
from app.rate_limiter import limiter
from app.cost_guard import cost_guard
from utils.google_llm import ask as llm_ask

# ─────────────────────────────────────────────────────────
# Redis Storage for Stateless Session (History)
# ─────────────────────────────────────────────────────────
from app.redis_client import redis_manager

_redis = redis_manager.get_client()
USE_REDIS = redis_manager.use_redis

if not USE_REDIS:
    _memory_history = {}

def get_history(session_id: str) -> list:
    if USE_REDIS:
        data = _redis.get(f"history:{session_id}")
        return json.loads(data) if data else []
    return _memory_history.get(session_id, [])

def save_history(session_id: str, history: list):
    if len(history) > 20: history = history[-20:] # Keep last 10 turns
    if USE_REDIS:
        _redis.setex(f"history:{session_id}", 3600 * 24, json.dumps(history))
    else:
        _memory_history[session_id] = history

# ─────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False

# ─────────────────────────────────────────────────────────
# Lifespan
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info(json.dumps({"event": "startup", "app": settings.app_name}))
    _is_ready = True
    yield
    _is_ready = False
    logger.info(json.dumps({"event": "shutdown"}))

# ─────────────────────────────────────────────────────────
# App & Middleware
# ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

# ─────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    session_id: str | None = None

class AskResponse(BaseModel):
    question: str
    answer: str
    session_id: str
    model: str
    timestamp: str

# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────

@app.get("/health", tags=["Ops"])
def health():
    return {
        "status": "ok",
        "uptime": round(time.time() - START_TIME, 1),
        "redis_connected": USE_REDIS
    }

@app.get("/ready", tags=["Ops"])
def ready():
    if not _is_ready: raise HTTPException(503, "Not ready")
    if USE_REDIS:
        try: _redis.ping()
        except: raise HTTPException(503, "Redis disconnected")
    return {"ready": True}

@app.post("/ask", response_model=AskResponse, tags=["Agent"])
async def ask_agent(
    body: AskRequest,
    _key: str = Depends(verify_api_key),
):
    # 1. Rate Limit
    limiter.check(_key[:8])

    # 2. Budget Check
    cost_guard.check_budget(_key[:8])

    # 3. Session Management
    session_id = body.session_id or str(uuid.uuid4())
    history = get_history(session_id)
    
    # Simple history context for LLM
    context = ""
    for msg in history[-4:]: # Use last 2 turns as context
        context += f"{msg['role']}: {msg['content']}\n"
    full_prompt = f"{context}user: {body.question}"

    # 4. LLM Call
    input_tokens = len(full_prompt.split()) * 2
    try:
        answer = llm_ask(full_prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("LLM request failed")
        raise HTTPException(status_code=502, detail="LLM provider error") from exc
    output_tokens = len(answer.split()) * 2

    # 5. Record Usage
    cost_guard.record_usage(_key[:8], input_tokens, output_tokens)

    # 6. Update History
    history.append({"role": "user", "content": body.question})
    history.append({"role": "assistant", "content": answer})
    save_history(session_id, history)

    return AskResponse(
        question=body.question,
        answer=answer,
        session_id=session_id,
        model=settings.llm_model,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

@app.get("/history/{session_id}", tags=["Agent"])
def view_history(session_id: str, _key: str = Depends(verify_api_key)):
    return {"session_id": session_id, "history": get_history(session_id)}

# ─────────────────────────────────────────────────────────
# Graceful Shutdown
# ─────────────────────────────────────────────────────────
def _handle_signal(signum, _frame):
    logger.info(f"Received signal {signum}, shutting down...")

signal.signal(signal.SIGTERM, _handle_signal)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        timeout_graceful_shutdown=30,
    )
