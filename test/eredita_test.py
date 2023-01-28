import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'src/pythonModules')))
from src import eredita
class TestEredita(unittest.TestCase):
	#* test ghigliottina *#
	def test_ghigliottina(self):
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
		result = eredita.ereditiers('il')
		self.assertIsNotNone(result)
		self.assertTrue(len(result) > 0)
	
	#* test prendere le immagini con le soluzioni dai tweet *#
	def test_get_tweet_soluzioni(self):
		expected = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
		result = eredita.get_tweet_soluzioni()
		self.assertEqual(result, expected)

	#* test easyocr *#
	def test_convert_image(self):
		img = 'https://pbs.twimg.com/media/FnLc_OSWAB4mBmR?format=jpg&name=900x900'
		result = eredita.convert_img2text(img)
		my_result = ['LEREDITA', '23 gennaio 2023', '#ghigliottina', 'FARE', 'BABY', 'ELETTRICO', 'PASSEGGERO', 'COSTUME', 'FENOMENO']
		self.assertEqual(result, my_result)
	
	def test_valid_input(self):
		# Test valid input: image file
		img = 'src/img/leredita.jpg'
		result = eredita.convert_img2text(img)
		self.assertIsInstance(result, list)
		self.assertGreater(len(result), 0)

	def test_invalid_input(self):
		# Test invalid input: not an image file or URL
		img = 'path/to/textfile.txt'
		with self.assertRaises(EasyOCRError):	# easyocr.Error code 3: "Image file not found"
			eredita.convert_img2text(img)
	
	def test_empty_input(self):
		# Test empty input: None
		img = None
		with self.assertRaises(EasyOCRError): 	# easyocr.Error code 3: "Image file not found"
			eredita.convert_img2text(img)

if __name__ == '__main__':
	unittest.main()
