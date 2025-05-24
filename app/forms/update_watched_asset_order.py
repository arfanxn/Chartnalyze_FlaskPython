from wtforms import Form, IntegerField, StringField, validators

class UpdateWatchedAssetOrderForm(Form):
    key = StringField('Key', [validators.DataRequired()])
    order = IntegerField('Order', [validators.DataRequired()])