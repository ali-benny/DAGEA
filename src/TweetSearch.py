import os
from os import listdir
import sys
sys.path.append("..")
import src.utils as utils
import configparser # EDIT: era import config
import sqlite3
try:
    import tweepy                  # Used for APIs
    import pandas as pd         # Used for data handling and debug
    import configparser         # Used for APIv1 initialization
    import csv                        # Used for APIv2
    import json                      # Used for APIv2
    import js2py
except ModuleNotFoundError:
    os.system('pip install tweepy')
    os.system('pip install pandas')
    os.system('pip install configparser')
    os.system('pip install csv')
    os.system('pip install json')
    os.system('pip install js2py')

global config
config = configparser.ConfigParser()
config.read(os.path.abspath('config.ini'))

class APIv1:
    ################################ API SETUP ################################
    section = 'twitter'		#! change it as your [param] on config.ini file 
    APILabel = 'APILabel'

    @classmethod
    def __init__(cls) -> None:
        global config
        api_key = config[cls.section]['api_key']
        api_key_secret = config[cls.section]['api_key_secret']
        access_token = config[cls.section]['access_token']
        access_token_secret = config[cls.section]['access_token_secret']

        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        cls.api = tweepy.API(auth)

    @classmethod
    def setSection(cls, section) -> None:
        cls.section = section

    @classmethod
    def setAPILabel(cls, APILabel) -> None:
        cls.APILabel = APILabel
    
    ################################  RESEARCH  ################################
    @classmethod
    def getGeoDatas(cls, tweet_id, client):
        tweetInfo = client.get_tweet(tweet_id, expansions=['geo.place_id'])
        geoDatas = {"latitude": 0.0, "longitude": 0.0, "taggedPlace": ''}
        try:
            place_id = tweetInfo.data.geo['place_id']
            placeObj = cls.api.geo_id(place_id)
            geoDatas.update({"latitude": placeObj.centroid[1]})
            geoDatas.update({"longitude": placeObj.centroid[0]})
            geoDatas.update({"taggedPlace": placeObj.full_name})
            return geoDatas
            #print(f"tweetInfo (response):{tweetInfo}")
            #print(f"tweeet_id: {tweet_id}, place_id: {place_id}, api.geo_id(place_id).centroid: {placeObj.centroid}")
        except TypeError:       # Caso in cui nel tweet non e' stato taggato alcun luogo
            #print(f"tweeet_id: {tweet_id}, api.geo_id(place_id).centroid: NO GEO ATTRIBUTE --> NO COORDINATES")
            return geoDatas
        
