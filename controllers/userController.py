from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required
from app import appInstance
from security import authenticate, indentity

users = []

jwt = JWT(appInstance, authenticate, indentity)


class User(Resource):
    @jwt_required()
    def get(self, name):
        user = next(filter(lambda user: user['name'] == name, users), None)
        return {'user': user}, 200 if user else 404
    
    def post(self, name):
        if next(filter(lambda user: user['name'] == name, users), None):
            return {"message": "Name {} already exists!".format(name)}, 400  # Bad request for sending invalid name.
        data = request.get_json()
        user = {'name': name, 'emil': data["email"]}
        users.append(user)
        return user, 201  # User is created if wait to create then return 202 as accepted


class UserList(Resource):
    def get(self):
        return {"users": users}, 200
