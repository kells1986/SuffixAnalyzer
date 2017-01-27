from flask import Flask, render_template
from flask import request
from flask import jsonify
import requests
from xml.etree import ElementTree
import urllib
app = Flask(__name__)

'''
Returns parsed XML tree with Wolfram response
'''
def make_wolfram_query(query):

	getVars = {'input': query, 'appid': "V6EEW2-VXJ6VY7GQA"}
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
	the_words = raw_text.split(" | ")
	return the_words

def get_definition_from_tree(tree):
	'''
	This will need to do some database stuff later
	'''
	return get_plaintext_result(tree)

@app.route("/")
def template_test():
    return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolfram_query():
	suffix_text = request.args.get('query')
	word_tree = make_wolfram_query(suffix_text)
	words = get_words_from_tree(word_tree)
	defin = []
	for word in words:
		def_tree = make_wolfram_query("define "+ word)
		defin.append(get_definition_from_tree(def_tree))

	for w,d in zip(words,defin):
		print w, d

	return jsonify(words)

if __name__ == '__main__':
    app.run(debug=True)