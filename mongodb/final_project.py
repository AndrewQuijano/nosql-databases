import sys
from pprint import pprint
import pymongo
from pymongo import MongoClient

# Put the use case you chose here. Then justify your database choice:
# Use Case: Hackernews
# Database selection: Mongodb
# Why?
# Mongodb has a flexible schema. This means that the design can easily change without all the
# complexities of relational databases if something like another column needed to be added. If
# hackernews expands
# Mongodb is scalable
# Finally, Mongodb software is free. the database administrator would only need to
# pay mongodb if they need technical support.

# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# If the server crashes.
# Since all the operations are atomic, there should be no data lost.
#
# What data is it not ok to lose in your app?
# What can you do in your commands to mitigate the risk of lost data?

# Create a client, this is the default
client = MongoClient()

# Get the database and collection
db = client.test
collection = db.movies

db.inventory.insert([
   { "_id" : 1, "username" : "Emily", "password": "passwerd", "Articles_Posted" : 120,  },
   { "_id" : 2, "username" : "Jae", "password": "passwerd123", "Articles_Posted" : 80,  },
   { "_id" : 3, "username" : "Debra", "password": "Unbreakable", "Articles_Posrted" : 60, },
])
print('Just created 3 users...')

db.inventory.insert([
   { "_id" : 1, "Title" : "Emily", "upvotes": 1, "comments:": "Your article is bad and you should feel bad!",
     "link":"www.google.com", "Author_id": 1},
   { "_id" : 2, "Title" : "Jae",   "upvotes": 1, "comments:": "Your article is bad and you should feel bad!",
     "link":"www.google.com", "Author_id": 1  },
   { "_id" : 3, "Title" : "Debra", "upvotes": 1,  "comments:": "Your article is bad and you should feel bad!",
     "link":"www.google.com", "Author_id": 1},
])
print('Created 15 other objects...')

# Action 1: From given example
# A user publishes an article (UPDATE)
def Action1():
    print('Action 1')

# Action 2: <describe the action here>
# A user sees a list of the 10 highest-voted articles
def Action2():
    print('Action 1')

# Action 3: <describe the action here>
# A user up-votes an article
def Action3():
    print('Action 1')

# Action 4: <describe the action here> (UPDATE)
# A user comments on an article
def Action4():
    print('Action 1')

# Action 5: <describe the action here>
# User changes their password
def Action5():
    print('Action 1')

# Action 6: <describe the action here>
# User Selects 10 most recently posted articles
def Action6():
    print('Action 1')

# Action 7: <describe the action here>
# see all articles a user posted
def Action7():
    print('Action 1')

# Action 8: <describe the action here>
# User deletes an article they posted
def Action8():
    print('Action 1')

# Program to read input from user and use as needed
def main():

    try:
        while(True):
            # Get input, Make sure you don't get EOF!
            try:
                var = input("HackerNews> ")
            except EOFError:
                print("Invalid: EOF Detected!")
                continue

            args = var.split(" ")
            if args[0] == "exit":
                print('Exiting')
                return

    except KeyboardInterrupt:
        print('\nctrl-c received, exiting')
        return

if __name__ == "__main__":
    main()