from wtforms import Form, StringField, validators 

class SavePostForm(Form):
    title = StringField('Title', [validators.Optional(), validators.Length(min=2, max=50)])
    body = StringField('Body', [validators.DataRequired()])