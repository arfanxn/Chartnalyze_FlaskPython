from wtforms import Form
from werkzeug.exceptions import UnprocessableEntity

def try_validate (form: Form): 
    if form.validate() == False:    
        raise UnprocessableEntity(form.errors)
    return True