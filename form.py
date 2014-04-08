from wtforms import Form, BooleanField, TextField, IntegerField, PasswordField, validators

class MealForm(Form):
    mealtable = IntegerField('Meal ID', [validators.NumberRange(min=40, max=110000000)])
    host = TextField('Host', [validators.Length(min=3, max=35)])
    place = TextField('Place', [validators.Length(min=3, max=35)])

class Signup(Form):
	firstname = TextField('First', [validators.Length(min=3, max=35)])
	lastname = TextField('Last', [validators.Length(min=3, max=35)])
	email = TextField('Email', [validate_email])

def validate_email(form, field):
	if "@princeton.edu" not in field:
		raise ValidationError(u'Must be a Princetonian!')