from wtforms import Form
from app.helpers.form_helpers import try_validate   

Form.try_validate = try_validate