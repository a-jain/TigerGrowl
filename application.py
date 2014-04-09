from flask import Flask
from flask import render_template, flash, url_for
from flask import request
from flask import redirect
import MySQLdb
import json
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

@application.route('/login')
@application.route('/login/<uid>')
def login(uid=None):
	sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d" % (int(uid))
	cursor.execute(sql)
	results = cursor.fetchone()
	if results:
		feedPrototype()
	else:
		url_for('registeruser')

	return render_template('fbids.html')

@application.route('/timeline')
def timeline():
	return render_template('timeline.html')

@application.route('/feedPrototype')
@application.route('/feedPrototype/<page>')
def feedPrototype(page=None):
	if page is None:
		offset = 0
	else:
		offset = page - 1

	#What if page number gives an offset that is too large?
		
	cursor.execute("SELECT * FROM ebdb.meal_table LIMIT 5 OFFSET %d" %(offset*5) )
	queryResults = cursor.fetchall()
	mealList = json.dumps(queryResults)
	return render_template('feed.html', mealList=mealList)

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@application.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
	form = Signup(request.form)
	if request.method == 'POST' and form.validate():

		netid = form.email.data.split('@')[0]
		sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid, photo_url) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\');" % (int(form.uid.data), form.firstname.data, form.lastname.data, netid, form.picurl.data)

		cursor.execute(sql)

		return redirect(url_for('feedPrototype'))
	return render_template('registeruser.html', form=form)

@application.route('/registermeal', methods=['GET', 'POST'])
def registermeal():
	form = MealForm(request.form)
	if request.method == 'POST' and form.validate():
		# user = User(form.mealtable.data, form.host.data, form.place.data)
		
		print form.mealtable.data
		print form.host.data
		print form.place.data
		sql = "INSERT INTO ebdb.meal_table (meal_id, host, place) VALUES (%d, \'%s\', \'%s\');" % (form.mealtable.data, form.host.data, form.place.data)
		print sql
		cursor.execute(sql)

		return redirect(url_for('feed'))
	return render_template('registermeal.html', form=form)

if __name__ == '__main__':
	application.run(debug=True)