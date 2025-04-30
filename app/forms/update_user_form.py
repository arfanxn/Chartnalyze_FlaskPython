from wtforms import Form, StringField, DateField, validators 

class UpdateUserForm(Form):
    name = StringField('Name', [validators.Optional() , validators.Length(min=2, max=50)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=16)])
    birth_date = DateField('Birth Date', [validators.Optional()], format='%Y-%m-%d')

