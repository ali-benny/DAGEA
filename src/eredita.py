from pythonModules.twitter import TweetSearch
try:
	import easyocr
except ModuleNotFoundError:
	import os
	os.system("pip install easyocr")

def ghigliottina():
	parola_vincente = ['']	# parole vincenti della settimana: array di 8 parole
	images = get_tweet_soluzioni()	# cerco tutti i tweet con le soluzioni della settimana

	for img in images:
		soluzioni = convert_img2text(img)	# converto l'immagine in testo e lo salvo

def get_tweet_soluzioni():
	images = []		# array di immagini con le soluzioni della settimana
	query = 'from:quizzettone "parola vincente" #ereditiers #ghigliottina'
	TweetSearch.setDatas(query=query, expansions=["attachments.media_keys","author_id","geo.place_id"], tweet_fields=["created_at", "attachments"], media_fields=["url"])	
	TweetSearch.researchDecree(researchType='researchByKeyword')
	response = TweetSearch.APIv2.response
	for tweet in response:
		if 'media' in tweet.entities:
			for media in tweet.extended_entities['media']:
				images.append(media['media_url'])
		else:
			print('ERROR: no media in tweet')
	return images
	
def convert_img2text(img):
	"""
	Per convertire e leggere un'immagine usiamo la libreria easyocr. 
	API doc: https://www.jaided.ai/easyocr/documentation/

	Le immagini che vorremo analizzare sono quelle postate da @quizzettone su twitter
	nei tweet con prima parola Amici e hashtag #ghigliottina
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
	Gli indici delle parole sono quelli a cui si riferiscono nell'array ricavato da easyocr
	"""
	reader = easyocr.Reader(['it'])
	result = reader.readtext(img, detail = 0)	# img può essere anche un URL, usiamo detail = 0 per avere solo il testo identificato
	return result
