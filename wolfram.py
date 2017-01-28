import requests
from xml.etree import ElementTree
import urllib
from database import *
import appid


def get_def_db(word):
	res = query_db('select * from words where word = ?',
                [word], one=True)
	if res != None:
		return res[2]
	else:
		return res

def set_def_db(word, definition):
	res = insert_db('words', fields=('word','definition'), values=(word,definition))
	return res

'''
Returns parsed XML tree with Wolfram response
'''
def make_wolfram_query(query):

	getVars = {'input': query, 'appid': appid.app_id}
	url_base = 'http://api.wolframalpha.com/v2/query?'
	
	url = url_base + urllib.urlencode(getVars)

	print url
	response = requests.get(url)

	raw_text = None
	tree = ElementTree.fromstring(response.content)
	return tree

def get_plaintext_result(tree):
	plaintext = None
	for pod in tree.findall('.//pod'):
		print pod.attrib['title']
		if pod.attrib['title'] == "Result":
			for pt in pod.findall('.//plaintext'):
				if pt.text:
					plaintext = pt.text
	return plaintext

def get_words_from_tree(tree):
	raw_text = get_plaintext_result(tree)
	if raw_text != None:
		the_words = raw_text.split(" | ")
		return the_words
	else:
		return None

def get_definition_from_tree(tree):
	'''
	This will need to do some database stuff later
	'''
	return get_plaintext_result(tree)

def get_definition(word):
	db_def = get_def_db(word)
	if db_def == None:
		def_tree = make_wolfram_query("define "+ word)
		wf_def = get_definition_from_tree(def_tree)
		if wf_def != None:
			db_def = wf_def
			set_def_db(word, db_def)
	return db_def