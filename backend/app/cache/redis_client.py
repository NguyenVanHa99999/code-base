import redis
import json
import logging
from typing import Any, Optional
from core.config import settings

logger = logging.getLogger(__name__)

# Lấy thông tin kết nối Redis từ cấu hình
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None
DEFAULT_TTL = settings.REDIS_DEFAULT_TTL

try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    redis_client.ping()
    logger.info(f"Redis connected: {REDIS_HOST}:{REDIS_PORT}")
except redis.ConnectionError as e:
    logger.warning(f"Redis unavailable, using in-memory fallback: {e}")
    
    class DummyRedis:
        """Fallback in-memory cache when Redis is not available"""
        def __init__(self):
            self._cache = {}
        
        def set(self, key, value, *args, **kwargs):
            self._cache[key] = value
            return True

        def setex(self, key, ttl, value):
            self._cache[key] = value
            return True

        def get(self, key, *args, **kwargs):
            return self._cache.get(key)

        def delete(self, key, *args, **kwargs):
            if key in self._cache:
                del self._cache[key]
                return 1
            return 0
            
        def flushdb(self, *args, **kwargs):
            self._cache.clear()
            return True

    redis_client = DummyRedis()


def set_cache(key: str, value: Any, ttl: int = DEFAULT_TTL) -> bool:
    """
    Lưu giá trị vào Redis cache
    
    Args:
        key: Khóa để lưu trữ giá trị
        value: Giá trị cần lưu (sẽ tự động chuyển thành JSON)
        ttl: Thời gian sống của key (giây), mặc định là 1 giờ
        
    Returns:
        bool: True nếu lưu thành công, False nếu có lỗi
    """
    try:
        serialized_value = json.dumps(value) if not isinstance(value, (str, int, float, bool)) else value
        return redis_client.set(key, serialized_value, ex=ttl)
    except Exception as e:
        logger.error(f"Cache set error: {e}")
        return False


def get_cache(key: str) -> Optional[Any]:
    """
    Lấy giá trị từ Redis cache
    
    Args:
        key: Khóa cần lấy giá trị
        
    Returns:
        Any: Giá trị của key hoặc None nếu không tìm thấy
    """
    try:
        value = redis_client.get(key)
        if value is None:
            return None
        
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    except Exception as e:
        logger.error(f"Cache get error: {e}")
        return None


def delete_cache(key: str) -> bool:
    """
    Xóa giá trị khỏi Redis cache
    
    Args:
        key: Khóa cần xóa
        
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    try:
        return bool(redis_client.delete(key))
    except Exception as e:
        logger.error(f"Cache delete error: {e}")
        return False


def flush_cache() -> bool:
    """
    Xóa toàn bộ cache (chỉ sử dụng trong môi trường phát triển)
    
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    try:
        return redis_client.flushdb()
    except Exception as e:
        logger.error(f"Cache flush error: {e}")
        return False
