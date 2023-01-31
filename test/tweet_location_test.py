import unittest
# from src import twitter
from flask import request

class TestTweetLocation(unittest.TestCase):
	search_word = 'world'

	def test_get_tweet_location(self):
		print('Getting tweet location...')
		# Arrange
		print(self.search_word+' is the search word')
		# Act
		by_keyword = twitter.GetTweetLocation('keyword', 2, self.search_word)
		print()
		
		by_user = twitter.GetTweetLocation('user', 2, self.search_word)
		# Assert
		for i in range(0, 2):
			self.assertIn(self.search_word, by_keyword[i][i])

if __name__ == '__main__':
	unittest.main()