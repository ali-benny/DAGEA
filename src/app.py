import TweetSearch as ts
import os
import getTweet
import twitter
import utils
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
renderfilename = 'search.html'
currentResearchMethod = ''
query = ''
tweetsLimit = 10
start_time = ''
end_time = ''
dates = utils.initializeDates()


@app.route('/', methods=('GET', 'POST'))
def home():	
	global currentResearchMethod, dates, query, tweetsLimit, start_time, end_time
	dates = utils.initializeDates()
	if request.method == 'POST':
		currentResearchMethod = request.form.get('researchBy')
		dates['minDateValue']=request.form['minDate']
		dates['maxDateValue']=request.form['maxDate']
		query=request.form['keyword']
		tweetsLimit=request.form['tweetsLimit']
		start_time=dates['minDateValue']
		end_time=dates['maxDateValue']
	return render_template('home.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates(), tweetsLimit=ts.APIv2.tweetsLimit)	

@app.route('/search', methods=('GET', 'POST'))
def search():						# the currently chosen search method
	global currentResearchMethod, dates, query, tweetsLimit, start_time, end_time
	if request.method == 'POST':		
		whatBtn = request.form['btnradio']
		if whatBtn == 'Stream':
			# stream 
			twitter.StreamByKeyword(request.form['keyword'])
		elif whatBtn == 'Search':			
			# getting tweets from twitter API
			if query == '':
				currentResearchMethod = request.form.get('researchBy')
				dates['minDateValue']=request.form['minDate']
				dates['maxDateValue']=request.form['maxDate']
				query=request.form['keyword']
				tweetsLimit=request.form['tweetsLimit']
				start_time=dates['minDateValue']
				end_time=dates['maxDateValue']
			ts.APIv2.setDatas(query=query, tweetsLimit=tweetsLimit, start_time=dates['minDateValue'], end_time=dates['maxDateValue'])
			ts.APIv2.researchDecree(researchType=currentResearchMethod)
		else:
			print('Error: unknown button')
		
		return render_template(
			renderfilename,
			tweetCards=ts.APIv2.createCard(),
			tweetsLimit=ts.APIv2.tweetsLimit,
			researchMethods=researchMethods,
			currentResearchMethod=currentResearchMethod,
			dates=dates
		)	# rendering flask template 'index.html'

	# twitter.__init__()		# getTweet and save them into db
	connection = sqlite3.connect('database.db')		# connecting to database
	connection.row_factory = sqlite3.Row  # read row from database
	# getting all tweet form db
	tweets = connection.execute('SELECT * FROM all_tweets').fetchall()
	connection.close()  # close connection to database

	# Reinizizalizzazione col fine di avere di avere un reset dei campi quanto si torna alla home
	ts.APIv2._APIv2__init__response()
	dates = utils.initializeDates()
	return render_template(
		renderfilename,
		tweetCards=ts.APIv2.createCard(),
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates
	)	# rendering flask template 'index.html'

@app.route('/eredita', methods=('GET', 'POST'))
def eredita():
	tweets = []  # list of tweets
	dates['minDateValue']=request.form['minDate']
	dates['maxDateValue']=request.form['maxDate']
	tweetsLimit = request.form['tweetsLimit']
	query = request.form['keyword']

	# getting tweets from twitter API
	currentResearchMethod = request.form.get('researchBy')
	ts.APIv2.setDatas(query=query, tweetsLimit=tweetsLimit, start_time=dates['minDateValue'], end_time=dates['maxDateValue'])
	ts.APIv2.researchDecree(researchType = currentResearchMethod)
	tweets = ts.APIv2.createCard()

	return render_template('eredita.html', 
		tweetCards=tweets,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates(), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/reazioneacatena')
def reazioneacatena():
	return render_template('reazioneacatena.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates(), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/fantacitorio')
def fantacitorio():
	return render_template('fantacitorio.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates(), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/chess')
def chessPage():
	return render_template('chess.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates(), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

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
