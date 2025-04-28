from wtforms import Form, EmailField, validators

class SendOtpForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.email(), validators.Length(min=2, max=50)])