"""Functions to operate the location table."""

import datetime
import random
from sqlalchemy.sql.expression import null, true
from sqlalchemy import func
from sqlalchemy import or_
from models.model import db
from models.model import Location
from models.model import Answer
from models.model import User
from models.model_operations.user_operations import get_user_by_id
#from models.model_operations.answer_operations import get_answers_by_user
from models.model_operations import answer_operations

DEBUG = False
def dbprint(*values: object):
    """
    The printing function for debugging.
    Enabled by the DEBUG flag.
    """
    if DEBUG:
        print(values)


def create_location(factory_id):
    """
    Create a location.

    Parameters
    ----------
    factory_id : str
        ID (uuid) provided by importing from the factory table.

    Returns
    -------
    location : Location
        The newly created location.
    """
    location = Location(factory_id=factory_id)

    db.session.add(location)
    db.session.commit()

    return location


def get_location_by_id(location_id):
    """
    Get a location by the location id.

    Parameters
    ----------
    location_id : int
        ID of the location.

    Returns
    -------
    location : Location
        The retrieved location object.
    """
    location = Location.query.filter_by(id=location_id).first()
    return location


def get_location_by_factory_id(factory_id):
    """
    Get a location by the factory id.

    Parameters
    ----------
    factory_id : int
        ID of the factory.

    Returns
    -------
    location : Location
        The retrieved location object.
    """
    location = Location.query.filter_by(factory_id=factory_id).first()
    return location


def set_location_done(location_id, is_done):
    """
    Set the current time to done_at to mark it is done.

    Parameters
    ----------
    location_id : int
        ID of the location.
    is_done : bool
        Set done or not done.

    Returns
    -------
    location : Location
        The retrieved location object.

    Raises
    ------
    exception : Exception
        When is_done is not bool
    exception : Exception
        When no location is found.
    """
    if not isinstance(is_done, bool):
        raise Exception("is_done shall be bool")

    location = Location.query.filter_by(id=location_id).first()

    if location is None:
        raise Exception("No location found in the database to update.")

    if is_done:
       location.done_at = datetime.datetime.now()
    else:
       location.done_at = None

    db.session.commit()
    return location


def remove_location(location_id):
    """
    Remove a location.

    Parameters
    ----------
    location_id : int
        ID of the location.

    Raises
    ------
    exception : Exception
        When no location is found.
    """
    location = Location.query.filter_by(id=location_id).first()

    if location is None:
        raise Exception("No location found in the database to delete.")

    db.session.delete(location)
    db.session.commit()


def get_locations(user_id, size, gold_standard_size):
    """
    Get the locations that can be returned to the front-end.

    Parameters
    ----------
    user_id : int
        ID of the user.
    size : int
        Total number of locations to be returned.
    gold_standard_size : int
        The number of locations that should include gold standard answers.
        There should be ("size" - "gold_standard_size") locations that are not labeled yet.

    Returns
    -------
    locations : list of Locations
        The list of retrieved location objects.

    Raises
    ------
    exception : Exception
        When size and gold_standard_size are not integers (or < 1).
    exception : Exception
        When gold standard does not exist.
    exception : Exception
        When gold standard size exceeds size.
    exception : Exception
        When we cannot find "gold_standard_size" of locations which have gold standards.
    exception : Exception
        When we cannot find "size" of locations.
    """
    if not isinstance(gold_standard_size, int):
        raise Exception("The gold_standard_size shall be an integer")
    if not isinstance(size, int):
        raise Exception("The gold_standard_size shall be an integer")
    if size < 1:
        raise Exception("The size must be greater or equal to 1.")
    if gold_standard_size < 1:
        raise Exception("The gold_standard_size must be greater or equal to 1.")
    if gold_standard_size > size:
        raise Exception("The gold standard size cannot exceed size.")

    if size == 0:
        return []

    # Get the user's answers
    target_user = get_user_by_id(user_id)
    user_answers = answer_operations.get_answers_by_user(target_user.id)
    user_answered_location_id_list = [answer.location_id for answer in user_answers]

    # Get the locations which have gold answers
    gold_answers_filter = Answer.query.filter(Answer.gold_standard_status==0)
    gold_location_id_list = [loc.location_id for loc in gold_answers_filter.distinct(Answer.location_id).all()]

    if len(gold_location_id_list) == 0:
        raise Exception("No gold standards exist. DB not initialized?", size)

    if len(gold_location_id_list) < gold_standard_size:
        err_msg = "Cannot find expected amount of locations which have gold standards :{}. {} are found.".format(
                gold_standard_size, len(gold_location_id_list))
        raise Exception(err_msg)

    # Get the locations which have been answered by the user, or already done.
    ex_location_filter = Location.query.filter(or_(Location.id.in_(user_answered_location_id_list), Location.done_at != None))
    ex_location_id_list = [loc.id for loc in ex_location_filter.all()]

    # Get locations which have gold standards
    gold_location_filter = Location.query.filter(Location.id.in_(gold_location_id_list))

    # Get to-be-excluded location ids, which are not either: 1. with gold answers 2. identified by the user before 3. Already labled done
    if len(ex_location_id_list) > 0:
        exclude_location_id_list = gold_location_id_list + ex_location_id_list
    else:
        exclude_location_id_list = gold_location_id_list

    wait_test_locations_filter = Location.query.filter(Location.id.not_in(exclude_location_id_list))

    sel_gold_location_list = []
    sel_wait_test_locations_list = []

    # Randomly sort and select the first locations which has been provideded gold answers
    if gold_standard_size > 0:
        rand_gold_location_list = gold_location_filter.order_by(func.random()).all()
        dbprint("Got {} gold rand_gold_location_list.".format(len(rand_gold_location_list)))
        sel_gold_location_list = rand_gold_location_list[0:gold_standard_size]
        dbprint("sel_gold_location_list : ", sel_gold_location_list)

    # Randomly sort and select the first locations which has exclude user answered ones plus those with gold answers
    if size > gold_standard_size:
        wait_test_locations_list = wait_test_locations_filter.order_by(func.random()).all()
        sel_wait_test_locations_list = wait_test_locations_list[0:(size - gold_standard_size)]
        dbprint("sel_wait_test_locations_list : ", sel_wait_test_locations_list)

    # Combine and shuffle the list
    location_list = sel_wait_test_locations_list
    if len(sel_gold_location_list) > 0:
        location_list += sel_gold_location_list
        random.shuffle(location_list)

    # Double confirm the amount
    if len(location_list) < size:
        raise Exception("Cannot find expected amount of locations", size)

    return location_list


