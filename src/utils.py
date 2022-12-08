import os
try:
    import datetime
    from datetime import timedelta, datetime
except ModuleNotFoundError:
    os.system('pip install datetime')

# File adibito all'inizializzazione delle strutture dati che andranno a riempure i campi del filtri della GUI
# File creato al fine di avere un app.py piu' pulito e senza codice riguardante il frontend

def initializeDates():
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    time = datetime.utcnow()
    start_time = time - timedelta(days=7)
    end_time = time - timedelta(seconds=15)     # Si sottraggono 15 secondi onde evitare: https://stackoverflow.com/questions/66728533/twitter-api-v2-response-failing-when-params-has-start-time-end-time
    start_time, end_time = start_time.strftime(dtformat), end_time.strftime(dtformat)
    start_time, end_time = start_time[0:len(start_time)-4], end_time[0:len(end_time)-4]
    return {"minDate":start_time, "minDateValue": start_time, "maxDate": end_time, "maxDateValue": end_time}

def initializeResearchMethods():
    researchMethods = [
        {'method':"", 'text':'Research by '},
        {'method':'researchByUser', 'text':'Research by user'},
        {'method':'researchByKeyword','text':'Research by keyword'},
        {'method':'researchByHashtag','text':'Research by hashtag'}
    ]	# A list containing all available search methods
    return researchMethods
