#!/usr/bin/env python3
"""
Module that defines the function `insert_school`
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection (Collection): pymongo collection object
        **kwargs: key-value pairs representing the document to insert

    Returns:
        Any: the new _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
