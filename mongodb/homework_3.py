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

# Get the database and collection
db = client.test
collection = db.movies

# movieCount = collection.find({}).count()
# print("There are " + str(movieCount) + " movies")
# print(collection.find({ })[0])

'''
A. Update all movies with "NOT RATED" at the "rated" key to be "Pending rating". 
The operation must be in-place and atomic.
'''

result = collection.update_many(
   { "rated": "NOT RATED" }, # Given this condition being true
   { "$set": { "rated": "Pending rating" }}
)

# print("result is: " + str(result.modified_count))
# pprint(collection.find({"rated": "NOT RATED"}).count())

'''
B. Find a movie with your genre in imdb and insert it into your database with the fields listed in the hw description.
insert it into your database with the fields listed below. Each field type must match that of the other documents in
the collection. For example, the genres field is an array, so your new document must also represent the genres as an array.
My Link:
https://www.imdb.com/search/title?title_type=short&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=17d3863a-3e07-4c9b-a09a-f643edc8e914&pf_rd_r=1QGYK8JNRENVXZBNN6QX&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_19
https://www.imdb.com/title/tt7860270/?ref_=adv_li_tt
'''

result_b = collection.insert_one
({
       "title": "pandas",
       "year": 2018,
       "countries": ["USA"],
       "genres": ["Documentary", "Short"],
       "directors": ["David Douglass", "Drew Fellman"],
       "imdb": { "id":1, "rating":7.7, "votes":38}
})
# print("result of part b is: " + list(result_b))

'''
C. Use the aggregation framework to find the total number of movies in your genre.
Example result:
=> [{"_id"=>"Comedy", "count"=>14046}]
unwind: https://docs.mongodb.com/manual/reference/operator/aggregation/unwind/
Count: https://docs.mongodb.com/manual/reference/operator/aggregation/count/
Another way to count documents in group:
https://stackoverflow.com/questions/40791907/what-does-sum1-mean-in-mongo
'''

resultsC = collection.aggregate
([
    { "$unwind": "$genres"},
    { "$match": { "genres": "Short" }},
    { "$group": { "_id": "=>Short", "count":{"$sum":1}}}
])
# print(type(resultsC))
# print(resultsC.find({ }))
'''
D. Use the aggregation framework to find the number of movies made in the country
you were born in with a rating of "Pending rating".
unwind, match, group, project.

Example result when country is Hungary:
=> [{"_id"=>{"country"=>"Hungary", "rating"=>"Pending rating"}, "count"=>9}]
'''

resultsD = collection.aggregate([
    { "$unwind": "$countries"},
    { "$match": { "rating": "Pending rating", "countries":"USA" }},
    { "$group": {"_id": "country=>USA, rating=>Pending rating", "count": {"$sum":1}}}
])
# print(list(resultsD))

'''
E. Create an example using the $lookup pipeline operator. See hw description for more info.
$lookup:
{
    from: <collections to join>,
    localField: <field from the input doucments>,
    foreignField: <field from the documents of the "from" collection>,
    as: <output array field>
}
Citation:
https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
'''
# To create new collections, I ran this on the shell...
# db.createCollection("orders")
# db.createCollection("inventory")

# Clean everything...
db.orders.remove( { } )
db.inventory.remove( { } )

# Now insert!
db.orders.insert([
   { "_id" : 3, "item" : "almonds", "price" : 12, "quantity" : 2 },
   { "_id" : 4, "item" : "pecans", "price" : 20, "quantity" : 1 }
])

db.inventory.insert([
   { "_id" : 5, "sku" : "almonds", "description": "product 1", "instock" : 120 },
   { "_id" : 6, "sku" : "bread", "description": "product 2", "instock" : 80 },
   { "_id" : 7, "sku" : "cashews", "description": "product 3", "instock" : 60 },
   { "_id" : 8, "sku" : "pecans", "description": "product 4", "instock" : 70 },
])

db.orders.aggregate([{
"$lookup":
{
    'from': "inventory",
    'localField': "item",
    'foreignField': "sku",
    'as': "inventory_docs"
}
}])