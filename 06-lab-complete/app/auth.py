"""
Authentication Module for Production AI Agent
Supports both API Key and JWT Authentication.
"""
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

# API Key Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# JWT Security
security = HTTPBearer(auto_error=False)
ALGORITHM = "HS256"

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the X-API-Key header."""
    if not api_key or api_key != settings.agent_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include header: X-API-Key: <key>",
        )
    return api_key

def create_jwt_token(username: str, role: str) -> str:
    """Create a JWT token for a user."""
    payload = {
        "sub": username,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Verify JWT token from Authorization header."""
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Include: Authorization: Bearer <token>",
        )
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")

def get_current_user(
    api_key: str = Depends(verify_api_key),
    # Optional: jwt_user: dict = Depends(verify_jwt_token)
) -> str:
    """
    Combined dependency. For this lab, we mainly use API Key.
    Returns the user identifier.
    """
    # In a real app, you might check if either API Key or JWT is valid.
    # Here we default to using the API Key's prefix as a user identifier if no JWT.
    return "default_user"
