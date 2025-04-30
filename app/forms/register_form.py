from wtforms import Form, StringField, DateField, EmailField, PasswordField, validators 

class RegisterForm(Form):
    name = StringField('Name', [validators.Optional(), validators.Length(min=2, max=50)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=2, max=16)])
    birth_date = DateField('Birth Date', [validators.Optional()], format='%Y-%m-%d')
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo('password')])

