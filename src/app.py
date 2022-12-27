import TweetSearch as ts
import os
import stream
import utils
import map as m
try:
	from flask import Flask, render_template, request
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
dates = utils.initializeDates('HTMLFormat')

def method_post(request):	
	"""
	The method_post function is an auxiliar function called when the user clicks on a button.
	It will call the research method of APIv2 and create cards with results.
	
	Parameters
	----------
		request
			Get the data from the form
	
	Returns
	-------
		The html code of the index
	"""
	global renderfilename, is_stream
	tweets = []  # list of tweets
	whatBtn = request.form['btnradio']
	tweetsLimit = request.form['tweetsLimit']
	query = request.form['keyword']
	currentResearchMethod = request.form.get('researchBy')
	dates['minDateValue']=request.form['minDate']
	dates['maxDateValue']=request.form['maxDate']
	map_vis = 'hidden'
	if whatBtn == 'Stream':
		is_stream = True
		# getting stream tweets
		stream.StreamByKeyword(query, (int)(tweetsLimit))
		tweets = stream.MyStream.tweets
	elif whatBtn == 'Search':
		# getting tweets from twitter API
		ts.APIv2.setDatas(query=query, tweetsLimit=tweetsLimit, start_time=dates['minDateValue'], end_time=dates['maxDateValue'])
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
		tweets = ts.APIv2.createCard()
		if request.form.get('isLocated') != None:	# ->see https://stackoverflow.com/questions/20941539/how-to-get-if-checkbox-is-checked-on-flask
			m.Map.__init__()
			m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
			map_vis = 'visible'
	else:
		print('Error: unknown button')
	# rendering flask template 'index.html'
	return render_template(
		renderfilename,
		tweetCards=tweets,
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility = map_vis
	)

@app.route('/', methods=('GET', 'POST'))
def homepage():
	global currentResearchMethod, dates, query, tweetsLimit, start_time, end_time, renderfilename, whatBtn
	if request.method == 'POST':
		renderfilename = 'search.html'
		method_post(request)
	# rendering flask template
	return render_template('home.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates('HTMLFormat'), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/search', methods=('GET', 'POST'))
def search():						# the currently chosen search method
	global currentResearchMethod, dates, query, tweetsLimit, start_time, end_time, renderfilename, is_stream
	is_stream = False
	renderfilename = 'search.html'
	if request.method == 'POST':	
		method_post(request)			# set the current research method
	
	if is_stream:
		# getting stream tweets
		tweets = stream.MyStream.tweets
	else:
		# Reinizizalizzazione col fine di avere di avere un reset dei campi quanto si torna alla home
		ts.APIv2._APIv2__init__response()
		# tweets = ts.APIv2.createCard()
		# m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata

	dates = utils.initializeDates('HTMLFormat')
	return render_template(
		renderfilename,
		# tweetCards=tweets,
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		# mapVisibility = 'hidden'
	)

@app.route('/map')
def mapInterface():
	return render_template('mapInterface.html')

@app.route('/eredita', methods=('GET', 'POST'))
def eredita():
	"""
	The eredita function is used to display the tweets of '#leredita' research.
	"""
	tweets = []  # list of tweets
	query = '#leredita'
	currentResearchMethod = 'researchByKeyword'
	global renderfilename, dates
	renderfilename = 'eredita.html'
	if request.method == 'POST':
		method_post(request)
		query = '' if request.form['keyword'] != '' else query
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = query, tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
	tweets = ts.APIv2.createCard()
	return render_template(renderfilename, 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates)

@app.route('/reazioneacatena', methods=('GET', 'POST'))
def reazioneacatena():
	"""
	The reazioneacatena function is used to get the tweets from twitter API.
	It returns a list of cards with the tweets and their information.
	"""
	tweets = []  # list of tweets
	query = '#reazioneacatena'
	currentResearchMethod = 'researchByKeyword'
	if request.method == 'POST':
		global renderfilename
		renderfilename = 'reazioneacatena.html'
		method_post(request)
		query = '' if request.form['keyword'] != '' else query
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = query, tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
	tweets = ts.APIv2.createCard()
	return render_template('reazioneacatena.html', 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates)

@app.route('/fantacitorio', methods=('GET', 'POST'))
def fantacitorio():
	tweets = []  # list of tweets
	query = '#fantacitorio'
	currentResearchMethod = 'researchByKeyword'
	if request.method == 'POST':
		global renderfilename
		renderfilename = 'fantacitorio.html'
		method_post(request)
		query = '' if request.form['keyword'] != '' else query
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = query, tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
	tweets = ts.APIv2.createCard()
	return render_template('fantacitorio.html', 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates)

@app.route('/chess')
def chessPage():
	return render_template('chess.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates('HTMLFormat'), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/explain', methods=('GET', 'POST'))
def explainPage():
	if request.method == 'POST':
		global renderfilename
		renderfilename = 'howItWorks.html'
		method_post(request)
	return render_template('howItWorks.html', 
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates)

@app.route('/startGame')
def chessGame():
	scacchi_101.__main__()
	# Va in loop perche' non esce mai dalla funzione __main__()
	return render_template('chess.html')

@app.route('/credits', methods = ('GET', 'POST'))
def creditsPage():
	if request.method == 'POST':
		global renderfilename
		renderfilename = 'credits.html'
		method_post(request)
	return render_template('credits.html',
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates)

if __name__ == "__main__":
	app.run(debug=True)
