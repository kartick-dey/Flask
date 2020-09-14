import pymysql
import dotenv
import os

dotenv.load_dotenv()


def db_connection():
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    # Connect to the database
    connection = pymysql.connect(host=db_host,
                                user=db_user,
                                password=db_password,
                                db=db_name,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    return connection