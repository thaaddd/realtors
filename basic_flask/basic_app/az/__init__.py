from flask import Blueprint

bp = Blueprint("az", __name__, template_folder="templates")

from basic_app.az import views
