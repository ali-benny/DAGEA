from flask import Flask, render_template, request
import getTweet
import sqlite3
import jinja2
import os

app = Flask(__name__)
startTweetLimit = 6
researchMethods = [
	{'method':"", 'text':'Research by '},
	{'method':'researchByUser', 'text':'Research by user'},
	{'method':'researchByKeyword','text':'Research by keyword and hashtag'}
]	# A list containing all available search methods

@app.route('/', methods=('GET', 'POST'))
def homepage():
	currentResearchMethod = ""							# the currently chosen search method
	if request.method == 'POST':
		keyword = request.form['keyword']		# getting keyword from form
		tweetLimit = request.form['tweetLimit']	# getting tweetLimit input, from the <input type="number" name="tweetLimit"> of index.html, in the form of a string
		currentResearchMethod = request.form.get('researchBy')
		
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
			currentResearchMethod=currentResearchMethod
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
		currentResearchMethod=currentResearchMethod
	)

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

if __name__=="__main__":
    app.run(debug=True)
