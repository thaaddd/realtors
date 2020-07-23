import os

DEBUG = True
SECRET_KEY = "dev"


SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/realtors",
)


CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_ALWAYS_EAGER = False
SQLALCHEMY_TRACK_MODIFICATIONS = False


# docker-compose run db psql -h db -U hello_flask -d hello_flask_dev
