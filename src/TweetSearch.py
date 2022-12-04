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
        cls.__init__response()

    @classmethod
    def __init__response(cls) -> None:
        cls.response = cls.client.get_user(id=0)    # Questa chiamata di get_user ritornera' un dato response vuoto (analogo ad una string avuota '')

    ################  ATTRIBUTE SETTING   ################
    dataFrames = []
    query = ''
    tweetsLimit = 10
    start_time = ''
    end_time = ''
    expansions = []

    @classmethod
    # TODO: Credo proprio che esistano strumenti migliori per implementare la semantica di questa funzione
    def setDatas(cls, query: str = None, tweetsLimit = None, start_time=None, end_time=None, expansions=None) -> None:
        if query is not None:
            cls.query = query
        if tweetsLimit is not None:
            cls.tweetsLimit = tweetsLimit
        if start_time is not None:
            cls.start_time = start_time
        if end_time is not None:
            cls.end_time = end_time
        if expansions is not None:
            cls.expansions = expansions

    @classmethod
    def getDataFrames(cls, responseField: int, field: str = None):
        try:
            if cls.dataFrames == [] or cls.dataFrames[responseField].empty:    # O non si e' chiamata nessuna funzione di ricerca o la chiamata non ha trovato nulla
                return ''
            else:
                return cls.dataFrames[responseField][field]
        except IndexError:
            print("ERROR: APIv2 Class, getDataFrames: except IndexError")
            return ''
        except KeyError:
            print("ERROR: APIv2 Class, getDataFrames: except KeyError")
            return ''

    ################  RESEARCH  ################
    @classmethod
    def researchDecree(cls, researchType: str) -> None:
        match researchType:
            case 'researchByUser':
                print('User research')
                cls.getTweetByUser(username=cls.query)
            case 'researchByKeyword':
                print('Keyword  research')
                cls.getTweetByKeyword(query=cls.query, tweetsLimit=cls.tweetsLimit, start_time=cls.start_time, end_time=cls.end_time, expansions=cls.expansions)
            case 'researchByHashtag':
                print('Hashtag  research')
                cls.getTweetByKeyword(query='#'+cls.query, tweetsLimit=cls.tweetsLimit, start_time=cls.start_time, end_time=cls.end_time, expansions=cls.expansions)
            case _:
                raise ValueError("ERROR: APIv2 Class, researchDecree: match error")
 
    @classmethod
    def getTweetByUser(cls, username: str) -> None:
        userData = cls.client.get_user(username=username).data
        if (userData is not None):      # Entra nell'if sse trova almeno un utente con quell'username
            userId = userData.id
            cls.response = cls.client.get_users_tweets(id=userId)
            #cls.createDataFrames(cls.response)

    @classmethod
    def getTweetByKeyword(cls, query: str, tweetsLimit=None, start_time=None, end_time=None, expansions=None) -> None:
        #cls.response = cls.client.search_recent_tweets(query=query, max_results=tweetsLimit, start_time=start_time, end_time=end_time)
        cls.response = cls.client.search_recent_tweets(query=query, max_results=tweetsLimit, expansions=expansions)
        #cls.createDataFrames(cls.response)

    ################  DATA HANDLING  ################
    @classmethod
    def createCard(cls):
        if cls.response.data is not None:
            card=[]
            for tweet in cls.response.data:
                text = tweet.text
                tmp = cls.client.get_user(id=tweet.author_id).data
                username = tmp if tmp is not None else 'Unknown'
                card.append({"username": username, "text": text})
                print(f"CARD:\n{card}")
            return card
        else:
            return ''

    @classmethod
    def createDataFrames(cls, response, field: str = 'all') -> None:
        cls.dataFrames = []
        match field:
            case 'all':
                cls.dataFrames.append(pd.DataFrame(response))
                cls.dataFrames.append(pd.DataFrame(response.data))
                cls.dataFrames.append(pd.DataFrame(response.includes))
                cls.dataFrames.append(pd.DataFrame(response.errors))
            case 'response':
                cls.dataFrames.append(pd.DataFrame(response))
            case 'data':
                cls.dataFrames.append(pd.DataFrame(response.data))
            case 'includes':
                cls.dataFrames.append(pd.DataFrame(response.includes))
            case 'errors':
                cls.dataFrames.append(pd.DataFrame(response.errors))
            case _:
                raise ValueError("ERROR: APIv2 Class, createDataFrames: match error")
        
    @classmethod
    def _createCsvFile(cls) -> None:
        try:
            '''
            i = 0
            for dataFrame in cls.dataFrames:
                i =+ 1
                dataFrame.to_csv('dataFrame'+str(i)+'.csv')
            '''
            cls.dataFrames[0].to_csv('response.csv')
            cls.dataFrames[1].to_csv('responseData.csv')
            cls.dataFrames[2].to_csv('responseIncludes.csv')
            cls.dataFrames[3].to_csv('responseErrors.csv')
        except AttributeError:      # Caso in cui dataFrames[i] sia vuoto (non si sono chiamati i metodi del'API)
            print("ATTENTION: currently there is no 'cls.dataFrames[i]' attribute in the APIv2 class.\nPossible causes:\n1) You haven't called any APIv2 method of the class yet --> Call one\n2) The call returned no results --> Try modifying the query")
