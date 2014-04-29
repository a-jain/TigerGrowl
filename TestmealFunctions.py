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
def remove:
	if not uid or not mealid:
		return redirect(url_for('home'))
		
	# get the guest table for the given uid
	cursor = db.cursor()
	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()
	
	firstGuestIndex = 5 #hardcoded; this is the index of the first guest
	guests = meal[firstGuestIndex:firstGuestIndex + 11]:
	
	# search guests for uid
	guest_X = 0
	for guest in guests:
	
		# check if the guest matches the selected user id
		if (guest == uid):
			break
		guest_X += 1

	user_index = guest_x
	
	# search guests for final non-null array index
	guest_Y = 0
	for guest in guests:
	
		# check if the guest matches the selected user id
		if (not guest):
			break
		guest_Y += 1

	last_full_index = guest_Y - 1
	last_full = guests[last_full_index]
	# The last_full_index will be -1 if the meal is empty. This should be impossible, so if we run into this problem
	# we've fucked up
	
	guestUIDString = "guest" + str(user_index)
	guestLastString = "guest" + str(last_full_index)
	
	# Now, update the uid at position user_index with uid at last_full_index.
	sql = "UPDATE ebdb.meal_table SET %s = %s WHERE meal_id=%s;" % (guestUIDString, last_full, mealid)
	cursor.execute(sql)
	
	# Then, update uid at position last_full_index with null.
	sql = "UPDATE ebdb.meal_table SET %s = NULL WHERE meal_id=%s;" % (guestLastString, mealid)
	cursor.execute(sql)

	cursor.close()
	
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
