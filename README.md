# tweetgrep

tweetgrep is a simple Python script that searches a Twitter user's tweets for a specific search term.

## Contents
* [Installation](#installation)
 * [Prerequisites](#prerequisites)
 * [Installing tweetgrep](#installingtweetgrep)
 * [Configuring tweetgrep](#configuringtweetgrep)
* [Usage](#usage)
* [How it works](#howitworks)
 * [Caching](#caching)
* [License](#license)
 
<a name="installation"></a>
## Installation

<a name="prerequisites"></a>
### Prerequisites

tweetgrep has only been tested on Linux with Python 3. It likely will not work cleanly with Python 2 without some modifications.

tweetgrep requires the Tweepy library, which can be installed via pip:

```
pip install tweepy
```

You will also need Twitter API keys and secrets that you can get by creating an application on https://apps.twitter.com 

<a name="installingtweetgrep"></a>
### Installing tweetgrep

Since tweetgrep is a standalone script, there really isn't much to install.

You can clone the entire repository:

```
git clone https://github.com/doza/tweetgrep.git
```

You can also download the script itself:

```
wget https://raw.githubusercontent.com/doza/tweetgrep/master/tweetgrep.py
```

Once tweetgrep.py is on your system, mark it as an executable if it isn't already:

```
chmod 755 tweetgrep.py
```

<a name="configuringtweetgrep"></a>
### Configuring tweetgrep

tweetgrep requires 4 pieces of information from Twitter in order to interact with the Twitter API:

1. CONSUMER_KEY
2. CONSUMER_SECRET
3. ACCESS_KEY
4. ACCESS_SECRET

These can all be found on the **Keys and Access Tokens** tab after creating an application on https://apps.twitter.com.

Once you have all of your personal Twitter API credentials, you have two options for configuring tweetgrep.  You can either use environment variables or place the information directly into the tweetgrep.py file.

#### Option 1: Credentials in Environment Variables

If you prefer to keep all of the Twitter API credentials in environment variables, you should make sure that the following are set in the shell where tweetgrep will be run:

1. TWITTER_CONSUMER_KEY
2. TWITTER_CONSUMER_SECRET
3. TWITTER_ACCESS_KEY
4. TWITTER_ACCESS_SECRET

#### Option 2: Credentials in tweetgrep.py

If you prefer to simply place your Twitter API credentials into the tweetgrep.py file, you should edit the following lines to place the relevant information in between the double quotes:

```
#Twitter API credentials
consumer_key = os.getenv('TWITTER_CONSUMER_KEY', "")
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', "")
access_key = os.getenv('TWITTER_ACCESS_KEY', "")
access_secret = os.getenv('TWITTER_ACCESS_SECRET', "")
```

For example:

```
#Twitter API credentials
consumer_key = os.getenv('TWITTER_CONSUMER_KEY', "ABLJHBDFISBD")
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', "AIBCODNDOSNV")
access_key = os.getenv('TWITTER_ACCESS_KEY', "AONVDO8iuB78")
access_secret = os.getenv('TWITTER_ACCESS_SECRET', "LKH82IKAV00")
```

Once your credential information is set, you are ready to use tweetgrep.

<a name="usage"></a>
## Usage

```
usage: tweetgrep.py [-h] [-d] [-i] [-b] [-r] [-V] search_string twitter_name

positional arguments:
  search_string       The string you are searching for in a user's tweets
  twitter_name        User's Twitter name you are searching

optional arguments:
  -h, --help          show this help message and exit
  -d, --debug         Enable debugging output
  -i, --ignore-case   Ignore case when searching
  -b, --brief-output  Only show the contents of the tweets without extra
                      information (date and link)
  -r, --regex         Search using a regex instead of a simple string
  -V, --version       show program's version number and exit
```

<a name="howitworks"></a>
## How it works

tweetgrep uses the Twitter API to download a user's tweets and search for the specified term or pattern.  At a high level, this is how it works:

1. tweetgrep leverages the Tweepy library to query the Twitter API using your credentials in order to download all of a user's tweets. **Note: due to limitations with the Twitter API, we are only able to retrieve and search the last 3,200 tweets from an individual user.**
2. All of the tweets returned by the API are stored in a local CSV file in the current directory that uses the naming convention username_cache.dat. For example, if you are searching tweets from the BillGates Twitter account the file will be named billgates_cache.dat.
3. tweetgrep then searches the tweets contained in the local .dat file and prints any results.

<a name="caching"></a>
### Caching

In order to speed up future searches and not constantly hit the API, tweetgrep first looks for a local cache file containing the user's tweets before requesting results from the API.  If a cache file exists and is less than 1 day old, that file will be used for the search.  If the file does not exist or is more than 1 day old, tweetgrep will query the Twitter API and use those results to create a new cache file that will be used for the search.

You may manually delete any of the cache.dat files to force tweetgrep to use the API instead of cached tweets.

<a name="license"></a>
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
