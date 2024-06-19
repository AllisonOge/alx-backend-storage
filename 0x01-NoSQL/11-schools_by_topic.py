#!/usr/bin/env python3
"""
Module that defines the function `schools_by_topic`
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection (Collection): pymongo collection object
        topic (str): topic searched

    Returns:
        List[Dict[str, Any]]: List of school documents that have the specified topic
    """
    return list(mongo_collection.find({ 'topics': topic }))
