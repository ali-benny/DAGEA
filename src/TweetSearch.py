import os
from os import listdir
import sys

sys.path.append("..")
import src.utils_filtersbar as filtersbar
import configparser  # EDIT: era import config

try:
    import tweepy  # Used for APIs
    import pandas as pd  # Used for data handling and debug
    import configparser  # Used for APIv1 initialization
except ModuleNotFoundError:
    os.system("pip install tweepy")
    os.system("pip install pandas")
    os.system("pip install configparser")

config = configparser.ConfigParser()
config.read(os.path.abspath("config.ini"))


class APIv2:
    query, username = "", ""
    tweetsLimit = 10
    start_time, end_time = None, None
    expansions = ["author_id", "geo.place_id"]
    tweet_fields = ["created_at"]
    place_fields = ["geo"]
    response = None

    @classmethod
    def __init__(cls) -> None:
        cls.client = tweepy.Client(bearer_token=config["twitter"]["bearer_token"])

    ################################  ATTRIBUTE SETTING   ################################
    @classmethod
    def setDatas(
        cls,
        query: str = None,
        tweetsLimit: int = None,
        start_time=None,
        end_time=None,
        expansions: list = None,
        tweet_fields: list = None,
    ) -> None:
        if query is not None:
            cls.query = query
        if (
            tweetsLimit is not None
            and 10 <= int(tweetsLimit)
            and int(tweetsLimit) <= 100
        ):
            cls.tweetsLimit = tweetsLimit
        # I parametri attuali {start|end}_time sono ritornati da HTML nella forma: YYYY-MM-DDTHH:DD e vanno
        # dunque fatte delle modifiche per adattarle al formato dell'API v2, ovvero:YYYY-MM-DDTHH:DD:SS:Z
        if start_time is not None:
            cls.start_time = start_time + ":00Z"
        else:
            cls.start_time = None
        if end_time is not None:
            cls.end_time = end_time + ":00Z"
        else:
            cls.end_time = None
        if expansions is not None:
            cls.expansions = expansions
        if tweet_fields is not None:
            cls.tweet_fields = tweet_fields

    ################################  OTHER  ################################
    @classmethod
    def researchDecree(cls, researchType: str) -> None:
        cls.start_time = filtersbar.updateTime(cls.start_time)
        match researchType:
            case "researchByUser":
                try:
                    userData = cls.client.get_user(username=cls.query).data
                    cls.response = cls.client.get_users_tweets(
                        id=userData.id,
                        max_results=cls.tweetsLimit,
                        expansions=cls.expansions,
                        tweet_fields=cls.tweet_fields,
                        place_fields=cls.place_fields,
                        start_time=cls.start_time,
                        end_time=cls.end_time,
                    )
                except tweepy.errors.NotFound:
                    cls.response = None
            case "researchByKeyword":
                try:
                    cls.response = cls.client.search_recent_tweets(
                        query=cls.query,
                        max_results=cls.tweetsLimit,
                        expansions=cls.expansions,
                        tweet_fields=cls.tweet_fields,
                        place_fields=cls.place_fields,
                        start_time=cls.start_time,
                        end_time=cls.end_time,
                    )
                except tweepy.errors.NotFound:
                    cls.response = None
            case "researchByHashtag":
                try:
                    cls.response = cls.client.search_recent_tweets(
                        query="#" + cls.query,
                        max_results=cls.tweetsLimit,
                        expansions=cls.expansions,
                        tweet_fields=cls.tweet_fields,
                        place_fields=cls.place_fields,
                        start_time=cls.start_time,
                        end_time=cls.end_time,
                    )
                except tweepy.errors.NotFound:
                    cls.response = None
            case _:
                raise ValueError("ERROR: APIv2 Class, researchDecree: match error")

    @classmethod
    def createCard(cls) -> list:
        if cls.response != None and cls.response.data is not None:
            card = []
            for tweet in cls.response.data:
                # tmp = cls.client.get_user(id=tweet.author_id).data
                # username = tmp if tmp is not None else 'Unknown'
                username = cls.response.includes["users"][0].username
                text = tweet.text
                createdAt = str(tweet.created_at)[
                    0:16
                ]  # Si taglia la parte della stringa contenente dai secondi in poi

                geoDatas = cls.getGeoDatasOfATweet(tweet=tweet)

                card.append(
                    {
                        "username": str(username),
                        "text": text,
                        "createdAt": createdAt,
                        "latitude": geoDatas.get("latitude"),
                        "longitude": geoDatas.get("longitude"),
                        "taggedPlace": geoDatas.get("taggedPlace"),
                    }
                )
            return card
        else:
            return ""

    @classmethod
    def hasCardsGeo(cls, cards: list) -> bool:
        for card in cards:
            if card["latitude"] != None and card["longitude"] != None:
                return True
        return False

    @classmethod
    def getGeoDatasOfATweet(cls, tweet) -> dict:
        geoDatas = {"latitude": None, "longitude": None, "taggedPlace": ""}
        if tweet["geo"] != None:  # Entra solo se nel tweet e' stato taggato un posto
            tweetPlaceId = tweet["geo"]["place_id"]
            for place in cls.response.includes["places"]:
                if (
                    tweetPlaceId == place.id
                ):  # Se il place_id del tweet viene trovato tra i place_id di response.includes
                    geoDatas["taggedPlace"] = place.full_name
                    bbox = place.geo["bbox"]
                    if (
                        bbox[0] != bbox[2] or bbox[1] != bbox[3]
                    ):  # Se si hanno due punti con coordinate diverse
                        latitudes = [bbox[1], bbox[3]]
                        longitudes = [bbox[0], bbox[2]]
                        geoDatas["latitude"] = sum(latitudes) / len(latitudes)
                        geoDatas["longitude"] = sum(longitudes) / len(longitudes)
                    else:  # Se i punti hanni identiche coordinate
                        geoDatas["latitude"] = bbox[0]
                        geoDatas["longitude"] = bbox[1]
                    return geoDatas
        return geoDatas
