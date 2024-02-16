"""
Celery server/worker configuration
https://docs.celeryq.dev/en/stable/userguide/configuration.html
"""

from avengercon.redis.config import redis_config

broker_connection_retry_on_startup = False
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-settings
result_backend = redis_config.redis_dsn
redis_backend_health_check_interval = 10
broker_url = redis_config.redis_dsn
include = [
    "avengercon.celery.tasks",
]
worker_prefetch_multiplier = 4
