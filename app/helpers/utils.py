import requests
import os
import datetime
from app.schemas import MetricsSchema
from types import SimpleNamespace

PRODUCT_BASE_URL = os.getenv('PRODUCT_BASE_URL')
PROJECT_ENDPOINT = f"{PRODUCT_BASE_URL}/projects"
APP_ENDPOINT = f"{PRODUCT_BASE_URL}/apps"
DATABASE_ENDPOINT = f"{PRODUCT_BASE_URL}/database"


def get_project_data(project_id, request):
    project_query_data = request.get_json()

    metric_schema = MetricsSchema()

    validated_query_data = metric_schema.load(
        project_query_data)

    # if errors:
    #     return dict(status='fail', message=errors), 400

    current_time = datetime.datetime.now()
    yesterday_time = current_time + datetime.timedelta(days=-1)

    start = validated_query_data.get('start', yesterday_time.timestamp())
    end = validated_query_data.get('end', current_time.timestamp())
    step = validated_query_data.get('step', '1h')

    project_response = requests.get(
        f"{PROJECT_ENDPOINT}/{project_id}", headers={
            "accept": "application/json",
            "Authorization": request.headers.get('Authorization')
        })

    if not project_response.ok:
        return SimpleNamespace(status='failed', message="Failed to fetch project for current user", status_code=400)

    project_response = project_response.json()

    project_data = project_response['data']['project']

    namespace = project_data['alias']
    prometheus_url = project_data['cluster']['prometheus_url']
    if not prometheus_url:
        return SimpleNamespace(status='fail', message='No prometheus url provided', status_code=404)

    os.environ["PROMETHEUS_URL"] = prometheus_url
    return SimpleNamespace(
        start=start,
        end=end,
        step=step,
        namespace=namespace,
        status_code=200
    )


def get_app_data(project_id, app_id, request):
    app_query_data = request.get_json()

    metric_schema = MetricsSchema()

    validated_query_data = metric_schema.load(
        app_query_data)

    # if errors:
    #   return dict(status='fail', message=errors), 400

    current_time = datetime.datetime.now()
    yesterday_time = current_time + datetime.timedelta(days=-1)

    start = validated_query_data.get('start', yesterday_time.timestamp())
    end = validated_query_data.get('end', current_time.timestamp())
    step = validated_query_data.get('step', '1h')

    # get project details
    project_response = requests.get(
        f"{PROJECT_ENDPOINT}/{project_id}", headers={
            "accept": "application/json",
            "Authorization": request.headers.get('Authorization')
        })

    if not project_response.ok:
        return SimpleNamespace(status='failed', message="Failed to fetch project for current user", status_code=400)

    project_response = project_response.json()
    project_data = project_response['data']['project']

    # get app details
    app_response = requests.get(
        f"{APP_ENDPOINT}/{app_id}", headers={
            "accept": "application/json",
            "Authorization": request.headers.get('Authorization')
        }
    )

    if not app_response.ok:
        return SimpleNamespace(status='failed', message="Failed to fetch app for current user", status_code=400)

    app_response = app_response.json()
    app_data = app_response['data']['apps']

    app_alias = app_data['alias']
    namespace = project_data['alias']

    prometheus_url = project_data['cluster']['prometheus_url']
    if not prometheus_url:
        return SimpleNamespace(status='fail', message='No prometheus url provided', status_code=404)

    os.environ["PROMETHEUS_URL"] = prometheus_url
    return SimpleNamespace(
        start=start,
        end=end,
        step=step,
        app_alias=app_alias,
        namespace=namespace,
        status_code=200
    )


def get_database_data(project_id, database_id, request):
    database_query_data = request.get_json()

    metric_schema = MetricsSchema()

    validated_query_data = metric_schema.load(
        database_query_data)

    current_time = datetime.datetime.now()
    yesterday_time = current_time + datetime.timedelta(days=-1)

    start = validated_query_data.get('start', yesterday_time.timestamp())
    end = validated_query_data.get('end', current_time.timestamp())
    step = validated_query_data.get('step', '1h')


    # get project details
    project_response = requests.get(
        f"{PROJECT_ENDPOINT}/{project_id}", headers={
            "accept": "application/json",
            "Authorization": request.headers.get('Authorization')
        })

    if not project_response.ok:
        return SimpleNamespace(status='failed', message="Failed to fetch project for current user", status_code=400)

    project_response = project_response.json()
    project_data = project_response['data']['project']

    # get database details
    database_response = requests.get(
        f"{DATABASE_ENDPOINT}/{database_id}", headers={
            "accept": "application/json",
            "Authorization": request.headers.get('Authorization')
        }
    )

    if not database_response.ok:
        return SimpleNamespace(status='failed', message="Failed to fetch databases", status_code=400)

    database_response = database_response.json()

    
    prometheus_url = project_data['cluster']['prometheus_url']
    if not prometheus_url:
        return SimpleNamespace(status='fail', message='No prometheus url provided', status_code=404)

    # os.environ["PROMETHEUS_URL"]  = "http://localhost:9090"

    os.environ["PROMETHEUS_URL"] = prometheus_url
    return SimpleNamespace(
        start=start,
        end=end,
        step=step,
        database=database_response.name,
        flavour=database_response.database_flavour_name ,
        status_code=200
    )



