"""Schema for object serialization and deserialization."""

from flask_marshmallow import Marshmallow
from models.model import User
from models.model import Location

# Use Marshmallow to simplify object–relational mapping
ma = Marshmallow()


class UserSchema(ma.Schema):
    """The schema for the User table, used for jsonify."""
    class Meta:
        model = User
        fields = ("id", "created_at", "client_id", "client_type")
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class LocationSchema(ma.Schema):
    """The schema for the location table, used for jsonify."""
    class Meta:
        model = Location
        fields = ("id", "factory_id")
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)        