import os
try:
    from flask import Flask, render_template, request, redirect, session
    from flask_session import Session
    import getTweet
    import sqlite3
    import chess
    import jinja2
except ModuleNotFoundError:
    os.system('pip install flask')
    os.system('pip install flask_session')
    os.system('pip install getTweet')
    os.system('pip install sqlite3')
    os.system('pip install chess')
    os.system('pip install jinja2')

import chess.svg
import game



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

startTweetLimit = 6
researchMethods = [
	{'method':"", 'text':'Research by '},
	{'method':'researchByUser', 'text':'Research by user'},
	{'method':'researchByKeyword','text':'Research by keyword and hashtag'}
]	# A list containing all available search methods
dataRangeInputs = [
	{'value':"",             'text':'Search from '},
	{'value':'today',        'text':'Search from today'},
	{'value':'oneDayAgo',    'text':'Search from 1 day ago'},
	{'value':'twoDaysAgo',   'text':'Search from 2 days ago'},
	{'value':'threeDaysAgo', 'text':'Search from 3 days ago'},
	{'value':'fourDaysAgo',  'text':'Search from 4 days ago'},
	{'value':'fiveDaysAgo',  'text':'Search from 5 days ago'},
	{'value':'sixDaysAgo',   'text':'Search from 6 days ago'},
	{'value':'sevenDaysAgo', 'text':'Search from 7 days ago'},
	{'value':'eightDaysAgo', 'text':'Search from 8 days ago'},
	{'value':'nineDaysAgo',  'text':'Search from 9 days ago'},
]

@app.route('/', methods=('GET', 'POST'))
def homepage():
	currentResearchMethod = ""							# the currently chosen search method
	currentRange = ""							# the currently chosen search method
	if request.method == 'POST':
		keyword = request.form['keyword']		# getting keyword from form
		tweetLimit = request.form['tweetLimit']	# getting tweetLimit input, from the <input type="number" name="tweetLimit"> of index.html, in the form of a string
		currentResearchMethod = request.form.get('researchBy')
		currentRange = request.form.get('currentRange')
		
		getTweet.convertDF2SQL(currentResearchMethod, int(tweetLimit), keyword)
		
		connection = sqlite3.connect('database.db')		# connecting to database
		connection.row_factory = sqlite3.Row	# read row from database
		tweets = connection.execute('SELECT * FROM tweet').fetchall() 	# getting all tweet form db
		connection.close()	# close connection to database

		return render_template(
			'index.html',
			tweets=tweets,
			tweetLimit=tweetLimit,
			researchMethods=researchMethods,
			currentResearchMethod=currentResearchMethod,
			dataRangeInputs=dataRangeInputs,
			currentRange=currentRange
		)	# rendering flask template 'index.html'
	getTweet.__main__()		# getTweet and save them into db
	connection = sqlite3.connect('database.db')		# connecting to database
	connection.row_factory = sqlite3.Row	# read row from database
	tweets = connection.execute('SELECT * FROM tweet').fetchall() 	# getting all tweet form db
	connection.close()	# close connection to database
	return render_template(
		'index.html',
		tweets=tweets,
		tweetLimit=startTweetLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dataRangeInputs=dataRangeInputs,
		currentRange=currentRange
	)

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

@app.route('/chess')
def chessPage():
	return render_template('chess.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

@app.route('/rules')
def rulePage():
	return render_template('chess_rules.html')

@app.route('/game')
def chessGame():
	if not session.get("scacchiera"):
		board = chess.Board()
		session["scacchiera"] = board
	else:
		board = session["scacchiera"]
	
	table = chess.svg.board(board)

	f = open('./static/img/board.svg', 'w')
	f.write(table)
	f.close()

	return render_template('partita.html', table=table)

@app.route('/give_move', methods=['GET', 'POST'])
def WTurn():
	if not session.get("scacchiera"):
		board = chess.Board() #creo la scacchiera nel session storage se non è presente
		session["scacchiera"] = board
	else:
		board = session["scacchiera"] #prendo la scacchira nel session storage se presente
	
	move=request.form['move'] #prendo la mossa in notazione algebrica
	if(board.turn):
		s = chess.Move.from_uci(move) #Prendo la mossa in input
		if(s in board.legal_moves): #Controllo che possa essere eseguita e che sia il turno del bianco
			board.push(s)
			session["scacchiera"] = board #la eseguo, aggiorno la scacchiera e controllo se la partita è terminata
			if(board.outcome() != None):
				if(board.outcome().winner == None):
					return render_template('draw.html')
				elif(board.outcome().winner):
					return render_template('white.html')
				else:
					return render_template('black.html')
			#invio il tweet con la mossa fatta
			return redirect('https://twitter.com/intent/tweet?text=La%20mia%20mossa%20in%20notazione%20algebrica:%20'+move+"%0AIl%20mio%20fen:%0A"+str(board)+ "%0AInserire%20casella%20di%20partenza%20e%20casella%20di%20arrivo%20per%20giocare" +"%0A%23ingsw2223")
	
	return render_template('partita.html')


@app.route('/get_move', methods=['GET', 'POST'])
def BTurn():
	if not session.get("scacchiera"):
		board = chess.Board() #creo la scacchiera nel session storage se non è presente
	else:
		board = session["scacchiera"] #prendo la scacchira nel session storage se presente

	account=request.form['account'] #prendo il nome dell'account per poter prendere il primo tweet

	if(board.turn):  #controllo che sia il turno del nero
		return render_template('partita.html')
	else:
		sit = game.__main__(board, account) #prendo la mossa più votata in risposta all'ultimo tweet e controllo se la partita è terminata
		if(sit == "Bianco"):
			return render_template("white.html")
		session["scacchiera"] = sit
	if(board.outcome() != None):
		if(board.outcome().winner == None):
			return render_template('draw.html')
		elif(board.outcome().winner):
			return render_template('white.html')
		else:
			return render_template('black.html')


if __name__=="__main__":
    app.run(debug=True)
