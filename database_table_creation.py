import pymysql
from config.database_connection import DBConnection

connection = DBConnection.db_connection()

def create_table():
    try:
        with connection.cursor() as cursor:
            # create_table_query = "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64) NOT NULL, password VARCHAR(255) NOT NULL)"
            # create_table_query = "CREATE TABLE items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(64) NOT NULL, price INT(25) NOT NULL)"
            create_table_query = "CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, public_id VARCHAR(255) NOT NULL, name VARCHAR(64) NOT NULL, password VARCHAR(255) NOT NULL, admin BOOLEAN NOT NULL)"
            # create_table_query = "CREATE TABLE todo (id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255) NOT NULL, complete BOOLEAN NOT NULL, user_id INT NOT NULL)"
            cursor.execute(create_table_query)
            connection.commit()
            print('Table created')
    except pymysql.MySQLError as e:
        print("Exception: ", e)

    finally:
        connection.close()
        print("Conncetion closed!")

def insert_data():
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` ( `username`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('kd-dey', 'kdey123'))
            connection.commit()
            print("Inserted!")
    except Exception as e:
        print(e)
        raise e
    finally:
        connection.close()
        print("Connection closed!")

def delete_table():
    # DROP TABLE tablename
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "DROP TABLE user"
            cursor.execute(sql)
            # connection.commit()
            print("Deleted!")
    except Exception as e:
        print(e)
        raise e
    finally:
        connection.close()
        print("Connection closed!")


create_table()
# insert_data()
# delete_table()
