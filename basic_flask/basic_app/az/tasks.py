from basic_app.celery import celery
from basic_app.az.models import Broker


@celery.task()
def cache_brokers():
    Broker.cache()
