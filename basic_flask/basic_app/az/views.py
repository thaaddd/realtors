from basic_app.az import bp
from basic_app.az.models import Broker, to_json
from basic_app.az.tasks import cache_brokers
from flask import request

# @app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE', 'PATCH'])


@bp.route("/realtors", methods=["GET"])
def realtors():
    return "return all realtors"


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


@bp.route("/cache")
def cache():
    result = cache_brokers.delay()
    # result.wait()
    return "Caching"
