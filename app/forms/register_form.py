from wtforms import Form, StringField , EmailField, PasswordField, validators 

class RegisterForm(Form):
    username = StringField(
        'Username', 
        [
            validators.DataRequired(message='Username is required'), 
            validators.Length(min=2, max=16, message='Username must be between 2 and 16 characters')
        ]
    )
    email = EmailField(
        'Email', 
        [
            validators.DataRequired(message='Email is required'), 
            validators.Email(message='Email is invalid')
        ]
    )
    password = PasswordField(
        'Password', 
        [
            validators.DataRequired(message='Password is required'), 
            validators.Length(min=8, max=50, message='Password must be between 8 and 50 characters')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        [
            validators.DataRequired(message='Confirm password is required'), 
            validators.Length(min=8, max=50, message='Confirm password must be between 8 and 50 characters'), 
            validators.EqualTo('password', message='Passwords do not match')
        ]
    )

