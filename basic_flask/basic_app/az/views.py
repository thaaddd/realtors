from basic_app.az import bp
from basic_app.az.models import Broker, Realtor, to_json
from basic_app.az.tasks import (
    cache_brokers as cache_brokers_task,
    cache_realtors as cache_realtors_task,
)
from flask import request

# @app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE', 'PATCH'])


@bp.route("/realtors", methods=["GET"])
def realtors():
    args = dict(request.args)
    limit = min(int(args.pop("limit", 0)) or 25, 100)
    order_by = args.pop("order_by", "id")
    offset = int(args.pop("offset", 0))

    # only going to do exact match filtering for now
    filters = {}
    for column in Realtor.__table__.columns:
        if column.name in args:
            filters[column.name] = args[column.name]

    query = (
        Realtor.query.filter_by(**filters)
        .order_by(order_by)
        .limit(limit)
        .offset(offset)
    )

    return to_json(query.all(), Realtor)


@bp.route("/brokers", methods=["GET"])
def brokers():
    "return all brokers"

    args = dict(request.args)
    limit = min(int(args.pop("limit", 0)) or 25, 100)
    order_by = args.pop("order_by", "id")
    offset = int(args.pop("offset", 0))

    # only going to do exact match filtering for now
    filters = {}
    for column in Broker.__table__.columns:
        if column.name in args:
            filters[column.name] = args[column.name]

    query = (
        Broker.query.filter_by(**filters).order_by(order_by).limit(limit).offset(offset)
    )

    return to_json(query.all(), Broker)


@bp.route("/brokers/<int:id>", methods=["GET"])
def get_broker(id):
    broker = Broker.query.filter_by(id=id).first_or_404()
    return broker.json


@bp.route("/realtors/<int:id>", methods=["GET"])
def get_realtor(id):
    realtor = Realtor.query.filter_by(id=id).first_or_404()
    return realtor.json


@bp.route("/brokers/cache")
def cache_brokers():
    result = cache_brokers_task.delay()
    return "Caching Brokers"


@bp.route("/realtors/cache")
def cache_realtors():
    result = cache_realtors_task.delay()
    return "Caching Realtors"
