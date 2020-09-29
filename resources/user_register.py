from flask_restful import Resource, reqparse
import logging as logger
from config.database_connection import DBConnection
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    """Checking the required parameter is exixts or not."""
    parser.add_argument('username', type=str, required=True, help="Username is required!")
    parser.add_argument('password', type=str, required=True, help="Password is required!")
    
    @classmethod
    def post(cls):
        logger.info("POST method called from UserRegister Resource")
        data = cls.parser.parse_args()
        """ Check the user is exixts or not."""
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exists!"}, 400

        """ Connecting to the db server"""
        connection = DBConnection.db_connection()
        """Inserting the user data into user table"""
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `users` ( `username`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (data['username'], data['password']))
                connection.commit()
                logger.info("Inserted data: ", data)
                connection.close()
                logger.info("Connection closed!")
                return {"message": "User created successfully."}, 201
        except Exception as e:
            logger.exception(e)
            return {"message": "Internal server error.", "error": e}, 500
            