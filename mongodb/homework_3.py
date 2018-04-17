# require the driver package
from pprint import pprint
import pymongo
from pymongo import MongoClient

# Other Comands executed
# pip install pymongo
# mongod (run database)

# mongorestore movies.bson
# mongo (connect to mongo shell)

# Create a client, this is the default
client = MongoClient()

# Get the database
db = client.test

# Start queries
collection = db.movies
movieCount = collection.find({}).count()
# print("There are " + str(movieCount) + " movies")
# print(collection.find({ })[0])

# A. Update all movies with "NOT RATED" at the "rated" key to be "Pending rating". The operation must be in-place and atomic.

result = collection.update_many(
   { "rated": "NOT RATED" }, # Given this condition being true
   { "$set": { "rated": "Pending rating" }}
)

# print("result is: " + str(result.modified_count))
# pprint(collection.find({"rated": "NOT RATED"}).count())

# B. Find a movie with your genre in imdb and insert it into your database with the fields listed in the hw description.
# insert it into your database with the fields listed below. Each field type must match that of the other documents in
# the collection. For example, the genres field is an array, so your new document must also represent the genres as an array.

# title (string)
# year (integer)
# countries (array)
# genres (array)
# directors (array)
# imdb (document with fields: 'id' (integer),
# 'rating' (float),
# 'votes' (integer).
# If the values aren't available for the movie you chose, find one that has those values or make the values up)

# My Link:
# https://www.imdb.com/search/title?title_type=short&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=17d3863a-3e07-4c9b-a09a-f643edc8e914&pf_rd_r=1QGYK8JNRENVXZBNN6QX&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_19
# https://www.imdb.com/title/tt7860270/?ref_=adv_li_tt

result_b = collection.insert_one
({
       "title": "pandas",
       "year": 2018,
       "countries": ["USA"],
       "genres": ["Documentary", "Short"],
       "directors": ["David Douglass", "Drew Fellman"],
       "imdb": { "id":1, "rating":7.7, "votes":38}
})
# print("result of part b is: " + str(result_b.modified_count))

# C. Use the aggregation framework to find the total number of movies in your genre.

# Example result:
#  => [{"_id"=>"Comedy", "count"=>14046}]

# SQL:
# Select * from imdb
# where rating = 'Short'
# group by
# unwind, match, group then project...

# unwind: https://docs.mongodb.com/manual/reference/operator/aggregation/unwind/
# Count: https://docs.mongodb.com/manual/reference/operator/aggregation/count/
'''
resultsC = collection.aggregate
([
    { "$unwind": "$genres"},
    { "$match": { "genres": "Short" }},
    { "$group": { "_id": "$genres", "$count":"count"}},
    { "$project": {"_id": "$genres", "$count":"count"}}
])
print(resultsC.modified_count)
'''

# D. Use the aggregation framework to find the number of movies made in the country
# you were born in with a rating of "Pending rating".
# unwind, match, group, project...

# Example result when country is Hungary:
#  => [{"_id"=>{"country"=>"Hungary", "rating"=>"Pending rating"}, "count"=>9}]

'''
resultsD = collection.aggregate([
    { "$unwind": "$countries"},
    { "$match": { "rating": "Pending rating", "countries":"USA" }},
    { "$group": {{"_id": "$countries", "rating":"$rating"}, "$count": "count"}},
    { "$project": {{"country": "$countries", "rating":"$rating"}, "$count": "count"}}
])
print(resultsD.modified_count)
'''

# E. Create an example using the $lookup pipeline operator. See hw description for more info.
#$lookup:
#{
#    from: <collections to join>,
#    localField: <field from the input doucments>,
#    foreignField: <field from the documents of the "from" collection>,
#    as: <output array field>
#}
#
# Citation:
# https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
# Also used the same insert command...
#
# db.createCollection("orders")
# db.createCollection("inventory")
# Used their insert command

db.orders.aggregate([{
'$lookup':
{
	'from': 'inventory',
	'localField': 'item',
	'foreignField': 'sku',
	'as': 'inventory_docs'
}
}])
# argument explanation...
# copy from inventory to orders
# In orders (local to orders)
# In inventory (local to inventory)
# name of new document appended
# From example, where item==sku, in orders, place the
# matching inventory document.

