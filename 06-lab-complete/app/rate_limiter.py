"""
Redis-based Rate Limiter
Falls back to in-memory if Redis is not available.
"""
import time
from collections import defaultdict, deque
from fastapi import HTTPException
from app.config import settings

from app.redis_client import redis_manager

# Use shared Redis client
_redis = redis_manager.get_client()
USE_REDIS = redis_manager.use_redis

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._windows: dict[str, deque] = defaultdict(deque)

    def check(self, user_id: str):
        if USE_REDIS:
            return self._check_redis(user_id)
        else:
            return self._check_memory(user_id)

    def _check_redis(self, user_id: str):
        key = f"rate_limit:{user_id}"
        now = time.time()
        
        # Use Redis pipeline for atomic operations
        pipe = _redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - self.window_seconds)
        pipe.zcard(key)
        pipe.zadd(key, {str(now): now})
        pipe.expire(key, self.window_seconds)
        results = pipe.execute()
        
        current_requests = results[1]
        if current_requests >= self.max_requests:
            # Clean up the extra entry we just added if we exceeded
            _redis.zrem(key, str(now))
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {self.max_requests} req/min",
                headers={"Retry-After": str(self.window_seconds)},
            )

    def _check_memory(self, user_id: str):
        now = time.time()
        window = self._windows[user_id]
        while window and window[0] < now - self.window_seconds:
            window.popleft()
        
        if len(window) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {self.max_requests} req/min",
                headers={"Retry-After": "60"},
            )
        window.append(now)

# Singleton instance
limiter = RateLimiter(max_requests=settings.rate_limit_per_minute)
