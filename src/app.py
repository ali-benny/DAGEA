from flask import Flask, render_template
import getTweet 
import sqlite3
import jinja2

app = Flask(__name__)

@app.route('/')
def homepage():
	connection = sqlite3.connect('database.db')
	connection.row_factory = sqlite3.Row
	tweets = connection.execute('SELECT * FROM tweet').fetchall()
	connection.close()
	return render_template('index.html', tweets=tweets)

if __name__=="__main__":
    app.run(debug=True)