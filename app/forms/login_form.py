from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    identifier = StringField('Identifier', [validators.DataRequired(), validators.Length(min=2, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=50)])