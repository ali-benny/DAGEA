import twitter

def GetTweet(function, maxTweet, searchVar, isLocated):
	"""
	The GetTweet function is used to get tweets from the Twitter API.
	It takes as input a function, maxTweet and searchVar. 
	
	Parameters
	----------
		function = "researchByUser" or "researchByKeyword"
			Select the type of research, and to specify if the user wants to get also location data
		maxTweet
			Specify the number of tweets to be retrieved
		searchVar
			Specify the search term
		isLocated = True or False
			Determine if the dataframe should be filtered by location or not
	
	Returns
	-------
		Error if function not found or not match
	"""
	if function == "researchByUser":
		user = searchVar
		df = twitter.GetTweetByUser(user, maxTweet, isLocated)
	elif function == "researchByKeyword":
		keyword = searchVar
		df = twitter.GetTweetByKeyword(keyword, maxTweet, isLocated)
	else: 
		df = ""
		return "ERROR: please insert correct parameter"	# non deve accadere mai
	twitter.convertDF2SQL(df, isLocated)
