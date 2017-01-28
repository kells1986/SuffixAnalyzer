from flask import Flask, render_template
from flask import request
from flask import jsonify
from database import *
from wolfram import *
import appid

app = Flask(__name__)

@app.route("/")
def template():
	return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolfram_query():
	suffix_text = request.args.get('query')
	word_tree = make_wolfram_query(suffix_text)
	words = get_words_from_tree(word_tree)
	defin = []
	result = []

	if words != None:
		for word in words[:appid.limit]:
			defin.append(get_definition(word))

		for w,d in zip(words[:appid.limit],defin):
			if d == None:
				d = "Could not find definition"
			result.append({"word":w, "definition":d})

	return jsonify(result)

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

if __name__ == '__main__':
	app.run(debug=True)
