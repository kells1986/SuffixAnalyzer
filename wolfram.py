import requests
from xml.etree import ElementTree
import urllib
from database import *
import appid


class WolframAPI(object):

	def __init__(self, app):
		self.databaseManager = DatabaseManager(app)

	def getDatabaseDefinition(self, word):
		res = self.databaseManager.queryDB('select * from words where word = ?',
                [word], one=True)
		if res != None:
			return res[2]
		else:
			return res

	def setDatabaseDefinition(self, word, definition):
		res = self.databaseManager.insertDB('words', fields=('word','definition'), values=(word,definition))
		return res

	'''
	Returns parsed XML tree with Wolfram response
	'''
	def makeWolframQuery(self, query):

		getVars = {'input': query, 'appid': appid.app_id}
		url_base = 'http://api.wolframalpha.com/v2/query?'
	
		url = url_base + urllib.urlencode(getVars)

		print url
		response = requests.get(url)

		raw_text = None
		tree = ElementTree.fromstring(response.content)
		return tree

	def getPlaintextResult(self,tree):
		plaintext = None
		for pod in tree.findall('.//pod'):
			if pod.attrib['title'] == "Result":
				for pt in pod.findall('.//plaintext'):
					if pt.text:
						plaintext = pt.text
		return plaintext

	def getWordsFromTree(self,tree):
		raw_text = self.getPlaintextResult(tree)
		if raw_text != None:
			the_words = raw_text.split(" | ")
			return the_words
		else:
			return None

	def getDefinitionFromTree(self,tree):
		return self.getPlaintextResult(tree)

	def getDefinition(self,word):
		db_def = self.getDatabaseDefinition(word)
		if db_def == None:
			def_tree = self.makeWolframQuery("define "+ word)
			wf_def = self.getDefinitionFromTree(def_tree)
			if wf_def != None:
				db_def = wf_def
				self.setDatabaseDefinition(word, db_def)
		return db_def

