#!/usr/bin/env python3
"""
Module that defines the function `top_students`
"""

def top_students(mongo_collection):
    """
    return all students sorted by average score.

    Args:
        mongo_collection (Collection): pymongo collection object

    Returns:
        List[Dict[str, Any]]: List of students sorted by average score, each
        with an averageScore key
    """
    pipeline = [
          {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': { '$avg': '$topics.score' }
                }
          },
            {
            '$sort': { 'averageScore': -1 }
          }
    ]
    return list(mongo_collection.aggregate(pipeline))
