import json
from prometheus_http_client import Prometheus
from flask_restful import Resource, request

from app.helpers.authenticate import (
    jwt_required
)
from app.helpers.utils import get_database_data
import os


class DatabaseSizeView(Resource):

    @jwt_required
    def post(self , project_id , database_id):

        database = get_database_data(project_id,database_id ,request)

        if database.status_code != 200:
            return dict(status='fail' , message = "An error occured getting database information") , database.status_code

        start = database.start
        end = database.end
        step = database.step

        prometheus = Prometheus()
        try:
            if (database.flavour == 'postgres'):
                data  = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric="sum(rate(pg_database_size_bytes{datname='" + database.name + "'}[5m]))"
                )
            else :
                return dict(status='success' , data=dict(message="Mysql not yet supported")),200
        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        new_data = json.loads(data)
        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                mem_case = {'timestamp': float(
                    value[0]), 'value': float(value[1])}
                final_data_list.append(mem_case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', data=dict(values=final_data_list)), 200



class DatabaseConnectionsView(Resource):

    @jwt_required
    def post(self , project_id , database_id):

        database = get_database_data(project_id,database_id ,request)

        if database.status_code != 200:
            return dict(status='fail' , message = "An error occured getting database information") , database.status_code

        start = database.start
        end = database.end
        step = database.step

        prometheus = Prometheus()
        try:
            if (database.flavour == 'postgres'):

                data  = prometheus.query_rang(
                    start=start,
                    end=end,
                    step=step,
                    metric="sum(rate(pg_stat_activity_count{datname='" + database.name + "'}[5m]))"
                )

            else :
                return dict(status='success' , data=dict(message="Mysql not yet supported")),200

        except Exception as error:
            return dict(status='fail', message=str(error)), 500

        new_data = json.loads(data)
        final_data_list = []

        try:
            for value in new_data["data"]["result"][0]["values"]:
                mem_case = {'timestamp': float(
                    value[0]), 'value': float(value[1])}
                final_data_list.append(mem_case)
        except:
            return dict(status='fail', message='No values found'), 404

        return dict(status='success', data=dict(values=final_data_list)), 200


