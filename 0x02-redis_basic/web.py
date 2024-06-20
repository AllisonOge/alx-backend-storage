#!/usr/bin/env python3
"""
script to cache the access count to a URL
"""
import requests
import redis
from typing import Callable
from functools import wraps

r = redis.Redis()


def cache_with_expiration(expiration: int):
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration (int): The expiration time in seconds for the cache.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            """wrapper function"""
            # Check if the URL is already cached
            cached_content = r.get(url)
            if cached_content:
                return cached_content.decode('utf-8')

            # Call the original function to get the content
            content = func(url)

            # Cache the content with an expiration time
            r.set(url, content, ex=expiration)

            return content
        return wrapper
    return decorator


@cache_with_expiration(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL and cache it.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Track the number of times the URL was accessed
    r.incr(f"count:{url}")

    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    get_page(test_url)
    get_page(test_url)
    print(f"Access count: {r.get(f'count:{test_url}').decode('utf-8')}")
