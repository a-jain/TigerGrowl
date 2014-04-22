import os.path
from flask import Flask, render_template, flash, url_for, request, redirect, abort
from flask import send_from_directory
from werkzeug.utils import secure_filename
import MySQLdb
import json
import slate
from form import *

application = Flask(__name__)
application.debug = True
application.secret_key = '\x99\x02~p\x90\xa3\xce~\xe0\xe6Q\xe3\x8c\xac\xe9\x94\x84B\xe7\x9d=\xdf\xbb&'

db = MySQLdb.connect(host="aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com",user="growladmin",passwd="youeatyet?",db="ebdb")
db.autocommit(True)

cursor = db.cursor()

@application.errorhandler(404)
def page_not_found(error):
	return "Sorry, this file/page doesn't exist", 404

@application.route('/')
@application.route('/home')
def home():
	return render_template('landing.html')

@application.route('/login/')
@application.route('/login/<uid>')
def login(uid=None):
	if not uid:
		return redirect(url_for('home'))

	sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d" % (int(uid))
	cursor.execute(sql)
	results = cursor.fetchone()
	if results:
		return redirect(url_for('feed'))
	else:
		return redirect(url_for('registeruser'))

@application.route('/timeline')
def timeline():
	return render_template('timeline.html')

@application.route('/feed')
def feed(page=None):
	if page is None:
		offset = 0
	else:
		offset = page - 1

	#What if page number gives an offset that is too large?
	cursor.execute("SELECT * FROM ebdb.meal_table LIMIT 5 OFFSET %d" %(offset*5) )
	queryResults = cursor.fetchall()
	mealList = json.dumps(queryResults)

	return render_template('feed.html', mealList=mealList)

@application.route('/exitpage')
def exitpage():
	return render_template('exit.html')

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@application.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
	try: 
		form = Signup(request.form)
		if request.method == 'POST' and form.validate():

			netid = form.email.data.split('@')[0]
			sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid, photo_url) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\');" % (int(form.uid.data), form.firstname.data, form.lastname.data, netid, form.picurl.data)

			cursor.execute(sql)

			return redirect(url_for('feed'))
		return render_template('registeruser.html', form=form)
	except ValidationError:
		return render_template("Bad email, gotta be princeton")
@application.route('/registermeal', methods=['GET', 'POST'])
def registermeal():
	form = MealForm(request.form)
	if request.method == 'POST' and form.validate():
		# user = User(form.mealtable.data, form.host.data, form.place.data)
		
		receivedDate = str(form.date.data).split('-')
		newDate = receivedDate[1] + '/' + receivedDate[2]

		receivedTime = str(form.time.data)[:-3]

		sql = "INSERT INTO ebdb.meal_table (host, place, date, time, user_id, publicprivate) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', %d, \'%s\');" % (form.host.data, form.place.data, newDate, receivedTime, int(form.uid.data), form.priv.data)
		print sql
		cursor.execute(sql)

		sql = "INSERT INTO ebdb.invitees (meal_id, host) VALUES (\'%s\', \'%s\');" % (cursor.lastrowid, form.host.data)
		cursor.execute(sql)

		# change to some exit page
		return redirect(url_for('exitpage'))
	return render_template('registermeal.html', form=form)

@application.route('/joinmeal/<mealid>/<uid>')
def joinmeal(uid=None, mealid=None, errorFlag=None):
	if not uid or not mealid:
		return redirect(url_for('home'))

	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()

	firstGuestIndex = 5 #hardcoded; this is the index of the first guest
	guest_x = 1
	for guest in meal[firstGuestIndex:firstGuestIndex + 12]:
		if (not guest):
			break
		guest_x += 1
		if (guest is uid):
			#Handle the case of them being already in the meal
			errorFlag = "Oops! You have already signed up for this meal."
			return render_template('feed.html', mealList=mealList, errorFlag=errorFlag)
			
	if (guest_x == 13): 
		pass
		#Handle the meal being full.
	guestString = "guest" + str(guest_x)
	sql = "UPDATE ebdb.meal_table SET %s=%s WHERE meal_id=%s;" % (guestString, uid, mealid)
	cursor.execute(sql)

	return redirect(url_for('mymeals', uid=uid))

@application.route('/mymeals')
@application.route('/mymeals/<uid>')
def mymeals(uid=None):
	if not uid:
		return redirect(url_for('home'))

	query = "SELECT * FROM ebdb.meal_table WHERE user_id = %s;" % (uid)
	cursor.execute(query)
	queryResults = cursor.fetchall()
	hostingMeals = json.dumps(queryResults)

	yourmeals = []
	for a in range(1, 12):
		guestString = "guest" + str(a)
		query = "SELECT * FROM ebdb.meal_table WHERE " + guestString + " = %s;" % (uid)
		cursor.execute(query)
		queryResults = cursor.fetchall()
		for each in queryResults:
			yourmeals.append(each)
	yourmeals = json.dumps(yourmeals)

	return render_template('mymeals.html', myhosts=hostingMeals, myguests=yourmeals)
	

# when invite friends is clicked, the following happens:
# pull user's friends from fb
# pull all userids in user_table
# cross reference. all fbids that are not in userids are added to blacklist = []
# we call the fb friend selector with the blacklist
# this returns some fb ids
# we add this to the sql database	
@application.route('/invite/<mealid>/<host>/<guests>')
def invite(mealid=None):
	if not mealid:
		return redirect(url_for('home'))

	guestList = json.loads(guests)
	
	for each in guestList:
		query = "INSERT INTO ebdb.invitees (meal_id, host, guest) VALUES (\'%s\', \'%s\', \'%s\');" % (mealid, host, each)
		cursor.execute(query)
	return redirect(url_for('mymeals', uid=host))

if __name__ == '__main__':
	application.run(debug=True)