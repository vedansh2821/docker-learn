import os

import redis

redis_client = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://redis:6379"),
    decode_responses=True,
)

# Fallback when no Redis is reachable (e.g. plain `docker run` without
# Compose): keep the count in memory so the app still answers instead of
# failing every request. Compose/Render runs use the real Redis counter.
_fallback_count = 0


def get_visit_count():
    global _fallback_count
    try:
        return redis_client.incr("visit_count")
    except redis.RedisError:
        _fallback_count += 1
        return _fallback_count
