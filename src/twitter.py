import configparser
import os
import pandas as pd  # for save tweet in SVG
import tweepy

def get_key(section, setting):
	"""
	The get_key function is a helper function that retrieves the value of a setting from the configuration file.
	
	:param section: Specify the section of the config file to read
	:param setting: Specify the setting that is being retrieved
	:return: The value of the setting in the specified section
	"""
	try:        
		key = config.get(section, setting)
	except configparser.NoOptionError:
		key = None
	return key

def __init__():
	# read configuration from config file
	global config
	config = configparser.ConfigParser()
	my_path = os.path.abspath('config.ini')
	config.read(my_path)
	section = 'twitter'		#! change it as your [param] on config.ini file 
	api_key = get_key(section, 'api_key')
	api_key_secret = get_key(section, 'api_key_secret')

	access_token = get_key(section, 'access_token')
	access_token_secret = get_key(section, 'access_token_secret')

	bearer_token = get_key(section, 'bearer_token')

	# authentication
	global api 
	# auth = tweepy.OAuthHandler(api_key, api_key_secret)#! deprecated: only for v1.0a
	api = tweepy.Client(
		bearer_token=bearer_token,
		consumer_key=api_key,
		consumer_secret=api_key_secret,
		access_token=access_token,
		access_token_secret=access_token_secret
	)

	# api = tweepy.API(auth)	# api istant 

	# # -- try to print my twitter home --
	# global public_tweets 
	# public_tweets = api.home_timeline()

	# for tweet in public_tweets:		# to print all in home
	# 	print(tweet.text)

	# print(public_tweets[0].text)		# to print only the first tweet in home
	# print(public_tweets[0].created_at)	# to print the first tweet time
	# print(public_tweets[0].user.screen_name)	# to print the user creator of the tweets
	
	
def GetTweetByKeyword(keywords, numTweet):
	'''
	Get Tweet by Hashtag and Keyword

	:param keywords: keyword or hashtag to search
	:param numTweet: max number of Tweet to get
	:return dataframe of all the finded tweet to convert
	'''
	limit = numTweet
	
	# tweets = tweepy.Cursor(api.search_all_tweets, query = keywords, max_result = 100, tweet_mode = 'extended').items(limit)	# this let us to get more than 100 tweets
	tweets = api.search_recent_tweets(query = keywords, tweet_fields=['user, full_text'])
	# -- create DataFrame --
	columns = ['user', 'tweet']
	data = []
	for tweet in tweets:
		data.append([tweet.user, tweet.full_text])

	data_frame = pd.DataFrame(data, columns = columns)
	return data_frame

'''
	Get Tweet by Username

	:param user: username to get Tweet
	:param numTweet: max number of Tweet to get
	:return dataframe of all the finded tweet to convert
'''
def GetTweetByUser(user, numTweet):
	limit = numTweet		# max num of tweet to get from the user
	tweets = tweepy.Cursor(api.user_timeline, screen_name = user, count = 200, tweet_mode = 'extended').items(limit)	# this let us to get more than 200 tweets
	# tweets = api.user_timeline(screen_name = user, count = limit, tweet_mode = 'extended')	# tweet_mode = 'extended' ci permette di leggfere tutto il contenuto del tweet senza avere troncamenti
	# -- create DataFrame --
	columns = ['user', 'tweet']
	data = []
	for tweet in tweets:
		data.append([tweet.user.screen_name, tweet.full_text])

	data_frame = pd.DataFrame(data, columns = columns)
	return data_frame