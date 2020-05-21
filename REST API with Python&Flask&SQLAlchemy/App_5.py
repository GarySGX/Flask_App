# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:12:41 2020

@author: GarySGX
"""
'''
from flask import Flask,request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app,authenticate,identity)
#creates a new endpoint ---- /auth
#the username and password is sent to the authenticate function 
#if username and password match that of in the authenticate function then it returns the user which is a sort of identity
#then the end point will return a JWT token and this token will be sent to the next request we make and call the the identity function which will return an user
items = []
class Item(Resource):
    @jwt_required()
    def get(self, name):
        #for item in items:
        #    if item['name'] == name:
        #        return item
        item = next(filter(lambda x:x['name'] == name,items),None)
        #comments: this is to create a function in lamda format that search x in the items list 
        # and if the x's name is equal to the name that we search for then it will return a list which 
        #is what the filter does, and next will return the first item in this itemlist and will return none
        #will return none if no more item that match the name
        
        return {'item':item}, 200 if item else 404
            
        #return {'items':None}, 404
        
    def post(self, name):
        if next(filter(lambda x:x['name'] == name,items),None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)},400
        
        
        data = request.get_json()
        item = {'name': name, 'price':data['price']}
        items.append(item)
        return item,201
    def delete(self, name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return {'message': 'Item deleted'}
    
class ItemList(Resource):
    def get(self):
        return {'items':items}
    
api.add_resource(Item,'/item/<string:name>')
app.run(port = 5000)
'''
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)