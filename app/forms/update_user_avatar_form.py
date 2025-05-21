from wtforms import Form, FileField, validators 
from app.helpers.form_helpers import allowed_file   

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class UpdateUserAvatarForm(Form):
    avatar = FileField('Avatar', [validators.Optional()])

    def validate_avatar(form, field): 
        if field.data:
            filename = field.data.filename
            if not allowed_file(filename, ALLOWED_EXTENSIONS):
                raise validators.ValidationError("File must be {} format".format(', '.join(sorted(ALLOWED_EXTENSIONS))))

