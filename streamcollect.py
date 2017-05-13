import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import json
from langdetect import detect
from langdetect import lang_detect_exception

#added by ink
def load_api_auth():
    """ loads api wrapper and OauthHandler"""

    consumer_key = ‘’
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # load the twitter API via tweepy
    return [tweepy.API(auth),auth]

def clean2(model):
    """further refines tweets only called on tweets which have passed preprocessing as
    to not waste resources"""
    cleaned = ''
    if model:
        for char in model:
            if char != ' ':
                if char.isalpha():
                    char = char.lower().strip()
            elif char == '.':
                char = ' '
            cleaned+=char
        cleaned = cleaned[0].upper()+cleaned[1:]
        if cleaned.find(' i ') != -1:
            cleaned = cleaned.replace(' i ', ' I ')
    return cleaned


#added by ink
def clean(tweet,tweet_map):
    """ takes string as arg returns tweets not containing filter terms (http,@,follow)
    also removes non-english tweets"""
    if tweet:
        try:
            if tweet.find('http')!=-1\
            or tweet.find('@')!=-1\
            or tweet.find('follow')!=-1\
            or detect(tweet) != 'en':
                return ''
            else:
                if tweet.find(' &amp; ') != -1:
                    tweet.replace(' &amp; ',' & ')
                try:
                    tweet_map[tweet]
                    return ''
                except KeyError:
                    #returns the tweet only if it's not in the map already
                    #to combat spam
                    tweet = clean2(tweet)
                    return tweet+'\n'
        except lang_detect_exception.LangDetectException:
            return ''

#updates the map with tweets and frequencies
#added by ink
def update_src(tweet_map, data):
    """ uses a map to reduce the amount of duplicate tweets """
    try:
        tweet_map[data] += 1
    except KeyError:
        tweet_map[data] = 0

#added by ink
def load_stream(dir, query):
    """ Starts stream with provided query and filename args """
    api_auth = load_api_auth()
    twitter_stream = Stream(api_auth[1], MyListener(dir, query))
    twitter_stream.filter(track=[query])

#slightly modified version of https://gist.github.com/bonzanini/af0463b927433c73784d
#that has some preprocessing added to keep file size down, and get only relevant material
class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.outfile = "./%s/formatted_%s_stream_.txt" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                #filtering tweets, then adding them to text file formatted
                #for markovify; added by ink
                tweet_map = {}
                    #f.write(data)
                #print(data)
                status = json.loads(data)
                if status['text']:
                    status = status['text']
                status = clean(status,tweet_map)
                update_src(tweet_map, status)
                if status:
                    f.write(status)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'
