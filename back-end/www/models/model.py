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
        The user type (0 is the admin, 1 is the normal user, -1 is the banned user).
    answers : relationship
        List of answers related to the user.
    """
    # Basic information
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    client_id = db.Column(db.String(255), unique=True, nullable=False)
    client_type = db.Column(db.Integer, nullable=False, default=1)

    # Build 1 to N relationship to the user table
    answers = db.relationship("Answer", backref=db.backref("user", lazy=True), lazy=True)

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
    done_at : datetime
        The time when the location is marked done.
    answers : relationship
        List of answers related to the location.
    """
    # Basic information
    id = db.Column(db.Integer, primary_key=True)
    factory_id = db.Column(db.String(255), nullable=False)

    # Others
    done_at = db.Column(db.DateTime, default=None)

    # Build 1 to N relationship to the answer table
    answers = db.relationship("Answer", backref=db.backref("location", lazy=True), lazy=True)

    def __repr__(self):
        return "<id=%r factory_id=%r done_at=%r>" %(self.id, self.factory_id, self.done_at)


class Answer(db.Model):
    """
    Class representing an answer.

    Attributes
    ----------
    id : int
        Unique identifier as primary key.
    timestamp : datetime
        The time when the location is marked done.
    year_old: int
        year Marks which year the satellite photo was taken from our geo sources.
    year_new: int
        A newer photo to be compared with the one taken in year_old.
    source_url_root : str
        URL to store the location on the map.
    land_usage : int
        User's answer of judging a construction is built.
        0 means unknown.
        1 means building.
        2 means farm.
    expansion : int
        User's answer of judging the construction is expanded.
        0 means unknown.
        1 means no new expansion.
        2 means yes (there is expansion).
    is_gold_standard : bool
        If it is a golden standard answer provided by admnin.
    bbox_left_top_lat : float
        The latitude of the top-left corner of the bounding box for displaying the focus.
    bbox_left_top_lng : float
        The longitude of the top-left corner of the bounding box for displaying the focus.
    bbox_bottom_right_lat : float
        The latitude of the bottom-right corner of the bounding box for displaying the focus.
    bbox_bottom_right_lng : float
        The longitude of the bottom-right corner of the bounding box for displaying the focus.
    zoom_level : int
        The zoom level for displaying the location.
    user_id : int
        Foreign key to the user table.
    location_id : int
        Foreign key to the location table.
    """
    # Basic information
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    year_old = db.Column(db.Integer, nullable=False)
    year_new = db.Column(db.Integer, nullable=False)
    source_url_root = db.Column(db.String, nullable=True)

    # User answers
    land_usage = db.Column(db.Integer, nullable=False)
    expansion = db.Column(db.Integer, nullable=False)
    is_gold_standard = db.Column(db.Boolean, nullable=False)
    bbox_left_top_lat = db.Column(db.Float, default=0)
    bbox_left_top_lng = db.Column(db.Float, default=0)
    bbox_bottom_right_lat = db.Column(db.Float, default=0)
    bbox_bottom_right_lng = db.Column(db.Float, default=0)
    zoom_level = db.Column(db.Integer, default=0)

    # Build N to 1 relationship to location and user table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)

    def __repr__(self):
        return "<id=%r user_id=%r location_id=%r timestamp=%r year_old=%r year_new=%r \
                source_url_root=%r land_usage=%r expansion=%r is_gold_standard=%r \
                bbox_left_top_lat=%r bbox_left_top_lng=%r bbox_bottom_right_lat=%r \
                bbox_bottom_right_lng=%r zoom_level=%r>" % (self.id,
                self.user_id, self.location_id, self.timestamp, self.year_old,
                self.year_new, self.source_url_root, self.land_usage, self.expansion,
                self.is_gold_standard, self.bbox_left_top_lat, self.bbox_left_top_lng,
                self.bbox_bottom_right_lat, self.bbox_bottom_right_lng, self.zoom_level)
