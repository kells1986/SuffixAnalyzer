from flask import Flask, render_template
from flask import request
from flask import jsonify
from wolfram import *
import appid

app = Flask(__name__)

@app.route("/")
def template():
	return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolframQuery():
	wlf = WolframAPI(app)
	suffix_text = request.args.get('query')
	word_tree = wlf.makeWolframQuery(suffix_text)
	words = wlf.getWordsFromTree(word_tree)
	defin = []
	result = []

	if words != None:
		for word in words[:appid.limit]:
			defin.append(wlf.getDefinition(word))

		for w,d in zip(words[:appid.limit],defin):
			if d == None:
				d = "Could not find definition"
			result.append({"word":w, "definition":d})

	return jsonify(result)


if __name__ == '__main__':
	app.run(debug=True)
