import os.path
from flask import Flask, render_template, flash, url_for, request, redirect, abort
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import MySQLdb
import json
from form import *
# from datetime import date

application = Flask(__name__)
application.secret_key = '\x99\x02~p\x90\xa3\xce~\xe0\xe6Q\xe3\x8c\xac\xe9\x94\x84B\xe7\x9d=\xdf\xbb&'
socketio = SocketIO(application)

db = MySQLdb.connect(host="aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com",user="growladmin",passwd="youeatyet?",db="ebdb")
db.autocommit(True)

@application.errorhandler(404)
def page_not_found(error):
	return render_template('error.html'), 404

@application.route('/')
@application.route('/home')
def home():
	return render_template('landing.html')

@application.route('/welcome')
def welcome():
	return render_template('welcome.html')


@application.route('/login/')
@application.route('/login/<uid>')
def login(uid=None):
	if not uid:
		return redirect(url_for('home'))

	cursor = db.cursor()
	sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d" % (int(uid))
	cursor.execute(sql)
	results = cursor.fetchone()
	cursor.close()
	if results:
		return redirect(url_for('feed'))
	else:
		return redirect(url_for('registeruser'))

@application.route('/timeline')
def timeline():
	return render_template('timeline.html')

@application.route('/feed')
@application.route('/feed/<errorFlag>')
def feed(errorFlag=None):

	cursor = db.cursor()
	#What if page number gives an offset that is too large?
	cursor.execute("SELECT * FROM ebdb.meal_table WHERE publicprivate = \'%s\' ORDER BY date, time" % "pub")
	queryResults = cursor.fetchall()
	mealList = json.dumps(queryResults)

	mealuids = []
	for meal in queryResults:
		mealuids.append(meal[15])

	queryresultList = []
	for i in range(0, len(mealuids)):
		sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d;" % (int(mealuids[i]))
		cursor.execute(sql)
		queryresultList.append(cursor.fetchone())


	hostList = json.dumps(queryresultList)
	cursor.close()
	return render_template('feed.html', mealList=mealList, hostList=hostList, errorFlag=errorFlag)

@application.route('/exitpage')
def exitpage():
	return render_template('exit.html')

@application.route('/registeruser', methods=['GET', 'POST'])
def registeruser():

	print("got to here 1")
	form = Signup(request.form)
	if request.method == 'POST' and form.validate():
		cursor = db.cursor()
		
		print("got to here 2")
		netid = form.email.data.split('@')[0]

		#check to make sure that this netid was not already present in the database
		sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid, photo_url) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\');" % (int(form.uid.data), form.firstname.data, form.lastname.data, netid, form.picurl.data)
		
		print("got to here3")
		cursor.execute(sql)
		cursor.close()
		
		print("got to here 4")
		return redirect(url_for('feed'))
		
		print("got to here 5")
	return render_template('registeruser.html', form=form)

@application.route('/registermeal', methods=['GET', 'POST'])
def registermeal():
	form = MealForm(request.form)
	
	if request.method == 'POST' and form.validate():
		# user = User(form.mealtable.data, form.host.data, form.place.data)
		cursor = db.cursor()
		
		receivedDate = str(form.date.data).split('-')
		newDate = "2014" + '-' + receivedDate[1] + '-' + receivedDate[2]
		
		receivedTime = str(form.time.data)[:-3]
		
		sql = "INSERT INTO ebdb.meal_table (place, date, time, user_id, publicprivate) VALUES (\'%s\', \'%s\', \'%s\', %d, \'%s\');" % (form.place.data, newDate, receivedTime, int(form.uid.data), form.priv.data)
		cursor.execute(sql)
		
		"""
		sql = "INSERT INTO ebdb.invitees (meal_id, user_id) VALUES (%d, %d);" % (int(cursor.lastrowid), int(form.uid.data))
		cursor.execute(sql)"""
		cursor.close()
		# change to some exit page
		return redirect(url_for('exitpage'))
	return render_template('registermeal.html', form=form)

