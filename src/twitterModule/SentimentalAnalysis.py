from textblob import TextBlob
import re
from better_profanity import profanity
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

from twitterModule.APIv2 import APIv2


class SentimentalAnalysis(APIv2):
    path = "./"  # path to store created graphs
    analysisReport = {}  # Percentuali delle analisi
    analysisDatas = {
        "users": [],
        "texts": [],
        "polarities": [],
        "sentiments": [],
    }  # Dati delle analisi

    @classmethod
    def __init__(cls, BEARER_TOKEN: str, path: str = "./") -> None:
        super().__init__(BEARER_TOKEN)
        cls.path = path

    ############################## GETTING DATA METHODS ##############################

    @classmethod
    def _cleanText(cls, text):
        if type(text) == float():
            return ""
        r = text.lower()
        r = profanity.censor(r)
        r = re.sub("'", "", r)  # This is to avoid removing contractions in english
        r = re.sub("@[A-Za-z0-9_]+", "", r)
        r = re.sub("#[A-Za-z0-9_]+", "", r)
        r = re.sub(r"http\S+", "", r)
        r = re.sub("[()!?]", " ", r)
        r = re.sub("\[.*?\]", " ", r)
        r = re.sub("[^a-z0-9]", " ", r)
        r = r.split()
        stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
        r = [w for w in r if not w in stopwords]
        r = " ".join(word for word in r)
        return r

    @classmethod
    def getTextsAndUsers(cls, response) -> list:
        texts, users = [], []
        for user in response.includes["users"]:
            for tweet in response.data:
                if tweet["author_id"] == user["id"]:
                    texts.append(tweet["text"])
                    users.append(user["username"])
        texts = [cls._cleanText(text) for text in texts]
        return users, texts

    @classmethod
    def getTextsAnalysis(cls, texts):
        textsAnalysis = [TextBlob(text) for text in texts]
        return textsAnalysis

    @classmethod
    def getPolarities(cls, textsAnalysis) -> list:
        polarities = []
        [polarities.append(obj.polarity) for obj in textsAnalysis]
        return polarities

    @classmethod
    def getSentiments(cls, polarities: list) -> list:
        sentiments = []
        for polarity in polarities:
            if polarity > 0:
                sentiments.append("positive")
            elif polarity < 0:
                sentiments.append("negative")
            else:
                sentiments.append("neutral")
        return sentiments

    @classmethod
    def getSentimentsCounters(cls, polarities: list) -> dict:
        positiveCounter, neutralCounter, negativeCounter = 0, 0, 0
        for polarity in polarities:
            if polarity > 0:
                positiveCounter += 1
            elif polarity < 0:
                negativeCounter += 1
            else:
                neutralCounter += 1
        sentimentsCounter = {
            "positiveCounter": positiveCounter,
            "neutralCounter": neutralCounter,
            "negativeCounter": negativeCounter,
        }
        return sentimentsCounter

    ############################## GRAPHS METHODS ##############################

    @classmethod
    def _saveGraph(cls, fig, graphName: str, savePath: str = "./") -> None:
        fig.savefig(savePath + graphName + ".svg")

    @classmethod
    def createCakeGraph(
        cls,
        sentimentsCounter: dict,
        graphName: str,
    ):
        pieLabels = ["Positive", "Neutral", "Negative"]
        populationShare = [
            sentimentsCounter["positiveCounter"],
            sentimentsCounter["neutralCounter"],
            sentimentsCounter["negativeCounter"],
        ]
        figureObject, axesObject = plt.subplots()
        axesObject.pie(
            populationShare, labels=pieLabels, autopct="%1.2f", startangle=90
        )
        axesObject.axis("equal")
        cls._saveGraph(fig=figureObject, graphName=graphName, savePath=cls.path)

    @classmethod
    def createWordCloud(cls, texts: list, graphName: str):
        allWords = " ".join([text for text in texts])
        wordcloud = WordCloud(
            width=800, height=500, random_state=21, max_font_size=110
        ).generate(allWords)
        plt.figure(figsize=(10, 7))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        wordcloud = wordcloud.to_file(cls.path + graphName + ".png")

    ############################## STATS METHODS ##############################

    @classmethod
    def _getPercentage(cls, total, part) -> int:
        return int((100 * float(part)) / float(total))

    @classmethod
    def getAnalisysReport(cls, sentimentsCounter: dict) -> dict:
        totalCount = sum(sentimentsCounter.values())
        analisysDatas = {
            "analyzedTweets": totalCount,
            "positivePercentage": cls._getPercentage(
                total=totalCount, part=sentimentsCounter["positiveCounter"]
            ),
            "neutralPercentage": cls._getPercentage(
                total=totalCount, part=sentimentsCounter["neutralCounter"]
            ),
            "negativePercentage": cls._getPercentage(
                total=totalCount, part=sentimentsCounter["negativeCounter"]
            ),
        }
        return analisysDatas

    ##############################  ##############################

    @classmethod
    def SentimentalAnalysis(cls, response) -> None:
        cls.analysisDatas['users'], cls.analysisDatas['texts'] = cls.getTextsAndUsers(response=response)
        textsAnalysis = cls.getTextsAnalysis(texts=cls.analysisDatas['texts'])
        cls.analysisDatas['polarities'] = cls.getPolarities(textsAnalysis=textsAnalysis)
        cls.analysisDatas['sentiments'] = cls.getSentiments(polarities=cls.analysisDatas['polarities'])
        sentimentsCounter = cls.getSentimentsCounters(polarities=cls.analysisDatas['polarities'])
        cls.analysisReport = cls.getAnalisysReport(sentimentsCounter=sentimentsCounter)

        cls.createCakeGraph(
            sentimentsCounter=sentimentsCounter,
            graphName="cakeGraph",
        )
        cls.createWordCloud(texts=cls.analysisDatas['texts'], graphName="wordCloud")