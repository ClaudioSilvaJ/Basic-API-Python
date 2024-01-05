from flask import Blueprint, jsonify, make_response
from flask_restx import Api, Resource
from User.user_dto import User
from mongo import MongoDB


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='User API', description='API para gerenciar usuários')

mongo = MongoDB(db_url='mongodb://localhost:27017/',
                db_name='PyDB',
                collection_name='Users')

class UserResource(Resource):
    def post(self):
        try:
            data = api.payload
            user = User(data['name'], data['email'])
            user_id = mongo.insert_user(user.to_dict())
        except KeyError:
            return make_response("Invalid Post", 400)
        return make_response(jsonify(user.to_dict()), 201)
    def get(self):
        users = mongo.get_users()
        if users:
            return users, 200
        return make_response("No users found", 404)
    
    def put(self, user_id):
        try:
            data = api.payload
            user = User(data['name'], data['email'])
            result = mongo.update_user(user_id, user.to_dict())
            if result:
                return ({'message': f'User with ID {user_id} updated'}), 200
            return ({'message': f'User with ID {user_id} not found'}), 404
        except KeyError:
            return ("Invalid Put", 400)

    def delete(self, user_id):
        result = mongo.delete_user(user_id)
        return ({'message': f'User with ID {user_id} deleted'}), 200

api.add_resource(UserResource, '/users', '/users/<string:user_id>', endpoint='users')
