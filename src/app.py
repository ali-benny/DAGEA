import TweetSearch as ts
import os
import stream

try:
	from flask import Flask, render_template, request
	import sqlite3
except ModuleNotFoundError:
    os.system('pip install flask')

from scacchi import scacchi_101
from scacchi import scacchi_engine

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
	is_stream = False
	if request.method == 'POST':
		tweets = []  # list of tweets
		whatBtn = request.form['btnradio']
		tweetsLimit = request.form['tweetsLimit']
		query = request.form['keyword']
		if whatBtn == 'Stream':
			is_stream = True
			# getting stream tweets
			stream.StreamByKeyword(query, (int)(tweetsLimit))
			tweets = stream.MyStream.tweets
		elif whatBtn == 'Search':
			# getting tweets from twitter API
			ts.APIv2.setDatas(query, tweetsLimit = tweetsLimit)
			currentResearchMethod = request.form.get('researchBy')
			ts.APIv2.researchDecree(researchType = currentResearchMethod)
			tweets = ts.APIv2.createCard()
		else:
			print('Error: unknown button')
		# rendering flask template 'index.html'
		return render_template(
			'index.html',
			tweetCards=tweets,
			tweetsLimit=ts.APIv2.tweetsLimit,
			researchMethods=researchMethods,
			currentResearchMethod=currentResearchMethod,
			dataRangeInputs=dataRangeInputs,
		)
	if is_stream:
		tweets = stream.MyStream.tweets
	else:
		ts.APIv2._APIv2__init__response()
		tweets = ts.APIv2.createCard()

	# rendering flask template 'index.html'
	return render_template(
		'index.html',
		tweetCards=tweets,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dataRangeInputs=dataRangeInputs,
	)	

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
