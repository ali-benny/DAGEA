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
from Fantacitorio import FantacitorioAnalysis as FA
from Fantacitorio import FantacitorioTeams as FT

import time

app = Flask(__name__)

ts.APIv2.__init__()
FA.FantacitorioAnalysis.__init__(path='./Fantacitorio/punti.xlsx', numberOfTurns=7)
#m.Map.__init__()

researchMethods = utils.initializeResearchMethods()
renderfilename = 'index.html'
currentResearchMethod = ''
query = ''
tweetsLimit = 10
dates = utils.initializeDates('HTMLFormat')
mapVisibility = 'hidden'

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
	mapVisibility = 'hidden'
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
		if ts.APIv2.hasCardsGeo(tweets):
			mapVisibility = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)
	else:
		print('Error: unknown button')
	if ts.APIv2.hasCardsGeo(tweets):
		mapVisibility = 'visible'
		m.Map.__init__()
		m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
	# rendering flask template 'index.html'
	return render_template(
		renderfilename,
		tweetCards=tweets,
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility = mapVisibility
	)

def renderSubmit(request, pageToRender: str):
	whatBtn = request.form['btnradio']
	tweetsLimit = request.form['tweetsLimit']
	query = request.form['keyword']
	currentResearchMethod = request.form.get('researchBy')
	dates['minDateValue']=request.form['minDate']
	dates['maxDateValue']=request.form['maxDate']
	mapVisibility = 'hidden'
	if whatBtn == 'Stream':
		stream.StreamByKeyword(query, (int)(tweetsLimit))
		tweets = stream.MyStream.tweets
	elif whatBtn == 'Search':
		ts.APIv2.setDatas(query=query, tweetsLimit=tweetsLimit, start_time=dates['minDateValue'], end_time=dates['maxDateValue'])
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
		tweets = ts.APIv2.createCard()
		if ts.APIv2.hasCardsGeo(tweets):
			mapVisibility = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)
	else:
		print('Error: unknown button')
	return render_template(pageToRender, 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility=mapVisibility
	)

@app.route('/', methods=('GET', 'POST'))
def homepage():
	tweets = []  # list of tweets
	query = ''
	currentResearchMethod = ''
	mapVisibility = 'hidden'
	if request.method == 'POST':
		if 'tweetResearchSubmit' in request.form:
			return renderSubmit(request=request, pageToRender='index.html')
	return render_template('index.html', 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility=mapVisibility
	)

@app.route('/eredita', methods=('GET', 'POST'))
def eredita():
	"""
	The eredita function is used to display the tweets of '#leredita' research.
	"""
	tweets = []  # list of tweets
	query = '#leredita'
	currentResearchMethod = 'researchByKeyword'
	mapVisibility = 'hidden'
	global renderfilename, dates
	renderfilename = 'eredita.html'
	if request.method == 'POST':
		return renderSubmit(request=request, pageToRender='eredita.html')
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = query, tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
		tweets = ts.APIv2.createCard()
		if ts.APIv2.hasCardsGeo(tweets):
			mapVisibility = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
	return render_template(renderfilename, 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility=mapVisibility
	)

@app.route('/reazioneacatena', methods=('GET', 'POST'))
def reazioneacatena():
	"""
	The reazioneacatena function is used to get the tweets from twitter API.
	It returns a list of cards with the tweets and their information.
	"""
	tweets = []  # list of tweets
	query = '#reazioneacatena'
	currentResearchMethod = 'researchByKeyword'
	mapVisibility = 'hidden'
	global renderfilename
	renderfilename = 'reazioneacatena.html'
	if request.method == 'POST':
		return renderSubmit(request=request, pageToRender='reazioneacatena.html')
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = query, tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
		tweets = ts.APIv2.createCard()
		if ts.APIv2.hasCardsGeo(tweets):
			mapVisibility = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
	return render_template('reazioneacatena.html', 
		tweetCards=tweets,
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates,
		mapVisibility=mapVisibility
	)

