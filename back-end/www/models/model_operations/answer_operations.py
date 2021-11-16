"""Functions to operate the location table."""

from models.model import db
from models.model import Answer

def create_answer(user_id, location_id, is_factory, is_expansion, is_gold_standard, bbox_left_up_lat, bbox_left_up_lng, bbox_right_down_lat, bbox_right_down_lng):
    """
    Create an answer reported by an user with a location.

    Parameters
    ----------
    user_id : int
        ID to the user table
    location_id : int
        ID to the location table
    is_factory : int
    is_expansion : int
    is_gold_answer : int
    bbox_left_up_lat, bbox_left_up_lng, bbox_right_down_lat, bbox_right_down_lng: float
        The coordinates for the 2 points forming the inner boundbox for displaying the focus.        

    Returns
    -------
    answer : Answer
        The newly created answer.  

    Raises
    ------
    exception : Exception
        Type check for is_factory, is_expansion, is_gold_standard to be integers
    """
    if(not isinstance(is_factory, int)):
        raise Exception("The is_factory shall be an integer")
    if(not isinstance(is_expansion, int)):
        raise Exception("The is_expansion shall be an integer")
    if(not isinstance(is_gold_standard, int)):
        raise Exception("The is_gold_standard shall be an integer")

    answer = Answer(user_id=user_id, location_id=location_id, is_factory=is_factory, is_expansion=is_expansion,
                    is_gold_standard=is_gold_standard, bbox_left_up_lat=bbox_left_up_lat, bbox_left_up_lng=bbox_left_up_lng,
                    bbox_right_down_lat=bbox_right_down_lat, bbox_right_down_lng=bbox_right_down_lng)

    db.session.add(answer)
    db.session.commit()

    return answer

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
    Get a list of answers by the location.

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



