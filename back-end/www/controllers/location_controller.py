"""The controller for https://[PATH]/location/"""

from flask import Blueprint
from flask import request
from flask import jsonify
import jwt
from util.util import decode_jwt
from config.config import config
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import try_wrap_response
from config.config import config
from models.model_operations.location_operations import get_locations
from models.schema import locations_schema

bp = Blueprint("location_controller", __name__)

@bp.route("", methods=["GET"])
def location():
    """
    The function for the front-end to retrieve random location data by specifying amount.

    Sample command to test:
    $ curl -H "Content-Type: application/json" -X GET http://localhost:5000/location?size=5\&gold_standard_size=1\&user_token=xxxx
    $ https://localhost:5000/location?&size=5&gold_standard_size=1?user_token=xxxxx
    
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
        The encoded JWT that stores location information:
        id : int
            ID of the location.
        factory_id : string
            The uuid imported from disfactory factory table.
    """    
    size = request.args.get("size")
    gold_standard_size = request.args.get("gold_standard_size")
    user_token = request.args.get("user_token")
    if size is None:
        e = InvalidUsage("Please provide size, the number of locations you want to get.")
        return handle_invalid_usage(e)

    try:
        i = int(size)
    except ValueError as ex:
        e = InvalidUsage("size must be an integer.")
        return handle_invalid_usage(e)
    except Exception as ex: 
        e = InvalidUsage("size must be an integer.")       
        return handle_invalid_usage(e)
    
    if int(size) < 2:
        e = InvalidUsage("The size must be greater or equal to 2.")
        return handle_invalid_usage(e)

    if gold_standard_size is None:                
        e = InvalidUsage("Please provide gold_standard_size, the number of gold standards.")
        return handle_invalid_usage(e)
    try:
        i = int(gold_standard_size)
    except ValueError as ex:
        e = InvalidUsage("gold_standard_size must be an integer.")
        return handle_invalid_usage(e)
    except Exception as ex: 
        e = InvalidUsage("gold_standard_size must be an integer.")       
        return handle_invalid_usage(e)

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
    if user_id is None:
        e = InvalidUsage("Cannot find user_id")
        return handle_invalid_usage(e)

    return try_get_locations(user_id, int(size), int(gold_standard_size))

@try_wrap_response
def try_get_locations(user_id, size, gold_standard_size):
    try:
        data = get_locations(user_id, size, gold_standard_size)
    except Exception as errmsg:
        e = InvalidUsage(repr(errmsg), status_code=400)
        return handle_invalid_usage(e)
    return jsonify({"data": locations_schema.dump(data)})
