import sys
sys.path.append("..")
import src.TweetSearch as ts
import src.utils as utils
import configparser

import unittest
import tweepy
import datetime
from datetime import timedelta, datetime

class TestTweetSearch(unittest.TestCase):
    
    @classmethod
    #def setUpClass(cls, needTweets):
    def setUpClass(cls):
        print('setupClass')
        ts.APIv2.__init__()
        #if needTweets:
        #    cls.client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
        cls.client = tweepy.Client(bearer_token=config.BEARER_TOKEN)

        datesAPIFormat = utils.initializeDates('APIFormat')
        datesHTMLFormat = utils.initializeDates('HTMLFormat')
        cls.commonParameters = {
            'query' : '#IngSw2022',
            'username' : '_Bastia__',
            'tweetsLimit' : 10,
            'start_time' : {'HTMLFormat': datesHTMLFormat['minDate'], 'APIFormat': datesAPIFormat['start_time']},
            'end_time' : {'HTMLFormat': datesHTMLFormat['maxDate'], 'APIFormat': datesAPIFormat['end_time']},
            'expansions' : ['author_id','geo.place_id'],
            'tweet_fields' : ['created_at']
        }

    def test___init__(self):
        #self.setUpClass(True)
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

        # Test dei casi in cui i parametri attuali == None
        ts.APIv2.setDatas(query=None, tweetsLimit = None, start_time=None, end_time=None, expansions=None, tweet_fields=None)
        self.assertEqual(ts.APIv2.query, '')
        self.assertTrue(10 <= ts.APIv2.tweetsLimit and ts.APIv2.tweetsLimit <= 100)
        self.assertEqual(ts.APIv2.start_time, None)
        self.assertEqual(ts.APIv2.end_time, None)
        self.assertEqual(ts.APIv2.expansions, ['author_id','geo.place_id'])
        self.assertEqual(ts.APIv2.tweet_fields, ['created_at'])

        # Test dei casi in cui i parametri hanno valori corretti (ovvero in forma che non creera' problemi alle API call)
        ts.APIv2.setDatas(query='#IngSw2022', tweetsLimit = 50, start_time='2022-01-01T01:01', end_time='2022-02-02T02:02',
            expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        self.assertEqual(ts.APIv2.query, '#IngSw2022')
        self.assertEqual(ts.APIv2.tweetsLimit, 50)
        self.assertEqual(ts.APIv2.start_time, '2022-01-01T01:01:00Z')
        self.assertEqual(ts.APIv2.end_time, '2022-02-02T02:02:00Z')

        # Test dei casi in cui i parametri hanno valori scorretti
        ts.APIv2.setDatas(tweetsLimit = 120)
        self.assertTrue(10 <= ts.APIv2.tweetsLimit and ts.APIv2.tweetsLimit <= 100)     # Se si inserisce un valore non consentito tweetLimit non vario o ha il suo valore di inizializzaione

    def test_reserachDecree(self):
        # Caso researchByUser
        self.setUpClass()        
        # Se si cerca un utente che non esiste il response non varia
        tmpResponse = ts.APIv2.response
        ts.APIv2.setDatas(query='UsernameInesist')
        ts.APIv2.researchDecree('researchByUser')
        self.assertEqual(ts.APIv2.response, tmpResponse)

        self.setUpClass()
        #ts.APIv2.setDatas(query=self.commonParameters['username'], tweetsLimit=self.commonParameters['tweetsLimit'], start_time=self.commonParameters['start_time']['HTMLFormat'], end_time=self.commonParameters['end_time']['HTMLFormat'], expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        ts.APIv2.setDatas(query=self.commonParameters['username'], tweetsLimit=self.commonParameters['tweetsLimit'], start_time=None, end_time=None, expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        # Se si cerca un utente valido senza filtri temporali
        ts.APIv2.researchDecree('researchByUser')
        userId = self.client.get_user(username=self.commonParameters['username']).data.id
        tmpResponse = self.client.get_users_tweets(id=userId, max_results=self.commonParameters['tweetsLimit'], start_time=None, end_time=None, expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        self.assertEqual(ts.APIv2.response, tmpResponse)

        # Se si cerca un utente valido con filtri temporali
        self.setUpClass()
        ts.APIv2.setDatas(query=self.commonParameters['username'], tweetsLimit=self.commonParameters['tweetsLimit'], start_time=self.commonParameters['start_time']['HTMLFormat'], end_time=self.commonParameters['end_time']['HTMLFormat'], expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        # Se si cerca un utente valido
        ts.APIv2.researchDecree('researchByUser')
        userId = self.client.get_user(username=self.commonParameters['username']).data.id
        tmpResponse = self.client.get_users_tweets(id=userId, max_results=self.commonParameters['tweetsLimit'], start_time=self.commonParameters['start_time']['APIFormat'], end_time=self.commonParameters['end_time']['APIFormat'], expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        self.assertEqual(ts.APIv2.response, tmpResponse)

        # Caso researchByKeyword
        self.setUpClass()
        self.commonParameters['start_time']['APIFormat'] = utils.updateTime(self.commonParameters['start_time']['APIFormat'])
        ts.APIv2.setDatas(query=self.commonParameters['query'], tweetsLimit=self.commonParameters['tweetsLimit'], start_time=self.commonParameters['start_time']['HTMLFormat'], end_time=self.commonParameters['end_time']['HTMLFormat'], expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'])
        ts.APIv2.researchDecree('researchByKeyword')
        tmpResponse = self.client.search_recent_tweets(query=self.commonParameters['query'], max_results=self.commonParameters['tweetsLimit'], expansions=self.commonParameters['expansions'], tweet_fields=self.commonParameters['tweet_fields'], start_time=self.commonParameters['start_time']['APIFormat'], end_time=self.commonParameters['end_time']['APIFormat'])
        self.assertEqual(ts.APIv2.response, tmpResponse)
        # Caso researchByHashtag
        ts.APIv2.setDatas(query=self.commonParameters['query'][1:len(self.commonParameters['query'])])
        ts.APIv2.researchDecree('researchByHashtag')
        self.assertEqual(ts.APIv2.response, tmpResponse)
        # Caso _
        with self.assertRaises(ValueError) as exc:
            ts.APIv2.researchDecree('')
        self.assertEquals(str(exc.exception), "ERROR: APIv2 Class, researchDecree: match error")

if __name__ == '__main__':
    unittest.main()