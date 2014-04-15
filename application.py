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

UPLOAD_FOLDER = 'static/spritz/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db = MySQLdb.connect(host="aa104vf4z8592ny.ct5w0yg0rrlk.us-east-1.rds.amazonaws.com",user="growladmin",passwd="youeatyet?",db="ebdb")
db.autocommit(True)

cursor = db.cursor()

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
	form = Signup(request.form)
	if request.method == 'POST' and form.validate():

		netid = form.email.data.split('@')[0]
		sql = "INSERT INTO ebdb.user_table (user_id, firstname, lastname, netid, photo_url) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\');" % (int(form.uid.data), form.firstname.data, form.lastname.data, netid, form.picurl.data)

		cursor.execute(sql)

		return redirect(url_for('feed'))
	return render_template('registeruser.html', form=form)

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
def joinmeal(uid=None, mealid=None):
	if not uid or not mealid:
		return redirect(url_for('home'))

	query = "SELECT * FROM ebdb.meal_table WHERE meal_id = %s;" % (mealid)
	cursor.execute(query)
	meal = cursor.fetchone()

	firstGuestIndex = 5 #hardcoded; this is the index of the first guest
	guest_x = 1
	for each in meal[firstGuestIndex:firstGuestIndex + 12]:
		if not each:
			break
		guest_x += 1

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
	
@application.route('/invite/<mealid>/<host>/<guests>')
def invite(mealid=None):
	if not mealid:
		return redirect(url_for('home'))

	guestList = json.loads(guests)
	
	for each in guestList:
		query = "INSERT INTO ebdb.invitees (meal_id, host, guest) VALUES (\'%s\', \'%s\', \'%s\');" % (mealid, host, each)
		cursor.execute(query)
	return redirect(url_for('mymeals', uid=host))

####################################################### 

@application.route('/spritz')
@application.route('/spritzme/<filename>')
def spritz(filename=None):
	if not filename:
		return render_template('spritz/spritz.html')

	else:
		url = url_for('uploaded_file', filename=filename)
		with open(url) as fp:
			doc=slate.PDF(fp)

		console.log(doc[0])
		return render_template('spritz/spritz.html') 

@application.route('/spritz/login_success')
def spritz_login():
	return render_template('spritz/login_success.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@application.route('/spritz/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload File to be Spritzed</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@application.route('/spritz/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
	application.run(debug=True)