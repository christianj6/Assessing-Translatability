from googletrans import Translator

def search(word):
	translator = Translator()
	text = word

	try:
		translation = translator.translate(text, dest='en', src='de').text if translator.translate(text, dest='en', src='de').text != translator.translate(text, dest='en', src='de').origin else False
		return translation
	
	except ValueError:
		print('You have exceeded the maximum number of queries with the GoogleTrans API. Consider activating a VPN. \n\nTranslations have been left empty.')
		empty = False
		return empty

	except ConnectionAbortedError:
		print('Your connection has been interrupted. \n\nTranslations have been left empty.')
		empty = False
		return empty

	