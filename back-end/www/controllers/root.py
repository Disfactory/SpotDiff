"""The controller for https://[PATH]/"""

from models.model import User
from models.model_operations import user_operations
from flask import Blueprint


bp = Blueprint("root", __name__)


@bp.route("/")
def hello_world():
    #print(User.query.all())
    users = user_operations.get_all_users()
    print("Users: ", len(users))
    return_string = "Hello, world! {}".format(len(users))
    #return "Hello, World!"
    return return_string
