from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import MySQLdb

application = Flask(__name__)
application.debug = True

db = MySQLdb.connect(host="aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com",user="growladmin",passwd="youeatyet?",db="ebdb")
db.autocommit(True)

cursor = db.cursor()

@application.route('/')
@application.route('/home')
def index():
	return render_template('landing.html')

@application.route('/feed')
def feed():
	return render_template('fbids.html')

@application.route('/feedPrototype')
def feedPrototype():
	return render_template('feed.html')

@application.route('/insertDB')
@application.route('/insertDB/<id>/<firstname>/<surname>/<netid>')
def dbinsert(id=None, firstname=None, surname=None, netid=None):
	sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid) VALUES (697769, 'Roberto', 'Flamenco', 'qqkk');"
	cursor.execute(sql)
	cursor.execute("SELECT * FROM ebdb.user_table;")
	# db.close()
	return render_template('hello.html', name="Success")

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=data[2])

if __name__ == '__main__':
	application.run(debug=True)