#cursor = whatever

def query_db(query):
    cur = cursor.execute(query)
    return cur.fetchall()

def seeAllMeals():
	""" return a list of all meals that your friends are hosting"""
	#get user's facebookid
	#get friendlist from graph API
	
	allmeals = []
	#for each friend in friendlist
		# get that friend's facebookid from graph API

		# get that friend's user_id from Users
		query = "SELECT * FROM ebdb.user_table where facebookid = " + str(facebookid) + ");"
		friend = query_db(query)
		friend_dinerid = friend[dinerid]
		
		# see which meals that friend is hosting
		query = "SELECT * FROM ebdb.meal_table where hostid = " + str(dinerid) + ");"
		meal = query_db(query)

		#you can manipulate the contents of "meal" if you like, by putting them into say a list mealData
		allmeals.append(meal)

	return allmeals

def seeYourMeals(facebookid):
	yourmeals = []

	#meals that I'm hosting
	yourmeals.append("hosting")
	query = "SELECT * FROM ebdb.meal_table where userid = " + str(facebookid) + ");"
	myHostedMeals = query_db(query)
	for each in myHostedMeals:
		yourmeals.append(each)

	yourmeals.append("guesting")
	for a in range(1, 12):
		guestString = "guest" + str(a)
		query = "SELECT * FROM ebdb.meal_table where guestString = " + str(facebookid) + ");"
		myGuestXMeals = query_db(query)
		for each in myGuestXMeals:
			yourmeals.append(each)

	return yourmeals
	
def hostMeal(location, currentHour, currentMin, currentSec, startHour, startMin, startSec, message):
	#get the user's facebookid, and then dinerid from users
	
	query = "SELECT * FROM ebdb.meal_table where hostid = " + str(dinerid) + ");"
	meal = query_db(query)

def joinMeal(meal_id):
	#get the user's facebookid
	
	query = "SELECT * FROM ebdb.meal_table where meal_id = " + str(meal_id) + ");"
	meal = query_db(query)

	firstGuestIndex = 5 #hardcoded; this is the index of the first guest
	guest_x = 1
	for each in meal[firstGuestIndex:firstGuestIndex + 12]:
		if (each == None):
			break;
		guest_x = guest_x + 1

	guestString = "guest" + str(guest_x)
	sql = "INSERT INTO ebdb.meal_table (\'%s\') VALUES (\'%s\');" % (guestString, user_id)
	query_db(sql)