"""The controller for https://[PATH]/"""

from models.model import User
from models.model_operations import user_operations
from models.model_operations import location_operations
from flask import Blueprint


bp = Blueprint("root", __name__)


@bp.route("/")
def hello_world():
    #print(User.query.all())
    users = user_operations.get_all_users()
    location_count = location_operations.get_location_count()
    #location_count = 10
    #print("Users: ", len(users))
    #return_string = "Hello, world! users:{} ".format(len(users))
    return_string = "Hello, world! users:{} locations:{}".format(len(users), location_count)
    #return_string = "Hello, world! users:{} locations:".format(0, location_count)
    #return "Hello, World!"
    return return_string
