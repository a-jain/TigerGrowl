#cursor = whatever

def query_db(query):
    cur = cursor.execute(query)
    return cur.fetchall()

def seeAllMeals(facebookid):
	#see meals that you are invited to
	visibleMeals = [] 
	query = "SELECT * FROM ebdb.invitees where guest = %s;"  % (str(facebookid))
	myVisibleMeals = query_db(query)
	for each in myVisibleMeals:
		query1 = "SELECT * FROM ebdb.meal_table where guest = %s;"  % (str(facebookid))
		mealData = query_db(query)	
		visibleMeals.append(mealData)
		
	return visibleMeals
	
def invite():
	#invites form data to meal. form.meal.data should be hidden and corresponding to meal_id of data, host.data to host, guest to facebookid of guest.
	query = "INSERT INTO ebdb.invitees (meal_id, host, guest) VALUES (%s, %d, %d);" % (form.meal.data, form.host.data, form.guest,data))
	query_db(query)
	
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
