#!/usr/bin/env python

#MIT License
#
#Copyright (c) 2017 Mike Cardosa 
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from __future__ import print_function
import sys
import os
import argparse
from datetime import datetime
import logging
import csv
import re

try:
    import tweepy
    tweepy_installed = True
except ImportError:
    tweepy_installed = False

__version__ = "0.2.0"    

# Twitter API credentials
consumer_key = os.getenv('TWITTER_CONSUMER_KEY', "")
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', "")
access_key = os.getenv('TWITTER_ACCESS_KEY', "")
access_secret = os.getenv('TWITTER_ACCESS_SECRET', "")


# fetch_all_tweets() based on https://gist.github.com/yanofsky/5436496
def fetch_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    # initialize a list to hold all the tweepy Tweets
    all_tweets = []  
    
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    
    # save most recent tweets
    all_tweets.extend(new_tweets)
    
    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
    
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        logging.debug("getting tweets before %s" % (oldest))
        
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        
        # save most recent tweets
        all_tweets.extend(new_tweets)
        
        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1
        
        logging.debug("...%s tweets downloaded so far" % (len(all_tweets)))
    
    # transform the tweepy tweets into a 2D array that will populate the csv 
    results = [[screen_name, tweet.id_str, tweet.created_at, tweet.text, "https://twitter.com/%s/status/%s" % (screen_name, tweet.id_str)] for tweet in all_tweets]

    return results
    




def main():
    # If the tweepy library isn't installed we need to exit
    if not tweepy_installed:
        print("Error: The tweepy library must be installed to use tweetgrep.")
        sys.exit()

    # Check to make sure all the Twitter API credentials are available
    if consumer_key == "":
        print("Error: consumer_key must be set in tweetgrep.py or set the TWITTER_CONSUMER_KEY environment variable")
        sys.exit()
    if consumer_secret == "":
        print("Error: consumer_secret must be set in tweetgrep.py or set the TWITTER_CONSUMER_SECRET environment variable")
        sys.exit()
    if access_key == "":
        print("Error: access_key must be set in tweetgrep.py or set the TWITTER_ACCESS_KEY environment variable")
        sys.exit()
    if access_secret == "":
        print("Error: access_secret must be set in tweetgrep.py or set the TWITTER_ACCESS_SECRET environment variable")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Enable debugging output",
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.WARNING)
    parser.add_argument("-i", "--ignore-case", help="Ignore case when searching",
        action="store_true", dest="ignore_case",
        default=False)
    parser.add_argument("-b", "--brief-output", help="Only show the contents of the tweets without extra information (date and link)",
        action="store_true", dest="brief_output",
        default=False)
    parser.add_argument("-r", "--regex", help="Search using a regex instead of a simple string",
        action="store_true", dest="use_regex",
        default=False)
    parser.add_argument("-f", "--force-download", help="Force a download of the user's tweets instead of using the local cache",
        action="store_true", dest="force_download",
        default=False)
    parser.add_argument("-V", "--version", action="version",
                    version="%(prog)s {version}".format(version=__version__))
    parser.add_argument("search_string", help="The string you are searching for in a user's tweets")
    parser.add_argument("twitter_name", help="User's Twitter name you are searching")

    args = parser.parse_args()

    logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', level=args.log_level)

    logging.debug("Twitter name: %s" % args.twitter_name)
    twitter_name = args.twitter_name
    # Remove the leading @ character if present in the Twitter name
    if twitter_name[0] == '@':
        twitter_name = twitter_name[1:]
        logging.debug('Cleaned Twitter name: %s' % twitter_name)
    logging.debug("Search term: %s" % args.search_string)
    search_string = args.search_string

    cache_name = "%s_cache.dat" % twitter_name
    logging.debug("Cache name: %s" % cache_name)

    # See if a cache file exists and it it does, how old it is in days
    try:
        cache_modified_time = os.path.getmtime(cache_name)
        cache_exists = True
        logging.debug("Found existing cache file")
        cache_modified_date = datetime.fromtimestamp(cache_modified_time)
        logging.debug("Cache modified date: %s" % cache_modified_date)
        day_diff = datetime.now() - cache_modified_date
        logging.debug("Cache file is %s days old" % day_diff.days)
    except:
        cache_exists = False
        logging.debug("Did not find existing cache file")
        create_cache = True
    
    
    if args.force_download is True or (cache_exists and day_diff.days >= 1):
        # If the cache is older than 1 day or if the -f flag was used we try to refresh the file
        logging.debug("Attempting to delete old cache file")
        try:
            os.remove(cache_name)
            logging.debug("Cache file successfully deleted")
            create_cache = True
        except OSError:
            logging.warn("Could not remove old cache file")
            logging.warn("Results could be stale. You should manually remove %s" % cache_name)
            create_cache = False
    elif cache_exists:
        # A cache file is found and is new enough to be used for the search
        logging.debug("Cache file is relatively new and will be used for this search")
        create_cache = False
    else:
        # No cache file found
        create_cache = True
        logging.debug("Need to create a new cache file")

    if create_cache:
        # Download all the tweets from the user's timeline (max 3200)
        user_tweets = fetch_all_tweets(twitter_name)

        # write the csv  
        with open(cache_name, 'wt') as f:
            logging.debug("Creating new cache file")
            writer = csv.writer(f)
            writer.writerow(["screen_name","id","created_at","text","status_link"])
            writer.writerows(user_tweets)

    if args.use_regex:
        regex = re.compile(search_string)

    with open(cache_name, 'rt') as f:
        hit_counter = 0
        tweet_counter = -1
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            tweet_counter += 1
            if args.ignore_case:
                tweet = row[3].lower()
                search_string = search_string.lower()
            else:
                tweet = row[3]

            if args.brief_output:
                output = "%s" % row[3]
            else:
                output = "%s\t%s\n%s" % (row[2], row[3], row[4])

            if not args.use_regex and search_string in tweet:
                hit_counter += 1
                print(output)
            elif args.use_regex and regex.search(tweet):
                hit_counter += 1
                print(output)
            else:
                pass

    print("Found %s total results in %s tweets" % (hit_counter, tweet_counter))


if __name__ == '__main__':
    main()
