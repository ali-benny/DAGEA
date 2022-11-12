from flask import Flask, render_template
import helloWorld
app = Flask(__name__)

@app.route('/')
def __main__():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()