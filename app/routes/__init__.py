from flask_restful import Api
from app.controllers import (
    IndexView, ProjectCPUView, ProjectMemoryUsageView,
    ProjectNetworkRequestView, AppCpuUsageView, AppMemoryUsageView, AppNetworkUsageView)

api = Api()

# Index route
api.add_resource(IndexView, '/')

# Projects routes
api.add_resource(ProjectCPUView, '/projects/<string:project_id>/metrics/cpu')
api.add_resource(ProjectMemoryUsageView,
                 '/projects/<string:project_id>/metrics/memory')
api.add_resource(ProjectNetworkRequestView,
                 '/projects/<string:project_id>/metrics/network')

# Apps routes
api.add_resource(AppMemoryUsageView,
                 '/projects/<string:project_id>/apps/<string:app_id>/memory')
api.add_resource(
    AppCpuUsageView, '/projects/<string:project_id>/apps/<string:app_id>/cpu')
api.add_resource(AppNetworkUsageView,
                 '/projects/<string:project_id>/apps/<string:app_id>/network')
