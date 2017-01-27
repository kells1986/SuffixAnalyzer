from flask import Flask, render_template
from flask import request
from flask import jsonify
import requests
from xml.etree import ElementTree
import urllib
import sqlite3
from flask import g

DATABASE = 'db/words.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(table, fields=(), values=()):
    cur = get_db()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    cur.commit()
    


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


@app.route("/")
def template_test():
    return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolfram_query():

	start = 0
	throttle = 5 # don't want to use my usage allowance

	suffix_text = request.args.get('query')
	word_tree = make_wolfram_query(suffix_text)
	words = get_words_from_tree(word_tree)
	defin = []
	result = []

	if words != None:
		for word in words[start:start+throttle]:
			defin.append(get_definition(word))

		for w,d in zip(words[start:start+throttle],defin):
			if d == None:
				d = "Could not find definition"
			result.append({"word":w, "definition":d})

	return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)