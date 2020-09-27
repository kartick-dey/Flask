import pymysql
import dotenv
import os
import logging as logger

dotenv.load_dotenv()


class DBConnection:
    """
    Connect to database
    """
    def db_connection():
        try:
            db_host = os.getenv("DB_HOST")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_name = os.getenv("DB_NAME")
            db_port = int(os.getenv("DB_PORT"))
            # Connect to the database
            connection = pymysql.connect(host=db_host,
                                        port=db_port,
                                        user=db_user,
                                        password=db_password,
                                        db=db_name,
                                        charset='utf8')
            logger.info("Connection established!")
        except pymysql.MySQLError as e:
            logger.exception('Exception: ', e)
            
        finally:
            return connection