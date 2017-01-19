# tweetgrep

tweetgrep is a simple Python script that searches a Twitter user's tweets for a specific search term.

## Installation

### Prerequisites

tweetgrep requires the Tweepy library, which can be installed via pip:

```
pip install tweepy
```

You will also need Twitter API keys and secrets that you can get by creating an application on https://apps.twitter.com 

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

## Usage



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
