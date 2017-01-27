from flask import Flask, render_template
from flask import request
from flask import jsonify
import requests
from xml.etree import ElementTree
import urllib
app = Flask(__name__)


@app.route("/")
def template_test():
    return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolfram_query():
	text = request.args.get('query')
	
	getVars = {'input': text, 'appid': "V6EEW2-VXJ6VY7GQA"}
	url_base = 'http://api.wolframalpha.com/v2/query?'
	
	url = url_base + urllib.urlencode(getVars)

	print url
	response = requests.get(url)
	
	tree = ElementTree.fromstring(response.content)
	for pod in tree.findall('.//pod'):
		print(pod.attrib['title'])
		for pt in pod.findall('.//plaintext'):
			if pt.text:
				print('-', pt.text)



	some_data = text.split(" ")
	return jsonify(some_data)

if __name__ == '__main__':
    app.run(debug=True)