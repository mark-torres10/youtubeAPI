"""Implement Redis cache.

Python Redis API docs: https://redis.io/docs/clients/python/
Installing Redis: https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/

Make sure that your local Redis server (if using a local Redis installation)
is on before running. Run the following in a CLI tool, from this directory.
```
redis-server ./redis.conf
```
"""
import json
from typing import Dict, Union

import redis

from db.redis.constants import DEFAULT_CACHE_TIME_SECONDS, REDIS_HOST, REDIS_PORT
from lib.log.logger import Logger

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
logger = Logger()

def cache_key(function_name: str, params: Dict) -> str:
    """Generate a cache key based on the API endpoint and parameters."""
    # Serialize the parameters as a JSON string
    params_str = json.dumps(params, sort_keys=True)
    return f"{function_name}:{params_str}"


def cache_data(function_name: str, params: Dict, data: Dict) -> None:
    """Cache the API response data in Redis."""
    key = cache_key(function_name, params)
    data_str = json.dumps(data)
    redis_conn.setex(key, DEFAULT_CACHE_TIME_SECONDS, data_str)


def get_cached_data(function_name: str, params: Dict) -> Union[Dict, None]:
    """Retrieve cached data from Redis if available."""
    key = cache_key(function_name, params)
    cached_data = redis_conn.get(key)
    if cached_data is not None:
        return json.loads(cached_data)
    logger.warning(
        f"Cached data not found for function {function_name} and params {params}"
    )  # noqa
    return None
