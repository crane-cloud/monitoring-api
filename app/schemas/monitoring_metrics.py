from marshmallow import Schema, fields, validate


class MetricsSchema(Schema):
    start = fields.Float()
    end = fields.Float()
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
