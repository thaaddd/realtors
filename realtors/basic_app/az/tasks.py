from basic_app.celery import celery
from basic_app.az.models import Broker, Realtor


@celery.task()
def cache_brokers():
    Broker.cache()


@celery.task()
def cache_realtors():
    Realtor.cache()
    Realtor.match_to_brokers()
