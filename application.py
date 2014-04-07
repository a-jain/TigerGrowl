from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flaskext.mysql import MySQL
import MySQLdb

mysql = MySQL()
application = Flask(__name__)
application.debug = True


db = MySQLdb.connect(host="aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com",user="growladmin",passwd="youeatyet?",db="ebdb")
#application.config['MYSQL_DATABASE_USER'] = 'growladmin'
#application.config['MYSQL_DATABASE_PASSWORD'] = 'youeatyet?' # DO NOT LEAVE PASSWORDS IN CODE
#application.config['MYSQL_DATABASE_DB'] = 'ebdb'
#application.config['MYSQL_DATABASE_HOST'] = 'aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com'
#mysql.init_app(application)
#db = mysql.connect()
db.autocommit(True)

cursor = db.cursor()
#cursor.execute("SELECT * from ebdb.user_table where firstname='Kevin'")
#result = db.store_result()

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
	sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid) VALUES (6969, 'Roberto', 'Flamenco', 'qqkk');"
	cursor.execute(sql)
	# db.commit()
	cursor.execute("SELECT * FROM ebdb.user_table;")
	print cursor.fetchall()

	db.close()
	return render_template('hello.html', name="Success")

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=data[2])


if __name__ == '__main__':
	application.run(debug=True)