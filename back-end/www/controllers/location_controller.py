"""The controller for https://[PATH]/location/"""

import time
import uuid
from flask import Blueprint
from flask import request
from flask import jsonify
from util.util import decode_user_token
from config.config import config
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import encode_jwt
from util.util import try_wrap_response
from config.config import config
from models.model_operations.location_operations import get_locations
from models.schema import locations_schema

bp = Blueprint("location_controller", __name__)

@bp.route("/", methods=["GET"])
def location():
    """
    The function for the front-end to retrieve random location data by specifying amount.

    Sample command to test:
    $ curl -d '{"user_token":"xxxxx", "size":"5", "gold_standard_size":"1"}' -H "Content-Type: application/json" -X GET http://localhost:5000/location/

    Parameters
    ----------
    user_token : str
        The encoded user JWT, issued by the back-end.
        (required)
    size : int
        Total number of locations to be returned.
        (required)
    gold_standard_size : int
        The number of locations that should include gold standard answers.
        There should be ("size" - "gold_standard_size") locations that are not labeled yet.
        (required)

    Returns
    -------
        The encoded JWT that stores location information.
    """    
    if request.method == "GET":
        request_json = request.get_json()

        size = 0
        gold_standard_size = 0

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

        if "size" in request_json and "gold_standard_size" in request_json:
            size = int(request_json["size"])
            gold_standard_size = int(request_json["gold_standard_size"])
        else:
            e = InvalidUsage("Please provide query size. size: total size of locations. gold_standard_size: locations which contains gold standards.", status_code=400)
            return handle_invalid_usage(e) 

        no_size = size is None
        no_gold_size = gold_standard_size is None

        if no_size or no_gold_size:
            e = InvalidUsage("Please provide query size. size: total size of locations. gold_standard_size: locations which contains gold standards.", status_code=400)
            return handle_invalid_usage(e)            
        else:
            return try_get_locations(user_id, size, gold_standard_size)

@try_wrap_response
def try_get_locations(user_id, size, gold_standard_size):
    data = get_locations(user_id, size, gold_standard_size)
    return jsonify({"data": locations_schema.dump(data)})
