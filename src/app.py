from flask import Flask, render_template, request
import getTweet
import sqlite3

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def homepage():
	"""
	The homepage function is used to render the index.html template and display all tweets from database.
	
	:return: The rendered template 'index'
	"""
	getTweet.__main__()
	if request.method == 'POST':
		keyword = request.form['keyword']		# getting keyword from form
		getTweet.convertDF2SQL('keyword', 20, keyword)
		connection = sqlite3.connect('database.db')		# connecting to database
		connection.row_factory = sqlite3.Row	# read row from database
		tweets = connection.execute('SELECT * FROM tweet').fetchall() 	# getting all tweet form db
		connection.close()	# close connection to database
		return render_template('index.html', tweets=tweets)		# rendering flask template 'index.html'
	getTweet.__main__()		# getTweet and save them into db
	connection = sqlite3.connect('database.db')		# connecting to database
	connection.row_factory = sqlite3.Row	# read row from database
	tweets = connection.execute('SELECT * FROM tweet').fetchall() 	# getting all tweet form db
	connection.close()	# close connection to database
	return render_template('index.html', tweets=tweets)		# rendering flask template 'index.html'

def isLocated():
	if request.method == 'POST':	
		check = request.form.get('check-geolocation')
		if check == 1:		# if is checked
			return True
		return False

if __name__=="__main__":
    app.run(debug=True)