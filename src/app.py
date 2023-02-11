import os
try:
    from flask import Flask, render_template, request, redirect
    import getTweet
    import sqlite3
    import jinja2
except ModuleNotFoundError:
    os.system('pip install flask')
    os.system('pip install getTweet')
    os.system('pip install sqlite3')
    os.system('pip install jinja2')


import game
import chess
import chess.svg

app = Flask(__name__)

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

#@app.route('/partita')
#def chessStart():
	#scacchi_101.__main__()
#	return render_template('chess.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

@app.route('/rules')
def rulePage():
	return render_template('chess_rules.html')

@app.route('/game')
def chessGame():
	board = chess.Board("8/8/8/8/4N3/8/8/8 w - - 0 1")#si può fare creando un nuovo html
	table = chess.svg.board(board)
	return render_template('partita.html')

@app.route('/give_move', methods=['GET', 'POST'])
def WTurn():
	board = chess.Board()
	move=request.form['move'] #prendo la mossa in notazione algebrica
	account=request.form['account'] #prendo il nome dell'account per poter prendere il primo tweet
	sit = game.__main__(board,move,account)#
	if(sit[2] == 'bianco'):
		pass #redirect to white winning page
	elif(sit[2] == 'nero'):
		pass #redirect to black winning page
	elif(sit[2] == 'none'):
		pass #redirect to draw page
	else:
	#scrivere il codice per session storage usa flask-session
	#quando si aggiorna il fen aggiungerlo al testo del tweet
		return redirect('https://twitter.com/intent/tweet?text=#ingsw2022/2023%20La%20mia%20mossa%20in%20notazione%20algebrica:%20' + move + sit[1])
	#aggiungere #ingsw2022/23 o qualcosa del genere al teso del tweet

#@app.route('get_move')
#def BTurn():
	game.__main__()

if __name__=="__main__":
    app.run(debug=True)
