import chess
import chess.svg
from collections import Counter
import twitter
import tweepy
import time

def countdown(t):
    
    while t:
        time.sleep(1)
        t -= 1

def white_turn(move, board):
    table = board
    if(move in list(table.legal_moves)):
        table.push_san(move)
        return table

def black_turn(account, board):
    api = twitter.__init__()
    countdown(60)
    tweets = api.user_timeline(screen_name = account, count = 1)
    tweet_id = [tweet.id for tweet in tweets] #riceve l'id dell'ultimo post utilizzato per giocare

    replies=[]
    for tweet in tweepy.Cursor(api.search,q='to:'+account, result_type='recent', timeout=999999).items(100):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):#prende le risposte dell'ultimo tweet
                replies.append(tweet.text)
    
    if(len(replies) == 0):
         pass#ritorna il fatto che non ci sono riaposte e quindi il bianco vince, posso passare una stringa

    c = Counter(replies)
    for i in range(c):
        if(c.most_common(i + 1) in list(board.legal_moves)):
              board.push_san(c.most_common(i + 1))
              return board

    #return bianco vince   
        


def __main__(board,move,account):
        
    #inserire dentro status le variabili passate così in caso di tasto sbagliato non succede nulla
    if(board.turn):
            status = white_turn(move,board)
    else:
            status = black_turn(account,board)

    return status
    #da fare anche i test per questo python

if __name__ == '__main__':
	__main__()