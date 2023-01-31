import configparser
import tweepy
import shutil
import os
from os.path import exists
try:
    import wget
except ModuleNotFoundError:
    os.system("pip install wget")

config = configparser.ConfigParser()
config.read(os.path.abspath("../config.ini"))

client = tweepy.Client(bearer_token=config["twitter"]["bearer_token"])


def getAllNames(method=client.search_recent_tweets) -> list:
    """
    It gets all the users who have tweeted with the hashtag #Fantacitorio

    :param method: the method to use to get the tweets
    :return: A list of dictionaries.
    """
    responses = tweepy.Paginator(
        method, query="#Fantacitorio", expansions=["author_id"], max_results=100
    )
    for response in responses:
        users = response.includes["users"]
    return users


def getPinnedTweetId(userName: str) -> int | None:
    """
    It takes a Twitter username as a string and returns the ID of the user's pinned tweet as an integer,
    or None if the user has no pinned tweet

    :param userName: The username of the account you want to get the pinned tweet ID from
    :type userName: str
    :return: The pinned tweet id of the user.
    """
    response = client.get_user(username=userName, expansions=["pinned_tweet_id"])
    if response.includes != {}:
        pinnedTweetId = response.includes["tweets"][0]["id"]
        return pinnedTweetId


def getTweetImageInfos(tweetId: int) -> dict | None:
    """
    It gets the tweet with the given ID, checks if it contains the hashtag #Fantacitorio, and if it
    does, it returns a dictionary with the image link and the image name

    :param tweetId: The ID of the tweet you want to get the image from
    :type tweetId: int
    :return: A dictionary with the image link and the image name.
    """
    response = client.get_tweet(
        id=tweetId, expansions=["attachments.media_keys"], media_fields=["url"]
    )
    if (
        "#Fantacitorio" in response.data["text"]
        or "#fantacitorio" in response.data["text"]
    ):
        imageLink = response.includes["media"][0]["url"]
        imageName = imageLink[imageLink.rindex("/") + 1 :]
        return {"imageLink": imageLink, "imageName": imageName}


def saveTweetImage(imageLink: str, imageName: str, path: str = "./"):
    """
    It downloads the image from the link provided, and saves it to the path provided

    :param imageLink: The link to the image you want to download
    :type imageLink: str
    :param imageName: The name of the image you want to save it as
    :type imageName: str
    :param path: The path to the folder where you want to save the images, defaults to ./
    :type path: str (optional)
    """
    if exists(path=path + imageName) == False:
        imageName = wget.download(url=imageLink)
        shutil.move("./" + imageName, path)


def saveUserTeamImage(user: str, path: str = "./") -> bool:
    """
    It gets the pinned tweet id of the user, gets the image infos of the tweet, and saves the image of
    the tweet. Returns true if the image has been saved, false otherwise.

    :param user: str = The user's username
    :type user: str
    :param path: The path to save the image to, defaults to ./
    :type path: str (optional)
    :return: A boolean value.
    """
    pinnedTweetId = getPinnedTweetId(user)
    if pinnedTweetId != None:
        imageInfos = getTweetImageInfos(tweetId=pinnedTweetId)
        if imageInfos != None:
            saveTweetImage(
                imageLink=imageInfos["imageLink"],
                imageName=imageInfos["imageName"],
                path=path,
            )
        return True
    return False


def generateFantacitorioTeamsImages(path: str = "./") -> None:
    # Getting all the users who have tweeted with the hashtag #Fantacitorio, and for each of them, it
    # is saving the image of their team.
    users = getAllNames()
    for user in users:
        saveUserTeamImage(user=user["username"], path=path)


if __name__ == "__main__":
    generateFantacitorioTeamsImages(path="../static/img/fantacitorio/teams/")
