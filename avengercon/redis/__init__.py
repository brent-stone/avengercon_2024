"""
Redis client and related functionality
"""

# This __future__ import annotations is needed to reconcile the 3.11 Python interpreter
# from being upset at function declaration time about clarifying the Redis generic as
# Redis[str] vs mypy being upset that the Redis type is left as a generic and needs to
# be clarified. PEP 563 proposes the deferred evaluation of type annotations as default
# behavior; however, this explicit import is needed to trigger that behavior in 3.11
# https://peps.python.org/pep-0563/
# https://discuss.python.org/t/type-annotations-pep-649-and-pep-563/11363/1
from __future__ import annotations
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
