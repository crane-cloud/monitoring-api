import json
from prometheus_http_client import Prometheus
from flask_restful import Resource, request

from app.helpers.authenticate import (
    jwt_required
)
from app.helpers.utils import get_app_data


class AppMemoryUsageView(Resource):
    @jwt_required
    def post(self, project_id, app_id):
        app = get_app_data(project_id, app_id, request)

        if app.status_code != 200:
            return dict(status='fail', message=app.message), app.status_code

        start = app.start
        end = app.end
        step = app.step
        app_alias = app.app_alias
        namespace = app.namespace
        prometheus = Prometheus()

        try:
            prom_memory_data = prometheus.query_rang(
                start=start,
                end=end,
                step=step,
                metric='sum(rate(container_memory_usage_bytes{container_name!="POD", image!="",pod=~"' + app_alias + '.*", namespace="' + namespace + '"}[5m]))')
        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        if not prom_memory_data:
            return dict(status='fail', message="Failed to connect to prometheus"), 500

        try:
            new_data = json.loads(prom_memory_data)
        except Exception as error:
            return dict(status='fail', message=str(prom_memory_data)), 500

        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                mem_case = {'timestamp': float(
                    value[0]), 'value': float(value[1])}
                final_data_list.append(mem_case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', data=dict(values=final_data_list)), 200


class AppCpuUsageView(Resource):
    @jwt_required
    def post(self, project_id, app_id):
        app = get_app_data(project_id, app_id, request)

        if app.status_code != 200:
            return dict(status='fail', message=app.message), app.status_code

        start = app.start
        end = app.end
        step = app.step
        app_alias = app.app_alias
        namespace = app.namespace
        prometheus = Prometheus()

        try:
            prom_cpu_data = prometheus.query_rang(
                start=start,
                end=end,
                step=step,
                metric='sum(rate(container_cpu_usage_seconds_total{container!="POD", image!="", namespace="' +
                namespace + '", pod=~"' + app_alias + '.*"}[5m]))')
        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        if not prom_cpu_data:
            return dict(status='fail', message="Failed to connect to prometheus"), 500

        try:
            new_data = json.loads(prom_cpu_data)
        except Exception as error:
            return dict(status='fail', message=str(prom_cpu_data)), 500

        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                case = {'timestamp': float(value[0]), 'value': float(value[1])}
                final_data_list.append(case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', data=dict(values=final_data_list)), 200


class AppNetworkUsageView(Resource):
    @jwt_required
    def post(self, project_id, app_id):
        app = get_app_data(project_id, app_id, request)

        if app.status_code != 200:
            return dict(status='fail', message=app.message), app.status_code

        start = app.start
        end = app.end
        step = app.step
        app_alias = app.app_alias
        namespace = app.namespace
        prometheus = Prometheus()

        try:
            prom_net_data = prometheus.query_rang(
                start=start,
                end=end,
                step=step,
                metric='sum(rate(container_network_receive_bytes_total{namespace="' +
                namespace + '", pod=~"' + app_alias + '.*"}[5m]))'
            )
        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        if not prom_net_data:
            return dict(status='fail', message="Failed to connect to prometheus"), 500

        try:
            new_data = json.loads(prom_net_data)
        except Exception as error:
            return dict(status='fail', message=str(prom_net_data)), 500

        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                case = {'timestamp': float(value[0]), 'value': float(value[1])}
                final_data_list.append(case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', data=dict(values=final_data_list)), 200
