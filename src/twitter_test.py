import unittest
import pandas as pd
import configparser
from twitter import get_key #, __init__

class TestGetKey(unittest.TestCase):

    def test_get_key(self):
        # da sostituire con i propri 'section' e 'setting' in tutti i campi dove c'è get_key
        api_key = get_key('twitter', 'api_key')
        self.assertEqual(api_key, 'api_key value') # inserire nel secondo campo la propria api key

        api_key_secret = get_key('twitter', 'api_key_secret')
        self.assertEqual(api_key_secret, 'api_key_secret value') # inserire nel secondo campo la propria api key secret

        access_token = get_key('twitter', 'access_token')
        self.assertEqual(access_token, 'access_token value') # inserire nel secondo campo il proprio access token

        access_token_secret = get_key('twitter', 'access_token_secret')
        self.assertEqual(access_token_secret, 'access_token_secret value') # inserire nel secondo campo il proprio access token secret

        # self.assertRaises(configparser.NoOptionError)

"""
class TestGetTweet(unittest.TestCase):

    def test_byKeyword(self):
        pass

    def test_byUser(self):
        pass
"""

if __name__ == '__main__':
    unittest.main()