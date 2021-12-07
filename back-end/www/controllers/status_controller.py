"""The controller for https://[PATH]/status/"""

from flask import Blueprint
from flask import request
from flask import jsonify
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import decode_user_token
from config.config import config
from models.model_operations.user_operations import get_user_done_location_count
from models.model_operations.user_operations import get_user_count
from models.model_operations.location_operations import get_location_is_done_count

bp = Blueprint("status_controller", __name__)

@bp.route("/", methods=["GET"])
def status():
    """
    The function for the front-end to retrieve status data.

    Sample command to test:
    $ curl -d '{"user_token":"xxx"}' -H "Content-Type: application/json" -X GET http://localhost:5000/status/

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
        request_json = request.get_json()

        if request_json is None:
            e = InvalidUsage("Please provide correct parameters.", status_code=400)
            return handle_invalid_usage(e)


        # Get user id from user_token.
        error, user_json = decode_user_token(request_json, config.JWT_PRIVATE_KEY, check_if_admin=False)
        if error is not None: return error

        user_id = user_json["user_id"]

        if user_id is None:
            e = InvalidUsage("Please provide correct user token.", status_code=400)
            return handle_invalid_usage(e) 

        return_status = {"individual_done_count" : get_user_done_location_count(user_id), 
                         "user_count" : get_user_count(), 
                         "location_is_done_count" : get_location_is_done_count()}

        return jsonify(return_status)

