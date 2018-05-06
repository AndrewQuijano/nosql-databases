import sys
from pprint import pprint
import pymongo
from pymongo import MongoClient

'''
Put the use case you chose here. Then justify your database choice:
Use Case: Hacker news
Database selection: Mongodb

Why?
1- Mongodb supports a flexible schema. This can be easily seen in this project as I was required to
make 8 models. But with MongoDB, I can easily add more models as mongodb was designed to not have to use join
like relational database (e. g. SQL).

2- Mongodb supports embedded documents, this works well with comments as
they are made of multiple parts (time, writer, data) and there are multiple comments
attached to an article

3- Querying in a field means the user can query a specific comment in an article and access
traits unique to that comment

4- It support aggregation, which is useful for commands like
counting number of users in the database

5- Mongodb is good for high availability systems because it supports fail over. In a
system where there is a primary and multiple secondary server, the secondary serves can become the
primary server if the primary server is out of commission.

6- Mongodb supports preference. If hacker news become a big business with multiple servers, a user
can use this to have high performance in reading articles, especially if there are not that many users
who write articles.

7- Mongodb supports sharding, meaning that when hacker news becomes a big business as well, the database
can be fragmented into multiple chunks. This can be useful to shard asks/answers and articles. It might be useful
#because there is probably a good chance ask/responding to asks will be more write intensive. But if it is sharded
the performance costs of writing can be mitigated and not effect users writing articles.

Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
If the server crashes.
Since all writes go to disk unlike Redis, there is no concern of data being lost on shutdown.

What data is it not ok to lose in your app?
The most important would be the users. Losing the username and passwords would be bad for business.
Also, it would be bad to lose the articles posted/questions from a user. This may make a customer feel devalued if we
do not take care of their data posts. By extension we also need to preserver their reading lists. With regards to job
lists, it will not be ok to lose because this might be a revenue source as the app could be used by recruiters.
Also, we want to ensure our users are happy knowing they got their job applications sent and they obtained the
job because of hacker news. Finally, the questions/answers also can not be lost by the app. The first reason is ensure
the happiness of our users. But also, this can avoid repeat questions getting asked saving the time of a user.

However, if a comment to an article is lost, it might not be crucial for hacker news to dedicate
resources to ensure they are maintained. This is because usually people will post and forget the comment. Also,
upvotes exist to determine the value of the article.
'''


# The <database.collection> is passed in
def init(collection):

    # Needed to time stamp stuff
    Object = ObjectId()

    collection.insert([
    { "username" : "Emily", "password": "passwerd" },
    { "username" : "Jae",   "password": "passwerd123"},
    { "username" : "Debra", "password": "Unhackable"},
    ])

    print('Created three default users...')

    # Build Article
    collection.insert([
    {
        "Title" : "How to pass NoSQL",
        "upvotes": 0,
        "timestamp": Object.getTimeStamp(),
        "comments:": [],
        "username" : "Emily",
    }
    ])

    # Build Reading List
    
    print('Created 15 other objects...')

# Action 1: From given example
# A user publishes an article (UPDATE)
def Action1(collection, user, title, link):

    # Check if the user exists
    userFound = collection.find({"username": user})

    if userFound == None:
        print('Invalid, User not found! Please register to post an entry!')

    # Insert document
    Action1Result  = collection.inventory.insert([{
        "Title": title,
        "upvotes": 0,
        "comments:": [],
        "link": link}])
    print(Action1Result)

# Action 2: <describe the action here>
# A user sees a list of the 10 highest-voted articles
def Action2():
    print('Action 1')

# Action 3: <describe the action here>
# A user up-votes an article
def Action3(collection, article):
    # Find the article and up vote it. DO IT in 1 UPDATE
    Action3Result = collection.update(
        {"Title": article},     # Given this condition being true
        {"$inc": {"upvotes": 1}}# Increment upvote
    )
    print(Action3Result)

# Action 4: <describe the action here> (UPDATE)
# A user comments on an article
def Action4(collection):
    print('Action 1')

# Action 5: <describe the action here>
# User changes their password
def Action5(collection):
    print('Action 1')

# Action 6: <describe the action here>
# User Selects 10 most recently posted articles
def Action6(collection):
    print('Action 1')

# Action 7: <describe the action here>
# see all articles a user posted
def Action7(collection):
    print('Action 1')

# Action 8: <describe the action here>
# User deletes an article they posted
def Action8(collection):
    print('Action 1')

# Program to read input from user and use as needed
def main():
    # Create a client, this is the default
    client = MongoClient()

    # Check if collection exists
    # if not, make it!
    currentCollections = client.getCollectionNames()
    if 'hackernews' not in currentCollections:
        print('Creating hacker news collection!')
        client.createCollection('hackernews')
    dbColl = client.hackernews
    init(dbColl)

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
                print('Exiting...')
                return

            try:
                actionNumber = int(args[0])
            except Exception as ex:
                continue

            if actionNumber == 1:
                if len(args) != 4:
                    print('Invalid number of arguments!')
                    continue
                user = args[1]
                title = args[2]
                link = [3]
                Action1(dbColl, user, title, link)

            elif actionNumber == 2:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action2(article)

            elif actionNumber == 3:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action3(article)

            elif actionNumber == 4:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action4(article)

            elif actionNumber == 5:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action5(article)

            elif actionNumber == 6:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action6(article)

            elif actionNumber == 7:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action7(article)

            elif actionNumber == 8:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action8(article)

            else:
                print('Invalid Action')

    except KeyboardInterrupt:
        print('\nctrl-c received, exiting')
        return

if __name__ == "__main__":
    main()