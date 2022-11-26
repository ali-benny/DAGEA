import sqlite3
import os
# from src import app
import twitter

def GetTweet(function, maxTweet, searchVar, isLocated=False):
	"""
	The GetTweet function is used to retrieve tweets from the Twitter API. 
	The function takes two parameters: a string representing the type of tweet (user or keyword), and a string representing the variable to search for that type of tweet (the user name or keyword). The function returns a dataframe containing all retrieved tweets.
	
	:param function: Determine which function to call
	:param maxTweet: Determine the maximum number of tweets that will be returned
	:param searchVar: Find the correct tweet
	:return: The dataframe of the tweets that were retrieved
	"""
	if function == "user":
		user = searchVar
		if isLocated:
			df = twitter.GetTweetByUser(user, maxTweet, location=True)
			convertDF2SQL(twitter.location_data_frame, 'location')	
		else:
			df = twitter.GetTweetByUser(user, maxTweet)
	elif function == "keyword":
		keyword = searchVar
		if isLocated:
			df = twitter.GetTweetByKeyword(keyword, maxTweet, location=True)
			convertDF2SQL(twitter.location_data_frame, 'location')	
		else:
			df = twitter.GetTweetByKeyword(keyword, maxTweet)
	else: 
		df = ""
		return "ERROR: please insert correct parameter"	# non deve accadere mai
	convertDF2SQL(df, 'database')

def convertDF2SQL(dataframe, fileName, location=False):
	"""
	The convertDF2SQL function takes a pandas dataframe and converts it to a SQL database.
	The function also saves the dataframe as a JSON file.
	
	:param dataframe: Insert the dataframe into the database
	:return: The connection to the database
	"""
	file = fileName + '.db'
	# -- create db --
	connection = sqlite3.connect(file)
	c = connection.cursor()
		# - create table -
	if location:
		c.execute("CREATE TABLE IF NOT EXISTS tweet (user TEXT, desc TEXT, location BOOLEAN)")
	else:
		c.execute('CREATE TABLE IF NOT EXISTS tweet (user TEXT, desc TEXT)')
	connection.commit()	# save my edits on connection
	
	# -- insert data_frame into db connection
	dataframe.to_sql('tweet', connection, if_exists='replace', index=False)
	file = fileName + '.json'
	dataframe.to_json(os.path.abspath(file))