import os

import redis


redis_client = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://redis:6379"),
    decode_responses=True,
)


def get_visit_count():
    return redis_client.incr("visit_count")