from config import database_connection

def get_users():
    connection = database_connection.db_connection()
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