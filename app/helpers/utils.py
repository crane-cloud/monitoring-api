import requests
import os
import datetime
from app.schemas import MetricsSchema
from types import SimpleNamespace

PRODUCT_BASE_URL = os.getenv('PRODUCT_BASE_URL')
PROJECT_ENDPOINT = f"{PRODUCT_BASE_URL}/projects"


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
