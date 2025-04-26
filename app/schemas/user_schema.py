from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.String(dump_only=True, validate=validate.Length(26))
    name = fields.String(required=True, validate=validate.Length(max=50))
    birth_date = fields.Date(required=True, format="%Y-%m-%d")
    email = fields.Email(required=True, validate=validate.Length(max=50))
    password = fields.String(
        required=True, 
        load_only=True,
        validate=validate.Length(min=8, max=255)
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)