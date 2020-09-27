from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import logging as logger
from config.database_connection import DBConnection

class Item(Resource):
    parser = reqparse.RequestParser()
    """Checking the required parameter is exixts or not."""
    parser.add_argument('name', type=str, required=True, help="Name field can't be blank!!")
    parser.add_argument('price', type=int, required=True, help="Price field can't be blank!!")
    def __init_(self, name, price):
        self.name = name
        self.price = price

    @jwt_required()
    def get(self, name):
        connection = DBConnection.db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `items` WHERE `name` = %s"
                cursor.execute(sql, (name))
                row = cursor.fetchone()
                logger.info("Fetch item by name:", row)
        except pymysql.MySQLError as e:
            logger.exception(e)
        finally:
            connection.close()
            logger.info("COnnection closed!")
        
        if row:
            return {"Item": { "name": row[0], "price": row[1]}}
        return {"message": "Item not found!"}
    
    @classmethod
    def post(cls, name):
        """ Check the item is exixts or not."""
        if next(filter(lambda item: item['name'] == name, items), None):
            return {"message": "Name {} already exists!".format(name)}, 400  # Bad request for sending invalid name.
        data = cls.parser.parse_args()
        item = {'name': name, 'price': data["price"]}
        items.append(item)
        return item, 201  # item is created if wait to create then return 202 as accepted

    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {"message": "item removed"}

    def put(self, name):
        data = cls.parser.parse_args()
        
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        
        return item, 200


class ItemList(Resource):
    def get(self):
        return {"items": items}, 200