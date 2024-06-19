#!/usr/bin/env python3
"""
module for `Cache` class
"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class"""
    def __init__(self):
        """Initialize the Cache class with a redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the data in Redis with randomly generated key and return the key.
        Args:
            data (Union[str, bytes, int, float]): the data to store in Redis
        Returns:
            str: the randomly generated key under which the data is stored.
        """
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key
