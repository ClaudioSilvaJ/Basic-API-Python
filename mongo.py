from pymongo import MongoClient
from bson import ObjectId

class MongoDB:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_user(self, user_data):
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
