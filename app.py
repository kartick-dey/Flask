from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import logging as logger
import dotenv
import os
from security import authenticate, indentity
# from controllers.userController import User, UserList

logger.basicConfig(level=logger.DEBUG)
# logger.basicConfig(filename='app.log', filemode='a' ,level=logger.DEBUG, format='%(process)d - %(asctime)s -%(name)s - %(levelname)s - %(message)s')

appInstance = Flask(__name__)
appInstance.secret_key = os.getenv("APP_SECRETE_KEY")
restServer = Api(appInstance)

jwt = JWT(appInstance, authenticate, indentity)

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {"message": "Name {} already exists!".format(name)}, 400  # Bad request for sending invalid name.
        data = request.get_json()
        item = {'name': name, 'price': data["price"]}
        items.append(item)
        return item, 201  # item is created if wait to create then return 202 as accepted

    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {"message": "item removed"}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name field can't be blank!!")
        parser.add_argument('price', type=int, required=True, help="Price field can't be blank!!")
        data = parser.parse_args()
        
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}, 200

restServer.add_resource(Item, '/item/<string:name>')
restServer.add_resource(ItemList, '/items')

if __name__ == "__main__":
    logger.debug("Starting the application")
    # from api import *
    appInstance.run(debug=True)