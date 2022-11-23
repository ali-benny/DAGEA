import unittest
import pandas as pd
import configparser
from tweepy import api, OAuthHandler
from twitter import get_key, __init__

class TestGetKey(unittest.TestCase):

    def setUp(self):
        # da sostituire con i propri 'section' e 'setting' in tutti i campi dove c'è get_key
        self.api_key = get_key('twitter', 'api_key')
        self.api_key_secret = get_key('twitter', 'api_key_secret')
        self.access_token = get_key('twitter', 'access_token')
        self.access_token_secret = get_key('twitter', 'access_token_secret')
       
    def test_get_key(self):
        self.assertEqual(self.api_key, 'api_key value') # inserire nel secondo campo la propria api key
        self.assertEqual(self.api_key_secret, 'api_key_secret value') # inserire nel secondo campo la propria api key secret
        self.assertEqual(self.access_token, 'access_token value') # inserire nel secondo campo il proprio access token
        self.assertEqual(self.access_token_secret, 'access_token_secret value') # inserire nel secondo campo il proprio access token secret

        # self.assertRaises(configparser.NoOptionError, get_key, 'twitter', None)
    
    def test__init__(self):
        if not self.api_key or not self.api_key_secret:
            self.fail("Wrong api key and/or secret")

"""
class TestGetTweet(unittest.TestCase):

    def test_byKeyword(self):
        pass

    def test_byUser(self):
        pass
"""

if __name__ == '__main__':
    unittest.main()