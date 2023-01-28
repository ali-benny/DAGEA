from src import eredita
import unittest
import easyocr

class TestEredita(unittest.TestCase):
	#* test easyocr *#
	def test_convert_image(self):
		img = 'https://pbs.twimg.com/media/FnLc_OSWAB4mBmR?format=jpg&name=900x900'
		result = eredita.convert_img2text(img)
		my_result = ['LEREDITA', '23 gennaio 2023', '#ghigliottina', 'FARE', 'BABY', 'ELETTRICO', 'PASSEGGERO', 'COSTUME', 'FENOMENO']
		self.assertEqual(result, my_result)
	
	def test_valid_input(self):
		# Test valid input: image file
		img = 'path/to/image.jpg'
		result = eredita.convert_img2text(img)
		self.assertIsInstance(result, list)
		self.assertGreater(len(result), 0)

	def test_valid_input_url(self):
		# Test valid input: image URL
		img_url = 'https://example.com/image.jpg'
		result = eredita.convert_img2text(img_url)
		self.assertIsInstance(result, list)
		self.assertGreater(len(result), 0)

	def test_invalid_input(self):
		# Test invalid input: not an image file or URL
		img = 'path/to/textfile.txt'
		with self.assertRaises(easyocr.Error):
			eredita.convert_img2text(img)
	
	def test_empty_input(self):
		# Test empty input: None
		img = None
		with self.assertRaises(easyocr.Error):
			eredita.convert_img2text(img)

if __name__ == '__main__':
	unittest.main()
