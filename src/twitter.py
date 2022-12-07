import os
import configparser
import pandas as pd  # for save tweet in SVG
import tweepy
import sqlite3
import time

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
	# init global variables
	location_data = []
	location_data_frame = []
	# read configuration from config file
	global config
	config = configparser.ConfigParser()
	my_path = os.path.abspath('config.ini')
	config.read(my_path)
	section = 'twitter'  # ! change it as your [param] on config.ini file
	global api_key, api_key_secret, access_token, access_token_secret
	api_key = get_key(section, 'api_key')
	api_key_secret = get_key(section, 'api_key_secret')

	access_token = get_key(section, 'access_token')
	access_token_secret = get_key(section, 'access_token_secret')

	# authentication v1.1
	auth = tweepy.OAuthHandler(api_key, api_key_secret)
	auth.set_access_token(access_token, access_token_secret)

	# # authentication v2
	# global client
	# client = tweepy.Client(get_key('twitter', 'bearer_token'))
	global api
	# api istant NOTE: add wait_on_rate_limit=True for 429 error
	api = tweepy.API(auth)
	return auth

def convertDF2SQL(dataframe, location=False, stream=False):
	"""
	The convertDF2SQL function takes a pandas dataframe and converts it to a SQL database.
	The function can also take an optional location argument, which will add the latitude and longitude if the research is with located tweets.

	Parameters
	----------
			dataframe
					Store the data in a sql database
			location
					Specify if the dataframe is a list of tweets or a list of located tweets
	"""
	global location_data
	# -- connect to db --
	connection = sqlite3.connect("database.db")
	c = connection.cursor()
	# - create table -
	if location:
		location_data_frame = pd.DataFrame(location_data, columns=['user', 'tweet', 'lat', 'lon'])
		c.execute(
			"CREATE TABLE IF NOT EXISTS located_tweet (user TEXT, tweet TEXT, lat DOUBLE, lon DOUBLE)")
		connection.commit()  # save my edits on connection
		location_data_frame.to_sql('located_tweet', connection, if_exists='replace', index=False)
		location_data_frame.to_json("located_tweet.json")

	c.execute(
		'CREATE TABLE IF NOT EXISTS all_tweets (user TEXT, tweet TEXT, location BOOLEAN, date DATETIME)')
	connection.commit()  # save my edits on connection
	if stream:
		dataframe.to_sql('all_tweets', connection, if_exists='append', index=False)
	dataframe.to_sql('all_tweets', connection, if_exists='replace', index=False)
	# save dataframe as json
	dataframe.to_json("all_tweets.json")

class MyStream(tweepy.StreamingClient):
	tweets =  []
	limit = 10
	dataframe = []
	def on_connect(self):
		print('Connected!')

	def on_status(self, status):
		self.tweets.append(status)
		if len(self.tweets) == self.limit:
			self.disconnect()
			convertDF2SQL(self.dataframe, stream=True)
	
	def on_tweet(self, tweet):
		# if tweet.refecenced_tweets == None:
		if not tweet.truncated:
			self.tweets.append([tweet.user.screen_name, tweet.text, tweet.place, tweet.created_at])
		else:
			self.tweets.append([tweet.user.screen_name, tweet.extended_tweet['full_text'], tweet.place, tweet.created_at])
		self.dataframe = pd.DataFrame(self.tweets, columns = ['user', 'tweet', 'location','date'])
		convertDF2SQL(self.dataframe, stream=True)


def StreamByKeyword(keywords):
	stream_tweet = MyStream(bearer_token=get_key('twitter','bearer_token'))
	for keyword in keywords:
		stream_tweet.add_rules(tweepy.StreamRule(keyword)) 	# add rules
	# stream_tweet.filter(tweet_fields=["referenced_tweets"])
	stream_tweet.filter()	# run the stream
	
	
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
			A dataframe with the columns: user, tweet, location
	"""
# TODO: add keyword control max 512 characters long
	data = []
	# -- get tweets --
	expansion = ["attachments.media_keys"]
	if location:	# if i want to get only tweet with location
		expansion.append("geo.place_id")
	if numTweet <= 100:
		tweets = api.search_tweets(q=keywords, count=numTweet, expansions = expansion)
		print('🎃')
	else:
		tweets = tweepy.Cursor(api.search_tweets, q=keywords, count = 100, expansions = expansion, tweet_mode='extended').items(numTweet)
	# -- save tweets in lists --
	# includes = tweets.includes
	# place = includes["geo"]
	for tweet in tweets:
		try:
			text = tweet.full_text
		except AttributeError:
			text = tweet.text
		# I want to save location of tweet?
		# print('📍', tweet.place.full_name)
			# location_data.append([tweet.user.screen_name, text, lon, lat])
		data.append((tweet.user.screen_name, text, tweet.place, tweet.created_at))
	# -- create DataFrame --
	data_frame = pd.DataFrame(data, columns=['user', 'tweet', 'location', 'date'])
	return data_frame

def GetTweetByUser(user, numTweet, location=False):
	"""
	The GetTweetByUser function takes a user and the number of tweets to retrieve. 
	It returns a DataFrame with the username, tweet text, and location (if available).

	Parameters
	----------
		user
				Specify the user's twitter handle
		numTweet
				Specify the number of tweets to be retrieved
		location
				Get the location of tweet

	Returns
	-------
			A dataframe with the searched tweets
	"""
	global location_data_frame
	global location_data
	data = []
	location_data = []
	location_data_frame = []
	# -- get tweets --
	if numTweet <= '100':
		# this let us to get more than 100 tweets
		tweets = api.user_timeline(screen_name=user, count=numTweet)
	else:
		tweets = tweepy.Cursor(api.user_timeline, screen_name=user,
							   count=200, tweet_mode='extended').items((int)(numTweet))
	# -- save tweets in lists --
	for tweet in tweets:
		if tweet.truncated:
			text = tweet.extended_tweet['full_text']
		else:
			text = tweet.text
		# I want to save location of tweet?
		if location and (tweet.coordinates is not None):
			lon = tweet.coordinates['coordinates'][0]
			lat = tweet.coordinates['coordinates'][1]
			location_data.append([tweet.user.screen_name, text, lon, lat])
		data.append((tweet.user.screen_name, text, (bool)(location), tweet.created_at))
	# -- create DataFrame --
	data_frame = pd.DataFrame(data, columns=['user', 'tweet', 'location', 'date'])
	location_data_frame = pd.DataFrame(location_data, columns=['user', 'tweet', 'lat', 'lon'])
	return data_frame
