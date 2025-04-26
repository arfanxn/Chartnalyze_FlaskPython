def create_response_body (status: int, message: str, data=None, additionals=None):
    body = {
        "status": status,
        "message": message,
    }

    if data is not None:
        body["data"] = data

    if additionals is not None:
        body.update(additionals)

    return body

def create_response_tuple (status: int, message: str, data=None, additionals=None):
    return create_response_body(status=status, message=message, data=data, additionals=additionals), status