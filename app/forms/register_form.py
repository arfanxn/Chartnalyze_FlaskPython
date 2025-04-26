from wtforms import Form, StringField , EmailField, PasswordField, validators 

class RegisterForm(Form):
    username = StringField(
        'Username', 
        [
            validators.DataRequired(), 
            validators.Length(min=2, max=16)
        ]
    )
    email = EmailField(
        'Email', 
        [
            validators.DataRequired(), 
            validators.Email()
        ]
    )
    password = PasswordField(
        'Password', 
        [
            validators.DataRequired(), 
            validators.Length(min=8, max=50)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        [
            validators.DataRequired(), 
            validators.Length(min=8, max=50), 
            validators.EqualTo('password')
        ]
    )

