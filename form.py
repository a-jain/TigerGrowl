from wtforms import Form, BooleanField, TextField, IntegerField, validators
from wtforms.validators import ValidationError, Required, Email, URL
from wtforms.fields import HiddenField, RadioField, SelectField
from wtforms_components import TimeFieldk, DateTimeField

from datetime import date
from wtforms_html5 import DateField

class MealForm(Form):
    place = SelectField(u'Choose a place', choices=[('Forbes', 'Forbes'), ('Mathey', 'Mathey'), ('Rocky', 'Rocky'), ('Whitman', 'Whitman'), ('Wilcox', 'Wilcox'), ('Wu', 'Wu'), ('Cannon', 'Cannon'), ('Cap and Gown', 'Cap and Gown'), ('Charter', 'Charter'), ('Cloister', 'Cloister'), ('Colonial', 'Colonial'), ('Cottage', 'Cottage'), ('Ivy', 'Ivy'), ('Quad', 'Quad'), ('Terrace', 'Terrace'), ('Tiger Inn', 'Tiger Inn'), ('Tower', 'Tower')])
    time = TimeField('Time (hh:mm)', [Required()])
    # format='%m/%d/%y', 
    date = DateField('Date (mm/dd)', validators=[Required(), DateRange(min=datetime(2014, 01, 12), max=datetime(2015, 01, 02))])
    priv = RadioField('Friends-only or Public', [Required()], choices=[('pvt', 'Private'), ('pub', 'Public')])
    uid = HiddenField('')

def validate_email(form, field):
	if "@princeton.edu" not in field.data.lower():
		raise ValidationError(u'Must have a @princeton.edu email address')

class Signup(Form):
	firstname = TextField('First Name', [Required(), validators.Length(min=2, max=45)])
	lastname = TextField('Last Name', [Required(), validators.Length(min=2, max=45)])
	email = TextField('Email', [Required(), Email(), validate_email])
	uid = HiddenField('', [Required()])
	picurl = HiddenField('')