@app.route('/fantacitorio', methods=('GET', 'POST'))
def fantacitorio():
	numberOfGraphs = utils.numberOfFolderFiles('./static/img/fantacitorio/politiciansGroups/')
	utils.deleteFolderFiles(path='./static/img/fantacitorio/userTeam/')
	userTeamResearch = {'username' : '', 'imagePath': './', 'imageVisibility' : 'hidden' }
	if request.method == 'POST':
		if 'searchTeamByUserSubmit' in request.form:
			username = request.form['usernameTextInput']
			userTeamPath = './static/img/fantacitorio/userTeam/'
			imageHasBeenSaved = FT.saveUserTeamImage(user=username, path=userTeamPath)
			userTeamResearch = {'username' : username, 'imagePath': utils.getFolderFilesNames(userTeamPath), 'imageVisibility' : 'visible' if imageHasBeenSaved else 'hidden' }
			return render_template('fantacitorio.html', 
				numberOfTurns=FA.FantacitorioAnalysis.numberOfTurns,
				numberOfGraphs=numberOfGraphs,
				turnsDataTable=FA.FantacitorioAnalysis.turnsInTableFormat,
				fantacitorioStats=FA.FantacitorioAnalysis.getStats(),
				fantacitorioStandings=FA.FantacitorioAnalysis.getStandings(),
				teamsImagesNames=utils.getFolderFilesNames('./static/img/fantacitorio/teams/'),
				userTeamResearch=userTeamResearch
			)
		elif 'politicianScoreUpdateSubmit' in request.form:
			politicianName = request.form['politicianName']
			scoreToAdd = request.form['politicianScoreUpdate']
			for politician in FA.FantacitorioAnalysis.simpleReport:
				if politicianName == politician['name']: 
					politician['totalScore'] += int(scoreToAdd)
					return render_template('fantacitorio.html', 
						numberOfTurns=FA.FantacitorioAnalysis.numberOfTurns,
						numberOfGraphs=numberOfGraphs,
						turnsDataTable=FA.FantacitorioAnalysis.turnsInTableFormat,
						fantacitorioStats=FA.FantacitorioAnalysis.getStats(),
						fantacitorioStandings=FA.FantacitorioAnalysis.getStandings(),
						teamsImagesNames=utils.getFolderFilesNames('./static/img/fantacitorio/teams/'),
						userTeamResearch=userTeamResearch
					)
	return render_template('fantacitorio.html',
		numberOfTurns=FA.FantacitorioAnalysis.numberOfTurns,
		numberOfGraphs=numberOfGraphs,
		turnsDataTable=FA.FantacitorioAnalysis.turnsInTableFormat,
		fantacitorioStats=FA.FantacitorioAnalysis.getStats(),
		fantacitorioStandings=FA.FantacitorioAnalysis.getStandings(),
		teamsImagesNames=utils.getFolderFilesNames('./static/img/fantacitorio/teams/'),
		userTeamResearch=userTeamResearch
	)

@app.route('/chess')
def chessPage():
	return render_template('chess.html', 
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=utils.initializeDates('HTMLFormat'), tweetsLimit=ts.APIv2.tweetsLimit)

@app.route('/startGame')
def chessGame():
	scacchi_101.__main__()
	# Va in loop perche' non esce mai dalla funzione __main__()
	return render_template('chess.html')

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

@app.route('/map')
def mapInterface():
	dates = utils.initializeDates('HTMLFormat')
	return render_template('mapInterface.html',
		tweetCards=[],
		keyword = query,
		tweetsLimit = 10,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dates=dates
	)

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


# zip(), str(), ... are not defined in jinja2 templates so we add them to global jinja2 template via Flask.template_global() function
@app.template_global(name='zip')
def _zip(*args, **kwargs): #to not overwrite builtin zip in globals
	return __builtins__.zip(*args, **kwargs)

@app.template_global(name='str')
def _str(*args, **kwargs): #to not overwrite builtin str in globals
	return __builtins__.str(*args, **kwargs)

@app.template_global(name='type')
def _type(*args, **kwargs): #to not overwrite builtin type in globals
	return __builtins__.type(*args, **kwargs)

@app.template_global(name='len')
def _len(*args, **kwargs): #to not overwrite builtin len in globals
	return __builtins__.len(*args, **kwargs)

@app.template_global(name='enumerate')
def _enumerate(*args, **kwargs): #to not overwrite builtin enumerate in globals
	return __builtins__.enumerate(*args, **kwargs)


if __name__ == "__main__":
	app.run(debug=True)
