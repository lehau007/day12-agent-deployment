"""
Redis-based Cost Guard
Protects budget by tracking token usage per user and globally.
"""
import time
import logging
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

# Prices (for reference)
PRICE_PER_1K_INPUT_TOKENS = 0.00015
PRICE_PER_1K_OUTPUT_TOKENS = 0.0006

# Attempt to connect to Redis
try:
    import redis
    if settings.redis_url:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
        _redis.ping()
        USE_REDIS = True
    else:
        USE_REDIS = False
except Exception:
    USE_REDIS = False

class CostGuard:
    def __init__(self, daily_budget_usd: float, global_daily_budget_usd: float):
        self.daily_budget_usd = daily_budget_usd
        self.global_daily_budget_usd = global_daily_budget_usd
        self._memory_daily_cost = 0.0
        self._memory_reset_day = time.strftime("%Y-%m-%d")

    def check_budget(self, user_id: str):
        if USE_REDIS:
            return self._check_redis(user_id)
        else:
            return self._check_memory(user_id)

    def _check_redis(self, user_id: str):
        today = time.strftime("%Y-%m-%d")
        global_key = f"cost:global:{today}"
        user_key = f"cost:user:{user_id}:{today}"
        
        global_cost = float(_redis.get(global_key) or 0.0)
        user_cost = float(_redis.get(user_key) or 0.0)
        
        if global_cost >= self.global_daily_budget_usd:
            raise HTTPException(503, "Global daily budget exhausted.")
        
        if user_cost >= self.daily_budget_usd:
            raise HTTPException(402, "Daily budget exceeded for this user.")

    def _check_memory(self, user_id: str):
        today = time.strftime("%Y-%m-%d")
        if today != self._memory_reset_day:
            self._memory_daily_cost = 0.0
            self._memory_reset_day = today
        
        if self._memory_daily_cost >= self.global_daily_budget_usd:
            raise HTTPException(503, "Global daily budget exhausted.")

    def record_usage(self, user_id: str, input_tokens: int, output_tokens: int):
        cost = (input_tokens / 1000) * PRICE_PER_1K_INPUT_TOKENS + (output_tokens / 1000) * PRICE_PER_1K_OUTPUT_TOKENS
        
        if USE_REDIS:
            today = time.strftime("%Y-%m-%d")
            global_key = f"cost:global:{today}"
            user_key = f"cost:user:{user_id}:{today}"
            
            _redis.incrbyfloat(global_key, cost)
            _redis.expire(global_key, 86400 * 2) # keep 2 days
            _redis.incrbyfloat(user_key, cost)
            _redis.expire(user_key, 86400 * 2)
        else:
            self._memory_daily_cost += cost
        
        return cost

# Singleton instance
cost_guard = CostGuard(
    daily_budget_usd=settings.daily_budget_usd,
    global_daily_budget_usd=settings.global_daily_budget_usd
)
