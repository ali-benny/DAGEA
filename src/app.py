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


filterDatas = {'researchMethods': utils.initializeResearchMethods(),
	'currentResearchMethod': '',
	'query': '',
	'tweetsLimit': 10,
	'dates': utils.initializeDates('HTMLFormat'),
	'mapVisibility': 'hidden'
	}

def renderSubmit(request, pageToRender: str):
	whatBtn = request.form['btnradio']
	filterDatas['tweetsLimit'] = request.form['tweetsLimit']
	filterDatas['query'] = request.form['keyword']
	currentResearchMethod = request.form.get('researchBy')
	filterDatas['dates']['minDateValue']=request.form['minDate']
	filterDatas['dates']['maxDateValue']=request.form['maxDate']
	filterDatas['mapVisibility'] = 'hidden'
	if whatBtn == 'Stream':
		stream.StreamByKeyword(filterDatas['query'], (int)(filterDatas['tweetsLimit']))
		tweets = stream.MyStream.tweets
	elif whatBtn == 'Search':
		ts.APIv2.setDatas(query=filterDatas['query'], tweetsLimit=filterDatas['tweetsLimit'], start_time=filterDatas['dates']['minDateValue'], end_time=filterDatas['dates']['maxDateValue'])
		ts.APIv2.researchDecree(researchType = currentResearchMethod)
		tweets = ts.APIv2.createCard()
		if ts.APIv2.hasCardsGeo(tweets):
			filterDatas['mapVisibility'] = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)
	else:
		print('Error: unknown button')
	return render_template(pageToRender, 
		tweetCards=tweets,
		keyword = filterDatas['query'],
		tweetsLimit = filterDatas['tweetsLimit'],
		researchMethods=filterDatas['researchMethods'],
		currentResearchMethod=currentResearchMethod,
		dates=filterDatas['dates'],
		mapVisibility=filterDatas['mapVisibility']
	)

@app.route('/', methods=('GET', 'POST'))
def homepage():
	tweets = []  # list of tweets
	if request.method == 'POST':
		if 'tweetResearchSubmit' in request.form:
			return renderSubmit(request=request, pageToRender='index.html')
	return render_template('index.html', 
		tweetCards=tweets,
		keyword = filterDatas['query'],
		tweetsLimit = filterDatas['tweetsLimit'],
		researchMethods=filterDatas['researchMethods'],
		currentResearchMethod=filterDatas['currentResearchMethod'],
		dates=filterDatas['dates'],
		mapVisibility=filterDatas['mapVisibility']
	)

@app.route('/eredita', methods=('GET', 'POST'))
def eredita():
	"""
	The eredita function is used to display the tweets of '#leredita' research.
	"""
	tweets = []  # list of tweets
	filterDatas['query'] = '#leredita'
	filterDatas['currentResearchMethod'] = 'researchByKeyword'
	if request.method == 'POST':
		return renderSubmit(request=request, pageToRender='eredita.html')
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = filterDatas['query'], tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = filterDatas['currentResearchMethod'])
		tweets = ts.APIv2.createCard()
		if ts.APIv2.hasCardsGeo(tweets):
			filterDatas['mapVisibility'] = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
	return render_template('eredita.html', 
		tweetCards=tweets,
		keyword = filterDatas['query'],
		tweetsLimit = filterDatas['tweetsLimit'],
		researchMethods=filterDatas['researchMethods'],
		currentResearchMethod=filterDatas['currentResearchMethod'],
		dates=filterDatas['dates'],
		mapVisibility=filterDatas['mapVisibility']
	)

@app.route('/reazioneacatena', methods=('GET', 'POST'))
def reazioneacatena():
	"""
	The reazioneacatena function is used to get the tweets from twitter API.
	It returns a list of cards with the tweets and their information.
	"""
	tweets = []  # list of tweets
	filterDatas['query'] = '#reazioneacatena'
	filterDatas['currentResearchMethod'] = 'researchByKeyword'
	filterDatas['mapVisibility'] = 'hidden'
	if request.method == 'POST':
		return renderSubmit(request=request, pageToRender='reazioneacatena.html')
	else:
		# getting tweets from twitter API
		ts.APIv2.setDatas(query = filterDatas['query'], tweetsLimit=10)
		ts.APIv2.researchDecree(researchType = filterDatas['currentResearchMethod'])
		tweets = ts.APIv2.createCard()
		if ts.APIv2.hasCardsGeo(tweets):
			filterDatas['mapVisibility'] = 'visible'
			m.Map.__init__()
			m.Map.addMarkers(tweets)	# Vengono aggiunti i mark per ogni coordinata trovata
	return render_template('reazioneacatena.html', 
		tweetCards=tweets,
		keyword = filterDatas['query'],
		tweetsLimit = filterDatas['tweetsLimit'],
		researchMethods=filterDatas['researchMethods'],
		currentResearchMethod=filterDatas['currentResearchMethod'],
		dates=filterDatas['dates'],
		mapVisibility=filterDatas['mapVisibility']
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
	return render_template('chess.html')

@app.route('/startGame')
def chessGame():
	scacchi_101.__main__()
	# Va in loop perche' non esce mai dalla funzione __main__()
	return render_template('chess.html')

@app.route('/explain', methods=('GET', 'POST'))
def explainPage():
	return render_template('howItWorks.html')

@app.route('/map')
def mapInterface():
	return render_template('mapInterface.html')

@app.route('/credits', methods = ('GET', 'POST'))
def creditsPage():
	return render_template('credits.html')


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
