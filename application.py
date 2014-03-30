from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/home')
def index():
	return render_template('CAS/index.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)


if __name__ == '__main__':
	app.run(host='0.0.0.0')