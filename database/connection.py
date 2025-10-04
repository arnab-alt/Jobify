from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME

def get_database():
    """Get MongoDB database connection"""
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DATABASE_NAME]
        # Test connection
        client.server_info()
        return db
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def get_collection(collection_name):
    """Get a specific collection"""
    db = get_database()
    if db is not None:
        return db[collection_name]
    return None