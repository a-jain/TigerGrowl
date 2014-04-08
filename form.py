from wtforms import Form, BooleanField, TextField, IntegerField, PasswordField, validators
from wtforms.validators import ValidationError, Required, Email

class MealForm(Form):
    mealtable = IntegerField('Meal ID', [Required(), validators.NumberRange(min=40, max=110000000)])
    host = TextField('Host', [Required(), validators.Length(min=3, max=35)])
    place = TextField('Place', [Required(), validators.Length(min=3, max=35)])

def validate_email(form, field):
	if "@princeton.edu" not in field.data:
		raise ValidationError(u'Must be a Princetonian!')

class Signup(Form):
	firstname = TextField('First', [Required(), validators.Length(min=3, max=35)])
	lastname = TextField('Last', [Required(), validators.Length(min=3, max=35)])
	email = TextField('Email', [Required(), Email(), validate_email])

