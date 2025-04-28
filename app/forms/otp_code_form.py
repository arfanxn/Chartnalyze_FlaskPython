from wtforms import Form, EmailField, IntegerField, validators

class OtpCodeForm(Form):
    code = IntegerField('Code', [validators.DataRequired(), validators.NumberRange(min=100000, max=999999)])