def get_location_is_done_count():
    """
    Get the count of locations which have been labled done.

    Returns
    -------
    count : int
        The amount of locations which have been labled done.
    """
    # Create an exclusive filter to get locations which have done_at date
    location_query = Location.query.filter(Location.done_at.isnot(None))
    count = location_query.count()
    return count


def get_location_count():
    """
    Get the total number of locations.

    Returns
    -------
    count : int
        The total number of locations.
    """
    count = Location.query.count()
    return count


def batch_process_answers(user_id, answers):
    """
    Process the answers returned by the front-end and write them into the database.

    Parameters
    ----------
    answers : list
        A list of answers provided by the front-end user.
        Each answer should be a dictionary with the following structure:
            {"timestamp": XXX,
             "location_id": XXX,
             "year_new": XXX,
             "year_old": XXX,
             "zoom_level": XXX,
             "bbox_bottom_right_lat": XXX,
             "bbox_bottom_right_lng": XXX,
             "bbox_left_top_lng": XXX,
             "bbox_left_top_lat": XXX,
             "land_usage": XXX,
             "source_url_root" : XXX,
             "expansion": XXX}
        The explanation of the parameters are in the answer table in the model.py file.

    Raises
    ------
    exception : Exception
        If "location_id" or "land_usage" or "expansion" not exist in the dictionary of an answer.
    exception : Exception
        When no gold standards are found.

    Returns
    ------
    True if the gold standard test passes.
    """
    if answers is None:
        raise Exception("Please provide answers.")    
    if user_id is None:
        raise Exception("Please provide user id.")    
    if len(answers) < 2:
        raise Exception("Not enough answers.")

    gold_test_pass_status = 0
    non_gold_answer_id_list = []

    # The first parse is to check the gold standard test result. 
    for idx in range(len(answers)):
        if "location_id" not in answers[idx] or \
            "land_usage" not in answers[idx] or \
            "expansion" not in answers[idx]:
            raise Exception("The answer format is not not correct.")    

        # Check every answer if gold standard exists
        status = answer_operations.check_answer_quality(answers[idx]["location_id"], answers[idx]["land_usage"], answers[idx]["expansion"])            
        if status == 0:
            non_gold_answer_id_list.append(idx)
        # status != 0, which means a gold standard exists. Assign gold_test_pass_status only once when an answer corresponding to gold answer found.
        else:
            if gold_test_pass_status == 0:
                gold_test_pass_status = status
                dbprint("{} gold_test_pass_status is {}".format(user_id, gold_test_pass_status))

    # If no answer corresponding to gold standard found, there must be something wrong.
    if(gold_test_pass_status == 0):
        raise Exception("The answer set is not correct.")    

    # If user passes gold standard test, check if locations from the answers need to be set done_at.
    if gold_test_pass_status == 1:
        for idx in non_gold_answer_id_list:
            # Check if another gold answer candidate exists and matches to mark the location done.
            result = answer_operations.check_gold_candidate_status(answers[idx]["location_id"], answers[idx]["land_usage"], answers[idx]["expansion"])
            if result == True:
                set_location_done(answers[idx]["location_id"], True)

    # Second parse to submit all the answers.
    for idx in range(len(answers)):
        answer_operations.create_answer(user_id, answers[idx]["location_id"], 
                        answers[idx]["year_old"], answers[idx]["year_new"], answers[idx]["source_url_root"], 
                        answers[idx]["land_usage"], answers[idx]["expansion"], gold_test_pass_status,
                        answers[idx]["bbox_left_top_lat"], answers[idx]["bbox_left_top_lng"], 
                        answers[idx]["bbox_bottom_right_lat"], answers[idx]["bbox_bottom_right_lng"], answers[idx]["zoom_level"], 
                        )

    if gold_test_pass_status == 1:
        return True
    else:
        return False
