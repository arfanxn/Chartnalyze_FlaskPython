from wtforms import Form, StringField, validators
from app.enums.role_enums import RoleName 

class AssignUserRoleForm(Form):
    user_id = StringField('User Id', [validators.DataRequired(), validators.Length(min=26, max=26)])
    role_name = StringField('Role Name', [validators.DataRequired(), validators.AnyOf([RoleName.ANALYST.value, RoleName.USER.value])])