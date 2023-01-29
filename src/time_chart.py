import json

def time_chart(response): 
	dataChart = [{'hour': i, 'tweet': 0} for i in range(24)] 	# creo un array di 24 elementi, uno per ogni ora
	# analizzo i tweet e scopro quanti sono in base all'ora
	for tweet in response.data:
		hour = tweet.created_at.strftime("%H")	# in che ora è stato pubblicato il tweet?
		dataChart[int(hour)]['tweet'] += 1
	jsonn = json.dumps(dataChart)
	print('🟨', jsonn)
	return jsonn