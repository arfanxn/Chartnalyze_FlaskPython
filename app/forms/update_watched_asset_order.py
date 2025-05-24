from wtforms import Form, IntegerField, validators

class UpdateWatchedAssetOrderForm(Form):
    order = IntegerField('Order', [validators.DataRequired()])