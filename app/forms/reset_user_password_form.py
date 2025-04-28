from wtforms import Form, PasswordField, IntegerField, validators

class ResetUserPasswordForm(Form):
    code = IntegerField('Code', [validators.DataRequired(), validators.NumberRange(min=100000, max=999999)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo('password')])