from flask import Flask
from flask import render_template
from flask import request

application = Flask(__name__)
application.debug = True

@application.route('/')
@application.route('/home')
def index():
	import _ssl;_ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_SSLv3
	import CASClient

	return CASClient.CASClient()
	#C = CASClient.CASClient()
	#netid = C.Authenticate()

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)


if __name__ == '__main__':
	application.run()