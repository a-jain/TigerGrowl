import os.path
from flask import Flask, render_template, flash, url_for, request, redirect, abort
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import MySQLdb
import json
from form import *


db = MySQLdb.connect(host="aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com",user="growladmin",passwd="youeatyet?",db="ebdb")
db.autocommit(True)

def testjoinmeal(uid, mealid):

	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()

	#f = open("TEMP_for_testing_joinmeal.txt", "w")
	firstGuestIndex = 5 #hardcoded; this is the index of the first guest
	guest_x = 1
	for guest in meal[firstGuestIndex:firstGuestIndex + 11]:
		if (not guest):
			break
		guest_x += 1
		
		
		#Check type of guest
		print("Type of guest is:")
		print(type(guest))
		
		print("Type of uid is:")
		print(type(uid))
		
		print("the guest is:")
		print(guest)
		
		print("the uid is:")
		print(uid)
		
		print("Do they match?")
		print(uid is guest)
		
		print("Does str(guest) match uid?")
		print(str(guest) is uid)
		
		print("What about with == instead of is?")
		print(guest == uid)
		
		if (str(guest) is uid):
			print("uid match")
			#Handle the case of them being already in the meal
			errorFlag = "1" # Already guest
			cursor.close()
			return "lolol uid match"
			
	if guest_x == 12:
		errorFlag = "2" # Full meal
		cursor.close()
		return "Lolol full meal"
		
	guestString = "guest" + str(guest_x)
	#sql = "UPDATE ebdb.meal_table SET %s=%s WHERE meal_id=%s;" % (guestString, uid, mealid)
	cursor.execute(sql)
	cursor.close()
	
	#f.close()

	# at this point we can consider the possibility that we actually want to send the user back to the feed page.
	# If we're deadset on sending them to mymeals then we can add a similar script handling to mymeals, but I think it might be better
	# to send them back to feed after joining a meal
	return "lolol it worked"


	
testjoinmeal('1486930511', '467244')
