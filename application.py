from flask import Flask
from flask import render_template, flash, url_for
from flask import request
from flask import redirect
import MySQLdb
from form import *
import facebook

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

@application.route('/feedPrototype')
def feedPrototype():
	return render_template('feed.html')

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name="kevinisgay")

@application.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
	form = Signup(request.form)
	if request.method == 'POST' and form.validate():
		# user = User(form.mealtable.data, form.host.data, form.place.data)
		
		# user = facebook.get_user_from_cookie(self.request.cookies, '1423477091234772', 'e6db8e28a8f2a150534abd4d8a5f4399')
		# print user

		print form.firstname.data
		print form.lastname.data
		print form.email.data

		netid = form.email.data.split('@')[0]
		sql = "INSERT INTO ebdb.user_table (firstname, lastname, netid) VALUES (\'%s\', \'%s\', \'%s\');" % (form.firstname.data, form.lastname.data, netid)

		cursor.execute(sql)

		return redirect(url_for('hello'))
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