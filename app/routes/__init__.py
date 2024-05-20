from flask_restful import Api
from app.controllers import (
    IndexView, ProjectUsageView, AppUsageView)

api = Api()

# Index route
api.add_resource(IndexView, '/')

# Projects routes
api.add_resource(ProjectUsageView,
                 '/projects/<string:resource>/metrics', endpoint='project_usage')
# Apps routes
api.add_resource(AppUsageView,
                 '/apps/<string:resource>/metrics', endpoint='app_usage')
