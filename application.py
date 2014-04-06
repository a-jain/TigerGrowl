from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flaskext.mysql import MySQL

application = Flask(__name__)
application.debug = True
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'trfoSVTV'
application.config['MYSQL_DATABASE_DB']

@application.route('/')
@application.route('/home')
def index():
	return render_template('landing.html')

@application.route('/feed')
def feed():
	return render_template('fbids.html')

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)


if __name__ == '__main__':
	application.run()