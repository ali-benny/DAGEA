import TweetSearch as ts
import os
try:
    from flask import Flask, render_template, request
except ModuleNotFoundError:
    os.system('pip install flask')

researchMethods = [
	{'method':"", 'text':'Research by '},
	{'method':'researchByUser', 'text':'Research by user'},
	{'method':'researchByKeyword','text':'Research by keyword'},
	{'method':'researchByHashtag','text':'Research by hashtag'}
]	# A list containing all available search methods
dataRangeInputs = [
	{'value':"", 'text':'Search from '},
	{'value':'today', 'text':'Search from today'},
	{'value':'oneDayAgo', 'text':'Search from 1 day ago'},
	{'value':'twoDaysAgo', 'text':'Search from 2 days ago'},
	{'value':'threeDaysAgo', 'text':'Search from 3 days ago'},
	{'value':'fourDaysAgo', 'text':'Search from 4 days ago'},
	{'value':'fiveDaysAgo', 'text':'Search from 5 days ago'},
	{'value':'sixDaysAgo', 'text':'Search from 6 days ago'},
	{'value':'sevenDaysAgo', 'text':'Search from 7 days ago'},
]

app = Flask(__name__)

ts.APIv2.__init__()

@app.route('/', methods=('GET', 'POST'))
def homepage():
	currentResearchMethod = ""							# the currently chosen search method
	if request.method == 'POST':
		#startDateRange = request.form.get('startDateRange')
		#endDateRange = request.form.get('endDateRange')
		ts.APIv2.setDatas(query=request.form['keyword'], tweetsLimit=request.form['tweetsLimit'], expansions=['author_id'])
		currentResearchMethod = request.form.get('researchBy')
		ts.APIv2.researchDecree(researchType=currentResearchMethod)

		return render_template(
			'index.html',
			tweetsText=ts.APIv2.getDataFrames(responseField=1, field='text'),
			tweetsLimit=ts.APIv2.tweetsLimit,
			researchMethods=researchMethods,
			currentResearchMethod=currentResearchMethod,
			dataRangeInputs=dataRangeInputs,
		)	# rendering flask template 'index.html'
	return render_template(
		'index.html',
		tweetsText=ts.APIv2.getDataFrames(responseField=1, field='text'),
		tweetsLimit=ts.APIv2.tweetsLimit,
		researchMethods=researchMethods,
		currentResearchMethod=currentResearchMethod,
		dataRangeInputs=dataRangeInputs,
	)

@app.route('/explain')
def explainPage():
	return render_template('howItWorks.html')

@app.route('/credits')
def creditsPage():
	return render_template('credits.html')

if __name__=="__main__":
    app.run(debug=True)
