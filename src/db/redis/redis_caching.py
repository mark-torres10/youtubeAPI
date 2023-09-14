"""Implement Redis cache.

Technically, Redis is an in-memory store, but for the purposes of a PoC we'll
persist the data. In a deployed instance, we can use Redis to avoid duplicate
requests to the API endpoints, but for local development a naive Redis cache
won't persist the data.

Python Redis API docs: https://redis.io/docs/clients/python/
Installing Redis: https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/
"""
import json
from typing import Dict, List

import redis

from db.redis.constants import (
    DEFAULT_CACHE_TIME_SECONDS, REDIS_HOST, REDIS_PORT
)

redis_conn = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
)

def cache_key(api_endpoint: str, params: Dict) -> str:
    """Generate a cache key based on the API endpoint and parameters."""
    # Serialize the parameters as a JSON string
    params_str = json.dumps(params, sort_keys=True)
    return f"{api_endpoint}:{params_str}"

def cache_data(api_endpoint: str, params: Dict, data: Dict) -> None:
    """Cache the API response data in Redis."""
    key = cache_key(api_endpoint, params)
    data_str = json.dumps(data)
    redis_conn.setex(
        key, DEFAULT_CACHE_TIME_SECONDS, data_str
    )

def get_cached_data(api_endpoint: str, params: Dict) -> Dict:
    """Retrieve cached data from Redis if available."""
    key = cache_key(api_endpoint, params)
    cached_data = redis_conn.get(key)
    if cached_data is not None:
        return json.loads(cached_data)
    return None


if __name__ == "__main__":
    print(redis_conn)
    breakpoint()