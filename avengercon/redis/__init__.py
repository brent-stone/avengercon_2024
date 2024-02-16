"""
Redis client and related functionality
"""

from typing import Optional

from redis import Redis
from redis import RedisError
from redis import from_url

from avengercon.logger import logger
from avengercon.redis.config import redis_config


def get_redis_client() -> Optional[Redis[str]]:
    """
    Get Redis client instance

    Returns: Redis client object; None upon error
    """
    try:
        redis_client: Redis[str] = from_url(
            url=redis_config.redis_dsn,
            decode_responses=True,
        )
        if not redis_client.ping():
            raise RedisError("ping failed")
        else:
            logger.debug(
                f"Redis connected at {redis_config.redis_host}:"
                f"{redis_config.redis_port}",
            )
        return redis_client
    except RedisError as e:
        logger.warning(f"Redis connection failed: {e}")
        return None
