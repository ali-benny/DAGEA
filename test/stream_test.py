import unittest

from src import stream

class TestStream(unittest.TestCase):
	def test_stream_1(self):	# test with 1 tweet
		stream.StreamByKeyword('hello', 1)
		self.assertEqual(len(stream.MyStream.tweets), 1)
	
	def test_stream_2(self):	# test with 2 tweets
		stream.StreamByKeyword('hola', 2)
		self.assertEqual(len(stream.MyStream.tweets), 2)
	
	def test_stream_3(self):	# test with 3 words
		stream.StreamByKeyword('my twitter test', 1)
		self.assertEqual(len(stream.MyStream.tweets), 1)
	
	def test_get_key(self):
		self.assertEqual(stream.get_key('twitter','wrong_setting'), None)

if __name__ == '__main__':
	unittest.main()