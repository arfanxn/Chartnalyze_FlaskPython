from wtforms import Form, StringField, IntegerField, validators

class QueryForm(Form):
    keyword = StringField('Keyword', [validators.Optional()])
    page = IntegerField('Page', [validators.Optional()], default=1)
    per_page = IntegerField('Integer Field', [validators.Optional()], default=10)
    joins = StringField('Joins', [validators.Optional()])
    filters = StringField('Wheres', [validators.Optional()])