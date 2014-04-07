from flask import Flask
from flask import render_template, flash
from flask import request
from flask import redirect
import MySQLdb
from form import *

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
	sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid) VALUES (6977769, 'Roberto', 'Flamenco', 'qqkk');"
	cursor.execute(sql)
	cursor.execute("SELECT * FROM ebdb.user_table;")
	# db.close()
	return render_template('hello.html', name="Success")

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name="kevinisgay")

@application.route('/registermeal', methods=['GET', 'POST'])
def registermeal():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		# user = User(form.mealtable.data, form.host.data, form.place.data)
		
		print form.mealtable.data
		print form.host.data
		print form.place.data
		sql = "INSERT INTO ebdb.meal_table (meal_id, host, place) VALUES (%d, \'%s\', \'%s\');" % (form.mealtable.data, form.host.data, form.place.data)
		print sql
		cursor.execute(sql)

		print 'Thanks for registering'
		# return redirect(url_for('hello'))
	return render_template('registermeal.html', form=form)

if __name__ == '__main__':
	application.run(debug=True)