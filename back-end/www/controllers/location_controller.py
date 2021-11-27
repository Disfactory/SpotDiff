"""The controller for https://[PATH]/location/"""

import time
import uuid
from flask import Blueprint
from flask import request
from flask import jsonify
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
    The function for the front-end to retrieve location data.

    Sample command to test:
    $ curl -d '{"size":"5", "gold_standard_size":"1"}' -H "Content-Type: application/json" -X GET http://localhost:5000/location/

    Parameters
    ----------
    client_id : str
        The client ID string provided by the front-end client.
    size : int
        Total number of locations to be returned.s
    gold_standard_size : int    
        Within size, the number of locations which includes gold standard answers    

    Returns
    -------
        The encoded JWT that stores location information.
    """    
    if request.method == "GET":
        request_json = request.get_json()

        size = 0
        gold_standard_size = 0
        if request_json is not None:
            if "client_id" in request_json:
                client_id = request_json["client_id"]
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
            return try_get_locations(size, gold_standard_size)

@try_wrap_response
def try_get_locations(size, gold_standard_size):
    data = get_locations(size, gold_standard_size)
    return jsonify({"data": locations_schema.dump(data)})
