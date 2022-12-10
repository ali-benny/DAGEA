import sys
sys.path.append("..")
import src.TweetSearch as ts
#import src.config as config
import config

import unittest
import tweepy

class TestTweetSearch(unittest.TestCase):
    
    @classmethod
    #def setUpClass(cls, needTweets):
    def setUpClass(cls):
        print('setupClass')
        ts.APIv2.__init__()
        #if needTweets:
        #    cls.client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
        cls.client = tweepy.Client(bearer_token=config.BEARER_TOKEN)

    def test___init__(self):
        #self.setUpClass(False)
        self.setUpClass()
        self.assertEqual(type(self.client), type(ts.APIv2.client))
        self.assertEqual(ts.APIv2.response, self.client.get_user(id=0))
        self.assertEqual(ts.APIv2.query, '')
        self.assertTrue(10 <= ts.APIv2.tweetsLimit and ts.APIv2.tweetsLimit <= 100)
        self.assertEqual(ts.APIv2.start_time, None)
        self.assertEqual(ts.APIv2.end_time, None)
        self.assertEqual(ts.APIv2.expansions, ['author_id','geo.place_id'])
        self.assertEqual(ts.APIv2.tweet_fields, ['created_at'])

    def test_setDatas(self):
        #self.setUpClass(False)
        self.setUpClass()
        ts.APIv2.setDatas(query=None, tweetsLimit = None, start_time=None, end_time=None)
        self.assertEqual(ts.APIv2.query, '')
        self.assertTrue(10 <= ts.APIv2.tweetsLimit and ts.APIv2.tweetsLimit <= 100)
        self.assertEqual(ts.APIv2.start_time, None)
        self.assertEqual(ts.APIv2.end_time, None)

        ts.APIv2.setDatas(query='str', tweetsLimit = 50, start_time='2022-01-01T01:01', end_time='2022-02-02T02:02')
        self.assertEqual(ts.APIv2.query, 'str')
        self.assertEqual(ts.APIv2.tweetsLimit, 50)
        self.assertEqual(ts.APIv2.start_time, '2022-01-01T01:01:00Z')
        self.assertEqual(ts.APIv2.end_time, '2022-02-02T02:02:00Z')

        ts.APIv2.setDatas(tweetsLimit = 120, start_time='2022-01-01T01:01', end_time='2022-02-02T02:02')
        self.assertTrue(10 <= ts.APIv2.tweetsLimit and ts.APIv2.tweetsLimit <= 100)     # Se si inserisce un valore non consentito tweetLimit non vario o ha il suo valore di inizializzaione


if __name__ == '__main__':
    unittest.main()