"""The controller for https://[PATH]/user/"""

import time
import uuid
from flask import Blueprint
from flask import request
from flask import jsonify
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import encode_jwt
from config.config import config
from models.model_operations.user_operations import get_user_by_client_id
from models.model_operations.user_operations import create_user


bp = Blueprint("user_controller", __name__)


@bp.route("/", methods=["POST"])
def user():
    """
    The function for the front-end client to log in.

    Use the following command to test:
    $ curl -d '{"client_id":"id"}' -H "Content-Type: application/json" -X POST http://0.0.0.0:5000/user/

    Parameters
    ----------
    client_id : str
        The client ID string provided by the front-end client.

    Returns
    -------
    user_token : str
        The encoded JWT that stores user information.
    """
    client_id = None
    request_json = request.get_json()
    if request_json is not None:
        if "client_id" in request_json:
            client_id = request_json["client_id"]

    # Get user id by client id, and issued an user jwt
    if client_id is None:
        e = InvalidUsage("Must have 'client_id'.", status_code=400)
        return handle_invalid_usage(e)
    else:
        user_token = get_user_token_by_client_id(client_id)
        if user_token is None:
            # This happens when the user is banned
            e = InvalidUsage("Permission denied.", status_code=403)
            return handle_invalid_usage(e)
        else:
            return_json = {"user_token": user_token}
            return jsonify(return_json)


def get_user_token_by_client_id(client_id):
    """
    Get the encoded user token by using client id.

    Parameters
    ----------
    client_id : str
        The ID provided by the front-end client.

    Returns
    -------
    user_token : str
        The JWT (JSON Web Token) of the corresponding user.
    """
    user = get_user_by_client_id(client_id)
    if user is None:
        user = create_user(client_id) # create a new user if not found
    user_id = user.id
    client_type = user.client_type
    if client_type == -1:
        return None # a banned user does not get the token
    else:
        user_token = encode_user_jwt(user_id=user_id, client_type=client_type)
        return user_token


def encode_user_jwt(**kwargs):
    """Encode user JWT (JSON Web Token)."""
    t = kwargs["iat"] if "iat" in kwargs else round(time.time())
    payload = {}
    payload["iat"] = t
    payload["jti"] = uuid.uuid4().hex
    payload["iss"] = "[CHANGE_THIS_TO_YOUR_ROOT_URL]"
    payload["exp"] = t + 3600 # the token will expire after one hour
    for k in kwargs:
        payload[k] = kwargs[k]
    return encode_jwt(payload, config.JWT_PRIVATE_KEY)
