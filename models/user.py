import pymysql
import logging as logger
from config.database_connection import DBConnection

connection = DBConnection.db_connection()

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        logger.debug("'find_by_username' function called!")
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

                logger.info("Return value from find_by_username: ", user)
                return user

        except pymysql.MySQLError as e:
            logger.exception(e)
        finally:
            connection.close()
            logger.info("Conncetion closed!")

    @classmethod
    def find_by_id(cls, _id):
        logger.debug("'find_by_id' function called!")
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

                logger.info("Return value from find_by_id: ", user)
                return user

        except pymysql.MySQLError as e:
            logger.exception(e)
        finally:
            connection.close()
            logger.info("Conncetion closed!")

    