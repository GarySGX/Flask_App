# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:13:34 2020

@author: GarySGX
"""
from models.user import UserModel

#users = [User(1,'bob','asdf')]
        

#this allows us to save the trouble of traversing through the user's list ,
#instead we can just search by username_mapping['bob'] or userid_mapping[1]



#username_mapping = { u.username: u for u in users}
#this is assigning a key value pair, the key is user's username and u  which is the value is the users
    
#userid_mapping = { u.id : u for u in users}
    
def authenticate(username,password):
    #user = username_mapping.get(username,None)
    user = UserModel.find_by_username(username)
    #it means that default value return to user is none otherwise it will be username
    if user and user.password == password:
    # or user safe_str_cmp but need to import from werkzug.security
        return user
    
def identity(payload):
    #payload is the contents of JWT token
    user_id = payload['identity']
    #extract identity from that payload
   # return userid_mapping.get(user_id,None)
    #retrieve user that matches this specific payload
    return UserModel.find_by_id(user_id)