@application.route('/joinmeal/<mealid>/<uid>')
def joinmeal(uid=None, mealid=None):
	if not uid or not mealid:
		return redirect(url_for('home'))
	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()

	#f = open("TEMP_for_testing_joinmeal.txt", "w")
	firstGuestIndex = 4 #hardcoded; this is the index of the first guest
	guest_x = 1
	for guest in meal[firstGuestIndex:firstGuestIndex + 11]:
		if (not guest):
			break
		guest_x += 1
		
		#type bashing
		if (type(uid) is int):
			str_uid = str(uid)
		else:
			str_uid = uid

		if (type(guest) is int):
			str_guest = str(guest)
		else:
			str_guest = guest


		if (str_guest == str_uid):
			#print("uid match")
			#Handle the case of them being already in the meal
			errorFlag = "1" # Already guest
			cursor.close()
			return redirect(url_for('feed', errorFlag=errorFlag))
			
	if guest_x == 12:
		errorFlag = "2" # Full meal
		cursor.close()
		return redirect(url_for('feed', errorFlag=errorFlag))
		
	guestString = "guest" + str(guest_x)
	sql = "UPDATE ebdb.meal_table SET %s=%s WHERE meal_id=%s;" % (guestString, uid, mealid)
	cursor.execute(sql)
	cursor.close()
	
	#f.close()
	
	# at this point we can consider the possibility that we actually want to send the user back to the feed page.
	# If we're deadset on sending them to mymeals then we can add a similar script handling to mymeals, but I think it might be better
	# to send them back to feed after joining a meal
	return redirect(url_for('mymeals', uid=uid, message="success"))

@application.route('/mymeals')
@application.route('/mymeals/<uid>')
@application.route('/mymeals/<uid>/<message>')
def mymeals(uid=None, message=None):
	if not uid:
		return redirect(url_for('/home'))
	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE user_id = %s;" % (uid)
	cursor.execute(query)
	queryResults = cursor.fetchall()
	hostingMeals = json.dumps(queryResults)

	yourmeals = []
	mealuids = []

	for a in range(1, 12):
		guestString = "guest" + str(a)
		query = "SELECT * FROM ebdb.meal_table WHERE " + guestString + " = %s;" % (uid)
		cursor.execute(query)
		queryResults = cursor.fetchall()
		for each in queryResults:
			yourmeals.append(each)
			mealuids.append(each[15])
	yourmeals = json.dumps(yourmeals)

	queryresultList = []
	for i in range(0, len(mealuids)):
		sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d" % (int(mealuids[i]))
		cursor.execute(sql)
		queryresultList.append(cursor.fetchone())

	hostnameList = json.dumps(queryresultList)
	cursor.close()
	return render_template('mymeals.html', myhosts=hostingMeals, hostnameList=hostnameList, myguests=yourmeals, message=message)

