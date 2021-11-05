"""Database model for the application."""

import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import MetaData


# Set the naming convention for database columns
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Initalize app with database
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))


class User(db.Model):
    """
    Class representing a User.

    Attributes
    ----------
    id : int
        Unique identifier.
    created_at : datetime
        A timestamp indicating when the user is created.
    client_id : str
        A unique identifier provided by the front-end client.
    client_type : int
        The user type (0 is the admin, 1 is the normal user, -1 is the banned user)
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    client_id = db.Column(db.String(255), unique=True, nullable=False)
    client_type = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return "<User id=%r created_at=%r client_id=%r client_type=%r>" % (
                self.id, self.created_at, self.client_id, self.client_type)


class Location(db.Model):
    """
    Class representing a location.

    Attributes
    ----------
    id : int
        Unique identifier as primary key.

    factory_id : str
        The uuid imported from disfactory factory table.
    
    year: integer
        year Marks which year the satellite photo was taken from our geo sources. 

    url : string
        URL stores the location on the map.

    bbox_left_up_lat
    bbox_left_up_lng
    bbox_right_down_lat
    bbox_right_down_lng:
        The coordinates for the 2 points forming the inner boundbox for displaying the focus.        

    done_at : datetime
        The time when the location is marked done.

    """

    # Basic information
    id = db.Column(db.Integer, primary_key=True)
    factory_id = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, default = 0)
    url = db.Column(db.String, nullable=True)

    # Display information
    bbox_left_up_lat = db.Column(db.Float, default = 0)
    bbox_left_up_lng = db.Column(db.Float, default = 0)
    bbox_right_down_lat = db.Column(db.Float, default = 0)
    bbox_right_down_lng = db.Column(db.Float, default = 0)
    
    # Others
    done_at = db.Column(db.DateTime)

    def __repr__(self):
        return "<id=%r factory_id=%r year=%r url=%r bbox_left_up_lat=%r bbox_left_up_lng=%r bbox_right_down_lat=%r bbox_right_down_lng=%r done_at=%r" %(
                self.id, self.factory_id, self.year, self.url, 
                self.bbox_left_up_lat, self.bbox_left_up_lng, self.bbox_right_down_lat, self.bbox_right_down_lng, 
                self.done_at)


