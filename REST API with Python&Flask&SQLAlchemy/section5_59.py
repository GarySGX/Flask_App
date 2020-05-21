# -*- coding: utf-8 -*-
"""
Created on Sun May 17 10:38:11 2020

@author: GarySGX
"""

import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()
#allow you to access things, retrieve from top of the database

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1,'jose','asdf')

insert_query = "INSERT INTO users VALUES(?,?,?)"

cursor.execute(insert_query,user)

users = [(2,'rolf','asdf'),
         (3,'anne','xyz')]

cursor.executemany(insert_query,users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()

