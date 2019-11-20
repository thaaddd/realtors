DEBUG = True
SECRET_KEY = "dev"

SQLALCHEMY_DATABASE_URI = "postgres://hello_flask:hello_flask@db:5432/hello_flask_dev"


CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_ALWAYS_EAGER = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
