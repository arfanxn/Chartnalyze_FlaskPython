from wtforms import Form, PasswordField, validators

class UpdateUserPasswordForm(Form):
    current_password = PasswordField('Current Password', [validators.DataRequired(), validators.Length(min=8, max=50)])

    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo('password')])