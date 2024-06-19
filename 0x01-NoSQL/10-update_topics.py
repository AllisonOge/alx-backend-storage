#!/usr/bin/env python3
"""
Module that defines the function `update_topics`
"""

def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.

    Args:
        mongo_collection (Collection): pymongo collection object
        name (str): school name to update
        topics (List[str]): list of topics approached in the school

    Returns:
        None
    """
    mongo_collection.update_many(
            { 'name': name },
            { '$set': { 'topics': topics } }
    )
