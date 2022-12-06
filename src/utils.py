import datetime
from datetime import timedelta

# File adibito all'inizializzazione delle strutture dati che andranno a riempure i campi del filtri della GUI
# File creato al fine di avere un app.py piu' pulito e senza codice riguardante il frontend

def initializeDates():
    currentDate = datetime.datetime.now()
    tmp = str(currentDate)
    maxDate = tmp[0:10] + 'T' + tmp[11:16]
    tmp = str(currentDate - timedelta(days=7))
    minDate = tmp[0:10] + 'T' + tmp[11:16]
    return {"minDate":minDate, "minDateValue": minDate, "maxDate": maxDate, "maxDateValue": maxDate}		# Returns a dictionary

def initializeResearchMethods():
	researchMethods = [
		{'method':"", 'text':'Research by '},
		{'method':'researchByUser', 'text':'Research by user'},
		{'method':'researchByKeyword','text':'Research by keyword'},
		{'method':'researchByHashtag','text':'Research by hashtag'}
	]	# A list containing all available search methods
	return researchMethods
