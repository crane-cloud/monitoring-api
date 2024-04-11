import os
import datetime
import json
from types import SimpleNamespace


import datetime
from prometheus_http_client import Prometheus
from flask_restful import Resource, request
from flask import current_app, render_template

from app.helpers.authenticate import (
    jwt_required
)

# Todo: figure out a way to connect to projects and get projects


class ProjectMemoryUsageView(Resource):

    @jwt_required
    def post(self, project_id):
        return dict(status='success', data=dict()), 200


class ProjectCPUView(Resource):
    # @jwt_required
    def post(self, project_id):
        return dict(status='success', data=dict()), 200


class ProjectNetworkRequestView(Resource):
    # @jwt_required
    def post(self, project_id):
        return dict(status='success', data=dict()), 200


class ProjectStorageUsageView(Resource):
    # @jwt_required
    def post(self, project_id):
        return dict(status='success', data=dict()), 200
