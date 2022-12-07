import sqlite3
import tweepy
import pandas as pd
import configparser
import os
import time

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
	limit = 16
	users = []

	def on_connect(self):
		self.client = tweepy.Client(get_key('twitter','bearer_token'))	# -- connect to twitter API --		
		self.connection = sqlite3.connect("database.db")	# -- connect to db --
		print('Connected!')

	def on_response(self, response):
		print('✨')
		tweet = response.data
		self.tweets.append(tweet)
		tmp = self.client.get_user(id=tweet.author_id).data
		username = tmp if tmp is not None else 'Unknown'
		# save tweets in a db table
		c = self.connection.cursor()
		# c.execute("CREATE TABLE IF NOT EXISTS all_tweets (user TEXT, text TEXT, date DATETIME)")
		c.execute(
		"INSERT INTO all_tweets (user, text, date) VALUES (?, ?, ?)",(username, tweet.text, tweet.created_at))
		self.connection.commit()  # save my edits on connection
		# we have more than 100 tweets?
		if len(self.tweets) == self.limit:
			self.disconnect()
		time.sleep(1)
	
	# def on_tweet(self, tweet):
		# if tweet.refecenced_tweets == None:
		# # if not tweet.truncated:
		# self.tweets.append([tweet.user.screen_name, tweet.text, tweet.created_at])
		# # else:
		# # 	self.tweets.append([tweet.user.screen_name, tweet.extended_tweet['full_text'], tweet.created_at])
		# convertDF2SQL(self.dataframe, stream=True)


def StreamByKeyword(keywords):
	stream_tweet = MyStream(get_key('twitter','bearer_token'))
	# for keyword in keywords:
	# 	stream_tweet.add_rules(tweepy.StreamRule(keyword)) 	# add rules
	stream_tweet.add_rules(tweepy.StreamRule(keywords)) 	# add rules
	stream_tweet.filter(expansions='author_id')	# run the stream