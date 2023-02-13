import chess
import chess.svg
from collections import Counter
import tweepy
import time
try:
	from pythonModules.twitter.TweetSearch import TweetSearch
except (ModuleNotFoundError, ImportError):
	from .pythonModules.twitter.TweetSearch import TweetSearch


def countdown(t):
    while t:
        time.sleep(1)
        t -= 1


def black_turn(account, board):
    api = TweetSearch.__init__()
    bianco = "Bianco"
    countdown(60)
    tweets = api.user_timeline(screen_name = account, count = 1)
    tweet_id = [tweet.id for tweet in tweets] #riceve l'id dell'ultimo post utilizzato per giocare

    replies=[]
    for tweet in tweepy.Cursor(api.search,q='to:'+account, result_type='recent', timeout=999999).items(100):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):#prende le risposte dell'ultimo tweet
                replies.append(tweet.text)
    
    if(len(replies) == 0):
         return bianco#ritorna il fatto che non ci sono riaposte e quindi il bianco vince, posso passare una stringa

    c = Counter(replies)
    for i in range(c):
        s = chess.Move.from_uci(c.most_common(i + 1))
        if(s in board.legal_moves):
              board.push(s)
              return board
    return bianco
  

def __main__(board, account):
    status = black_turn(account ,board)
    return status


if __name__ == '__main__':
	__main__()
