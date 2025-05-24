from wtforms import Form, StringField, IntegerField, validators

class StoreWatchedAssetForm(Form):
    key = StringField('Key', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    symbol = StringField('Symbol', [validators.DataRequired()])
    order = IntegerField('Order', [validators.Optional()])
    image_url = StringField('Image Url', [validators.DataRequired()])