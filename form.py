from wtforms import Form, BooleanField, TextField, IntegerField, PasswordField, validators

class RegistrationForm(Form):
    mealtable = IntegerField('Meal ID', [validators.NumberRange(min=40, max=1100000)])
    host = TextField('Host', [validators.Length(min=3, max=35)])
    place = TextField('Place', [validators.Length(min=3, max=35)])