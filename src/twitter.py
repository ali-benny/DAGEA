import configparser
import os
import pandas as pd  # for save tweet in SVG
import tweepy

global location_data	# list of tweet with coordinates with [user, text, lon, lat]
global location_data_frame

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
	"""
	The __init__ function is called automatically every time the class is 
	instantiated. It can take arguments, but doesn’t return anything. The __init__ 
	method has to do with creating and initializing an object.
	
	Returns
	-------
		The api object
	"""
	# read configuration from config file
	global config
	config = configparser.ConfigParser()
	my_path = os.path.abspath('config.ini')
	config.read(my_path)
	section = 'twitter'  #! change it as your [param] on config.ini file
	api_key = get_key(section, 'api_key')
	api_key_secret = get_key(section, 'api_key_secret')

	access_token = get_key(section, 'access_token')
	access_token_secret = get_key(section, 'access_token_secret')

	# authentication
	auth = tweepy.OAuthHandler(api_key, api_key_secret)
	auth.set_access_token(access_token, access_token_secret)

	global api
	# api istant NOTE: add wait_on_rate_limit=True for 429 error
	api = tweepy.API(auth)
	return api

def GetTweetByKeyword(keywords, numTweet, location=False):
	"""
	The GetTweetByKeyword function takes a list of keywords and the number of tweets you want to get. 
	It save and create a dataframe of all tweet searched and if i want to get only tweet with location i save the tweet with location in a dedicated list.
	It's important to say that it ALWAYS save the tweet in the dataframe [also the tweet without location when i searched location].
	
	## Parameters
		keywords
			Search for tweets with the given keywords
		numTweet
			Limit the number of tweets that will be returned
		location=False
			Indicate whether or not you want to save the location of each tweet
	
	## Returns
		A dataframe with the columns: user, tweet
	"""
	data = []
	location_data = []
	# -- get tweets --
	if numTweet <= 100:
		tweets = api.search_tweets(q = keywords, count = numTweet)	# this let us to get more than 100 tweets
	else:
		tweets = tweepy.Cursor(api.search_tweets, q = keywords, count = 100).items(numTweet)
	# -- save tweets in lists --
	for tweet in tweets:
		data.append((tweet.user.screen_name, tweet.text))
		# I want to save location of tweet?
		if location and (tweet.coordinates is not None): 
			lon = tweet.coordinates['coordinates'][0]
			lat = tweet.coordinates['coordinates'][1]
			location_data.append([tweet.user.screen_name, tweet.text, lon, lat])
	# -- create DataFrame --
	columns = ['user', 'tweet']
	data_frame = pd.DataFrame(data, columns = columns)
	columns = ['user', 'tweet', 'lat', 'lon']
	location_data_frame = pd.DataFrame(location_data, columns = columns)
	location_data_frame.to_json('location.json')
	return data_frame

def GetTweetByUser(user, numTweet, location=False):
	tweets = tweepy.Cursor(api.user_timeline, screen_name = user, count = 200, tweet_mode = 'extended').items(numTweet)
	# -- create DataFrame --
	columns = ['user', 'tweet']
	data = []
	for tweet in tweets:
		data.append([tweet.user.screen_name, tweet.full_text])
	data_frame = pd.DataFrame(data, columns = columns)
	return data_frame
