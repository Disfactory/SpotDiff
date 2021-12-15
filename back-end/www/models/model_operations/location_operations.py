"""Functions to operate the location table."""

import datetime
import random

from sqlalchemy.sql.expression import null, true
from sqlalchemy import func
from models.model import db
from models.model import Location
from models.model import Answer
from models.model import User
from models.model_operations.user_operations import get_user_by_id
from models.model_operations.answer_operations import get_answers_by_user


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
        When size and gold_standard_size are not integers (or < 0).
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
    if size < 0:
        raise Exception("The size must be greater or equal to 0.")
    if gold_standard_size < 0:
        raise Exception("The gold_standard_size must be greater or equal to 0.")
    if gold_standard_size > size:
        raise Exception("The gold standard size cannot exceed size.")

    if size == 0:
        return []

    # Get the user's answers
    target_user = get_user_by_id(user_id)
    user_answers = get_answers_by_user(target_user.id)
    user_answered_location_id_list = [answer.location_id for answer in user_answers]

    # Get the locations which have gold answers
    gold_answers_filter = Answer.query.filter(Answer.is_gold_standard)
    gold_location_id_list = [loc.location_id for loc in gold_answers_filter.distinct(Answer.location_id).all()]

    if len(gold_location_id_list) == 0:
        raise Exception("No gold standards exist. DB not initialized?", size)

    if len(gold_location_id_list) < gold_standard_size:
        err_msg = "Cannot find expected amount of locations which have gold standards :{}. {} are found.".format(
                gold_standard_size, len(gold_location_id_list))
        raise Exception(err_msg)

    # Get the locations which have been answered by the user
    # TODO: need to select the locations where the Location.done_at is None (have not been identified)
    user_identified_location_filter = Location.query.filter(Location.id.in_(user_answered_location_id_list))
    user_identified_locations = [loc.id for loc in user_identified_location_filter.all()]

    gold_location_filter = Location.query.filter(Location.id.in_(gold_location_id_list))

    # Get to-be-excluded location ids, which are not either with gold answers or identified by the user before
    if len(user_identified_locations) > 0:
        exclude_location_id_list = gold_location_id_list + user_identified_locations
    else:
        exclude_location_id_list = gold_location_id_list

    non_gold_locations_filter = Location.query.filter(Location.id.not_in(exclude_location_id_list))

    sel_gold_location_list = []
    sel_non_gold_location_list = []

    # Randomly sort and select the first locations which has been provideded gold answers
    if gold_standard_size > 0:
        rand_gold_location_list = gold_location_filter.order_by(func.random()).all()
        dbprint("Got {} gold rand_gold_location_list.".format(len(rand_gold_location_list)))
        sel_gold_location_list = rand_gold_location_list[0:gold_standard_size]
        dbprint("sel_gold_location_list : ", sel_gold_location_list)

    # Randomly sort and select the first locations which has exclude user answered ones plus those with gold answers
    if size > gold_standard_size:
        rand_none_gold_location_list = non_gold_locations_filter.order_by(func.random()).all()
        sel_non_gold_location_list = rand_none_gold_location_list[0:(size - gold_standard_size)]
        dbprint("sel_non_gold_location_list : ", sel_non_gold_location_list)

    # Combine and shuffle the list
    location_list = sel_non_gold_location_list
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
