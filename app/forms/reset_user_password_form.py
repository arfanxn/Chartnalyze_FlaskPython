from wtforms import Form, PasswordField, IntegerField, EmailField, validators

class ResetUserPasswordForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo('password')])
    code = IntegerField('Code', [validators.DataRequired(), validators.NumberRange(min=100000, max=999999)])