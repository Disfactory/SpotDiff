"""The controller for https://[PATH]/answer/"""

from flask import Blueprint
from flask import request
from flask import jsonify
from util.util import InvalidUsage
from util.util import handle_invalid_usage
from util.util import decode_user_token
from config.config import config
from models.model_operations.answer_operations import batch_process_answers

bp = Blueprint("answer_controller", __name__)

@bp.route("/", methods=["POST"])
def answer():
    """
    The function for the front-end to submit answers if passing the gold-standard test.

    Sample command to test:

    $ curl -d '{"user_token":"xxxx","data":[{"location_id":1, "year_new":2017, "year_old":2010, 
    "source_url_root":"www.test.org", "is_gold_standard":false, "bbox_left_top_lat":24.0962704615941, 
    "bbox_left_top_lng":"120.462878886353","bbox_bottom_right_lat":24.0962704615941, 
    "bbox_bottom_right_lng":120.462878886353, "land_usage":1, "expansion":1, "zoom_level":0}, 
    {"location_id":8, "year_new":2017, "year_old":2010, "source_url_root":"www.test.org", "is_gold_standard":false, 
    "bbox_left_top_lat":24.0962704615941, "bbox_left_top_lng":"120.462878886353",
    "bbox_bottom_right_lat":24.0962704615941, "bbox_bottom_right_lng":120.462878886353, 
    "land_usage":1, "expansion":1, "zoom_level":0}]}' -H "Content-Type: application/json"
     -X POST http://localhost:5000/answer/

    Parameters
    ----------
    user_token : str
        The encoded user JWT, issued by the back-end.
        (required)
    data : list of dict
        The answers, in the format [{"FIELD1:"VALUE1","FIELDS2":"VALUE2", ...}].
        (required)
        FIELDS:
            year_old: int
                year Marks which year the satellite photo was taken from our geo sources.
                (required)
            year_new: int
                A newer photo to be compared with the one taken in year_old.
                (required)
            source_url_root : str
                URL to store the location on the map.
                (required)
            land_usage : int
                User's answer of judging a construction is built.
                0 means unknown.
                1 means building.
                2 means farm.
                (required)
            expansion : int
                User's answer of judging the construction is expanded.
                0 means unknown.
                1 means no new expansion.
                2 means yes (there is expansion).
                (required)
            bbox_left_top_lat : float
                The latitude of the top-left corner of the bounding box for displaying the focus.
                (optional)
            bbox_left_top_lng : float
                The longitude of the top-left corner of the bounding box for displaying the focus.
                (optional)
            bbox_bottom_right_lat : float
                The latitude of the bottom-right corner of the bounding box for displaying the focus.
                (optional)
            bbox_bottom_right_lng : float
                The longitude of the bottom-right corner of the bounding box for displaying the focus.
                (optional)
            zoom_level : int
                The zoom level for displaying the location.
                (optional)
            user_id : int
                Foreign key to the user table.
                (required)
            location_id : int
                Foreign key to the location table.
                (required)

    Returns
    -------
        {"Passed":True|False}
    """    
    if request.method == "POST":
        rj = request.get_json()

        if rj is None:
            e = InvalidUsage("Please provide correct parameters.", status_code=400)
            return handle_invalid_usage(e)

        # Get user id from user_token.
        error, user_json = decode_user_token(rj, config.JWT_PRIVATE_KEY, check_if_admin=False)
        if error is not None: return error

        user_id = user_json["user_id"]

        if user_id is None:
            e = InvalidUsage("Please provide correct user token.", status_code=400)
            return handle_invalid_usage(e) 

        if "data" not in rj:
            e = InvalidUsage("Please provide data.", status_code=400)
            return handle_invalid_usage(e) 

        # Check all the answers from frontend to decide the next step.
        try:
            pass_status = batch_process_answers(user_id, rj["data"])
        except Exception as errmsg:
            e = InvalidUsage(repr(errmsg), status_code=400)
            return handle_invalid_usage(e)

        if pass_status:
            return_status = {"Passed" : True}
        else:            
            return_status = {"Passed" : False}

        return jsonify(return_status)



