"""
Redis Cache Snippet - Template/Snippet Reutilizável

This module provides a cache system class for managing cache operations using Redis.
It can be used with Django or as a standalone utility.

**IMPORTANTE:** Este é um template/snippet. Copie e adapte para seu projeto.

Usage:
    # Django
    from core.templates.cache.redis_cache_snippet import CacheSystem
    from django.conf import settings

    cache = CacheSystem(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=0
    )
    cache.save("user:123", {"name": "John", "email": "john@example.com"}, expiration=3600)
    data = cache.read("user:123")

    # Standalone
    cache = CacheSystem(host="localhost", port=6379, password=None, db=0)
    cache.save("key", {"data": "value"}, expiration=60)
"""

import json
from typing import Any, Dict, Optional, Union

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None


class CacheSystem:
    """
    Cache system class for managing cache operations using Redis.

    This class provides methods to save, read, and remove data from the cache
    with optional expiration times.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_timeout: int = 3600,
    ):
        """
        Initializes the CacheSystem with a Redis connection.

        Args:
            host: Redis host address (default: "localhost").
            port: Redis port (default: 6379).
            db: Redis database number (default: 0).
            password: Redis password (default: None).
            default_timeout: Default expiration time in seconds (default: 3600).

        Raises:
            ImportError: If redis package is not installed.
            redis.exceptions.ConnectionError: If a connection to Redis cannot be established.
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis package is required. Install with: pip install redis"
            )

        self.redis_host = host
        self.redis_port = port
        self.redis_db = db
        self.redis_password = password
        self.default_timeout = default_timeout

        self.redis_client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db,
            password=self.redis_password,
            decode_responses=False,  # We handle encoding manually
        )

        try:
            self.redis_client.ping()
        except redis.exceptions.ConnectionError as e:
            raise redis.exceptions.ConnectionError(
                f"Could not connect to Redis at {host}:{port}: {e}"
            ) from e

    def save(
        self,
        key: str,
        value: Union[Dict[str, Any], str, int, float, bool],
        expiration: Optional[int] = None,
    ) -> None:
        """
        Save data to the cache with an optional expiration time.

        Args:
            key: The key to store the data under.
            value: The data to store (dict, str, int, float, bool).
            expiration: The expiration time in seconds. If None, uses default_timeout.

        Raises:
            ValueError: If the expiration parameter is not an integer or None.
            redis.exceptions.RedisError: If there is an error while interacting with Redis.
        """
        if expiration is None:
            timeout = self.default_timeout
        elif isinstance(expiration, int) and expiration >= 0:
            timeout = expiration
        else:
            raise ValueError("Expiration must be a non-negative integer (seconds) or None.")

        try:
            # Serialize value to JSON if it's a dict
            if isinstance(value, dict):
                serialized_value = json.dumps(value)
            elif isinstance(value, (str, int, float, bool)):
                serialized_value = json.dumps(value)
            else:
                raise ValueError(f"Unsupported value type: {type(value)}. Use dict, str, int, float, or bool.")

            self.redis_client.setex(key, timeout, serialized_value)
        except redis.exceptions.RedisError as e:
            raise redis.exceptions.RedisError(f"Failed to save data to Redis: {e}") from e

    def read(self, key: str) -> Optional[Union[Dict[str, Any], str, int, float, bool]]:
        """
        Read data from the cache.

        Args:
            key: The key to retrieve the data from.

        Returns:
            Union[Dict[str, Any], str, int, float, bool, None]: The data retrieved from the cache,
            or None if the key does not exist.

        Raises:
            redis.exceptions.RedisError: If there is an error while interacting with Redis.
            json.JSONDecodeError: If the data retrieved from Redis is not valid JSON.
        """
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None

            # Decode bytes to string
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            # Deserialize JSON
            return json.loads(value)
        except redis.exceptions.RedisError as e:
            raise redis.exceptions.RedisError(f"Failed to read data from Redis: {e}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to decode JSON data from Redis: {e.msg}", e.doc, e.pos
            ) from e

    def remove(self, key: str) -> None:
        """
        Remove data from the cache.

        Args:
            key: The key to remove from the cache.

        Raises:
            redis.exceptions.RedisError: If there is an error while interacting with Redis.
        """
        try:
            self.redis_client.delete(key)
        except redis.exceptions.RedisError as e:
            raise redis.exceptions.RedisError(f"Failed to remove data from Redis: {e}") from e

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        try:
            return bool(self.redis_client.exists(key))
        except redis.exceptions.RedisError as e:
            raise redis.exceptions.RedisError(f"Failed to check key existence: {e}") from e

    def get_ttl(self, key: str) -> Optional[int]:
        """
        Get the time-to-live (TTL) of a key in seconds.

        Args:
            key: The key to check.

        Returns:
            Optional[int]: TTL in seconds, or None if key doesn't exist or has no expiration.
        """
        try:
            ttl = self.redis_client.ttl(key)
            return ttl if ttl >= 0 else None
        except redis.exceptions.RedisError as e:
            raise redis.exceptions.RedisError(f"Failed to get TTL: {e}") from e

