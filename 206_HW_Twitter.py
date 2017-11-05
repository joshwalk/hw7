import unittest
import tweepy
import requests
import json
import twitter_info


## SI 206 - HW
## Joshua Walker
## Your section day/time: Thu 6-7pm

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = 'cache_twitter_searches.json' # JSON file for caching

# the following code is modeled after cache_example.py from class
try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

def getSearchWithCaching(search_query):
    if search_query in CACHE_DICTION: # if search term is found in cache, use this data
        print("using cache")
        return CACHE_DICTION[search_query] # returns cached results of that query
    else: # if not, get the data from Twitter
        print("fetching")
        results = api.search(q=search_query, count=5)
        try:
            CACHE_DICTION[search_query] = results
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache) # writes results of that query to cache
            fw.close() # Close the open file
            return CACHE_DICTION[search_query] # returns results of that query
        except:
            print("not in cache and invalid search")
            return None

count = 0
while count < 3: # runs the following 3 times
    search_term = input("Enter tweet term: ")
    data = getSearchWithCaching(search_term) # runs input through function
    for tweet in data["statuses"]: # for each tweet, prints text and time
        print("TEXT: " + tweet["text"])
        print("CREATED AT: " + tweet["created_at"] + "\n")
    count += 1
