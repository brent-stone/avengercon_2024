"""
Example Redis client tasks
https://github.com/redis/redis-py
"""

from typing import Optional

from avengercon.redis import get_redis_client


def hello_redis() -> Optional[str]:
    """
    A simple function that returns a greeting while keeping track of how many times this
    has happened using a cached value in Redis

    Returns: A greeting string; None upon connection error

    """
    l_client = get_redis_client()
    if l_client is None:
        return None
    l_redis_hello_count: Optional[str] = l_client.get("avengercon_hello_count")
    if l_redis_hello_count is None:
        l_redis_hello_count = "1"
    else:
        l_redis_hello_count = str(1 + int(l_redis_hello_count))
    l_client.set("avengercon_hello_count", l_redis_hello_count)
    l_client.set(
        "hello_redis",
        f"Redis has said 'Hello Avengercon' " f"{l_redis_hello_count} times.",
    )
    return l_client.get("hello_redis")