@application.route('/remove')
@application.route('/remove/<mealid>')
@application.route('/remove/<mealid>/<uid>')
def remove(mealid=None, uid=None):
	print("got to here1")
	if not uid or not mealid:
		return redirect(url_for('home'))
	print("got to here 2")
	# get the guest table for the given uid
	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()
	print("got to here 3")
	firstGuestIndex = 4 #hardcoded; this is the index of the first guest
	guests = meal[firstGuestIndex:firstGuestIndex + 11]
	print("got to here 4")
	# search guests for uid
	guest_X = 1
	for guest in guests:
		# check if the guest matches the selected user id
		if (guest == uid):
			break
		guest_X += 1

	print(guest_X)
	print(guest)
	user_index = guest_X
	print("got to here 5")
	# search guests for final non-null array index
	guest_Y = 0
	for guest in guests:
	
		# check if the guest matches the selected user id
		if (not guest):
			break
		guest_Y += 1
	print("got to here 6")
	last_full_index = guest_Y
	last_full = guests[last_full_index]
	# The last_full_index will be -1 if the meal is empty. This should be impossible, so if we run into this problem then
	# we've made some kind of error
	
	guestUIDString = "guest" + str(user_index)
	guestLastString = "guest" + str(last_full_index)
	print("guestUIDString is")
	print(guestUIDString)
	print("guestLastString is")
	print(guestLastString)
	print("last_full is")
	print(last_full)
	# Now, update the uid at position user_index with uid at last_full_index.
	sql = "UPDATE ebdb.meal_table SET %s = %s WHERE meal_id=%s;" % (guestUIDString, last_full, mealid)
	cursor.execute(sql)
	print ("got to here 7")
	# Then, update uid at position last_full_index with null.
	#sql = "UPDATE ebdb.meal_table SET %s = NULL WHERE meal_id=%s;" % (guestLastString, mealid)
	#cursor.execute(sql)
	print("got to here 8 - we've finished the removal (ostensibly)")

	##### This is what happens when you route to mymeals; you need to query to get an updated version of this information.
	"""
	query = "SELECT * FROM ebdb.meal_table WHERE user_id = %s;" % (uid)
	cursor.execute(query)
	queryResults = cursor.fetchall()
	hostingMeals = json.dumps(queryResults)

	yourmeals = []
	mealuids = []

	print("got to here9 2.0")
	for a in range(1, 12):
		guestString = "guest" + str(a)
		query = "SELECT * FROM ebdb.meal_table WHERE " + guestString + " = %s;" % (uid)
		cursor.execute(query)
		queryResults = cursor.fetchall()
		for each in queryResults:
			yourmeals.append(each)
			mealuids.append(each[15])
	yourmeals = json.dumps(yourmeals)

	print("got to here10")
	queryresultList = []
	for i in range(0, len(mealuids)):
		sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d" % (int(mealuids[i]))
		cursor.execute(sql)
		queryresultList.append(cursor.fetchone())

	hostnameList = json.dumps(queryresultList)
	cursor.close()
	
	print("got to here13")
	return render_template('mymeals.html', myhosts=hostingMeals, hostnameList=hostnameList, myguests=yourmeals, message = "werked/twerked")
	"""
	
	return redirect(url_for('mymeals', uid=uid, message='success1'))
	
# when invite friends is clicked, the following happens:
# pull user's friends from fb
# pull all userids in user_table
# cross reference. all fbids that are not in userids are added to blacklist = []
# we call the fb friend selector with the blacklist
# this returns some fb ids
# we add this to the sql database	
@application.route('/invite/<mealid>')
def invite(mealid=None):
	if not mealid:
		return redirect(url_for('home'))
	
	# for each in guestList:
	# 	query = "INSERT INTO ebdb.invitees (meal_id, host, guest) VALUES (\'%s\', \'%s\', \'%s\');" % (mealid, host, each)
	# 	cursor.execute(query)
	return render_template('invite.html', mealid=mealid)
	# return redirect(url_for('mymeals', uid=host))

@application.route('/inviter/<mealid>', methods=['POST'])
def inviters(mealid=None):
	# mealid = request.form['mealid']
	# names = request.form['names']

	# print mealid
	# print json.loads(names)

	# with some error code
	if not request.form:
		return redirect(url_for('feed'))

	print "check this kevin"
	# print request.data
	# print request.form['friend1']
	# print request.form.itervalues()

	for i in request.form.itervalues():
		cursor = db.cursor()
		sql = "INSERT INTO ebdb.invitees (meal_id, guest) VALUES (%d, %d);" % (int(mealid), int(i))
		cursor.execute(sql)
		print i

	cursor.close()
		
	print "wtf"

	return redirect(url_for('feed'))

@socketio.on('notify')
def test_message(message):
    emit('my response',
         {'data': message['data']})

if __name__ == '__main__':
	application.run(debug=True)
	socketio.run(application)
