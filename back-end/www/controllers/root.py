"""The controller for https://[PATH]/"""

from models.model import User
from models.model_operations import user_operations
from models.model_operations import location_operations
from models.model_operations import answer_operations
from flask import Blueprint


bp = Blueprint("root", __name__)


@bp.route("/")
def hello_world():
    if False:
        users = user_operations.get_all_users()
        location_count = location_operations.get_location_count()
        #gold_answer_count = answer_operations.get_gold_answer_count()

        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4

    
        answer_operations.create_answer(1, 3, 2000, 2010, "", 0, 1, 0, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer_operations.create_answer(1, 4, 2000, 2010, "", 0, 1, 0, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        gold_answer_count = answer_operations.get_gold_answer_count()
        answer_count = answer_operations.get_answer_count()
        #location_count = 10
        #print("Users: ", len(users))
        #return_string = "Hello, world! users:{} ".format(len(users))
        return_string = "Hello, world! users:{} locations:{} answers:{}".format(len(users), location_count, answer_count)
        #return_string = "Hello, world! users:{} locations:".format(0, location_count)
        #return "Hello, World!"
        return return_string
    else:
        return "Hello, World!"
    
    