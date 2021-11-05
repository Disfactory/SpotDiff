from basic_tests import BasicTest
from models.model_operations import location_operations
from models.model import db
import unittest


class LocationTest(BasicTest):
    """Test case for locations."""

    def setUp(self):
        db.create_all()

    def test_create_location(self):
        """
          Create a location and check if returns a location, and its factory_id as expected. Pass if both.
        """
        FACTORY_ID = "AAAA"
        location = location_operations.create_location(FACTORY_ID)
        #print("create location : " + location.factory_id)
        assert location in db.session
        assert location.factory_id == FACTORY_ID

    def test_remove_location(self):
        """
          Remove the created test case in the previous test. 
          Check if the location first existed in db, then removed successfully. Pass if both.
        """
        FACTORY_ID = "EEEE"
        location = location_operations.create_location(FACTORY_ID)
        assert location in db.session
        location_id = location.id
        location_operations.remove_location(location_id)
        assert location not in db.session

    def test_get_location_by_id(self):
        """
          1. Create a location, get its returned id.
          2. Check if it can be retrieved by the previously returned id. Pass if id is the same.
        """
        FACTORY_ID = "BBBB"
        location = location_operations.create_location(FACTORY_ID)
        location_id = location.id
        retrieved_location = location_operations.get_location_by_id(location_id)
        assert retrieved_location.id == location_id

    def test_get_location_by_factory_id(self):
        """
          1. Create a location with specified factory_id
          2. Get the location with the factory_id. Pass if it exists and the factory_id matches.
        """
        FACTORY_ID = "CCCC"
        location = location_operations.create_location(FACTORY_ID)
        retrieved_location = location_operations.get_location_by_factory_id(FACTORY_ID)
        assert retrieved_location != None
        assert retrieved_location.id == location.id

    def test_config_location_basic_by_id(self):
        """
        1. create a location
        2. Change its factory_id, year, url. Pass if all matched.
        """        
        FACTORY_ID = "DDDD"
        NEW_FACTORY_ID = "XXXX"
        YEAR = 1234
        URL = "www.xxx.org"

        location = location_operations.create_location(FACTORY_ID)
        retrieved_location = location_operations.get_location_by_factory_id(FACTORY_ID)
        assert retrieved_location.id == location.id
        
        retrieved_location = location_operations.update_location_basic_by_id(location.id, NEW_FACTORY_ID, YEAR, URL)
        assert retrieved_location.factory_id == NEW_FACTORY_ID
        assert retrieved_location.year == YEAR
        assert retrieved_location.url == URL

        
    def test_config_location_bbox_by_id(self):
        """
        1. create a location, check if successful
        2. Change its bounding box position. Pass if all coordinates match.
        """        
        FACTORY_ID = "DDDD"
        BBOX_LEFT_UP_LAT = 0.1
        BBOX_LEFT_UP_LNG = 0.2
        BBOX_RIGHT_DOWN_LAT = 0.3
        BBOX_RIGHT_DOWN_LNG = 0.4

        location = location_operations.create_location(FACTORY_ID)
        retrieved_location = location_operations.get_location_by_factory_id(FACTORY_ID)
        assert retrieved_location.id == location.id
        
        updated_location = location_operations.update_location_bbox_by_id(retrieved_location.id, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        assert updated_location.bbox_left_up_lat == BBOX_LEFT_UP_LAT
        assert updated_location.bbox_left_up_lng == BBOX_LEFT_UP_LNG
        assert updated_location.bbox_right_down_lat == BBOX_RIGHT_DOWN_LAT
        assert updated_location.bbox_right_down_lng == BBOX_RIGHT_DOWN_LNG


if __name__ == "__main__":
    unittest.main()
