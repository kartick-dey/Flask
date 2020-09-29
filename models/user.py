import pymysql
import logging as logger
from config.database_connection import DBConnection

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        logger.debug("'find_by_username' function called!")
        connection = DBConnection.db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s"
                cursor.execute(sql, (username))
                row = cursor.fetchone()
                logger.info(row)
                if row:
                    user = cls(*row)
                else:
                    user = None

                connection.close()
                logger.info("Conncetion closed!")
                logger.info("Return value from find_by_username: {}".format(user))
                return user

        except pymysql.MySQLError as e:
            logger.exception(e)
            

    @classmethod
    def find_by_id(cls, _id):
        logger.debug("'find_by_id' function called!")
        connection = DBConnection.db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE id = %s"
                cursor.execute(sql, (_id))
                row = cursor.fetchone()
                logger.info(row)
                if row:
                    user = cls(*row)
                else:
                    user = None

                connection.close()
                logger.info("Conncetion closed!")
                logger.info("Return value from find_by_id: {}".format(user))
                return user

        except pymysql.MySQLError as e:
            logger.exception(e)
            

    