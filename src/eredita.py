import os
try:
	from pythonModules.twitter.TweetSearch import TweetSearch
except (ModuleNotFoundError, ImportError):
	from .pythonModules.twitter.TweetSearch import TweetSearch

try:
	import easyocr
except ModuleNotFoundError:
	os.system("pip install numpy==1.24.1 -q")
	os.system("pip3 install torch torchvision torchaudio")
	os.system("pip install easyocr -q")
try:	from dateparser import parse
except ModuleNotFoundError:
		os.system("pip install dateparser")
# *dipendenze necessarie per easyocr*
import cv2
from matplotlib import pyplot as plt
import numpy as np
# *fine dipendenze*
from datetime import date, datetime
from datetime import timedelta

puntata = {'data': '', 'indovina': [], 'vincente': ''}
tweet_an = 0
def ghigliottina():
	"""
	* Caratteristiche immagini *
	formato: height = 510px
	struttura del testo:
		0. L'Eredità
		1. data [dd mese yyyy]
		2. #ghigliottina
		3. parola 1
		4. parola 2	
		5. parola 3
		6. parola 4
		7. parola 5
		8. parola finale da indovinare
	Gli indici delle parole sono quelli nell'array soluzioni
	"""
	global puntata
	images = get_tweet_soluzioni()	# cerco tutti i tweet con le soluzioni della settimana
	# for img in images:
	soluzioni = convert_img2text(images[0])	# converto l'immagine in testo e lo salvo
	puntata['data'] = soluzioni[1]
	puntata['indovina'] = soluzioni[3:8]
	puntata['vincente'] = (str)(soluzioni[8])
	return puntata

def get_data(data):	
	'''Convert a date string 'data' in the format "dd month year" to "dd-mm-year"'''
	date_object = parse(data)
	if date_object is None:
		return date.today().strftime("%Y-%m-%d")
	return date_object.strftime("%Y-%m-%d") 

def ereditiers(parola_vincente):
	query = '#ghigliottina OR #leredita OR #eredita'	#NOTA: le lettere accentate twitter le considera come lettere normali
	total = 0
	winner = 0
	global tweet_an		# numero di tweet analizzati
	global puntata
	tweet_an = 0
	end_time = None
	data_ultima_puntata = get_data(puntata['data'])
	if datetime.strptime(data_ultima_puntata, "%Y-%m-%d") >= date.today() - timedelta(days = 1):	# se la puntata non è stata trasmessa ieri
		end_time = "{}T20:10".format(data_ultima_puntata)	# cerco fino alle 20:10 del giorno della puntata
	TweetSearch.setDatas(query=query, tweepyCursor=True, end_time=end_time)		
	TweetSearch.researchDecree(researchType='researchByKeyword')
	paginator = TweetSearch.response
	if paginator is not None:
		for response in paginator:
			for tweet in response.data:
				tweet_an += 1
				if (data_ultima_puntata + ' 18:45') <= tweet.created_at.strftime("%Y-%m-%d %H:%M") <= (data_ultima_puntata + ' 20:00'): 	# controllo che il tweet sia stato pubblicato durante l'orario della puntata
					total+=1
					if parola_vincente.lower() in tweet.text.lower():	# controllo che il tweet contenga la parola vincente: converto tutto in minuscolo per evitare problemi con le maiuscole
						winner+=1
	return [winner, total-winner]

def total():
	global tweet_an
	return tweet_an

def get_tweet_soluzioni():
	images = []		# array di immagini con le soluzioni della settimana
	query = 'from:quizzettone "parola vincente" #ereditiers #ghigliottina'
	TweetSearch.setDatas(query=query, expansions=["attachments.media_keys","author_id","geo.place_id"], tweet_fields=["created_at", "attachments"], media_fields=["url"])		
	TweetSearch.researchDecree(researchType='researchByKeyword')
	response = TweetSearch.response
	media = {m["media_key"]: m for m in response.includes['media']}	# media contiene le immagini dei tweet
	for tweet in response.data:
		attachments = tweet.data['attachments']
		media_keys = attachments['media_keys']
		if media[media_keys[0]].url:
				# print('📸',media[media_keys[0]].url)		#DEBUG stampa l'url dell'immagine
				try:
					images.append(media[media_keys[0]].url)
				except EasyOCRError as e:
						print('🚫', e.message)
	return images
	
def convert_img2text(img):
	"""
	Per convertire e leggere un'immagine usiamo la libreria easyocr. 
	API doc: https://www.jaided.ai/easyocr/documentation/
	"""
	reader = easyocr.Reader(['it'], gpu=False)
	result = reader.readtext(img, detail = 0)	# img può essere anche un URL, usiamo detail = 0 per avere solo il testo identificato
	return result


"""
* Errori EasyOCR *
"Error 1": indica che non è stato specificato un modello OCR.
"Error 2": indica che il modello OCR specificato non esiste.
"Error 3": indica che l'immagine fornita non è valida o non è stata trovata.
"Error 4": indica che c'è un problema di connessione con il server di riconoscimento OCR.
"Error 5": indica un errore interno del server di riconoscimento OCR.
"Error 6": indica un errore di licenza.
"""