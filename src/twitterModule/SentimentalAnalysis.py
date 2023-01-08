import matplotlib.pyplot as plt
from textblob import TextBlob
import nltk

nltk.downloader.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from twitterModule.TweetSearch import TweetSearch


class SentimentalAnalysis(TweetSearch):
    positive, negative, neutral, polarity = 0, 0, 0, 0
    tweet_list, neutral_list, negative_list, positive_list = [], [], [], []
    path = "./"  # path to store created graphs

    @classmethod
    def __init__(cls, BEARER_TOKEN: str, path: str = "./") -> None:
        super().__init__(BEARER_TOKEN=BEARER_TOKEN)
        cls.path = path

    @classmethod
    def _percentage(cls, part, whole) -> float:
        return 100 * float(part) / float(whole)

    @classmethod
    def _analyzeResponse(cls) -> None:
        for tweet in cls.response.data:
            cls.tweet_list.append(tweet.text)
            analysis = TextBlob(tweet.text)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
            neg = score["neg"]
            neu = score["neu"]
            pos = score["pos"]
            comp = score["compound"]
            cls.polarity += analysis.sentiment.polarity
            if neg > pos:
                cls.negative_list.append(tweet.text)
                if type(cls.negative) == type(str()):
                    cls.negative = float(cls.negative)
                cls.negative += 1
            elif pos > neg:
                cls.positive_list.append(tweet.text)
                if type(cls.positive) == type(str()):
                    cls.positive = float(cls.positive)
                cls.positive += 1
            elif pos == neg:
                cls.neutral_list.append(tweet.text)
                if type(cls.neutral) == type(str()):
                    cls.neutral = float(cls.neutral)
                cls.neutral += 1

        cls.positive = cls._percentage(part=cls.positive, whole=cls.tweetsLimit)
        cls.negative = cls._percentage(part=cls.negative, whole=cls.tweetsLimit)
        cls.neutral = cls._percentage(part=cls.neutral, whole=cls.tweetsLimit)
        cls.polarity = cls._percentage(part=cls.polarity, whole=cls.tweetsLimit)
        cls.positive = format(cls.positive, ".1f")
        cls.negative = format(cls.negative, ".1f")
        cls.neutral = format(cls.neutral, ".1f")

    @classmethod
    def _buildResponseGraph(cls, graphName: str) -> None:
        labels = [
            "Positive [" + str(cls.positive) + "%]",
            "Neutral [" + str(cls.neutral) + "%]",
            "Negative [" + str(cls.negative) + "%]",
        ]
        sizes = [cls.positive, cls.neutral, cls.negative]
        colors = ["yellowgreen", "blue", "red"]
        fig = plt.figure()
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.style.use("default")
        plt.legend(labels)
        plt.title(f"Sentiment Analysis Result for keyword: '{cls.query}'")
        plt.axis("equal")
        # plt.show()
        cls._saveGraph(fig=fig, graphName=graphName, savePath=cls.path)

    @classmethod
    def _saveGraph(cls, fig, graphName: str, savePath: str = "./") -> None:
        fig.savefig(savePath + graphName + ".svg")

    @classmethod
    def _resetClassVars(cls):
        cls.positive, cls.negative, cls.neutral, cls.polarity = 0, 0, 0, 0
        vtweet_list, cls.neutral_list, cls.negative_list, cls.positive_list = (
            [],
            [],
            [],
            [],
        )

    @classmethod
    def getSentimentalDatas(cls) -> dict:
        sentimentalDatas = {
            "analyzedTweets": len(cls.tweet_list),
            "positiveTweets": len(cls.positive_list),
            "negativeTweets": len(cls.negative_list),
            "neutralTweets": len(cls.neutral_list),
        }
        return sentimentalDatas

    @classmethod
    def SentimentalAnalysis(cls, response=None) -> dict:
        cls._resetClassVars()
        cls.response = response
        cls._analyzeResponse()
        cls._buildResponseGraph(graphName="cakeGraph")
        return cls.getSentimentalDatas()
