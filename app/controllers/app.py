import json
from prometheus_http_client import Prometheus
from flask_restful import Resource, request

from app.helpers.authenticate import (
    jwt_required
)
from app.helpers.utils import get_app_data, is_valid_prometheus_query


class AppUsageView(Resource):
    @jwt_required
    def post(self, resource):
        if resource not in ['cpu', 'memory', 'network']:
            return dict(status='fail', message='Invalid resource name, pass cpu, memory, network'), 400

        app = get_app_data(request)

        start = app.start
        end = app.end
        step = app.step
        app_alias = app.app_alias
        namespace = app.namespace
        prometheus = Prometheus()

        if step:
            is_valid, message = is_valid_prometheus_query(step, start, end)
            if not is_valid:
                return dict(status='fail', message=message), 400

        try:
            if resource == 'cpu':
                prom_data = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric='sum(rate(container_cpu_usage_seconds_total{container!="POD", image!="", namespace="' +
                    namespace + '", pod=~"' + app_alias + '.*"}[5m]))')
            elif resource == 'memory':
                prom_data = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric='sum(rate(container_memory_usage_bytes{container_name!="POD", image!="",pod=~"' + app_alias + '.*", namespace="' + namespace + '"}[5m]))')
            elif resource == 'network':
                prom_data = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric='sum(rate(container_network_receive_bytes_total{namespace="' +
                    namespace + '", pod=~"' + app_alias + '.*"}[5m]))'
                )
            else:
                return dict(status='fail', message='Invalid resource name, pass cpu, memory, network'), 400
        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        if not prom_data:
            return dict(status='fail', message="Failed to connect to prometheus"), 500

        try:
            new_data = json.loads(prom_data)
        except Exception as error:
            return dict(status='fail', message=str(prom_data)), 500

        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                case = {'timestamp': float(value[0]), 'value': float(value[1])}
                final_data_list.append(case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', resource=resource, data=dict(values=final_data_list)), 200
