#!/usr/bin/env python3
"""
module for `Cache` class
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    Args:
        method (Callable): the method to be wrapped.
    Returns:
        Callable: the wrapped method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        # increment the count for the method's qualified name
        self._redis.incr(method.__qualname__)
        # call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.
    Args:
        method (Callable): the method to be wrapped.
    Returns:
        Callable: the wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        # create input and output list keys
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'

        # store the input arguments
        self._redis.rpush(input_key, str(args))

        # call the original method and get the output
        output = method(self, *args, **kwargs)

        # store the output
        self._redis.rpush(output_key, output)

        return output
    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """Initialize the Cache class with a redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    Args:
        method (Callable): the method to replay the call history for
    """
    # create the input and output list keys
    input_key = f'{method.__qualname__}:inputs'
    output_key = f'{method.__qualname__}:outputs'

    # retrieve inputs and outputs from Redis
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    # print the call history
    print(f'{method.__qualname__} was called {len(inputs)} times:')
    for ip, op in zip(inputs, outputs):
        print(f'{method.__qualname__}(*{ip.decode("utf-8")}) -> {op.decode("utf-8")}')
