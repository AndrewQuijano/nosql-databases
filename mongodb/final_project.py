import sys
from pprint import pprint
import pymongo
import datetime
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

    print(Users)
    print('Created Four default users...')

    # Build Article: 1, 2, 3
    # Article is Primary Key
    Articles = db.Article.insert([
    {
        "Title" : "How to pass NoSQL",
        "upvotes": 1,
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
        "upvotes": 0,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": ["The article was useful in completing the 3 programming assignments."],
        "username": "Debra",
    }
    ])
    print(Articles)

    # Build Reading List: 4
    Reading = db.Reading_List.insert([
        {"user": "Andrew", "Titles": ["How to pass NoSQL", "How to pass AP", "How to pass Network Security"]}
    ])
    print(Reading)

    # Build Job entry 5
    Job = db.Jobs.insert([
        {
            "Post Title": "Google looking for qualified programmers",
            "timestamp" : datetime.datetime.utcnow(),
            "link": "www.google.com",
            "usera_applied":[],
        }
    ])
    print(Job)

    # Build Question 6 and 7, 8
    # Primary Key: Question
    Questions = db.FAQ.insert([
        {
            "Question": "How do I use Mongodb?"
        },
        {
            "Question": "How do I use scapy?"
        },
        {
            "Question": "How do I make a file system?",
        }
    ])
    print(Questions)

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
    print(Market)

    # Articles commented 12, 13, 14 (3 seperate users commented
    User_comments = db.User_Commens.insert([
        {
            "username":"Emily",
            "comment": ["I learned how to code in C in this class"]
        },
        {
            "username": "Andrew",
            "comment": ["The article was useful in completing the 3 programming assignments."]
        },
        {
            "username": "Debra",
            "comment": ["That is so cool that the daughter of Professor Stolfo is teaching at Columbia as well!"]
        }
    ])
    print(User_comments)

    # List of questions 15
    # Primary Key: User
    User_Asks = db.User_Questions.insert([
        {
            "user": "Andrew",
            "Question": ["How do I use Mongodb?", "How do I use scapy?", "How do I make a file system?"]
        }
    ])
    print(User_Asks)

    print('Created 15 other objects...')

# Action 1: From given example
# A user publishes an article (INSERT)
def Action1(db, user, title):

    # Check if the user exists
    userFound = db.Article.find({"username": user})

    if userFound == None:
        print('Invalid, User not found! Please register to post an entry!')

    # Insert (create) document
    Action1Result  = db.Article.inventory.insert_one([{
        "Title": title,
        "upvotes": 0,
        "timestamp": datetime.datetime.utcnow(),
        "comments:": [],
        "username": user
    }])
    print(Action1Result)

# Action 2: <describe the action here>
# A user sees a list of the 1 highest-voted articles
def Action2(db):
    Action2Result = db.Article.find().sort({"$upvotes":1}).limit(1)
    print(Action2Result)

# Action 3: <describe the action here>
# A user up-votes an article
def Action3(db, article):

    # Find the article and up vote it. DO IT in 1 UPDATE
    Action3Result = db.Article.update(
        {"Title": article},     # Given this condition being true
        {"$inc": {"upvotes": 1}}# Increment upvote
    )
    if Action3Result == None:
        print('Invalid, Article does NOT exist!')
    else:
        print(Action3Result)

# Action 4: <describe the action here>
# A user comments on an article
def Action4(db, user, article, comment):

    # Check if User exists
    userFound = db.User.find({"username": user})

    if userFound == None:
        print('Invalid, User not found! Please register to post an entry!')

    # Check if Article exists
    articleFound = db.User.find({"Title": article})

    if articleFound == None:
        print('Invalid, Article not found!')

    # Add comment into array of Articles
    Action3Result = db.Article.update([
        { "Article":article},
        { "$push": { "comment": comment}}
    ])
    print(Action3Result)

    # Add comment to list of all user_comments
    Action3Resultpart2 = db.User_Comments.insert([
        {"user": user},
        {"$push": {"comment": comment}}
    ])
    print(Action3Resultpart2)


# Action 5: <describe the action here>
# User changes their password
def Action5(db, username, newPasswd):
    Action3Result = db.User.update(
        {"username": username},     # Given this condition being true
        {"$set": {"password": newPasswd}}
    )
    print(Action3Result)

# Action 6: <describe the action here>
# Find all posted in a Market Place
def Action6(db, user):
    Action6Result = db.MarketPlace.find({"user": user});
    print(Action6Result)

# Action 7: <describe the action here>
# see all questions a user posted
def Action7(collection, user):
    userAsks = collection.find({"username": user})
    print(userAsks)

# Action 8: <describe the action here>
# Delete an Article
def Action8(collection, article):

    # Delete from Articles
    Action8Result = collection.delete_one({"Title": article})
    print(Action8Result)

    # Delete all comments in user...
    # Action8Resultpart2 = collection.delete_many({"Title": article})
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

    init(db)
    # Can create collection and check if they exist...
    print('Initialized hackernews MongoDB...')

    try:
        while(True):

            print("Action 1: A user publishes an article                    arguments: <1, username, title>")
            print("Action 2: List the 10 highest upvoted articles           arguments: <2>")
            print("Action 3: Upvote article                                 arguments: <3, article>")
            print("Action 4: User adds comment                              arguments: <4, article, comment>")
            print("Action 5: User changes their password                    arguments: <5, username, newPassword>")
            # Find all entries in marketplace by user
            print("Action 6: Show all users with posts in Marketplace       arguments: <6, username>")
            print("Action 7: See all questions a user posted                arguments  <7, username>")
            print("Action 8: User deletes an article they posted            arguments  <8, article>")
            print("Or type 'exit' to close the shell...")

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

            # Action 1: From given example
            # A user publishes an article

            if actionNumber == 1:
                if len(args) != 3:
                    print('Invalid number of arguments!')
                    continue
                user = args[1]
                title = args[2]
                Action1(dbColl, user, title)

            # Action 2: <describe the action here>
            # A user sees a list of the 1 highest-voted articles

            elif actionNumber == 2:
                if len(args) != 1:
                    print('Invalid number of arguments!')
                    continue
                Action2(dbColl)

            # Action 3: <describe the action here>
            # A user up-votes an article
            elif actionNumber == 3:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action3(dbColl, article)

            # Action 4: <describe the action here>
            # A user comments on an article
            elif actionNumber == 4:
                if len(args) != 3:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                comment = args[2]
                Action4(dbColl, article, comment)

            # Action 5: <describe the action here>
            # User changes their password
            elif actionNumber == 5:
                if len(args) != 3:
                    print('Invalid number of arguments!')
                    continue
                user = args[1]
                newPasswd = args[2]
                Action5(dbColl, user, newPasswd)

            # Action 6: <describe the action here>
            # User Selects 10 most recently posted articles
            elif actionNumber == 6:
                if len(args) != 1:
                    print('Invalid number of arguments!')
                    continue
                Action6(dbColl)

            # Action 7: <describe the action here>
            # see all questions a user posted
            elif actionNumber == 7:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                user = args[1]
                Action7(dbColl, user)

            # Action 8: <describe the action here>
            # User deletes an article they posted
            elif actionNumber == 8:
                if len(args) != 2:
                    print('Invalid number of arguments!')
                    continue
                article = args[1]
                Action8(dbColl, article)

            else:
                print('Invalid Action')

    except KeyboardInterrupt:
        print('\nctrl-c received, exiting')
        return

if __name__ == "__main__":
    main()