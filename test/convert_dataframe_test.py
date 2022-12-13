import unittest
from src import getTweet
from src import twitter


class TestConversion(unittest.TestCase):
	dataframe = []

	def test_getTweet(self):
		print('Init api key...')
		twitter.__init__()
		self.dataframe = twitter.GetTweetByKeyword('#Days100Code', 20)
		print('Get tweet by keyword!')

	def test_convert_dataframe(self):
		print('Convert dataframe to db...')
		getTweet.convertDF2SQL(self.dataframe, 'database')
		print('...done!')