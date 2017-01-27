from flask import Flask, render_template
from flask import request
from flask import jsonify
app = Flask(__name__)


@app.route("/")
def template_test():
    return render_template('template.html')

@app.route('/wolfram-query', methods=['GET'])
def wolfram_query():
	text = request.args.get('query')
	some_data = text.split(" ")
	return jsonify(some_data)

if __name__ == '__main__':
    app.run(debug=True)