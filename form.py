from wtforms import Form, BooleanField, TextField, IntegerField, validators
from wtforms.validators import ValidationError, Required, Email, URL
from wtforms.fields import HiddenField, DateField, RadioField
from wtforms_components import TimeField

class MealForm(Form):
    host = TextField('Host', [Required(), validators.Length(min=3, max=45)])
    place = TextField('Place', [Required(), validators.Length(min=3, max=45)])
    time = TimeField('Time', [Required()])
    date = DateField('Date (mm/dd)', format='%m/%d', validators=[Required()])
    priv = RadioField('Friends-only or Public', choices=[('pvt', 'Private'), ('pub', 'Public')])
    uid = HiddenField('', [Required()])

def validate_email(form, field):
	if "@princeton.edu" not in field.data.lower():
		raise ValidationError(u'Must have a @princeton.edu email address')

class Signup(Form):
	firstname = TextField('First Name', [Required(), validators.Length(min=2, max=45)])
	lastname = TextField('Last Name', [Required(), validators.Length(min=2, max=45)])
	email = TextField('Email', [Required(), Email(), validate_email])
	uid = HiddenField('', [Required()])
	picurl = HiddenField('')