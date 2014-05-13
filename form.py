from wtforms import Form, BooleanField, TextField, IntegerField, validators
from wtforms.validators import ValidationError, Required, Email, URL
from wtforms.fields import HiddenField, RadioField, SelectField
from wtforms_components import TimeField

from datetime import date, datetime
from wtforms_html5 import DateField, DateRange

import locale
locale.setlocale(locale.LC_ALL, 'en_GB.utf8')

class MealForm(Form):

	currentYear = int(datetime.now().strftime('%Y'))
	currentMonth = int(datetime.now().strftime('%m'))
	currentDay  = int(datetime.now().strftime('%d'))

	place = SelectField(u'Choose a place', choices=[('Forbes', 'Forbes'), ('Mathey', 'Mathey'), ('Rocky', 'Rocky'), ('Whitman', 'Whitman'), ('Wilcox', 'Wilcox'), ('Wu', 'Wu'), ('Cannon', 'Cannon'), ('Cap and Gown', 'Cap and Gown'), ('Charter', 'Charter'), ('Cloister', 'Cloister'), ('Colonial', 'Colonial'), ('Cottage', 'Cottage'), ('Ivy', 'Ivy'), ('Quad', 'Quad'), ('Terrace', 'Terrace'), ('Tiger Inn', 'Tiger Inn'), ('Tower', 'Tower')])
	time = TimeField('Time (hh:mm)', [Required(message=(u'Invalid Time.'))])
	# format='%m/%d/%y', 
<<<<<<< HEAD
	date = DateField('Date (mm/dd/yyyy) in the next month', format='%m/%d/%Y', validators=[DateRange(min=date(currentMonth, currentDay, currentYear), max=date((currentMonth+1) % 12, min(currentDay, 28)))], currentYear)
	priv = RadioField('Friends-only or Public', [Required()], choices=[('pvt', 'Private'), ('pub', 'Public')])
=======
	date = DateField('Date (mm/dd/yyyy) in the next month', format='%m/%d/%Y', validators=[Required(message=(u'Date is invalid.')), DateRange(min=date(currentYear, currentMonth, currentDay), max=date(currentYear, (currentMonth+1) % 12, min(currentDay, 28)))])
	priv = RadioField('Friends-only or Public', [Required(message=(u'Private or public?'))], choices=[('pvt', 'Private'), ('pub', 'Public')])
>>>>>>> FETCH_HEAD
	uid = HiddenField('')

def validate_email(form, field):
	if "@princeton.edu" not in field.data.lower():
		raise ValidationError(u'Must have a @princeton.edu email address')

class Signup(Form):
	firstname = TextField('First Name', [Required(), validators.Length(min=1, max=44)])
	lastname = TextField('Last Name', [Required(), validators.Length(min=1, max=44)])
	email = TextField('Email', [Required(), Email(), validate_email])
	uid = HiddenField('', [Required()])
	picurl = HiddenField('')