import os

import redis


redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)


def get_visit_count():
    return redis_client.incr("visit_count")