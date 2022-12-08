import os
from os import listdir
import config
try:
    import tweepy                  # Used for APIs
    import pandas as pd         # Used for data handling and debug
    import configparser         # Used for APIv1 initialization
    import csv                        # Used for APIv2
    import json                      # Used for APIv2
    import datetime
    from datetime import timedelta, datetime
    import js2py
except ModuleNotFoundError:
    os.system('pip install tweepy')
    os.system('pip install pandas')
    os.system('pip install configparser')
    os.system('pip install csv')
    os.system('pip install json')
    os.system('pip install js2py')

class APIv1:
    ################################ API SETUP ################################
    section = 'twitter'		#! change it as your [param] on config.ini file 
    APILabel = 'APILabel'

    @classmethod
    def __init__(cls) -> None:
        config = configparser.ConfigParser()
        config.read(os.path.abspath('config.ini'))
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
    def getCoordinates(cls, tweet_id, client):
        tweetInfo = client.get_tweet(tweet_id, expansions=['geo.place_id'])
        try:
            place_id = tweetInfo.data.geo['place_id']
            placeObj = cls.api.geo_id(place_id)
            return placeObj.centroid
            #print(f"tweetInfo (response):{tweetInfo}")
            #print(f"tweeet_id: {tweet_id}, place_id: {place_id}, api.geo_id(place_id).centroid: {placeObj.centroid}")
        except TypeError:       # Caso in cui nel tweet non e' stato taggato alcun luogo
            #print(f"tweeet_id: {tweet_id}, api.geo_id(place_id).centroid: NO GEO ATTRIBUTE --> NO COORDINATES")
            return [0.0,0.0]
        
class APIv2:
    ################################ API SETUP ################################
    @classmethod
    def __init__(cls) -> None:
        cls.client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
        cls.__init__response()
        cls.query = ''
        cls.tweetsLimit = 10
        cls.start_time = None
        cls.end_time = None
        cls.expansions = ['author_id','geo.place_id']
        cls.tweet_fields=['created_at']

    @classmethod
    def __init__response(cls) -> None:
        cls.response = cls.client.get_user(id=0)    # Questa chiamata di get_user ritornera' un dato response vuoto (analogo ad una string avuota '')

    ################################  ATTRIBUTE SETTING   ################################
    @classmethod
    # TODO: Credo proprio che esistano strumenti migliori per implementare la semantica di questa funzione
    def setDatas(cls, query: str = None, tweetsLimit = None, start_time=None, end_time=None) -> None:
        if query is not None:
            cls.query = query
        if tweetsLimit is not None and 10 <= int(tweetsLimit) and int(tweetsLimit) <= 100:
            cls.tweetsLimit = tweetsLimit
        # I parametri attuali {start|end}_time sono ritornati da HTML nella forma: YYYY-MM-DDTHH:DD e vanno
        # dunque fatte delle modifiche per adattarle al formato dell'API v2, ovvero:YYYY-MM-DDTHH:DD:SS:Z
        if start_time is not None:
            cls.start_time = start_time + ':00Z'
        if end_time is not None:
            cls.end_time = end_time + ':00Z'

    ################################  RESEARCH  ################################
    @classmethod
    def researchDecree(cls, researchType: str) -> None:
        # Quando si usa l'API v2 di twitter, twitter in automatico determina qual e' il valore limite del parametro start_time (ovvero: momento x in cui l'API v2 viene invocata - 7 giorni),
        # e, onde evitare errori di valori di start_time non validi, lo si aggiorna (qualora fosse necessario) prima di chiamare la API v2
        dtformat = '%Y-%m-%dT%H:%M:%SZ'
        currentDate = datetime.utcnow()
        validStartDate = currentDate - timedelta(days=7)
        validStartDate = validStartDate.strftime(dtformat)
        if cls.start_time < validStartDate:
            cls.start_time = validStartDate

        match researchType:
            case 'researchByUser':
                cls.getTweetByUser(username=cls.query, start_time=cls.start_time, end_time=cls.end_time)
            case 'researchByKeyword':
                cls.getTweetByKeyword(query=cls.query, tweetsLimit=cls.tweetsLimit, start_time=cls.start_time, end_time=cls.end_time)
            case 'researchByHashtag':
                cls.getTweetByKeyword(query='#'+cls.query, tweetsLimit=cls.tweetsLimit, start_time=cls.start_time, end_time=cls.end_time)
            case _:
                raise ValueError("ERROR: APIv2 Class, researchDecree: match error")
 
    @classmethod
    def getTweetByUser(cls, username: str, tweetsLimit=None, start_time=None, end_time=None) -> None:
        userData = cls.client.get_user(username=username).data
        if (userData is not None):      # Entra nell'if sse trova almeno un utente con quell'username
            userId = userData.id
            cls.response = cls.client.get_users_tweets(id=userId, max_results=tweetsLimit, expansions=cls.expansions, tweet_fields=cls.tweet_fields, start_time=start_time, end_time=end_time)

    @classmethod
    def getTweetByKeyword(cls, query: str, tweetsLimit=None, start_time=None, end_time=None) -> None:
        #cls.response = cls.client.search_recent_tweets(query=query, max_results=tweetsLimit, start_time=start_time, end_time=end_time)
        cls.response = cls.client.search_recent_tweets(query=query, max_results=tweetsLimit, expansions=cls.expansions, tweet_fields=cls.tweet_fields, start_time=start_time, end_time=end_time)
        #APIv2._createMarksJson()

    ################################  OTHER  ################################
    @classmethod
    def createCard(cls):
        if cls.response.data is not None:
            card=[]
            APIv1.__init__()
            for tweet in cls.response.data:
                tmp = cls.client.get_user(id=tweet.author_id).data
                username = tmp if tmp is not None else 'Unknown'
                text = tweet.text
                createdAt = str(tweet.created_at)[0:16]     # Si taglia la parte della stringa contenente dai secondi in poi
                coordinates = APIv1.getCoordinates(tweet_id=tweet.id, client=cls.client)
                card.append({"username": username, "text": text, "createdAt": createdAt, "coordinates": coordinates})
            return card
        else:
            return ''

    @classmethod
    def _createMarksJson(cls):
        coordinates=[]
        APIv1.__init__()
        if cls.response.data is not None:       # cls.response.data == None quando la ricerca fatta non ha prodotto risultati
            for tweet in cls.response.data:
                tweetCoordinates = APIv1.getCoordinates(tweet_id=tweet.id, client=cls.client)
                coordinates.append({"latitude": tweetCoordinates[1], "longitude": tweetCoordinates[0]})
            
            # TODO: Questo file dovrebbe essere eliminato una volta compiuto il suo scopo?
            with open('coordinates.json', 'w') as file:
                file.write(json.dumps(coordinates))

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
    def _deleteCsvFiles(cll)-> None:
        myPath = os.path.dirname(os.path.abspath(__file__)) + '/'
        for file in listdir(myPath):
            if file.endswith('.csv'):
                os.remove(myPath + file)
