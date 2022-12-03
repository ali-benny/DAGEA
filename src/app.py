import sqlite3
from flask import Flask, render_template, request

import getTweet
import twitter

app = Flask(__name__)
startTweetLimit = 5
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
	"""
	The homepage function is used to render the index.html template and display all tweets from database.

	:return: The rendered template 'index'
	"""
	currentResearchMethod = ""							# the currently chosen search method
	isLocated = False
	twitter.__init__()
	if request.method == 'POST':
		keyword = request.form['keyword']		# getting keyword from form
		currentResearchMethod = request.form.get('researchBy')
		# getting tweetLimit input, from the <input type="number" name="tweetLimit"> of index.html, in the form of a string
		tweetLimit = request.form['tweetLimit']
		whatBtn = request.form['btnradio']
		print('✨',whatBtn)
		if whatBtn == 'Stream':
			twitter.StreamByKeyword(keyword)
		elif whatBtn == 'Search':
			if request.form.get('isLocated'):	# use form.get because you will get None as default value if the key doesn't exist. ->see https://stackoverflow.com/questions/11285613/check-if-a-form-input-is-checked-in-flask
				isLocated = True
			# getting tweets from twitter API
			getTweet.GetTweet(currentResearchMethod, (int)(tweetLimit), keyword, isLocated)
		else:
			print('Error: unknown button')
		connection = sqlite3.connect('database.db')		# connecting to database
		connection.row_factory = sqlite3.Row  # read row from database
		# getting all tweet form db
		tweets = connection.execute('SELECT * FROM all_tweets').fetchall()
		connection.close()  # close connection to database
		# rendering flask template 'index.html'
		return render_template('index.html',
							   tweets=tweets,
							   tweetLimit=tweetLimit,
							   location=isLocated,
							   researchMethods=researchMethods,
							   currentResearchMethod=currentResearchMethod,
							   )
	# twitter.__init__()		# getTweet and save them into db
	connection = sqlite3.connect('database.db')		# connecting to database
	connection.row_factory = sqlite3.Row  # read row from database
	# getting all tweet form db
	tweets = connection.execute('SELECT * FROM all_tweets').fetchall()
	connection.close()  # close connection to database

	# rendering flask template 'index.html'
	return render_template('index.html',
						   tweets=tweets,
						   location=isLocated,
						   tweetLimit=startTweetLimit,
						   researchMethods=researchMethods,
						   currentResearchMethod=currentResearchMethod,
						   #    markers=markers
						   )

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

if __name__ == "__main__":
	app.run(debug=True)
