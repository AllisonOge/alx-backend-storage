#!/usr/bin/env python3
"""
module for `Cache` class
"""
import redis
import uuid
from typing import Union, Optional, Callable


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

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve the data from Redis and optionally apply a conversion function.
        Args:
            key (str): the key to retrieve the data from Redis.
            fn (Optional[Callable]): the optional conversion function to apply.
        Returns:
            Optional[Union[str, bytes, int, float]]: the retrieved data, optionally converted.
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data from Redis and convert it to a string.
        Args:
            key (str): the key to retrieve the data from Redis
        Returns:
            Optional[str]: the retrieved data as a string
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data from Redis and convert it to an integer.
        Args:
            key (str): the key to retrieve the data from Redis
        Returrns:
            Optional[int]: the retrieved data as an integer
        """
        return self.get(key, fn=int)
