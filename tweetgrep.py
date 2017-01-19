#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import argparse
import logging

try:
    import tweepy
    tweepy_installed = True
except ImportError:
    tweepy_installed = False

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


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
        logging.debug("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        
        #save most recent tweets
        all_tweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1
        
        logging.debug("...%s tweets downloaded so far" % (len(all_tweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    results = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]

    return results
    
    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)



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

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(level=args.log_level)
    handler = logging.FileHandler('tweetgrep.log')
    handler.setLevel(args.log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    

if __name__ == '__main__':
    main()