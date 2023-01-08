import os
import tweepy
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob
import nltk

nltk.downloader.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from TweetSearch import APIv2

"""
import sys
import tweepy
import numpy as np
import os
import pycountry
import re
import stringfrom wordcloud import WordCloud, STOPWORDS
from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
"""


class SentimentalAnalysis(APIv2):
    positive, negative, neutral, polarity = 0, 0, 0, 0
    tweet_list, neutral_list, negative_list, positive_list = [], [], [], []
    query, numberOfTweets = "", 0
    responses = None
    path = "./"  # path to store created graphs

    @classmethod
    # def __init__(cls, BEARER_TOKEN: str) -> None:
    def __init__(cls, path: str = "./") -> None:
        super().__init__()
        cls.path = path

    @classmethod
    def setResearchDatas(cls, query: str = None, numberOfTweets: int = None) -> None:
        cls.query = query
        cls.numberOfTweets = numberOfTweets

    @classmethod
    def _getResponse(cls):
        cls.responses = tweepy.Paginator(
            method=cls.client.search_recent_tweets, query=cls.query, max_results=100
        ).flatten(limit=cls.numberOfTweets)

    @classmethod
    def _percentage(cls, part, whole):
        return 100 * float(part) / float(whole)

    @classmethod
    def _analyzeResponse(cls):
        for tweet in cls.responses:
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
                cls.negative += 1
            elif pos > neg:
                cls.positive_list.append(tweet.text)
                cls.positive += 1
            elif pos == neg:
                cls.neutral_list.append(tweet.text)
                cls.neutral += 1

        cls.positive = cls._percentage(part=cls.positive, whole=cls.numberOfTweets)
        cls.negative = cls._percentage(cls.negative, cls.numberOfTweets)
        cls.neutral = cls._percentage(cls.neutral, cls.numberOfTweets)
        cls.polarity = cls._percentage(cls.polarity, cls.numberOfTweets)
        cls.positive = format(cls.positive, ".1f")
        cls.negative = format(cls.negative, ".1f")
        cls.neutral = format(cls.neutral, ".1f")

    @classmethod
    def _buildResponseGraph(cls, graphName: str):
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
    def _saveGraph(cls, fig, graphName: str, savePath: str = "./"):
        fig.savefig(savePath + graphName + ".svg")

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
    def SentimentalAnalysis(cls, ) -> dict:
        cls._getResponse()
        cls._analyzeResponse()
        cls._buildResponseGraph(graphName='cakeGraph')
        return cls.getSentimentalDatas()

    @classmethod
    def createDataFrames(cls):
        cls.tweet_list = pd.DataFrame(cls.tweet_list)
        cls.neutral_list = pd.DataFrame(cls.neutral_list)
        cls.negative_list = pd.DataFrame(cls.negative_list)
        cls.positive_list = pd.DataFrame(cls.positive_list)


if __name__ == "__main__":
    numberOfTweets = 100
    query = "qatar"
    SentimentalAnalysis.__init__(path="./static/img/graphs/")
    SentimentalAnalysis.setResearchDatas(query=query, numberOfTweets=numberOfTweets)
    SentimentalAnalysis.SentimentalAnalysis()
