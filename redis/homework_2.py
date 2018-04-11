import redis
import datetime


ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432

def article_vote(redis, user, article):
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=ONE_WEEK_IN_SECONDS)

    if not datetime.datetime.fromtimestamp(redis.zscore('time:', article)) < cutoff:
        # Get the Article ID
        article_id = article.split(':')[-1]
        
        # Increase vote count by 1
        if redis.sadd('voted:' + article_id, user): 
            redis.zincrby('score:', VOTE_SCORE, article)
            redis.hincrby(article, 'votes', 1)

def article_switch_vote(redis, user, from_article, to_article):
    # HOMEWORK 2 Part I
    # Get Both Article ID, see above method
    article_to = from_article.split(':')[-1]
    article_from = to_article.split(':')[-1]

    # Move Article
    redis.smove('vote: ' + article_from, 'vote: ' + article_to, user)

    # Use the same method as above to increment count
    redis.zincrby('score:', VOTE_SCORE, article_to)
    redis.hincrby(article_to, 'votes', 1)

    # Use the same method but this time decrement the vote by using -1
    redis.zincrby('score:', VOTE_SCORE, article_from)
    redis.hincrby(article_from, 'votes', -1)
    pass

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
# user:3 up votes article:1
article_vote(redis, "user:3", "article:1")
# user:3 up votes article:3
article_vote(redis, "user:3", "article:3")
# user:5 switches their vote from article:1 to article:0 
# (Article 8 -1 Vote, Article 1 +1 Vote)
article_switch_vote(redis, "user:2", "article:8", "article:1")

# Which article's score is between 10 and 20?
# PRINT THE ARTICLE'S LINK TO STDOUT:
# HOMEWORK 2 Part II

# Get all values from 10 to 20
article = redis.zrange('score:',10, 20)

# Get the link
easterEgg = redis.hget(article[0],'link')

# I got the egg!
print easterEgg
