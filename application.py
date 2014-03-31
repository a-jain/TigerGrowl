from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

application = Flask(__name__)
application.debug = True

@application.route('/')
@application.route('/home')
def index():
<<<<<<< HEAD
	return render_template('landing.html')
=======
	import _ssl;_ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_SSLv3
	import CASClient

	return redirect('https://fed.princeton.edu/cas/', code=302)
	#C = CASClient.CASClient()
	#netid = C.Authenticate()
>>>>>>> b57bb2702bc9d35fb7cd4bfa1cce76e61d1aaf88

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)


if __name__ == '__main__':
	application.run()