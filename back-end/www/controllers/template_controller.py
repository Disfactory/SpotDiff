"""The controller for https://[PATH]/template/"""

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import decode_user_token
from util.util import try_wrap_response
from config.config import config


bp = Blueprint("template_controller", __name__)


@bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"])
def template():
    """
    The function for operating the XXX table.

    Parameters
    ----------
    user_token : str
        The encoded user JWT, issued by the back-end.
        (required for POST, PATCH, and DELETE)
    xxx : str
        This is the xxx parameter.

    Returns
    -------
    XXX
        This is the XXX object.
    """
    rj = request.json

    # Sanity and permission check
    # (POST, PATCH, and DELETE methods are for administrators only)
    if request.method in ["POST", "PATCH", "DELETE"]:
        error, _ = decode_user_token(rj, config.JWT_PRIVATE_KEY, check_if_admin=True)
        if error is not None: return error

    # Process the request
    if request.method == "GET":
        xxx = request.args.get("xxx")
        return jsonify({"method": "GET"})
    elif request.method == "POST":
        xxx = rj.get("xxx")
        return try_create_xxx(xxx)
    elif request.method == "PATCH":
        e = InvalidUsage("Test bad request.", status_code=400)
        return handle_invalid_usage(e)
    elif request.method == "DELETE":
        return try_delete_xxx()
    else:
        # Wrong methods
        e = InvalidUsage("Method not allowed.", status_code=405)
        return handle_invalid_usage(e)


@try_wrap_response
def try_create_xxx(xxx):
    return jsonify({"data": "xxx"})


@try_wrap_response
def try_delete_xxx():
    return make_response("", 204)
