#!/usr/bin/env/python

import datetime
from pprint import  pprint
from pymongo import MongoClient
import pymongo

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
However, because I had to submit this project quickly to study for other finals, I did NOT implement transactions.
So for example, it is possible to write a comment on the Comments collection, but not write it to Articles. 
This would be difficult to time correctly, but this condition does exist.

What data is it not ok to lose in your app?
The most important would be the users. Losing the username and passwords would be bad for business. We can't afford to 
lose any data in the marketplace as we want our users to enjoy buying/selling products on our app.
Also, it would be bad to lose the articles posted/questions from a user. This may make a customer feel devalued if we
do not take care of their data posts. By extension we also need to preserve their reading lists. With regards to job
lists, it will not be ok to lose because this might be a revenue source as the app could be used by recruiters.
Also, we want to ensure our users are happy knowing they got their job applications sent and they obtained the
job because of hacker news. Finally, the questions/answers also can not be lost by the app. The first reason is ensure
the happiness of our users. But also, this can avoid repeat questions getting asked saving the time of a user.

However, if a comment to an article is lost, it might not be crucial for hacker news to dedicate
resources to ensure they are maintained. This is because usually people will post and forget the comment. Also,
upvotes exist to determine the value of the article.
'''


# The <database.collection> is passed in
def init(db):

    # Do I need to add TYPE (Article, Reading list, etc?)
    Users = db.User.insert([
    { "username" : "Emily", "password": "passwerd"},
    { "username" : "Jae",   "password": "passwerd123"},
    { "username" : "Debra", "password": "Unhackable"},
    { "username": "Andrew", "password": "final"}
    ])

    # Build Article: 1, 2, 3
    # Article is Primary Key
    Articles = db.Article.insert([
    {
        "Title" : "How to pass NoSQL",
        "upvotes": 10,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": ["That is so cool that the daughter of Professor Stolfo is teaching "
                                   "at Columbia as well!"],
        "username" : "Emily",
    },
    {
        "Title": "How to pass AP",
        "upvotes": 0,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": ["I learned how to code in C in this class!"],
        "username": "Jae",
    },
    {
        "Title": "How to pass Network Security",
        "upvotes": 20,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": ["The article was useful in completing the 3 programming assignments."],
        "username": "Debra",
    },
    {
        "Title": "Code",
        "upvotes": 0,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": [""],
        "username": "Andrew",
    }
    ])

    # Build Reading List: 4
    Reading = db.Reading_List.insert([
        {"user": "Andrew", "Titles": ["How to pass NoSQL", "How to pass AP", "How to pass Network Security"]}
    ])

    # Build Job entry 5
    Job = db.Jobs.insert([
        {
            "Post Title": "Google looking for qualified programmers",
            "timestamp" : datetime.datetime.utcnow(),
            "link": "www.google.com",
            "usera_applied":[],
        }
    ])

    # Build Question 6 and 7, 8
    # Primary Key: Question
    Questions = db.FAQ.insert([
        {
            "Question": "How do I use Mongodb?",
            "Answers": []
        },
        {
            "Question": "How do I use scapy?",
            "Answers": []
        },
        {
            "Question": "How do I make a file system?",
            "Answers": []
        }
    ])

    # Build Articles Comments to Questions: 9, 10, 11
    # Articles are Primary Key here!

    Market = db.MarketPlace.insert([
        {
            "user":"Jae",
            "price":10.0,
            "Product Descrption": "C textbook"
        },
        {
            "user": "Jae",
            "price": 10.0,
            "Product Descrption": "C++ textbook"
        },
        {
            "user": "Emily",
            "price": 10.0,
            "Product Descrption": "MongoDB textbook"
        }
    ])

    # Articles commented 12, 13, 14 (3 seperate users commented
    User_comments = db.User_Comments.insert([
        {
            "user":"Emily",
            "comment": ["I learned how to code in C in this class"]
        },
        {
            "user": "Andrew",
            "comment": ["The article was useful in completing the 3 programming assignments."]
        },
        {
            "user": "Debra",
            "comment": ["That is so cool that the daughter of Professor Stolfo is teaching at Columbia as well!"]
        }
    ])

    # List of questions 15
    # Primary Key: User
    User_Asks = db.User_Questions.insert([
        {
            "user": "Andrew",
            "Question": ["How do I use Mongodb?", "How do I use scapy?", "How do I make a file system?"]
        }
    ])
    print('Created 15 other objects...')

# Action 1: From given example
# A user publishes an article (INSERT)
def Action1(db, user, title):
    name = ' '.join(title)
    print("user: " + str(user) + " title: " + str(name))

    # Check if the user exists
    userFound = db.Article.find({"username": user})
    if userFound == None:
        print('Invalid, User not found! Please register to post an entry!')
    else:
        print('User Exists! Proceed!')

    # Insert (create) document
    Action1Result = db.Article.insert({
        "Title": str(name),
        "upvotes": 0,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": [],
        "username": str(user),
    })
    if Action1Result != None:
        print('Succesfully added article: ' + name)
    else:
        print('Failed to submit article: ' + name)

# Action 2: <describe the action here>
# A user sees a list of the 1 highest voted article
def Action2(db):
    Sort = db.Article.find().sort('upvotes', pymongo.DESCENDING).limit(10)
    for doc in Sort:
        pprint(doc)

# Action 3: <describe the action here>
# A user up-votes an article
def Action3(db, article):
    art = ' '.join(article)
    # Find the article and up vote it. DO IT in 1 UPDATE
    Action3Result = db.Article.update_one(
        {"Title": art},             # Given this condition being true
        {"$inc": {"upvotes": 1}}    # Increment upvote
    )

    if Action3Result.modified_count == 1:
        print('Just upvoted ' + str(art))
    elif Action3Result.modified_count == 0:
        print('No such Article was found!' + str(art))

# Action 4: <describe the action here>
# A user comments on an article
def Action4(db, user, article, comment):
    comm = ' '.join(comment)
    print("Action 4) user: " + str(user) + " article: " + str(article) + " comment: " + str(comm))

    # Add comment into array of Articles
    Action4Result = db.Article.update_one(
        { "Title": str(article)},
        { "$push": { "comment": str(comm)}}
    )

    Action4Resultpart2 = db.User_Comments.update_one(
        {"user": str(user)},
        {"$push": {"comment": str(comm)}}
    )

    if Action4Result.modified_count == 1:
        print('Added comment to article: ' + str(article))
    elif Action4Result.modified_count == 0:
        print('No such Article was found!' + str(article) + 'Denied to modify User_Comments Table!')

    # For some odd reason, once I do the above step I can get to here?
    # So yeah...either way the second command would have worked regardless
    # Add comment to list of all user_comment

    if Action4Resultpart2.modified_count == 1:
        print('Successfully added entry to User_Comments: ' + str(user))
    elif Action4Resultpart2.modified_count == 0:
        print('No such user found!: ' + str(user))

# Action 5: <describe the action here>
# User changes their password
def Action5(db, username, newPasswd):
    Action5Result = db.User.update_one(
        {"username": username},     # Given this condition being true
        {"$set": {"password": newPasswd}}
    )
    if Action5Result.modified_count == 1:
        print('User: ' + str(username) + ' has new password: ' + str(newPasswd))
    elif Action5Result.modified_count == 0:
        print('Invalid: User NOT found!')

# Action 6: <describe the action here>
# Find all posted in a Market Place
def Action6(db, user):
    Action6Result = db.MarketPlace.find({"user": user})
    for doc in Action6Result:
        pprint(doc)

# Action 7: <describe the action here>
# see all questions a user posted
def Action7(db, user):
    userAsks = db.User_Questions.find({"user": user})
    for doc in userAsks:
        pprint(doc)

# Action 8: <describe the action here>
# Delete an Article
def Action8(db, article):
    art = ' '.join(article)
    print("Action 8: delete: " + art)

    # Delete from Article
    Action8Result = db.Article.delete_one({"Title": art})
    if Action8Result.deleted_count == 1:
        print("Article Deleted..." + str(art))
    elif Action8Result.deleted_count == 0:
        print("Failed to delete..." + str(art))
    else:
        print("You deleted more than 1 article? Did you duplicate?" + str(art))

    # For future development...Delete all comments in User_Comments
    # Or maybe we can keep it, just as a permanent record?

    # Delete all comments in user...
    # Action8Resultpart2 = db.User_Comments.delete_many({"Title": article})
    # print(Action8Resultpart2)

# Program to read input from user and use as needed
def main():
    # Create a client, this is the default
    client = MongoClient()

    # Get the Data bases
    db = client.final

    # Check if collection exists
    currentCollections = db.collection_names()

    # if not, make it!
    # Remember collection = table, since I have 8 models, that is 8 collections

    # Model 1
    if 'Article' not in currentCollections:
        print('Creating Article collection!')
        db.create_collection('Article')

    # Model 2
    elif 'Reading_List' not in currentCollections:
        print('Creating Reading_List collection!')
        db.create_collection('Reading_List')

    # Model 3
    elif 'Jobs' not in currentCollections:
        print('Creating Jobs collection!')
        db.create_collection('Jobs')

    # Model 4
    elif 'MarketPlace' not in currentCollections:
        print('Creating MarketPlace collection!')
        db.create_collection('MarketPlace')

    # Model 5
    elif 'User' not in currentCollections:
        print('Creating User collection!')
        db.create_collection('User')

    # Model 6
    elif 'User_Comments' not in currentCollections:
        print('Creating User_Comments collection!')
        db.create_collection('User_Comments')

    # Model 7
    elif 'FAQ' not in currentCollections:
        print('Creating FAQ collection!')
        db.create_collection('FAQ')

    # Model 8
    elif 'User_Questions' not in currentCollections:
        print('Creating User_Questions collection!')
        db.create_collection('User_Questions')

    # Clean up Everything
    db.Article.delete_many({})
    db.Reading_List.delete_many({})
    db.Jobs.delete_many({})
    db.MarketPlace.delete_many({})
    db.User.delete_many({})
    db.User_Comments.delete_many({})
    db.FAQ.delete_many({})
    db.User_Comments.delete_many({})

    init(db)

    # Can create collection and check if they exist...
    print('Initialized hackernews MongoDB...')

    try:
        while(True):

            print(" ")
            print("Action 1: A user publishes an article                    arguments: <1, username, title>")
            print("Action 2: List the 10 highest upvoted article           arguments: <2>")
            print("Action 3: Upvote article                                 arguments: <3, article>")
            print("Action 4: User adds comment.                             arguments: <4, user arg[1] article "
                  "args[2], comment args[3:]>")
            print("Action 5: User changes their password                    arguments: <5, username, newPassword>")
            # Find all entries in marketplace by user
            print("Action 6: Show all users with posts in Marketplace       arguments: <6, username>")
            print("Action 7: See all questions a user posted                arguments  <7, username>")
            print("Action 8: User deletes an article they posted            arguments  <8, article>")
            print("Or type 'exit' to close the shell...")

            # Get input, Make sure you don't get EOF!
            # Python 2.x
            try:
                var = raw_input("Hacker News> ")
            except EOFError:
                print('EOF Found: Exiting...')
                return

            args = var.split(" ")
            if args[0] == "exit":
                print('Exiting...')
                return

            try:
                actionNumber = int(args[0])
            except Exception as ex:
                continue

            # Action 1: From given example
            # A user publishes an article

            if actionNumber == 1:
                user = args[1]
                title = args[2:]
                Action1(db, user, title)

            # Action 2: <describe the action here>
            # A user sees a list of the 10 highest-voted articles

            elif actionNumber == 2:
                if len(args) != 1:
                    print('Invalid number of arguments! (Action 1)')
                    continue
                Action2(db)

            # Action 3: <describe the action here>
            # A user up-votes an article
            elif actionNumber == 3:
                article = args[1:]
                Action3(db, article)

            # Action 4: <describe the action here>
            # A user comments on an article
            elif actionNumber == 4:
                user = args[1]
                article = args[2]
                comment = args[3:]
                Action4(db, user, article, comment)

            # Action 5: <describe the action here>
            # User changes their password
            elif actionNumber == 5:
                if len(args) != 3:
                    print('Invalid number of arguments! (Action 5)')
                    continue
                user = args[1]
                newPasswd = args[2]
                Action5(db, user, newPasswd)

            # Action 6: <describe the action here>
            # Find all instances of user in Marketplace
            elif actionNumber == 6:
                if len(args) != 2:
                    print('Invalid number of arguments! (Action 6)')
                    continue
                user = args[1]
                Action6(db, user)

            # Action 7: <describe the action here>
            # see all questions a user posted
            elif actionNumber == 7:
                if len(args) != 2:
                    print('Invalid number of arguments! (Action 7)')
                    continue
                user = args[1]
                Action7(db, user)

            # Action 8: <describe the action here>
            # User deletes an article they posted
            elif actionNumber == 8:
                article = args[1:]
                Action8(db, article)

            else:
                print('Invalid Action...')

    except KeyboardInterrupt:
        print('\nctrl-c received, exiting')
        return

if __name__ == "__main__":
    main()