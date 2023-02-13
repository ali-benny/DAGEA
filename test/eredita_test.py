import unittest
import configparser
import os
from src import eredita
from src.pythonModules.twitter.TweetSearch import TweetSearch

def init():		
	config = configparser.ConfigParser()
	my_path = os.path.abspath('config.ini')
	config.read(my_path)
	TweetSearch.__init__(BEARER_TOKEN=config.get('twitter','bearer_token'))

class TestEredita(unittest.TestCase):
	#* test ghigliottina *#
	def test_ghigliottina(self):
		init()
		result = eredita.ghigliottina()
		self.assertIsNotNone(result)
		self.assertTrue(len(result['data']) > 0)
		self.assertTrue(len(result['indovina']) > 0)
		self.assertTrue(len(result['vincente']) > 0)

	#* test get_data *#
	def test_valid_date_string(self):
		# Test valid date string with correct format
		date_string = "01 January 2021"
		expected_output = "2021-01-01"
		self.assertEqual(eredita.get_data(date_string), expected_output)
	
	def test_valid_date_string_with_different_format(self):
		# Test valid date string with different format
		date_string = "2022-03-20"
		expected_output = "2022-03-20"
		self.assertEqual(eredita.get_data(date_string), expected_output)

	#* test ereditiers *#
	def test_ereditiers(self):		#! il risultato cambia sempre di giornata in giornata, quindi non posso fare un test preciso
		init()
		result = eredita.ereditiers('ghigliottina')
		self.assertIsNotNone(result)
		self.assertTrue(len(result) > 0)
	
	def test_total(self):
		self.assertIsNotNone(eredita.total())
		
	#* test easyocr *#
	def test_convert_image(self):
		img = 'https://pbs.twimg.com/media/FnLc_OSWAB4mBmR?format=jpg&name=900x900'
		result = eredita.convert_img2text(img)
		my_result = ['LEREDITA', '23 gennaio 2023', '#ghigliottina', 'FARE', 'BABY', 'ELETTRICO', 'PASSEGGERO', 'COSTUME', 'FENOMENO']
		self.assertEqual(result, my_result)
	
if __name__ == '__main__':
	unittest.main()
