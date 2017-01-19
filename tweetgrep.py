#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import argparse
from datetime import datetime
import logging
import csv

try:
    import tweepy
    tweepy_installed = True
except ImportError:
    tweepy_installed = False

#Twitter API credentials
consumer_key = os.getenv('TWITTER_CONSUMER_KEY', "")
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', "")
access_key = os.getenv('TWITTER_ACCESS_KEY', "")
access_secret = os.getenv('TWITTER_ACCESS_SECRET', "")


#fetch_all_tweets() based on https://gist.github.com/yanofsky/5436496
def fetch_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    all_tweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    
    #save most recent tweets
    all_tweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        logger.debug("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        
        #save most recent tweets
        all_tweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1
        
        logger.debug("...%s tweets downloaded so far" % (len(all_tweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    results = [[screen_name, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), "https://twitter.com/%s/status/%s" % (screen_name, tweet.id_str)] for tweet in all_tweets]

    return results
    




def main():
    if not tweepy_installed:
        print("Error: The tweepy library must be installed to use tweetgrep.")
        sys.exit()

    if consumer_key == "":
        print("Error: consumer_key must be set in tweetgrep.py")
        sys.exit()
    if consumer_secret == "":
        print("Error: consumer_secret must be set in tweetgrep.py")
        sys.exit()
    if access_key == "":
        print("Error: access_key must be set in tweetgrep.py")
        sys.exit()
    if access_secret == "":
        print("Error: access_secret must be set in tweetgrep.py")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Enable debugging output",
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.WARNING)
    parser.add_argument("search_string", help="The string you are searching for in a user's tweets")
    parser.add_argument("twitter_name", help="User's Twitter name you are searching")

    args = parser.parse_args()

    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level=args.log_level)
    handler = logging.FileHandler('tweetgrep.log')
    handler.setLevel(args.log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug("Twitter name: %s" % args.twitter_name)
    twitter_name = args.twitter_name
    logger.debug("Search term: %s" % args.search_string)
    search_string = args.search_string

    cache_name = "%s_cache.dat" % twitter_name
    logger.debug("Cache name: %s" % cache_name)

    try:
        cache_modified_time = os.path.getmtime(cache_name)
        cache_exists = True
        logger.debug("Found existing cache file")
        cache_modified_date = datetime.fromtimestamp(cache_modified_time)
        logger.debug("Cache modified date: %s" % cache_modified_date)
        day_diff = datetime.now() - cache_modified_date
        logger.debug("Cache file is %s days old" % day_diff.days)
    except:
        cache_exists = False
        logger.debug("Did not find existing cache file")
        create_cache = True
    
    
    if cache_exists and day_diff.days >= 1:
        #If the cache is older than 1 day we try to refresh it
        logger.debug("Attempting to delete old cache file")
        try:
            os.remove(cache_name)
            logger.debug("Cache file successfully deleted")
            create_cache = True
        except OSError:
            logger.warn("Could not remove old cache file")
            logger.warn("Results could be stale. You should manually remove %s" % cache_name)
            create_cache = False
    elif cache_exists:
        logger.debug("Cache file is relatively new and will not be removed")
        create_cache = False
    else:
        create_cache = True
        logger.debug("Need to create a new cache file")

    if create_cache:
        user_tweets = fetch_all_tweets(twitter_name)

        #write the csv  
        with open(cache_name, 'w') as f:
            logger.debug("Creating new cache file")
            writer = csv.writer(f)
            writer.writerow(["screen_name","id","created_at","text","status_link"])
            writer.writerows(user_tweets)




if __name__ == '__main__':
    main()