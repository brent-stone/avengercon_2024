"""
Celery server/worker configuration
https://docs.celeryq.dev/en/stable/userguide/configuration.html
"""

from avengercon.redis.config import redis_config

include = [
    "avengercon.celery.tasks",
]

result_backend = redis_config.redis_dsn
broker_url = redis_config.redis_dsn
# Note: It's likely that the following environment variables are going to take precedence
# over the settings above in the downstream Kombu dependency.
# CELERY_BROKER_URL, CELERY_RESULT_BACKEND
# Celery will break in subtle ways because it will get de-synced from the Kombu config
# which looks (seemingly exclusively) for the environment variables. Thus, explicitly
# declare the configs here for clarity of intent but be attentive to ensuring the
# environment variables are set and correct for the given environment (e.g. are we
# running in the container or are we running code on a developer's localhost, external
# to the running container/proxy, that needs a different connection host & port
# reflected in the environment variables?

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-settings
redis_backend_health_check_interval = 10
broker_connection_retry_on_startup = False
worker_prefetch_multiplier = 4
