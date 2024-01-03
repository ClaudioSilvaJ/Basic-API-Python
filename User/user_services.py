from flask import Blueprint, jsonify, make_response
from flask_restx import Api, Resource
from user_dto import User
from mongo import MongoDB


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='User API', description='API para gerenciar usuários')

mongo = MongoDB(db_url='mongodb://localhost:27017/',
                db_name='PyDB',
                collection_name='user_collection')

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
        return jsonify({'users': []}), 200
    
    def put(self, user_id):
        data = api.payload
        return jsonify({'message': f'Update user with ID {user_id}'}), 200

    def delete(self, user_id):
        return jsonify({'message': f'Delete user with ID {user_id}'}), 200

api.add_resource(UserResource, '/users', '/users/<int:user_id>', endpoint='users')
