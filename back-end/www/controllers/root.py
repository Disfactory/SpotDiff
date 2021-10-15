"""The controller for https://[PATH]/"""

from models.model import User
from flask import Blueprint


bp = Blueprint("root", __name__)


@bp.route("/")
def hello_world():
    print(User.query.all())
    return "Hello, World!"
