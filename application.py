import os.path
from flask import Flask, render_template, flash, url_for, request, redirect, abort
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import MySQLdb
import json
from form import *
from datetime import datetime

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

	clearOldMeals()
	
	cursor = db.cursor()
	#What if page number gives an offset that is too large?
	cursor.execute("SELECT * FROM ebdb.meal_table WHERE publicprivate = \'%s\' ORDER BY date, time" % "pub")
	queryResults = cursor.fetchall()
	mealList = json.dumps(queryResults)

	GuestNames = getGuestNames(queryResults)

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
	return render_template('feed.html', mealList=mealList, hostList=hostList, GuestNames=GuestNames, errorFlag=errorFlag)

@application.route('/exitpage')
def exitpage():
	return render_template('exit.html')

@application.route('/registeruser', methods=['GET', 'POST'])
def registeruser():

	#print("got to here 1")
	form = Signup(request.form)
	if request.method == 'POST' and form.validate():
		cursor = db.cursor()
		
		#print("got to here 2")
		netid = form.email.data.split('@')[0]

		#check to make sure that this netid was not already present in the database
		sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid, photo_url) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\');" % (int(form.uid.data), form.firstname.data, form.lastname.data, netid, form.picurl.data)
		
		#print("got to here3")
		cursor.execute(sql)
		cursor.close()
		
		#print("got to here 4")
		return redirect(url_for('feed'))
		
		#print("got to here 5")
	return render_template('registeruser.html', form=form)

@application.route('/registermeal', methods=['GET', 'POST'])
def registermeal():
	form = MealForm(request.form)
	
	if request.method == 'POST' and form.validate():
		# user = User(form.mealtable.data, form.host.data, form.place.data)
		cursor = db.cursor()
		
		# received as month-day-year
		receivedDate = str(form.date.data).split('/')
		newDate = receivedDate[2] + '-' + receivedDate[0] + '-' + receivedDate[1]
		
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
	
	hostid = meal[15]
	
	print("this is the hostid")
	print(hostid)
	print("hostid type:")
	print(type(hostid))
	print("uid type:")
	print(type(uid))
	print("uid is:")
	print(uid)
	
	#type bashing
	if (type(uid) is int):
		str_uid = str(uid)
	else:
		str_uid = uid
	
	if (type(hostid) is int):
		str_hostid = str(hostid)
	else:
		str_hostid = hostid
			
	if str_hostid == str_uid: 
			errorFlag = "3" # They are the host
			cursor.close()
			return redirect(url_for('feed', errorFlag=errorFlag))
				
	#f = open("TEMP_for_testing_joinmeal.txt", "w")
	firstGuestIndex = 4 #hardcoded; this is the index of the first guest
	guest_x = 1
	for guest in meal[firstGuestIndex:firstGuestIndex + 11]:
		
		if (not guest):
			break
		guest_x += 1
		
		# even more type bashing
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
		
	clearOldMeals()
	
	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE user_id = %s;" % (uid)
	cursor.execute(query)
	queryResults = cursor.fetchall()
	hostingMeals = json.dumps(queryResults)

	queryInvite = "SELECT * FROM ebdb.invitees WHERE guest = %s" % (uid)
	cursor.execute(queryInvite)
	queryInviteResults = cursor.fetchall()
	invitedMeals = json.dumps(queryInviteResults)

	yourInvites = []
	InviteNames = []

	tempQuery1 = "SELECT * FROM ebdb.invitees WHERE guest = %s" % (uid)
	cursor.execute(tempQuery1)
	queryTempResults = cursor.fetchall()
	for row in queryTempResults:
		tempQuery2 = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s" % row[0]
		cursor.execute(tempQuery2)
		queryResults = cursor.fetchall()
		for each in queryResults:
			yourInvites.append(each)
			InviteNames.append(each[15])
	yourInvites = json.dumps(yourInvites)

	InviteMealNames = []
	for i in range(0, len(InviteNames)):
		sql = "SELECT * FROM ebdb.user_table WHERE user_id = %d" % (int(InviteNames[i]))
		cursor.execute(sql)
		InviteMealNames.append(cursor.fetchone())

	yourmeals = []
	mealuids = []

	for a in range(1, 12):
		guestString = "guest" + str(a)

		query = "SELECT * FROM ebdb.meal_table WHERE " + guestString + " = %s ORDER BY date, time" % (uid)
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
	invitenameList = json.dumps(InviteMealNames)
	cursor.close()
	return render_template('mymeals.html', myhosts=hostingMeals, yourinvites=yourInvites, invited=invitedMeals, hostnameList=hostnameList, invitenameList=invitenameList, myguests=yourmeals, message=message)

