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
    print(res)
    return jsonify(res)


@api.after_request
def after_request(response):
    """ Logging every api request. """
    app.logger.info(
        "%s [%s] %s %s %s %s %s %s %s",
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
