import datetime
import sqlite3
import tweepy
import configparser
import os

global rule_id
rule_id = 0

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


class MyStream(tweepy.StreamingClient):
	tweets = ([])
	def main(self, limit):
		self.limit = limit
		if limit >= 50:
			self.limit = 50

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
		# self.connection = sqlite3.connect("database.db")	# -- connect to db --
		global rule_id
		rule_id = 0
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
		self.tweets.append({"username": username, "text": tweet.text, "createdAt": datetime.date.today()})
		all_tweets = self.tweets
		if len(self.tweets) == self.limit:		# have we find enough tweets?
			self.disconnect()	# -- yes: need to disconnect stream --
			self.tweets = ([])
			self.limit = 0
		return all_tweets
	
	def on_exception(self, exception):
		print("EXC: ",exception)
		return super().on_exception(exception)

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
	n_try = 0
	for n_try in range(2):
		try:
			n_try += 1
			global rule_id
			stream_tweet = MyStream(get_key('twitter','bearer_token'))
			stream_tweet.main(tweetsLimit)
			# rule_id += 1
			# stream_tweet.add_rules(tweepy.StreamRule(keywords, id=(str)(rule_id))) 	# add rules
			stream_tweet.add_rules(tweepy.StreamRule(keywords)) 	# add rules
			stream_tweet.filter(expansions=['author_id'])	# run the stream	
			# rules = stream_tweet.get_rules()
			# if rules != None and rule_id>=tweetsLimit:
			# 	stream_tweet.delete_rules(ids=[rule.id for rule in rules.data])	
			break
		except Exception as e:
			if e.status_code == 429:
				# Handle error: too many connections
				print("Stream encountered HTTP error: 429 Too Many Connections")
			else:
				# Handle other exceptions
				print("Stream encountered an error:", e)
			if n_try == 2:
				stream_tweet.tweets.append({'username':'Hai cercato di avere lo stream di troppi tweet, riprova più tardi', 'text': ''})