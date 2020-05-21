# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:45:25 2020

@author: GarySGX
"""
'''
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required
import sqlite3

class Item(Resource):
    #this parser is defined in front to make it a class method 
    #it can be called by using Item.paser...
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,#no request can come through with no price
        help="This field cannot be left blank!"
    )
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item':{'name':row[0],'price':row[1]}}
        return {'message':'Item not found'},404

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
       
        return {'message':'Item not found'}

        
  
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)},400

        data = Item.parser.parse_args()
        #gonna pass the arguments that come through the json payload and put valid ones in data
        #only the arguments specified price will be passed through  
        item = {'name': name, 'price': data['price']}
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))
        
        connection.commit()
        connection.close()
        
        return item

    
    def delete(self, name):
        global items
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query,(name,))
        
        connection.commit()
        connection.close()
    
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}
'''
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}