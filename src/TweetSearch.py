import os
try:
    import tweepy
    import sqlite3
    import pandas as pd
    import configparser
except ModuleNotFoundError:
    os.system('pip install tweepy')
    os.system('pip install sqlite3')
    os.system('pip install config')
    os.system('pip install pandas')
    os.system('pip install configparser')

#! CURRENTLY UNTESTED CLASS 
class APIv1:
    ################ API SETUP ################
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
    
    ################  RESEARCH  ################
    tweetsLimit = 10

    @classmethod
    def setTweetsLimit(cls, tweetsLimit) -> None:
        cls.tweetsLimit=int(tweetsLimit)

    @classmethod
    def getTweetByKeyword(cls, researchPeriod: int, query: str, fromDate=None, toDate=None) -> None:
        match researchPeriod:
            case 0:
                print('last30Days')
                tweets = cls.api.search_30_day(cls.APILabel, query=query, maxResults=cls.tweetsLimit, fromDate=fromDate, toDate=toDate)
                cls._createDataFrame(tweets)
            case 1:
                print('always')
                tweets = cls.api.search_full_archive(cls.APILabel, query=query, maxResults=cls.tweetsLimit, fromDate=fromDate, toDate=toDate)
                cls._createDataFrame(tweets)
            case _:
                raise ValueError("match error")

    @classmethod
    def _createDataFrame(cls, tweets) -> None:
        # TODO: Handle wich fields must be saved and wich colums must be created
        columns = ['Time', 'User', 'Tweet']
        data = []
        for tweet in tweets:
            data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
        cls.dataFrame = pd.DataFrame(data, columns=columns)

#! CURRENTLY UNTESTED CLASS 
class SQLIntegration(APIv1):
    @classmethod
    def __init__(cls) -> None:
        APIv1.__init__()

    @classmethod
    def convertDF2SQL(cls) -> None:
        connection = sqlite3.connect('database.db')
        c = connection.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS tweet (user, desc)')
        connection.commit()	# save my edits on connection
        cls.dataFrame.to_sql(cls.section, connection, if_exists='replace', index=False)

class APIv2:
    # TODO(?) -> None: Vale la pena cercare di creare una tabella SQL anche per l'API v2?
    ################ API SETUP ################
    @classmethod
    def __init__(cls) -> None:
        # TODO: Trovare un modo migliore per esportare questo token di mrd
        cls.client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAC9YjAEAAAAA8mWmHYSXfAYFTtl2JTBaKP6SKac%3DvjWg4UEGQovjZMb5EBPmwjuIktxnOouIvBi0yUCjFZCWZEtW8q')
    
    ################  SET ATTRIBUTES  ################
    query = ''
    tweetsLimit = 10
    start_time = ''
    end_time = ''
    dataFrame = pd.DataFrame()      # Initialize an empty DataFrame

    @classmethod
    # TODO: Credo che in python esistano strumenti migliori per implementare la semantica di questa funzione
    def setDatas(cls, query: str = None, tweetsLimit = None, start_time=None, end_time=None) -> None:
        if query is not None:
            cls.query = query
        if tweetsLimit is not None:
            cls.tweetsLimit = tweetsLimit
        if start_time is not None:
            cls.start_time = start_time
        if end_time is not None:
            cls.end_time = end_time

    @classmethod
    def isDataFrameEmpty(cls) -> bool:
        tmp = cls.dataFrame()
        return tmp.empty()

    @classmethod
    def getDataFrame(cls, request: str = None) -> None:
        match request:
            case 'text':
                return '' if cls.dataFrame.empty else cls.dataFrame[request]
            case _:                
                return '' if cls.dataFrame.empty else cls.dataFrame

    ################  RESEARCH  ################
    @classmethod
    def getTweetByUser(cls, username: str) -> None:
        userData = cls.client.get_user(username=username).data
        if (userData is not None):      # Entra nell'if sse trova un utente con quel nickname
            userId = userData.id
            response = cls.client.get_users_tweets(id=userId)
            cls.dataFrame = pd.DataFrame(response.data)

    @classmethod
    def getTweetByKeyword(cls, query: str, tweetsLimit=None, start_time=None, end_time=None) -> None:
        #response = cls.client.search_recent_tweets(query=query, max_results=tweetsLimit, start_time=start_time, end_time=end_time)
        response = cls.client.search_recent_tweets(query=query, max_results=tweetsLimit)
        cls.dataFrame = pd.DataFrame(response.data)
    
    @classmethod
    def _createCsvFile(cls) -> None:
        try:
            cls.dataFrame.to_csv('APIv2DataFrame.csv')
        except AttributeError:      # Caso in cui il dataFrame sia vuoto (non si sono chiamati i metodi del'API)
            print("ATTENTION: currently there is no 'dataFrame' attribute in the AP Iv2 class.\nPossible causes:\n1) You haven't called any APIv2 method of the class yet --> Call one\n2) The call returned no results --> Try modifying the query")

    @classmethod
    def researchDecree(cls, researchType: str) -> None:
        match researchType:
            case 'researchByUser':
                print('User research')
                cls.getTweetByUser(username=cls.query)
            case 'researchByKeyword':
                print('Keyword  research')
                cls.getTweetByKeyword(query=cls.query, tweetsLimit=cls.tweetsLimit, start_time=cls.start_time, end_time=cls.end_time)
            case 'researchByHashtag':
                print('Hashtag  research')
                cls.getTweetByKeyword(query='#'+cls.query, tweetsLimit=cls.tweetsLimit, start_time=cls.start_time, end_time=cls.end_time)
            case _:
                raise ValueError("ERROR: API v2 Class, researchDecree: match error")
