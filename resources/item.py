import pymysql
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import logging as logger
from config.database_connection import DBConnection


class Item(Resource):
    parser = reqparse.RequestParser()
    """Checking the required parameter is exixts or not."""
    parser.add_argument('name', type=str, required=True,
                        help="Name field can't be blank!!")
    parser.add_argument('price', type=int, required=True,
                        help="Price field can't be blank!!")

    def __init_(self, name, price):
        self.name = name
        self.price = price

    @jwt_required()
    def get(self, name):
        try:
            result = self.find_by_name(name)
        except Exception as e:
            return {"message": "Internal server error.", "error": e}, 500
        if result:
            return {"Item": result}, 200
        return {"message": "Item not found!"}, 404

    @classmethod
    def find_by_name(cls, name):
        result = None
        connection = DBConnection.db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `items` WHERE `name` = %s"
                cursor.execute(sql, (name))
                result = cursor.fetchall()
                logger.info("Fetch item by name: {}".format(result))
                connection.close()
                logger.info("Connection closed!")
                if result:
                    return result
                return None
        except pymysql.MySQLError as e:
            logger.exception(e)

    @classmethod
    def post(cls, name):
        try:
            result = cls.find_by_name(name)
        except Exception as e:
            return {"message": "Internal server error.", "error": e}, 500
        if result:
            return {"message": "An item with name '{}' already exixts.".format(name)}, 400
        item = cls.parser.parse_args()
        try:
            cls.insert(item)
            return {"message": "item inserted!", "item": item}, 201
        except Exception as e:
            logger.exception(e)
            return {"message": "Internal server error.", "error": e}, 500

        # if next(filter(lambda item: item['name'] == name, items), None):
        #     return {"message": "Name {} already exists!".format(name)}, 400  # Bad request for sending invalid name.
        # return item, 201  # item is created if wait to create then return 202 as accepted

    @classmethod
    def insert(cls, item):
        connection = DBConnection.db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `items`(`name`, `price`) VALUES (%s, %s)"
            cursor.execute(sql, (item['name'], item['price']))
            connection.commit()
            logger.info("item inserted! - {}".format(item))
            connection.close()
            logger.info("Connection closed!")

    def delete(self, name):
        connection = DBConnection.db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `items` WHERE `name` = %s"
                cursor.execute(sql, (name))
                connection.commit()
                logger.info("Data deleted! -Name of the item: {}".format(name))
                connection.close()
                logger.info("Connection closed!")
                return {"message": "Item removed"}, 204
        except pymysql.MySQLError as e:
            logger.exception(e)
            return {"message": "Internal server error.", "error": e}, 500

    @classmethod
    def put(cls, name):
        item = cls.parser.parse_args()
        try:
            result = cls.find_by_name(item['name'])
        except Exception as e:
            return {"message": "Internal server error.", "error": e}, 500

        if result:
            try:
                cls.insert(item)
                return {"message": "item inserted!", "item": item}, 201
            except Exception as e:
                logger.exception(e)
                return {"message": "Internal server error.", "error": e}, 500
        else:
            try:
                cls.update(item)
                return {"message": "Item Updated", "item": item}, 205
            except Exception as e:
                logger.exception(e)
                return {"message": "Internal server error.", "error": e}, 500

    @classmethod
    def update(cls, item):
        connection = DBConnection.db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE `items` SET `name` = %s `price` = %s WHERE `name` = %s"
            cursor.execute(
                sql, (item['name'], item['price'], item['name']))
            connection.commit()
            logger.info("item updated! - {}".format(item))
            connection.close()
            logger.info("Connection closed!")


class ItemList(Resource):
    def get(self):
        result = None
        connection = DBConnection.db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `items`"
                cursor.execute(sql)
                result = cursor.fetchall()
                logger.info("Fetch items are : {}".format(result))
                connection.close()
                logger.info("Connection closed!")
                items = []
                if result:
                    for item in result:
                        items.append({'name': item[0], 'price': item[1]})
                    return {"Item": items}, 200
                return {"message": "Items not found!"}, 404
        except pymysql.MySQLError as e:
            logger.exception(e)
            return {"message": "Internal server error.", "error": e}, 500
