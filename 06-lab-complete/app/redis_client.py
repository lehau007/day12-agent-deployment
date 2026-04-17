"""
Redis connection helper.
"""
import redis
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self):
        self._redis = None
        self.use_redis = False

    def connect(self):
        if not settings.redis_url:
            self.use_redis = False
            return False

        try:
            self._redis = redis.from_url(settings.redis_url, decode_responses=True)
            self._redis.ping()
            self.use_redis = True
            print("✅ Connected to Redis")
            return True
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}")
            self.use_redis = False
            return False

    def get_client(self):
        return self._redis

redis_manager = RedisManager()
# Connect once at module level or during lifespan
redis_manager.connect()
