from flask import Flask, render_template
import getTweet 
import sqlite3

app = Flask(__name__)

@app.route('/')
def __main__():
	connection = sqlite3.connect('database.db')
	connection.row_factory = sqlite3.Row
	posts = connection.execute('SELECT * FROM post').fetchall()
	connection.close()
	return render_template('index.html', posts=posts)

if __name__ == '__main__':
	app.run()