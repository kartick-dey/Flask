from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import logging as logger
import dotenv
import os
from security import authenticate, indentity
from resources.user_register import UserRegister
from resources.item import Item, ItemList
# from controllers.userController import User, UserList

logger.basicConfig(level=logger.DEBUG)
# logger.basicConfig(filename='app.log', filemode='a' ,level=logger.DEBUG, format='%(process)d - %(asctime)s -%(name)s - %(levelname)s - %(message)s')

appInstance = Flask(__name__)
appInstance.secret_key = os.getenv("APP_SECRETE_KEY")
restServer = Api(appInstance)

jwt = JWT(appInstance, authenticate, indentity)

restServer.add_resource(Item, '/item/<string:name>')
restServer.add_resource(ItemList, '/items')
restServer.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    logger.debug("Starting the application")
    # from api import *
    appInstance.run(debug=True)