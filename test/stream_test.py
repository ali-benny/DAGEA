import unittest
from src import stream

class TestStream(unittest.TestCase):
	def test_stream_one_tweet(self):
		print('test_stream_one_tweet...')
		stream.StreamByKeyword('test', 1)
		if self.assertEqual(len(stream.MyStream.tweets), 1):
			print('test_stream_one_tweet: OK')
	
	def test_stream_two_tweets(self):
		print('test_stream_two_tweets...')
		stream.StreamByKeyword('test', 2)
		if self.assertEqual(len(stream.MyStream.tweets), 2):
			print('test_stream_two_tweets: OK')
	
	def test_stream_three_keyword(self):
		print('test_stream_three_keyword...')
		stream.StreamByKeyword(['test', 'twitter', 'the'], 1)
		if self.assertEqual(len(stream.MyStream.tweets), 1):
			print('test_stream_three_keyword: OK')