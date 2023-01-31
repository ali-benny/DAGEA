import json
from datetime import datetime

def time_chart(response): 
	dataChart = [{'hour': i, 'tweet': 0} for i in range(24)] 	# creo un array di 24 elementi, uno per ogni ora
	# analizzo i tweet e scopro quanti sono in base all'ora
	for tweet in response.data:
		if not isinstance(tweet.created_at, datetime):
			tweet.created_at = datetime.strptime(tweet.created_at, '%Y-%m-%d %H:%M:%S') # converto la data in datetime
		hour = tweet.created_at.strftime("%H")	# in che ora è stato pubblicato il tweet?
		dataChart[int(hour)]['tweet'] += 1
	jsonn = json.dumps(dataChart)
	return jsonn