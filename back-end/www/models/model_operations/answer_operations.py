"""Functions to operate the location table."""

from models.model import db
from models.model import Answer


def create_answer(user_id, location_id, year_old, year_new,
        source_url_root, land_usage, expansion, is_gold_standard,
        bbox_left_top_lat, bbox_left_top_lng, bbox_bottom_right_lat,
        bbox_bottom_right_lng, zoom_level):
    """
    Create an answer reported by an user with a location.

    Parameters
    ----------
    user_id : int
        Foreign key to the user table.
        (required)
    location_id : int
        Foreign key to the location table.
        (required)
    year_old: int
        The year where the satellite photo was taken from our geo sources.
        (required)
    year_new: int
        A newer photo to be compared with the one taken in year_old.
        (required)
    source_url_root : str
        URL to store the location on the map.
        (required)
    land_usage : int
        User's answer of judging if the land is a farm or has buildings.
        (check the answer table in model.py for the meaning of the values)
        (required)
    expansion : int
        User's answer of judging the construction is expanded.
        (check the answer table in model.py for the meaning of the values)
        (required)
    is_gold_standard : bool
        If it's a golden standard answer provided by admnin.
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

    Returns
    -------
    answer : Answer
        The newly created answer.

    Raises
    ------
    exception : Exception
        Type checking for land_usage, expansion, year_old, year_new, and is_gold_standard.
    """
    if not isinstance(land_usage, int):
        raise Exception("The land_usage shall be an integer")
    if not isinstance(expansion, int):
        raise Exception("The expansion shall be an integer")
    if not isinstance(is_gold_standard, bool):
        raise Exception("The is_gold_standard shall be a bool")
    if not isinstance(year_old, int):
        raise Exception("The photo year shall be an integer")
    if not isinstance(year_new, int):
        raise Exception("The photo year shall be an integer")

    answer = Answer(user_id=user_id, location_id=location_id, year_old=year_old,
            year_new=year_new, source_url_root=source_url_root, land_usage=land_usage,
            expansion=expansion, is_gold_standard=is_gold_standard,
            bbox_left_top_lat=bbox_left_top_lat, bbox_left_top_lng=bbox_left_top_lng,
            bbox_bottom_right_lat=bbox_bottom_right_lat,
            bbox_bottom_right_lng=bbox_bottom_right_lng, zoom_level=zoom_level)

    db.session.add(answer)
    db.session.commit()

    return answer


def get_answer_count():
    """
    Get total number of answers, excluding gold answers.
    """
    answer_count = Answer.query.filter_by(is_gold_standard=False).count()
    return answer_count


def get_answer_by_id(answer_id):
    """
    Get an answer by the answer_id.

    Parameters
    ----------
    answer_id : int
        ID of the answer.

    Returns
    -------
    answer : Answer
        The retrieved answer object.
    """
    answer = Answer.query.filter_by(id=answer_id).first()
    return answer


def get_answers_by_user(user_id):
    """
    Get a list of answers by the user id.

    Parameters
    ----------
    user_id : int
        ID of the user.

    Returns
    -------
    answers : Answer
        The list of answers reported by the specified user.
    """
    answers = Answer.query.filter_by(user_id=user_id).all()
    return answers


def get_answers_by_location(location_id):
    """
    Get a list of answers by specified location.

    Parameters
    ----------
    location_id : int
        ID of the location.

    Returns
    -------
    answers : Answer
        The list of answers reported with the specified location.
    """
    answers = Answer.query.filter_by(location_id=location_id).all()
    return answers


def get_answers_by_user_and_location(user_id, location_id):
    """
    Get a list of answers by specified user id and location.

    Parameters
    ----------
    user_id : int
        ID of the user.
    location_id : int
        ID of the location.
    Returns
    -------
    answers : Answer
        The list of answers reported by the specified user and location.
    """
    answers = Answer.query.filter_by(user_id=user_id, location_id=location_id).all()

    return answers


def get_gold_answer_by_location(location_id):
    """
    Get the (first) gold answer specified by location id.

    Parameters
    ----------
    location_id : int
        ID of the location.
    Returns
    -------
    answers : Answer
        The gold answer.
    """
    answer = Answer.query.filter_by(is_gold_standard=True, location_id=location_id).first()
    return answer


def remove_answer(answer_id):
    """
    Remove an answer.

    Parameters
    ----------
    answer_id : int
        ID of the answer.

    Raises
    ------
    exception : Exception
        When no answer is found.
    """
    answer = get_answer_by_id(answer_id)

    if answer is None:
        raise Exception("Cannot find answer with id ", answer_id)

    db.session.delete(answer)
    db.session.commit()


def check_answer_correctness(location_id, land_usage, expansion):
    """
    Check the correctness of the answer.

    Parameters
    ----------
    location_id : int
        ID of the location.
    land_usage : int
        User's answer of judging if the land is a farm or has buildings.
        (check the answer table in model.py for the meaning of the values)
    expansion : int
        User's answer of judging the construction is expanded.
        (check the answer table in model.py for the meaning of the values)

    Return
    ------
    int
        Result of the checking.
        0 means passing the quality test.
        1 means failing the quality test.
        2 means no gold standard exists.
    """

    gold_answer = Answer.query.filter_by(is_gold_standard=True, location_id=location_id).first()

    # If the gold answer doesn't exist
    if gold_answer is None:
        return 2

    # If the gold answer exists, check the correctness
    if gold_answer.land_usage == land_usage and gold_answer.expansion == expansion:
        return 0
    else:
        return 1