@application.route('/accept/<mealid>/<uid>')
def accept(mealid=None, uid=None):
	if not uid or not mealid:
		return redirect(url_for('home'))
	cursor = db.cursor()
	#print "accept: cursor opened"
	deletequery = "DELETE FROM ebdb.invitees WHERE (meal_id, guest) = (%s, %s);" % (mealid,uid)
	cursor.execute(deletequery)
	#print "accept: row deleted"
	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	#print "accept: meal fetched"
	meal = cursor.fetchone()
	if not meal:
		#print "accept: this is not a meal"
		abort(404)


	hostid = meal[15]
	
	#type bashing
	if (type(uid) is int):
		str_uid = str(uid)
	else:
		str_uid = uid
	
	if (type(hostid) is int):
		str_hostid = str(hostid)
	else:
		str_hostid = hostid
			
	if str_hostid == str_uid: 
			errorFlag = "3" # They are the host
			cursor.close()
			return redirect(url_for('feed', errorFlag=errorFlag))
	#print "accept: type bashed"	
	#f = open("TEMP_for_testing_joinmeal.txt", "w")
	firstGuestIndex = 4 #hardcoded; this is the index of the first guest
	guest_x = 1
	for guest in meal[firstGuestIndex:firstGuestIndex + 11]:
		
		if (not guest):
			break
		guest_x += 1
		
		# even more type bashing
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
	#print "accept: accepted"
	cursor.close()
	return redirect(url_for('mymeals', uid=uid))

@application.route('/reject/<mealid>/<uid>')
def reject(mealid=None, uid=None):
	if not uid or not mealid:
		return redirect(url_for('home'))
	cursor = db.cursor()
	#print "accept: cursor opened"
	deletequery = "DELETE FROM ebdb.invitees WHERE (meal_id, guest) = (%s, %s);" % (mealid,uid)
	cursor.execute(deletequery)
	cursor.close()
	return redirect(url_for('mymeals', uid=uid))

