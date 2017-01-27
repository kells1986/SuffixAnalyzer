from flask import Flask, render_template
from flask import request
from flask import jsonify
app = Flask(__name__)


@app.route("/")
def template_test():
    return render_template('template.html')

@app.route('/wolfram-query', methods=['POST'])
def wolfram_query():
	text = request.form['query']
	print text
	return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=True)