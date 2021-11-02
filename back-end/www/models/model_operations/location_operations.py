"""Functions to operate the location table."""

from models.model import db
from models.model import Location

def create_location(factory_id):
    """
    Create a location.

    Parameters
    ----------
    factory_id : str
        ID(uuid) provided by importing from the factory table
    year : Date

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
    location_id : Int
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
    factory_id : Int
        ID of the factory.

    Returns
    -------
    location : Location
        The retrieved location object.
    """
    location = Location.query.filter_by(factory_id=factory_id).first()

    return location


def update_location_by_id(location_id, factory_id):
    """
    Update location data by location id.
    Parameters
    ----------
    location_id : int
        ID of the location.

    Returns
    -------
    location : Location
        The retrieved location object.

    Raises
    ------
    exception : Exception
        When no location is found.

    """
    location = Location.query.filter_by(id=location_id).first()

    if location is None:
        raise Exception("No user found in the database to update.")

    location.factory_id = factory_id

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
        raise Exception("No user found in the database to delete.")

    db.session.delete(location)
    db.session.commit()


def get_all_locations():
    """
    Get all locations.

    Returns
    -------
    locations : list of Locations
        The list of retrieved location objects.
    """
    locations = Location.query.all()

    return locations


