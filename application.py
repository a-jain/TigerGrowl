from flask import Flask
from flask import render_template
from flask import request

application = Flask(__name__)
application.debug = True

@application.route('/')
@application.route('/home')
def index():
	return render_template('landing.html')

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)


if __name__ == '__main__':
	application.run()