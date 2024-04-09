from flask_restful import Api
from app.controllers import (
    IndexView, ProjectCPUView, ProjectMemoryUsageView,
    ProjectNetworkRequestView, ProjectStorageUsageView, IndexView)

api = Api()

# Index route
api.add_resource(IndexView, '/')

# Projects routes
api.add_resource(ProjectCPUView, '/projects/<string:project_id>/metrics/cpu')
api.add_resource(ProjectMemoryUsageView,
                 '/projects/<string:project_id>/metrics/memory')
api.add_resource(ProjectNetworkRequestView,
                 '/projects/<string:project_id>/metrics/network')
api.add_resource(ProjectStorageUsageView,
                 '/projects/<string:project_id>/metrics/storage')
