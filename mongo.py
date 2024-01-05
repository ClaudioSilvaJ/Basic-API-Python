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
    
    def get_users(self):
        users = []
        for user in self.collection.find():
            user['_id'] = str(user['_id'])
            users.append(user)
        return users
    
    def update_user(self, user_id, user_data):
        result = self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_data})
        return result.modified_count
    
    def delete_user(self, user_id):
        result = self.collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count
