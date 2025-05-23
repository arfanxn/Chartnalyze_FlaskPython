from wtforms import Form, StringField, validators

class AssignUserRoleForm(Form):
    user_id = StringField('User Id', [validators.DataRequired(), validators.Length(min=26, max=26)])
    role_id = StringField('Role Id', [validators.DataRequired(), validators.Length(min=26, max=26)])
