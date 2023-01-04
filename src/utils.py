import os
try:
    import datetime
    from datetime import timedelta, datetime
except ModuleNotFoundError:
    os.system('pip install datetime')

# File adibito all'inizializzazione delle strutture dati che andranno a riempure i campi del filtri della GUI
# File creato al fine di avere un app.py piu' pulito e senza codice riguardante il frontend

def getFolderFilesNames(path: str) -> list | str:
    filesNames = []
    for file in os.scandir(path):
        if file.name != '.gitkeep':
            filesNames.append(path + file.name)
    if len(filesNames) == 1:
        return filesNames[0]
    else:
        return filesNames

def deleteFolderFiles(path: str) -> None:
    for file in os.scandir(path):
        if file.name != ".gitkeep":
            os.remove(file)

def numberOfFolderFiles(path: str) -> int:
    fileCounter = 0
    for file in os.scandir(path):
        fileCounter += 1
    return fileCounter

def initializeDates(returnCase: str):
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    time = datetime.utcnow()
    start_time = time - timedelta(days=7)
    end_time = time - timedelta(seconds=15)     # Si sottraggono 15 secondi onde evitare: https://stackoverflow.com/questions/66728533/twitter-api-v2-response-failing-when-params-has-start-time-end-time
    start_time, end_time = start_time.strftime(dtformat), end_time.strftime(dtformat)
    match returnCase:
        case 'HTMLFormat':
            start_time, end_time = start_time[0:len(start_time)-4], end_time[0:len(end_time)-4]
            return {"minDate":start_time, "minDateValue": start_time, "maxDate": end_time, "maxDateValue": end_time}
        case 'APIFormat':
            return {"start_time":start_time[0:17] + '00Z', "end_time": end_time[0:17] + '00Z'}
        case _:
            #TODO
            pass

def updateTime(obsoleteStartTime):
    try:
        # Quando si usa l'API v2 di twitter, twitter in automatico determina qual e' il valore limite del parametro start_time (ovvero: momento x in cui l'API v2 viene invocata - 7 giorni),
        # e, onde evitare errori di valori di start_time non validi, lo si aggiorna (qualora fosse necessario) prima di chiamare la API v2
        dtformat = '%Y-%m-%dT%H:%M:%SZ'
        validStartDate = (datetime.utcnow() - timedelta(days=7)).strftime(dtformat)
        if obsoleteStartTime < validStartDate:
            return validStartDate
        else:
            return obsoleteStartTime
    except TypeError:
        pass

def initializeResearchMethods():
    researchMethods = [
        {'method':"", 'text':'Research by '},
        {'method':'researchByUser', 'text':'Research by user'},
        {'method':'researchByKeyword','text':'Research by keyword'},
        {'method':'researchByHashtag','text':'Research by hashtag'}
    ]	# A list containing all available search methods
    return researchMethods
