import unittest

from src import stream

class TestStream(unittest.TestCase):
	def test_stream_one_tweet(self):
		stream.StreamByKeyword('cactus', 1)
		self.assertEqual(len(stream.MyStream.tweets), 1)
	
	def test_stream_two_tweets(self):
		stream.StreamByKeyword('cactus', 2)
		self.assertEqual(len(stream.MyStream.tweets), 2)
	
	def test_stream_three_keyword(self):
		stream.StreamByKeyword(['cactus', 'twitter', 'the'], 1)
		self.assertEqual(len(stream.MyStream.tweets), 1)

if __name__ == '__main__':
	unittest.main()