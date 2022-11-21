import tweepy
import configparser
import pandas as pd 	# for save tweet in SVG
from pyodide import create_proxy


# def __init__(self):
write("main", "Initialization...")
# read config from config.ini
config = configparser.ConfigParser()
config.read('../config.ini')

api_key = config['DAGEA']['api_key']
api_key_secret = config['DAGEA']['api_key_secret']

access_token = config['DAGEA']['access_token']
access_token_secret = config['DAGEA']['access_token_secret']

# TEST: verifica se prende i campi corretti
# 	print(api_key) 

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

global api = tweepy.API(auth)	# api istant

# -- try to print my twitter home --
global public_tweets = api.home_timeline()

# for tweet in public_tweets:		# to print all in home
# 	print(tweet.text)

# print(public_tweets[0].text)		# to print only the first tweet in home
# print(public_tweets[0].created_at)	# to print the first tweet time
# print(public_tweets[0].user.screen_name)	# to print the user creator of the tweet

# --- SEARCH TWEETS BY HASHTAG OR KEYWORDS ---
def GetTweetByKeyword():
	limit = 300
	write("main", "Getting Tweet ...")

	input = Element("keyword")
	keywords = input.value
	input.value = ""
	
	tweets = tweepy.Cursor(api.search_tweets, q = keywords, count = 100, tweet_mode = 'extended').items(limit)	# this let us to get more than 100 tweets
	# create DataFrame
	columns = ['user', 'tweet']
	data = []
	for tweet in tweets:
		data.append([tweet.user.screen_name, tweet.full_text])

	data_frame = pd.DataFrame(data, columns = columns)
	Element("returnTLB").element.innerHTML =  data_frame.to_html()

# --- GET TWEET BY USER --- 
def GetTweetByUser():
	user  = 'veritasium'	# user tweets that I want to get the tweet
	limit = 300		# max num of tweet to get from the user
	tweets = tweepy.Cursor(api.user_timeline, screen_name = user, count = 200, tweet_mode = 'extended').items(limit)	# this let us to get more than 200 tweets
	# tweets = api.user_timeline(screen_name = user, count = limit, tweet_mode = 'extended')	# tweet_mode = 'extended' ci permette di leggfere tutto il contenuto del tweet senza avere troncamenti
	# create DataFrame
	columns = ['user', 'tweet']
	data = []
	for tweet in tweets:
		data.append([tweet.user.screen_name, tweet.full_text])

	data_frame = pd.DataFrame(data, columns = columns)
	print(data_frame.to_html())