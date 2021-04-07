import logging
from datetime import datetime

from elasticsearch import Elasticsearch, RequestsHttpConnection
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, render_template, request

api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def index():
    return jsonify({"message": "👋🌎"})


@api.route("/es", methods=["GET"])
def es_test():
    es = Elasticsearch(
        hosts=[{"host": "host.docker.internal", "port": 9200}],
        connection_class=RequestsHttpConnection,
        max_retries=30,
        retry_on_timeout=True,
        request_timeout=30,
    )
    res = es.search(index="salary", body={"query": {"match_all": {}}})
    return jsonify(res)


@api.route("/stats", methods=["POST"])
def get_salary_statistics():
    json_body = request.get_json()
    if json_body:
        location = json_body.get("location")
        job_title = json_body.get("job_title")
    else:
        location = request.args.get("location")
        job_title = request.args.get("job_title")

    query_filters = []

    if location:
        query_filters.append(
            {"multi_match": {"query": location, "fields": ["city", "state"]}}
        )

    if job_title:
        query_filters.append(
            {"match": {"job_title": {"query": job_title, "fuzziness": "AUTO"}}}
        )

    es = Elasticsearch(
        hosts=[{"host": "host.docker.internal", "port": 9200}],
        connection_class=RequestsHttpConnection,
        max_retries=30,
        retry_on_timeout=True,
        request_timeout=30,
    )

    res = es.search(
        index="salary",
        body={
            "query": {
                "bool": {"must": query_filters if query_filters else {"match_all": {}}}
            },
            "size": 0,
            "aggs": {
                "mean_salary": {"avg": {"field": "wage_rate"}},
                "median_salary": {
                    "percentiles": {"field": "wage_rate", "percents": [50]}
                },
                "salary_percentiles": {
                    "percentiles": {"field": "wage_rate", "percents": [25, 75]}
                },
            },
        },
    )
    result = {
        "statistics": res["aggregations"],
        "num_results": res["hits"]["total"]["value"],
    }
    return jsonify(result)


@api.after_request
def after_request(response):
    """ Logging every api request. """
    app.logger.info(
        "%s [%s] %s %s %s %s %s %s",
        request.remote_addr,
        datetime.utcnow(),
        request.method,
        request.path,
        request.scheme,
        response.status,
        response.content_length,
        request.user_agent,
    )
    return response
