from wtforms import Form, EmailField, IntegerField, validators

class UpdateUserEmailForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.email(), validators.Length(min=2, max=50)]) # the new email
    code = IntegerField('Code', [validators.DataRequired(), validators.NumberRange(min=100000, max=999999)])