import TweetSearch as ts
import os
import stream
import getTweet
import twitter
import utils
import map as m
try:
	from flask import Flask, render_template, request
	import sqlite3
except ModuleNotFoundError:
	os.system('pip install flask')

from scacchi import scacchi_101
from scacchi import scacchi_engine

app = Flask(__name__)

ts.APIv2.__init__()
researchMethods = utils.initializeResearchMethods()

@app.route('/', methods=('GET', 'POST'))
def homepage():
	currentResearchMethod = ""							# the currently chosen search method
	is_stream = False
	dates = utils.initializeDates('HTMLFormat')
	m.Map.__init__()
	if request.method == 'POST':
		tweets = []  # list of tweets
		dates['minDateValue']=request.form['minDate']
		dates['maxDateValue']=request.form['maxDate']
				
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
			currentResearchMethod = request.form.get('researchBy')
			ts.APIv2.setDatas(query=query, tweetsLimit=tweetsLimit, start_time=dates['minDateValue'], end_time=dates['maxDateValue'])
			ts.APIv2.researchDecree(researchType = currentResearchMethod)
			tweets = ts.APIv2.createCard()
			m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
		else:
			print('Error: unknown button')
		# rendering flask template 'index.html'
		return render_template(
			'index.html',
			tweetCards=tweets,
			tweetsLimit=ts.APIv2.tweetsLimit,
			researchMethods=researchMethods,
			currentResearchMethod=currentResearchMethod,
			dates=dates,
			mapVisibility = 'visible'
		)
	if is_stream:
		tweets = stream.MyStream.tweets
	else:
		# Reinizizalizzazione col fine di avere di avere un reset dei campi quanto si torna alla home
		ts.APIv2._APIv2__init__response()
		tweets = ts.APIv2.createCard()

	# rendering flask template 'index.html'
	return render_template(
		'index.html',
		tweetCards=tweets,
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility = 'hidden'
	)

@app.route('/map')
def mapInterface():
	return render_template('mapInterface.html')

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

@app.route('/chess')
def chessPage():
	return render_template('chess.html')

@app.route('/startGame')
def chessGame():
	scacchi_101.__main__()
	# Va in loop perche' non esce mai dalla funzione __main__()
	return render_template('chess.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

if __name__ == "__main__":
	app.run(debug=True)
