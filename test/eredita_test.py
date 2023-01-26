from src import eredita
import unittest

class TestEredita(unittest.TestCase):
	def test_convert_image(self):
		img = 'https://pbs.twimg.com/media/FnLc_OSWAB4mBmR?format=jpg&name=900x900'
		result = eredita.convert_img2text(img)
		my_result = ['LEREDITA', '23 gennaio 2023', '#ghigliottina', 'FARE', 'BABY', 'ELETTRICO', 'PASSEGGERO', 'COSTUME', 'FENOMENO']
		self.assertEqual(result, my_result)
	
	def test_get_img_from_tweet(self):
		# controllare seritorna un URL