""" this program will test the functions of our program on the sqlite database. I strongly recommend you keep the mysql
database exactly the same as the sqlite, so that we will not have headaches when it is time to start testing our project."""

import sqlite3
from flask import g
DATABASE = '/testDB'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
app = Flask(__name__)

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def signUp(facebookid):
	""" get your id into the database """
	#log into facebook
	#get fb id from facebook data
	#sanitize the input if necessary

	#enter the facebook data with data obtained from graph API into users
	query = "insert into users(facebookid) values(" + str(facebookid) + ");"
	query_db(query)

def seeMeals():
	""" return a list of all meals that your friends are hosting"""
	#get user's facebookid
	#get friendlist from graph API
	
	allmeals = []
	#for each friend in friendlist
		# get that friend's facebookid from graph API

		# get that friend's dinerid from Users
		query = "select * from users where facebookid = " + str(facebookid) + ");"
		friend = query_db(query)
		friend_dinerid = friend[dinerid]
		
		# see which meals that friend is hosting
		query = "select * from meals where hostid = " + str(dinerid) + ");"
		meal = query_db(query)

		#you can manipulate the contents of "meal" if you like, by putting them into say a list mealData
		allmeals.append(meal)

	return allmeals

def hostMeal(location, currentHour, currentMin, currentSec, startHour, startMin, startSec, message):
	#get the user's facebookid, and then dinerid from users
	
	query = "select * from meals where hostid = " + str(dinerid) + ");"
	meal = query_db(query)

