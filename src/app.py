import TweetSearch as ts
import os
import getTweet
import twitter
try:
	from flask import Flask, render_template, request
	import sqlite3
except ModuleNotFoundError:
    os.system('pip install flask')

researchMethods = [
	{'method':"", 'text':'Research by '},
	{'method':'researchByUser', 'text':'Research by user'},
	{'method':'researchByKeyword','text':'Research by keyword'},
	{'method':'researchByHashtag','text':'Research by hashtag'}
]	# A list containing all available search methods
dataRangeInputs = [
	{'value':"", 'text':'Search from '},
	{'value':'today', 'text':'Search from today'},
	{'value':'oneDayAgo', 'text':'Search from 1 day ago'},
	{'value':'twoDaysAgo', 'text':'Search from 2 days ago'},
	{'value':'threeDaysAgo', 'text':'Search from 3 days ago'},
	{'value':'fourDaysAgo', 'text':'Search from 4 days ago'},
	{'value':'fiveDaysAgo', 'text':'Search from 5 days ago'},
	{'value':'sixDaysAgo', 'text':'Search from 6 days ago'},
	{'value':'sevenDaysAgo', 'text':'Search from 7 days ago'},
]

app = Flask(__name__)

ts.APIv2.__init__()

@app.route('/', methods=('GET', 'POST'))
def homepage():
	currentResearchMethod = ""							# the currently chosen search method
	currentRange = ""							# the currently chosen search method
	if request.method == 'POST':
		
		ts.APIv2.setDatas(query=request.form['keyword'], tweetsLimit=request.form['tweetsLimit'])
		currentResearchMethod = request.form.get('researchBy')
		ts.APIv2.researchDecree(researchType=currentResearchMethod)
		'''
		whatBtn = request.form['btnradio']
		if whatBtn == 'Stream':
			twitter.StreamByKeyword(ts.APIv2.query)
		elif whatBtn == 'Search':
			if request.form.get('isLocated'):	# use form.get because you will get None as default value if the key doesn't exist. ->see https://stackoverflow.com/questions/11285613/check-if-a-form-input-is-checked-in-flask
				isLocated = True
			# getting tweets from twitter API
			getTweet.GetTweet(currentResearchMethod, (int)(ts.APIv2.tweetsLimit), ts.APIv2.query, isLocated)
		else:
			print('Error: unknown button')
			'''
		connection = sqlite3.connect('database.db')		# connecting to database
		connection.row_factory = sqlite3.Row  # read row from database
		# getting all tweet form db
		tweets = connection.execute('SELECT * FROM all_tweets').fetchall()
		connection.close()  # close connection to database
		# rendering flask template 'index.html'
		
		return render_template(
			'index.html',
			tweetCards=ts.APIv2.createCard(),
			tweetsLimit=ts.APIv2.tweetsLimit,
			researchMethods=researchMethods,
			currentResearchMethod=currentResearchMethod,
			dataRangeInputs=dataRangeInputs,
		)	# rendering flask template 'index.html'

	# twitter.__init__()		# getTweet and save them into db
	connection = sqlite3.connect('database.db')		# connecting to database
	connection.row_factory = sqlite3.Row  # read row from database
	# getting all tweet form db
	tweets = connection.execute('SELECT * FROM all_tweets').fetchall()
	connection.close()  # close connection to database

	ts.APIv2._APIv2__init__response()
	return render_template(
		'index.html',
		tweetCards=ts.APIv2.createCard(),
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dataRangeInputs=dataRangeInputs,
	)	# rendering flask template 'index.html'

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

@app.route('/chess')
def chessPage():
	return render_template('chess.html')

@app.route('/startGame')
def chessGame():
	print('PRIMA: scacchi_101.__main__()')
	scacchi_101.__main__()
	# Va in loop perche' non esce mai dalla funzione __main__()
	return render_template('chess.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

if __name__ == "__main__":
	app.run(debug=True)
