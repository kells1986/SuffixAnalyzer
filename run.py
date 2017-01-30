from flask import Flask, render_template, Response
from flask import request
from flask import jsonify
from wolfram import *
import appid
import json

app = Flask(__name__)

@app.route("/")
def template():
	return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolframQuery():
	wlf = WolframAPIClient()
	suffix_text = request.args.get('query')
	words = wlf.getWordsFromSuffix(suffix_text)
	defin = []
	result = []
	def generate(words):
		with app.app_context():
			if words != None:
				for word in words[:appid.limit]:
					d = wlf.getDefinition(word)
					if d == None:
						d = "Could not find definition"
					yield "data:word,"+word+ ",definition,"+d+"\n\n"

	return Response(generate(words), mimetype='text/event-stream')


if __name__ == '__main__':
	app.run(debug=True)
