from flask_restful import Resource
import logging as logger
from config import database_connection

connection = database_connection.db_connection()

class UserController(Resource):
    def get(self):
        logger.debug("Inside get method")
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM user_data"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Expression as e:
            return e

        finally:
            connection.close()
            return {"Message": "Get from method"}, 200

    def post(self):
        logger.debug("Inside post method")

    def put(self):
        logger.debug("Inside put method")

    def delete(self):
        logger.debug("Inside delete method")