"""The controller for https://[PATH]/status/"""

from flask import Blueprint
from flask import request
from flask import jsonify
import jwt
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import decode_jwt
from config.config import config
from models.model_operations.user_operations import get_user_done_location_count
from models.model_operations.user_operations import get_user_count
from models.model_operations.location_operations import get_location_is_done_count
from models.model_operations.answer_operations import get_answer_count

bp = Blueprint("status_controller", __name__)
@bp.route("", methods=["GET"])
def status():
    """
    The function for the front-end to retrieve status data.

    Sample command to test:
    $ curl -H "Content-Type: application/json" -X GET http://localhost:5000/status?user_token=xxxx
    $ https://localhost:5000/status?user_token=xxxxx

    Parameters
    ----------
    user_token : str
        The encoded user JWT, issued by the back-end.
        (required)

    Returns
    -------
        The encoded JWT that stores status information, including:
        individual_done_count : Int
            Number of locations identified by the user.
        user_count : Int
            Number of total users.
        location_is_done_count : Int
            The number of locations that have been labeled.
    """    
    if request.method == "GET":
        user_token = request.args.get("user_token")
        if user_token is None:
            e = InvalidUsage("Please provide user_token.")
            return handle_invalid_usage(e)

    try:
        user_json = decode_jwt(user_token, config.JWT_PRIVATE_KEY)
    except jwt.InvalidSignatureError as ex:
        e = InvalidUsage(ex.args[0], status_code=401)
        return (handle_invalid_usage(e), None)
    except Exception as ex:
        e = InvalidUsage(ex.args[0], status_code=401)
        return (handle_invalid_usage(e), None)

    user_id = user_json["user_id"]

    try:
        user_done_count = get_user_done_location_count(user_id)
    except Exception as errmsg:
        e = InvalidUsage(repr(errmsg), status_code=400)
        return handle_invalid_usage(e)

    try:
        user_count = get_user_count()
    except Exception as errmsg:
        e = InvalidUsage(repr(errmsg), status_code=400)
        return handle_invalid_usage(e)

    try:
        loc_done_count = get_location_is_done_count()
    except Exception as errmsg:
        e = InvalidUsage(repr(errmsg), status_code=400)
        return handle_invalid_usage(e)

    return_status = {"individual_done_count" : user_done_count, 
                        "user_count" : user_count, 
                        "answer_count" : get_answer_count(),
                        "location_is_done_count" : loc_done_count}

    return jsonify(return_status)

 