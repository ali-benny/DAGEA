from flask import Flask, render_template
import getTweet 
import sqlite3
import jinja2
import os

app = Flask(__name__)

@app.route('/')
def homepage():
	getTweet.__main__()		# getTweet and save them into db
	connection = sqlite3.connect('database.db')		# connecting to database
	connection.row_factory = sqlite3.Row	# read row from database
	tweets = connection.execute('SELECT * FROM tweet').fetchall() 	# getting all tweet form db
	connection.close()	# close connection to database
	return render_template('index.html', tweets=tweets)		# rendering flask template 'index.html'

if __name__=="__main__":
    app.run(debug=True)