class APIv2:
    ################################ API SETUP ################################
    @classmethod
    def __init__(cls) -> None:
        global config
        # cls.client = tweepy.Client(bearer_token=config.BEARER_TOKEN)  #! EDIT: questo metodo non è corretto
        cls.client = tweepy.Client(bearer_token=config['twitter']['bearer_token'])
        cls.__init__response()
        cls.query = ''
        cls.username = ''
        cls.tweetsLimit = 10
        cls.start_time = None
        cls.end_time = None
        cls.expansions = ['author_id','geo.place_id']
        cls.tweet_fields = ['created_at']

    @classmethod
    def __init__response(cls) -> None:
        # cls.response = cls.client.get_user(id=0)    # Questa chiamata di get_user ritornera' un dato response vuoto (analogo ad una string avuota '')
        cls.response = ''

    ################################  ATTRIBUTE SETTING   ################################
    @classmethod
    # TODO: Credo proprio che esistano strumenti migliori per implementare la semantica di questa funzione
    def setDatas(cls, query: str = None, tweetsLimit = None, start_time=None, end_time=None, expansions=None, tweet_fields=None) -> None:
        if query is not None:
            cls.query = query
        if tweetsLimit is not None and 10 <= int(tweetsLimit) and int(tweetsLimit) <= 100:
            cls.tweetsLimit = tweetsLimit
        if start_time is not None:
            # I parametri attuali {start|end}_time sono ritornati da HTML nella forma: YYYY-MM-DDTHH:DD e vanno
            # dunque fatte delle modifiche per adattarle al formato dell'API v2, ovvero:YYYY-MM-DDTHH:DD:SS:Z
            cls.start_time = start_time + ':00Z'
        else:
            cls.start_time = None
        if end_time is not None:
            cls.end_time = end_time + ':00Z'
        else:
            cls.end_time = None
        if expansions is not None and type(expansions) == type([]):
            cls.expansions = expansions
        else:
            cls.expansions = ['author_id','geo.place_id']
        if tweet_fields is not None and type(tweet_fields) == type([]):
            cls.tweet_fields = tweet_fields
        else:
            cls.tweet_fields = ['created_at']

    ################################  RESEARCH  ################################
    @classmethod
    def researchDecree(cls, researchType: str) -> None:
        cls.start_time = utils.updateTime(cls.start_time)
        match researchType:
            case 'researchByUser':
                userData = cls.client.get_user(username=cls.query).data
                if (userData is not None):      # Entra nell'if sse trova almeno un utente con quell'username
                    userId = userData.id
                    cls.response = cls.client.get_users_tweets(id=userId, max_results=cls.tweetsLimit, expansions=cls.expansions, tweet_fields=cls.tweet_fields, start_time=cls.start_time, end_time=cls.end_time)
            case 'researchByKeyword':
                cls.response = cls.client.search_recent_tweets(query=cls.query, max_results=cls.tweetsLimit, expansions=cls.expansions, tweet_fields=cls.tweet_fields, start_time=cls.start_time, end_time=cls.end_time)
            case 'researchByHashtag':
                cls.response = cls.client.search_recent_tweets(query='#'+cls.query, max_results=cls.tweetsLimit, expansions=cls.expansions, tweet_fields=cls.tweet_fields, start_time=cls.start_time, end_time=cls.end_time)
            case _:
                raise ValueError("ERROR: APIv2 Class, researchDecree: match error")

    ################################  OTHER  ################################
    @classmethod
    def createCard(cls) -> list:
        if cls.response.data is not None:
            card=[]
            APIv1.__init__()
            for tweet in cls.response.data:
                # tmp = cls.client.get_user(id=tweet.author_id).data
                # username = tmp if tmp is not None else 'Unknown'
                username = cls.response.includes['users'][0].username
                text = tweet.text
                createdAt = str(tweet.created_at)[0:16]     # Si taglia la parte della stringa contenente dai secondi in poi
                geoDatas = APIv1.getGeoDatas(tweet_id=tweet.id, client=cls.client)
                card.append({"username": str(username), "text": text, "createdAt": createdAt, "latitude": geoDatas.get('latitude'), "longitude": geoDatas.get('longitude'), "taggedPlace": geoDatas.get('taggedPlace')})   # NOTE: a noi non serve vedere le coordinate sulla card del tweet
            return card
        else:
            return ''

    @classmethod
    def hasCardsGeo(cls, cards: list) -> bool:
        for card in cards:
            if card['latitude'] != 0.0 or card['longitude'] != 0.0:
                return True
        return False

    ################################  DEBUG  ################################
    @classmethod
    def _createDataFrames(cls) -> None:
        cls.dataFrames = []
        cls.dataFrames.append(pd.DataFrame(cls.response))
        cls.dataFrames.append(pd.DataFrame(cls.response.data))
        try:
            cls.dataFrames.append(pd.DataFrame(cls.response.includes))
        except ValueError:      # Caso in cui i campi di response,includedes hanno lunghezze diverse (a causa della presenza di piu' valori nel campo extensions)
            pass
        cls.dataFrames.append(pd.DataFrame(cls.response.errors))
    
    @classmethod
    def _createCsvFiles(cls) -> None:
        cls._deleteCsvFiles()             # Si eliminano i .csv di ricerche passate
        cls._createDataFrames()     # E si creano quelli coi nuovi dati
        try:
            cls.dataFrames[0].to_csv('response.csv')
            cls.dataFrames[1].to_csv('responseData.csv')
            try:
                cls.dataFrames[2].to_csv('responseIncludes.csv')
                cls.dataFrames[3].to_csv('responseErrors.csv')
            except IndexError:
                cls.dataFrames[2].to_csv('responseErrors.csv')
        except AttributeError:      # Caso in cui dataFrames[i] sia vuoto (non si sono chiamati i metodi del'API)
            print("ATTENTION: currently there is no 'cls.dataFrames[i]' attribute in the APIv2 class.\nPossible causes:\n1) You haven't called any APIv2 method of the class yet --> Call one\n2) The call returned no results --> Try modifying the query")

    @classmethod
    def _deleteCsvFiles(cls)-> None:
        myPath = os.path.dirname(os.path.abspath(__file__)) + '/'
        for file in listdir(myPath):
            if file.endswith('.csv'):
                os.remove(myPath + file)
