"""Functions to operate the location table."""

from models.model import db
from models.model import Answer


def create_answer(user_id, location_id, year_old, year_new, source_url_root, land_usage, expansion, is_gold_standard, bbox_left_top_lat, bbox_left_top_lng, bbox_bottom_right_lat, bbox_bottom_right_lng, zoom_level):
    """
    Create an answer reported by an user with a location.

    Parameters
    ----------
    user_id : int
        Foreign key to User table
    location_id : int
        Foreign key to Location table
    year_old: int
        year Marks which year the satellite photo was taken from our geo sources. 
    year_new: int
        A newer photo to be compared with the one taken in year_old
    source_url_root : str
        URL to store the location on the map.
    land_usage : int
        User's answer of judging a construction is built. 0: construction, 1: unknown, 2: farm
    expansion : int
        User's answer of judging the construction is expanded. 0: unknown, 1: nope, 2:yes
    is_gold_standard : Boolean
        If it's a golden standard answer provided by admnin.
    bbox_left_top_lat, bbox_left_top_lng, bbox_bottom_right_lat, bbox_bottom_right_lng : float
        The coordinates for the 2 points forming the inner boundbox for displaying the focus.        
    zoom_level : int
        The zoom level for displaying.        
    Returns
    -------
    answer : Answer
        The newly created answer.  

    Raises
    ------
    exception : Exception
        Type checking for land_usage, expansion, year_old, year_new to be integers, is_gold_standard to be boolean.
    """
    if(not isinstance(land_usage, int)):
        raise Exception("The land_usage shall be an integer")
    if(not isinstance(expansion, int)):
        raise Exception("The expansion shall be an integer")
    if(not isinstance(is_gold_standard, bool)):
        raise Exception("The is_gold_standard shall be a bool")
    if(not isinstance(year_old, int)):
        raise Exception("The photo year shall be an integer")
    if(not isinstance(year_new, int)):
        raise Exception("The photo year shall be an integer")

    answer = Answer(user_id=user_id, location_id=location_id, year_old=year_old, year_new=year_new, source_url_root=source_url_root, land_usage=land_usage, expansion=expansion,
                    is_gold_standard=is_gold_standard, bbox_left_top_lat=bbox_left_top_lat, bbox_left_top_lng=bbox_left_top_lng,
                    bbox_bottom_right_lat=bbox_bottom_right_lat, bbox_bottom_right_lng=bbox_bottom_right_lng, zoom_level=zoom_level)

    db.session.add(answer)
    db.session.commit()

    return answer


def create_answer_with_result(user_id, location_id, year_old, year_new, source_url_root, land_usage, expansion, is_gold_standard, bbox_left_top_lat, bbox_left_top_lng, bbox_bottom_right_lat, bbox_bottom_right_lng, zoom_level):
    """
    Create an answer and return if it passed or not by checking the gold standards.

    Parameters
    ----------
    user_id : int
        Foreign key to User table
    location_id : int
        Foreign key to Location table
    year_old: int
        year Marks which year the satellite photo was taken from our geo sources. 
    year_new: int
        A newer photo to be compared with the one taken in year_old
    source_url_root : str
        URL to store the location on the map.
    land_usage : int
        User's answer of judging a construction is built. 0: construction, 1: unknown, 2: farm
    expansion : int
        User's answer of judging the construction is expanded. 0: unknown, 1: nope, 2:yes
    is_gold_standard : Boolean
        If it's a golden standard answer provided by admnin.
    bbox_left_top_lat, bbox_left_top_lng, bbox_bottom_right_lat, bbox_bottom_right_lng : float
        The coordinates for the 2 points forming the inner boundbox for displaying the focus.        
    zoom_level : int
        The zoom level for displaying.        
    Returns
    -------
    compare_result : integer
        Compare with the gold answer. 
        0: Pass
        1: Fail
        -1: Gold doesn't exist

    Raises
    ------
    exception : Exception
        Type checking for land_usage, expansion, year_old, year_new to be integers, is_gold_standard to be boolean.
    """
    new_answer = create_answer(user_id, location_id, year_old, year_new, source_url_root, land_usage, expansion, is_gold_standard, bbox_left_top_lat, bbox_left_top_lng, bbox_bottom_right_lat, bbox_bottom_right_lng, zoom_level)

    # Bypass the gold standard itself
    if(is_gold_standard):
        return 0

    # Get the gold answer and compare result
    compare_result = 0
    gold_answer = Answer.query.filter_by(is_gold_standard=True, location_id=location_id, year_old=year_old, year_new=year_new).first()
    if(gold_answer != None):
        if ((gold_answer.land_usage == land_usage) and (gold_answer.expansion == expansion)):
            compare_result = 0
        else:
            compare_result = 1    
    else:
        compare_result = -1

    return compare_result
    

def get_answer_count():
    """
    Get total number of answers exclusive of gold answers
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


def is_answer_passed(answer_id):
    """
    Test if the answer passes the test (with the gold standard)

    Parameters
    ----------
    answer_id : int
        ID of the answer.

    Raises
    ------
    exception : Exception
        When no answer is found.    
    """    
    is_passed = False
    my_answer = get_answer_by_id(answer_id)
    
    if(my_answer is None):
        raise Exception("Cannot find the answer.")

    gold_answer = Answer.query.filter_by(is_gold_standard=True, location_id=my_answer.location_id).first()

    if(gold_answer is None):
        raise Exception("Cannot find the gold standard answer.")

    if(gold_answer.land_usage == my_answer.land_usage and gold_answer.expansion == my_answer.expansion):
        is_passed = True

    return is_passed    