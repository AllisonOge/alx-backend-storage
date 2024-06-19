#!/usr/bin/env python3
"""
Module that defines the `list_all` function
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Args:
        mongo_collection: pymongo collection object

    Returns:
        List of documents, or an empty list if no documents are found
    """
    return list(mongo_collection.find())