@application.route('/remove/<mealid>/<uid>')
def remove(mealid=None, uid=None):
	
	if not uid or not mealid:
		return redirect(url_for('home'))
	
	# get the guest table for the given uid
	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()
	if not meal:
		abort(404)

	firstGuestIndex = 4 #hardcoded; this is the index of the first guest
	if not meal[firstGuestIndex]:
		abort(404)

	guests = meal[firstGuestIndex:firstGuestIndex + 10]
	#print("got to here 4")
	# search guests for uid
	guest_X = 1
	for guest in guests:
		# check if the guest matches the selected user id
		if (guest == uid):
			break
		guest_X += 1

	if guest_X >= 11: # i.e. said guest is not in meal
		abort(404)

	user_index = guest_X
	# search guests for final non-null array index
	guest_Y = 0
	for guest in guests:
		# check if the guest matches the selected user id
		if not guest:
			break
		guest_Y += 1

	last_full_index = guest_Y
	
	last_full = guests[last_full_index-1]
	
	# The last_full_index will be -1 if the meal is empty. This should be impossible, so if we run into this problem then
	# we've made some kind of error
	
	guestUIDString = "guest" + str(user_index)
	guestLastString = "guest" + str(last_full_index)
	
	# Now, update the uid at position user_index with uid at last_full_index.
	sql = "UPDATE ebdb.meal_table SET %s = %s WHERE meal_id=%s;" % (guestUIDString, last_full, mealid)
	print (sql)
	cursor.execute(sql)
	
	# Then, update uid at position last_full_index with null.
	sql = "UPDATE ebdb.meal_table SET %s = NULL WHERE meal_id=%s;" % (guestLastString, mealid)
	cursor.execute(sql)
	
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

	print ("check this kevin")
	# print request.data
	# print request.form['friend1']
	# print request.form.itervalues()

	mistake = False
	
	cursor = db.cursor()
	for i in request.form.itervalues():
		# print "kevin's a slut"
		# check if user is already invited.
		sql = "SELECT * FROM ebdb.invitees WHERE meal_id = %d" % int(mealid)
		# print "such an outrageous whore"
		cursor.execute(sql)
		# print "taht the world has ever known"
		is_invited_already = False #is the user already invited to this meal? Reset 2 false
		invitees = cursor.fetchall()
		for each in invitees:
			if (str(each[2]) == str(i)):
				is_invited_already = True
				mistake = True
				break

		# check that user is not already a guest
		is_guest_already = False
		if not is_invited_already:
			sql = "SELECT * FROM ebdb.meal_table WHERE meal_id = %d" % int(mealid)
			cursor.execute(sql)
			mealinfo = cursor.fetchone()
			firstGuestIndex = 4
			guests = mealinfo[firstGuestIndex:firstGuestIndex + 11]
			for guest in guests:
				if str(guest) == str(i):
					is_guest_already = True
					mistake = True
					break

				
		# if the user isn't already invited and isn't already a guest, then invite him
		if not is_invited_already and not is_guest_already:
			sql = "INSERT INTO ebdb.invitees (meal_id, guest, hostnotification, guestnotification) VALUES (%d, %d, %d, %d);" % (int(mealid), int(i), 0, 0)
		 	cursor.execute(sql)
		print i

	cursor.close()
		
	print "wtf"
	
	if (mistake == True):
		errorFlag = "4"
	else: 
		errorFlag = "0a"
		
	return redirect(url_for('feed', errorFlag = errorFlag))
	
@socketio.on('notify')
def test_message(message):
    emit('my response',
         {'data': message['data']})

def clearOldMeals():

	currentDate = datetime.now().strftime('%Y-%m-%d')
	thisHour = int(datetime.now().strftime('%H'))
	currentMin = int(datetime.now().strftime('%M'))
	
	if (currentMin >= 10):
		lastMin = currentMin - 10
		lastHour = thisHour
		
	else:
	
		if (thisHour != 0):
			lastHour = thisHour - 1
			lastMin = currentMin + 50
		else:
			lastHour = 0
			lastMin = 0
		
	print("0.9")
	cursor = db.cursor()
	
	sql = "DELETE FROM ebdb.meal_table WHERE date < \'%s\';" % (currentDate) 
	cursor.execute(sql)
	
	print("1")
	
	sql = "DELETE FROM ebdb.meal_table WHERE date = \'%s\' AND time < \'%02d:%02d\';" % (currentDate, lastHour, lastMin) 
	cursor.execute(sql)
	print("2")
	cursor.close()	
	print("if you get here Gil's code worked fine")

def getGuestNames(mealList):
	# get all the guest names for guest1
	cursor = db.cursor()
	ListofLists = []


	for i in range(0, len(mealList)):
		newList = []
		j = 4	
		while mealList[i][j] is not None and j < 15: 
			sql = "SELECT * FROM ebdb.user_table where user_id=%s;" % (mealList[i][j])
			cursor.execute(sql)
			temp = cursor.fetchone()
			newList.append(temp)
			j=j+1
		ListofLists.append(newList)

		dump = json.dumps(ListofLists)

	return dump


	
	
if __name__ == '__main__':
	application.run(debug=True)
	socketio.run(application)
