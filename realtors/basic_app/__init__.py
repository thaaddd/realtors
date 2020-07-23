from basic_app import config
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def load_models():
    from basic_app.az import models


load_models()


def init_extensions(app):
    db.init_app(app)


def init_views(app):
    from basic_app import az

    app.register_blueprint(az.bp, url_prefix="/az")


def create_app(config=config):
    app = Flask(__name__)
    app.config.from_object(config)

    init_extensions(app)
    init_views(app)

    return app


manager = Manager(create_app)


@manager.command
def init_db():

    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    db.init_app(flask_app)

    db.create_all()
