import twitter
import sqlite3

def convertDF2SQL(function, maxTweet, findParam):
	"""
	The convertDF2SQL function takes in a function, maxTweet and findParam. 
	In base alla funzione che voglio usare per cercare tweet,
	ricavo il dataframe e lo salvo in un file database.db
	
	:param function: Specify which function to use
	:param maxTweet: Limit the number of tweets that will be downloaded
	:param findParam: param to search by de function
	:return: database.db file otherwise send Error if no correct parameter
	
	..notes: https://www.youtube.com/watch?v=hDNxHiybF8Q
	https://datatofish.com/pandas-dataframe-to-sql/
	"""
	if function == "GetTweetByUser":
		user = findParam
		df = twitter.GetTweetByUser(user, maxTweet)
	elif function == "GetTweetByKeyword":
		keyword = findParam
		df = twitter.GetTweetByKeyword(keyword, maxTweet)
	else: 
		df = ""
		return "ERROR: please insert correct parameter"
	
	# -- create db --
	connection = sqlite3.connect('database.db')
	c = connection.cursor()
		# - create table -
	c.execute('CREATE TABLE IF NOT EXISTS tweet (user, desc)')
	connection.commit()	# save my edits on connection
	
	# -- insert data on data_frame into db connection
	# df = df.to_html()
	df.to_sql('tweet', connection, if_exists='replace', index=False)

def __main__():
	twitter.__init__()
	convertDF2SQL('GetTweetByKeyword', 200, 'prova')

if __name__ == '__main__':
	__main__()