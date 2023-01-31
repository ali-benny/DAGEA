import unittest

from src import stream

class TestStream(unittest.TestCase):	
	def test_stream(self):	# test with 2 tweets
		stream.StreamByKeyword('karma', 2)
		result = stream.MyStream.tweets
		if (result['username'] == 'Hai cercato di avere lo stream di troppi tweet, riprova più tardi'):
			self.assertEqual(result['text'], '')
		else:
			self.assertEqual(len(stream.MyStream.tweets), 2)
	
	def test_get_key(self):
		self.assertEqual(stream.get_key('twitter','wrong_setting'), None)

if __name__ == '__main__':
	unittest.main()