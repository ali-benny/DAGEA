import os
# import sys
import random
# sys.path.append("..")
from .utils import filtersbar 
from .APIv2 import APIv2

try:
    import tweepy
except ModuleNotFoundError:
    os.system("pip install tweepy")


class TweetSearch(APIv2):
    @classmethod
    def __init__(cls, BEARER_TOKEN: str) -> None:
        super().__init__(BEARER_TOKEN=BEARER_TOKEN)

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
                    if cls.tweepyCursor == True:        #INFO: https://docs.tweepy.org/en/v4.12.1/v2_pagination.html
                        cls.response = tweepy.Paginator(cls.client.search_recent_tweets,
                            query=cls.query,
                            expansions=cls.expansions,
                            tweet_fields=cls.tweet_fields,
                            place_fields=cls.place_fields,
                            start_time=cls.start_time,
                            end_time=cls.end_time,
                            media_fields=cls.media_fields,
                            max_results=100, limit=random.randint(2, 8))
                    else:
                        cls.response = cls.client.search_recent_tweets(
                        query=cls.query,
                        max_results=cls.tweetsLimit,
                        expansions=cls.expansions,
                        tweet_fields=cls.tweet_fields,
                        place_fields=cls.place_fields,
                        start_time=cls.start_time,
                        end_time=cls.end_time,
                        media_fields=cls.media_fields,
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
    def createCard(cls) -> list | str:
        if cls.response != None and cls.response.data is not None:
            cards = []
            for tweet in cls.response.data:
                username = cls.client.get_user(id=tweet.author_id).data['username']
                text = tweet.text
                createdAt = str(tweet.created_at)[
                    0:16
                ]  # Si taglia la parte della stringa contenente dai secondi in poi
                geoDatas = cls.getGeoDatasOfATweet(tweet=tweet)
                cards.append(
                    {
                        "username": str(username),
                        "text": text,
                        "createdAt": createdAt,
                        "latitude": geoDatas.get("latitude"),
                        "longitude": geoDatas.get("longitude"),
                        "taggedPlace": geoDatas.get("taggedPlace"),
                    }
                )
            return cards
        else:
            return ""

    @classmethod
    def cardHaveCoordinates(cls, cards: list) -> bool:
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