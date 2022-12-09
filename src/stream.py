import datetime
import sqlite3
import tweepy
import pandas as pd
import configparser
import os

def get_key(section, setting):
	"""
	The get_key function is a helper function that retrieves the value of a setting from the configuration file.

	:param section: Specify the section of the config file to read
	:param setting: Specify the setting that is being retrieved
	:return: The value of the setting in the specified section
	"""
	
	config = configparser.ConfigParser()
	my_path = os.path.abspath('config.ini')
	config.read(my_path)
	try:
		key = config.get(section, setting)
	except configparser.NoOptionError:
		key = None
	return key


def convertDF2SQL(dataframe, stream=False):
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
	# -- connect to db --
	connection = sqlite3.connect("database.db")
	c = connection.cursor()
	# - create table -
	c.execute(
		'CREATE TABLE IF NOT EXISTS all_tweets (user TEXT, text TEXT, date DATETIME)')
	connection.commit()  # save my edits on connection
	if stream:
		dataframe.to_sql('all_tweets', connection, if_exists='append', index=False)
	else:
		dataframe.to_sql('all_tweets', connection, if_exists='replace', index=False)
	# save dataframe as json
	dataframe.to_json("all_tweets.json")

class MyStream(tweepy.StreamingClient):
	tweets = ([])
	limit = 0

	def main(self, limit=1):
		self.limit = limit

	def on_connect(self):
		"""
		The on_connect function is called when the bot connects to Twitter. It sets up a tweepy client, 
		connects to the database, and prints a message indicating that it has connected.
		
		Parameters
		----------
			self
				Reference the class instance
		
		Returns
		-------
			A connection to the twitter api
		"""
		self.client = tweepy.Client(get_key('twitter','bearer_token'))	# -- connect to twitter API --		
		self.connection = sqlite3.connect("database.db")	# -- connect to db --
		print('Connected!')

	def on_response(self, response):
		"""
		The on_response function is called when a response is received from the stream.
		It takes the response as an argument and adds it to our list of tweets.
		
		Parameters
		----------
			self
				Access the attributes and methods of the class in python
			response
				Get the data of the tweet
		
		Returns
		-------	
			The tweets lists
		"""
		tweet = response.data
		username = response.includes['users'][0].username
		self.tweets.append({"user": username, "text": tweet.text, "date": datetime.date.today()})
		# we have find some tweets?
		if len(self.tweets) >= self.limit:
			self.disconnect()
		return self.tweets


def StreamByKeyword(keywords, tweetsLimit):
	"""
	The StreamByKeyword function takes a list of keywords and returns the tweets that contain those keywords.
	
	Parameters
	----------
		keywords
			Specify the keywords that you want to filter for
		tweetsLimit
			Limit the number of tweets that are streamed
	
	Returns
	-------	
		A list of tweets
	"""
	stream_tweet = MyStream(get_key('twitter','bearer_token'))
	stream_tweet.main(tweetsLimit)
	# for keyword in keywords:
	# 	stream_tweet.add_rules(tweepy.StreamRule(keyword)) 	# add rules
	stream_tweet.add_rules(tweepy.StreamRule(keywords)) 	# add rules
	stream_tweet.filter(expansions=['author_id','attachments.media_keys'])	# run the stream
