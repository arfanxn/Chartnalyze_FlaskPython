from wtforms import Form, StringField, validators

class StoreWatchedAssetForm(Form):
    key = StringField('Key', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    symbol = StringField('Symbol', [validators.DataRequired()])
    image_url = StringField('Image Url', [validators.DataRequired()])