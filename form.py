from wtforms import Form, BooleanField, TextField, IntegerField, validators
from wtforms.validators import ValidationError, Required, Email, URL
from wtforms.fields import HiddenField, RadioField, SelectField, DateField
from wtforms_components import TimeField, DateRange

from datetime import date, datetime


def validate_date(form, field):
	if "2014" not in str(field.data) and "2015" not in str(field.data):
		raise ValidationError(u'Don\'t get ahead of yourself!')

class MealForm(Form):

	currentYear = int(datetime.now().strftime('%Y'))
	currentMonth = int(datetime.now().strftime('%m'))
	currentDay  = int(datetime.now().strftime('%d'))

	place = SelectField(u'Choose a place', choices=[('Forbes', 'Forbes'), ('Mathey', 'Mathey'), ('Rocky', 'Rocky'), ('Whitman', 'Whitman'), ('Wilcox', 'Wilcox'), ('Wu', 'Wu'), ('Cannon', 'Cannon'), ('Cap and Gown', 'Cap and Gown'), ('Charter', 'Charter'), ('Cloister', 'Cloister'), ('Colonial', 'Colonial'), ('Cottage', 'Cottage'), ('Ivy', 'Ivy'), ('Quad', 'Quad'), ('Terrace', 'Terrace'), ('Tiger Inn', 'Tiger Inn'), ('Tower', 'Tower')])
	time = TimeField('Time (hh:mm)', [Required(message=(u'Invalid Time'))])
	date = DateField('Date (mm/dd/yyyy)', format='%m/%d/%Y', validators=[validate_date, Required(message=(u'Invalid Date')), DateRange(min=datetime.now().date())])
	priv = RadioField('Friends-only or Public', [Required(message=(u'Public or Private?'))], choices=[('pvt', 'Private'), ('pub', 'Public')])
	uid = HiddenField('', [Required()])

def validate_email(form, field):
	if "@princeton.edu" not in field.data.lower():
		raise ValidationError(u'Must have a @princeton.edu email address')

class Signup(Form):
	firstname = TextField('First Name', [Required(message=(u'Invalid Name')), validators.Length(min=1, max=44)])
	lastname = TextField('Last Name', [Required(message=(u'Invalid Name')), validators.Length(min=1, max=44)])
	email = TextField('Email', [Required(message=(u'Invalid Email')), Email(), validate_email])
	uid = HiddenField('', [Required()])
	picurl = HiddenField('')