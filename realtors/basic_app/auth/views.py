from basic_app.auth import bp
from basic_app.auth.models import User


@bp.route("/")
def helldo():
    # u = User.query.filter_by(username=username).first_or_404()
    # return "Hello, {}!".format(u.username)
    return "nichae"


@bp.route("/<username>")
def hello(username):
    # u = User.query.filter_by(username=username).first_or_404()
    return "Hello, {}!".format(username)
