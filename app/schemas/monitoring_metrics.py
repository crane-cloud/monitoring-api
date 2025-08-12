from marshmallow import Schema, fields, validate, ValidationError


def validate_timestamp(value):
    if value is None:
        return None  
        
    if isinstance(value, bool):
        raise ValidationError('Please send a timestamp value (numeric format)')
    
    # Check for date-like strings
    if isinstance(value, str) and any(char in value for char in ['-', '/', ':', 'T', 'Z']):
        raise ValidationError('Please send a timestamp value (numeric format), not a date string')
    
    # Convert to float
    try:
        timestamp = float(value)
    except (ValueError, TypeError):
        raise ValidationError('Please send a timestamp value (numeric format)')

    # Range check
    if timestamp < 0 or (timestamp < 1e10 and timestamp < 946684800) or timestamp > 4e12:
        raise ValidationError('Invalid timestamp range')
        
    return timestamp


class MetricsSchema(Schema):
    start = fields.Raw(validate=validate_timestamp, allow_none=True)
    end = fields.Raw(validate=validate_timestamp, allow_none=True)
    step = fields.String(validate=[
        validate.Regexp(
            regex=r'^(?!\s*$)', error='step value should be a valid string'
        )
    ])
    project_id = fields.String()
    project_name = fields.String()
    app_name = fields.String()
    app_id = fields.String()
    prometheus_url = fields.String()


class UserGraphSchema(Schema):
    start = fields.Date()
    end = fields.Date()
    set_by = fields.String(
        validate=[
            validate.OneOf(["year", "month"],
                           error='set_by should be year or month'
                           ),
        ])


class AppGraphSchema(Schema):
    start = fields.Date()
    end = fields.Date()
    set_by = fields.String(
        validate=[
            validate.OneOf(["year", "month"],
                           error='set_by should be year or month'
                           ),
        ])
