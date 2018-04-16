# require the driver package
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
db = client.amazon

# Start queries
db.find({"items.fruit": "banana"}).count()

# A. Update all movies with "NOT RATED" at the "rated" key to be "Pending rating". The operation must be in-place and atomic.
db.inventory.updateMany(
   { rated: "NOT RATED" },
   {
     $set: { "rated": "Pending rating" },
     $currentDate: { lastModified: true }
   }
)
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

db.inventory.insertOne(
   {
       title: "pandas",
       year: 2018,
       counties: ["USA"],
       genres: { "Documentary", "Short" }
       directors: {"David Douglass", "Drew Fellman"}
       #imdb{ id=1, rating=7.7, votes =38}
    )

# C. Use the aggregation framework to find the total number of movies in your genre.

# Example result:
#  => [{"_id"=>"Comedy", "count"=>14046}]

# SQL:
# Select * from imdb
# where rating = 'Short'
# group by
db.orders.aggregate([
    { $match: { genre: "Short" },
    { $group: { _id=>"$genre", count=>{$count: "$match"}}}}
])

# D. Use the aggregation framework to find the number of movies made in the country you were born in with a rating of "Pending rating".
db.orders.aggregate([
    { $match: { rating: "Pending rating", countries:"USA" }, #Check for USA?
    { $group: { _id=>{country=>"$countries", rating=>Pending rating}, count=>{$count: "$match"}}
    }}}
])

# Example result when country is Hungary:
#  => [{"_id"=>{"country"=>"Hungary", "rating"=>"Pending rating"}, "count"=>9}]

# E. Create an example using the $lookup pipeline operator. See hw description for more info.
#$lookup:
#{
#    from: <collections to join>,
#    localField: <field from the input doucments>,
#    foreignField: <field from the documents of the "from" collection>,
#    as: <output array field>
#}

$lookup:
{
    from: hw4.pro, hw4.con
    localField: <field from the input doucments>,
    foreignField: <field from the documents of the "from" collection>,
    as: <output array field>
}