from pythonModules.twitter.TweetSearch import TweetSearch
import os
# *dipendenze necessarie per easyocr*
import cv2
from matplotlib import pyplot as plt
import numpy as np
# *fine dipendenze*
try:
	import easyocr
except ModuleNotFoundError:
	os.system("pip install numpy==1.24.1 -q")
	os.system("pip3 install torch torchvision torchaudio")
	os.system("pip install easyocr -q")
try:	from dateparser import parse
except ModuleNotFoundError:
		os.system("pip install dateparser")

puntata = {'data': '', 'indovina': [], 'vincente': ''}

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
	puntata['indovina']= soluzioni[3:8]
	puntata['vincente'] = (str)(soluzioni[8])
	return puntata

def get_data(data):	
	'''Convert a date string 'data' in the format "dd month year"  to "dd-mm-year"'''
	date_object = parse(data)
	formatted_date = date_object.strftime("%Y-%m-%d")
	return formatted_date

def ereditiers(parola_vincente):
	query = '#ghigliottina OR #leredita OR #eredita'	#NOTA: le lettere accentate twitter le considera come lettere normali
	total = 0
	winner = 0
	TweetSearch.setDatas(query=query, tweetsLimit=99)		
	TweetSearch.researchDecree(researchType='researchByKeyword')
	response = TweetSearch.response
	data_ultima_puntata = get_data(puntata['data'])
	for tweet in response.data:
		if (data_ultima_puntata + ' 18:45') <= str(tweet.created_at)[0:16] <= (data_ultima_puntata + ' 20:00'): 	# controllo che il tweet sia stato pubblicato durante l'orario della puntata
			total+=1
			if parola_vincente.lower() in tweet.text.lower():	# controllo che il tweet contenga la parola vincente: converto tutto in minuscolo per evitare problemi con le maiuscole
				winner+=1
				# print('🏆', tweet.text)
			# else:
				# print('👎', tweet.text)
		# else:
		# 	print('🕒', tweet.text)
	return [winner, total-winner]

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
				print('📸',media[media_keys[0]].url)
				images.append(media[media_keys[0]].url)
	return images
	
def convert_img2text(img):
	"""
	Per convertire e leggere un'immagine usiamo la libreria easyocr. 
	API doc: https://www.jaided.ai/easyocr/documentation/
	"""
	reader = easyocr.Reader(['it'], gpu=False)
	result = reader.readtext(img, detail = 0)	# img può essere anche un URL, usiamo detail = 0 per avere solo il testo identificato
	return result
