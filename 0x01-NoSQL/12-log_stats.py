#!/usr/bin/env python3
"""
script to log stats
"""
from pymongo import MongoClient

def log_stats():
    """Provides stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # count total number of documents
    total_logs = collection.count_documents({})

    # count documents for each HTTP method
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_counts = { method: collection.count_documents(
                              { 'method': method }) for method in methods }

    # count documents with method=GET and path=/status
    status_check = collection.count_documents({ 'method': 'GET', 'path': '/status' })

    # print results
    print(f'{total_logs} logs')
    print('Methods:')
    for method in methods:
        print(f'\tmethod {method}: {method_counts[method]}')
    print(f'{status_check} status check')


if __name__ == '__main__':
    log_stats()
