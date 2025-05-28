from wtforms import Form, StringField, validators 

class StoreCommentForm(Form):
    parent_id = StringField('Parent Id', [validators.Optional()])
    body = StringField('Body', [validators.DataRequired()])