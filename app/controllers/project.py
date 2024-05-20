import json
from prometheus_http_client import Prometheus
from flask_restful import Resource, request
from app.helpers.utils import get_project_data

from app.helpers.authenticate import (
    jwt_required
)


class ProjectUsageView(Resource):
    @jwt_required
    def post(self, resource):
        if resource not in ['cpu', 'memory', 'network']:
            return dict(status='fail', message='Invalid resource name, pass cpu, memory, network'), 400

        project = get_project_data(request)

        if project.status_code != 200:
            return dict(status='fail', message=project.message), project.status_code

        start = project.start
        end = project.end
        step = project.step
        namespace = project.namespace
        prometheus = Prometheus()

        try:
            if resource == 'cpu':
                prom_data = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric='sum(rate(container_cpu_usage_seconds_total{container!="POD", image!="",namespace="' +
                    namespace+'"}[5m]))'
                )
            elif resource == 'memory':
                prom_data = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric='sum(rate(container_memory_usage_bytes{container_name!="POD", image!="", namespace="'+namespace+'"}[5m]))')
            elif resource == 'network':
                prom_data = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric='sum(rate(container_network_receive_bytes_total{namespace="' +
                    namespace+'"}[5m]))'
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
                mem_case = {'timestamp': float(
                    value[0]), 'value': float(value[1])}
                final_data_list.append(mem_case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', resource=resource, data=dict(values=final_data_list)), 200

        project = get_project_data(project_id, request)

        if project.status_code != 200:
            return dict(status='fail', message=project.message), project.status_code

        start = project.start
        end = project.end
        step = project.step
        namespace = project.namespace
        prometheus = Prometheus()

        try:
            prom_ntw_data = prometheus.query_rang(
                start=start,
                end=end,
                step=step,
                metric='sum(rate(container_network_receive_bytes_total{namespace="' +
                namespace+'"}[5m]))'
            )
        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        if not prom_ntw_data:
            return dict(status='fail', message="Failed to connect to prometheus"), 500

        try:
            new_data = json.loads(prom_ntw_data)
        except Exception as error:
            return dict(status='fail', message=str(prom_ntw_data)), 500

        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                mem_case = {'timestamp': float(
                    value[0]), 'value': float(value[1])}
                final_data_list.append(mem_case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', data=dict(values=final_data_list)), 200
