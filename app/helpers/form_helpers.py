from wtforms import Form
from app.exceptions import ValidationException

def get_error_message(form: Form, field_name: str = None):
    """
    Get the first error message from a form. If `field_name` is specified,
    return the first error message from that field. Otherwise, return the
    first error message from the first field with errors.

    :param form: The form to get the error message from.
    :type form: Form
    :param field_name: The name of the field to get the error message from.
    :type field_name: str
    :return: The first error message from the form or field, or None if no errors.
    :rtype: str or None
    """
    # If no field_name is provided, get the first error message from the first field with errors
    if field_name is None:
        for field_errors in form.errors.values():
            if field_errors:  # Check if the list of errors is not empty
                return field_errors[0]  # Return the first error message
        return None  # No errors found
    
    # If field_name is provided, return the first error message from that specific field
    if field_name in form.errors:
        return form.errors[field_name][0] if form.errors[field_name] else None
    
    return None  # If the field has no errors or does not exist


def try_validate (form: Form): 
    if form.validate() == False:    
        message = get_error_message(form)
        raise ValidationException(message, form.errors)
    
    return True
