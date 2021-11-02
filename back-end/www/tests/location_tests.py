from basic_tests import BasicTest
from models.model_operations import location_operations
from models.model import db
import unittest


class LocationTest(BasicTest):
    """Test case for locations."""

    def setUp(self):
        db.create_all()

    def test_create_location(self):
        location = location_operations.create_location("AAAA")
        #print("create location : " + location.factory_id)
        assert location in db.session

    def test_get_location_by_id(self):
        factory_id = "BBBB"
        location = location_operations.create_location(factory_id)
        location_id = location.id
        retrieved_location = location_operations.get_location_by_id(location_id)
        assert retrieved_location.id == location_id

    def test_get_location_by_factory_id(self):
        factory_id = "CCCC"
        location = location_operations.create_location(factory_id)
        retrieved_location = location_operations.get_location_by_factory_id(factory_id)
        assert retrieved_location.id == location.id

    def test_remove_user(self):
        factory_id = "DDD"
        location = location_operations.create_location(factory_id)
        assert location in db.session
        location_id = location.id
        location_operations.remove_location(location_id)
        assert location not in db.session


if __name__ == "__main__":
    unittest.main()
