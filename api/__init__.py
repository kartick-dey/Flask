from flask_restful import Api
from .UserController import UserController

from app import appInstance

restServer = Api(appInstance)

restServer.add_resource(UserController, "/api/v1.0/user")