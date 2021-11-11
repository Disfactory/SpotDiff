"""Functions to operate the location table."""

from models.model import db
from models.model import Location

def create_location(factory_id, photo_year, photo_url=""):
    """
    Create a location.

    Parameters
    ----------
    factory_id : str
        ID (uuid) provided by importing from the factory table
    photo_year : int
        The year the photo was taken
    photo_url : str
        The url to fetch the photo    

    Returns
    -------
    location : Location
        The newly created location.  

    Raises
    ------
    exception : Exception
        When photo year is not an integer        
    """
    
    if(not isinstance(photo_year, int)):
        raise Exception("The photo year shall be an integer")
    
    location = Location(factory_id=factory_id, year=photo_year, url=photo_url)

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


def update_location_basic_by_id(location_id, factory_id="", photo_year=0, photo_url=""):
    """
    Update location basic information by location id.

    Parameters
    ----------
    location_id : int
        ID of the location.
    factory_id : str
        factory_id from disfactory/factory table. Leave it "" if not updating.
    photo_year : int
        The year which the photo was taken. Leave it 0 if not updating.
    photo_url : str
        The url which greps the photo. Leave it "" if ont updating.                

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
        raise Exception("No location found in the database to update.")

    if factory_id != "":
        location.factory_id = factory_id

    if photo_year > 0:
        location.year = photo_year

    if photo_url != "":
        location.url = photo_url

    db.session.commit()

    return location

def update_location_bbox_by_id(location_id, bbox_left_up_lat, bbox_left_up_lng, bbox_right_down_lat, bbox_right_down_lng):
    """
    Update location bouding box information by location id.

    Parameters
    ----------
    location_id : int
        ID of the location.
    bbox_left_up_lat, bbox_left_up_lng, bbox_right_down_lat, bbox_right_down_lng: float
        The coordinates for the 2 points forming the inner boundbox for displaying the focus.        

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
        raise Exception("No location found in the database to update.")

    location.bbox_left_up_lat = bbox_left_up_lat
    location.bbox_left_up_lng = bbox_left_up_lng
    location.bbox_right_down_lat = bbox_right_down_lat
    location.bbox_right_down_lng = bbox_right_down_lng

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


