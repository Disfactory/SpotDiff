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
