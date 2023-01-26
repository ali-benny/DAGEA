import os

try:
    import tweepy  # Used for APIs
except ModuleNotFoundError:
    os.system("pip install tweepy")


class APIv2:
    client, response = None, None
    query, username = "", ""
    tweetsLimit = 10
    start_time, end_time = None, None
    expansions = ["author_id","geo.place_id"]
    tweet_fields = ["created_at"]
    place_fields = ["geo"]
    media_fields = None
    @classmethod
    def __init__(cls, BEARER_TOKEN: str) -> None:
        cls.client = tweepy.Client(bearer_token=BEARER_TOKEN)

    @classmethod
    def setDatas(
        cls,
        query: str = None,
        tweetsLimit: int = None,
        start_time=None,
        end_time=None,
        expansions: list = None,
        tweet_fields: list = None,
        media_fields:list = None
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
        if media_fields is not None:
            cls.media_fields = media_fields
