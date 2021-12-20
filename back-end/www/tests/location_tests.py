from basic_tests import BasicTest
from models.model_operations import location_operations
from models.model_operations import answer_operations
from models.model_operations import user_operations
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
        Create a location, get its returned id.
        Check if it can be retrieved by the previously returned id. Pass if id is the same.
        """
        FACTORY_ID = "AAAA"

        location = location_operations.create_location(FACTORY_ID)
        location_id = location.id
        retrieved_location = location_operations.get_location_by_id(location_id)
        assert retrieved_location.id == location_id

    def test_get_location_by_factory_id(self):
        """
        Create a location with specified factory_id
        Get the location with the factory_id. Pass if it exists and the factory_id matches.
        """
        FACTORY_ID = "CCCC"

        location = location_operations.create_location(FACTORY_ID)
        retrieved_location = location_operations.get_location_by_factory_id(FACTORY_ID)
        assert retrieved_location != None
        assert retrieved_location.id == location.id

    def test_set_location_done(self):
        """
        Create a location with specified factory_id
        Set it done and check the done date. Pass if it's first None then not None after set.
        """
        FACTORY_ID = "CCCC"

        location = location_operations.create_location(FACTORY_ID)
        assert(location.done_at == None)

        location_done = location_operations.set_location_done(location.id, True)
        assert(location_done.done_at != None)

    def test_get_locations(self):
        """
        Test no location situation. Pass if assert raises.
        Create several Answers which belong to 8 locations.
            Only Loc#2 and Loc#3 have gold answers.
            Loc#6 never answered by anyone.
            Loc#7 has been identified by user u2.
            Loc#8 is marked Done.
        Randomly get locations for user 2, size=5 and gold_standard_size=1 for 10 times.
            Pass if 5 locations are gotten (not including Loc#7 or Loc#8).
            And only 1 of the 2 locations which have gold answers are gotten.
        Test not enough gold standards. Pass if assert raises.
        Test not enough location. Pass if assert raises.
        """
        IS_GOLD_STANDARD = 0
        PASS_GOLD_TEST = 1
        FAIL_GOLD_TEST = 2

        u1 = user_operations.create_user("111")
        u2 = user_operations.create_user("222")

        # Check for no location exist exception.
        with self.assertRaises(Exception) as context:
            locations = location_operations.get_locations(u2.id, 5, 1)

        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")
        l4 = location_operations.create_location("DDD")
        l5 = location_operations.create_location("EEE")
        l6 = location_operations.create_location("FFF")
        l7 = location_operations.create_location("GGG")
        l8 = location_operations.create_location("GGG")

        # Mark l8 done, so it shouldn't be gotten.
        location_operations.set_location_done(l8.id, True)

        # Only l2 and l3 has gold answers. l1, l4, l5, l6 doesn't, so they will always be gotten.
        answer_operations.create_answer(u1.id, l1.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)

        answer_operations.create_answer(u1.id, l2.id, 2000, 2010, "", 1, 1, IS_GOLD_STANDARD, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l2.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l2.id, 2000, 2010, "", 1, 1, FAIL_GOLD_TEST, 0, 0, 0, 0, 0)

        answer_operations.create_answer(u1.id, l3.id, 2000, 2010, "", 1, 1, IS_GOLD_STANDARD, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l3.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l3.id, 2000, 2010, "", 1, 1, FAIL_GOLD_TEST, 0, 0, 0, 0, 0)

        answer_operations.create_answer(u1.id, l4.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l4.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l4.id, 2000, 2010, "", 1, 1, FAIL_GOLD_TEST, 0, 0, 0, 0, 0)

        answer_operations.create_answer(u1.id, l5.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)
        answer_operations.create_answer(u1.id, l5.id, 2000, 2010, "", 1, 1, FAIL_GOLD_TEST, 0, 0, 0, 0, 0)

        # User answered l7, so it shouldn't be gotten.
        answer_operations.create_answer(u2.id, l7.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST, 0, 0, 0, 0, 0)

        # Test a common scenario.
        for i in range(10):
            locations = location_operations.get_locations(u2.id, 5, 1)

        assert len(locations)==5
        assert not (l2 in locations and l3 in locations)
        assert  l2 in locations or l3 in locations
        assert not (l7 in locations or l8 in locations)

        # Check if exception raises : not enough gold standards.
        with self.assertRaises(Exception) as context:
          locations = location_operations.get_locations(u2.id, 5, 3)

        # Check if exception raises : not enough locations.
        with self.assertRaises(Exception) as context:
          locations = location_operations.get_locations(u2.id, 7, 3)

    def test_get_location_is_done_count(self):
        """
        Create 4 locations, mark 3 to be done.
        Get the location is done count. Pass if 3.
        """
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")
        l4 = location_operations.create_location("DDD")

        location = location_operations.set_location_done(l1.id, True)
        location = location_operations.set_location_done(l2.id, True)
        location = location_operations.set_location_done(l4.id, True)

        count = location_operations.get_location_is_done_count()
        assert count == 3

    def test_get_location_count(self):
        """
        Create 4 locations
        Get the location count. Pass if 4.
        """
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")
        l4 = location_operations.create_location("DDD")
        count = location_operations.get_location_count()
        assert count == 4

    def test_batch_process_answers(self):
        """
        Location #l1 has gold standard.
        User u1 passes the standard test, and submit answers to #l2 and #l3.
        User u2 fails the standard test, only #l2 matches u1's answer.
        User u3 passes the standard test, only #l2 matches u1's answer.
        User u4 passes the standard test, only #l4 matches u1's answer.
        Pass if location done_at correct after each user's answer submit, and individual_done_count correct.
        """
        IS_GOLD_STANDARD = 0
        user1 = user_operations.create_user("123")
        user2 = user_operations.create_user("456")
        user3 = user_operations.create_user("789")
        user_admin = user_operations.create_user("ADMIN")
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")

        assert(l2.done_at==None)

        # l1 has gold answer.
        A_gold = answer_operations.create_answer(user_admin.id, l1.id, 2000, 2010, "", 1, 1, IS_GOLD_STANDARD,
                0, 0, 0, 0, 0)

        user1_answers=[
            {"location_id": l1.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 1,
             "expansion": 1,
             "source_url_root": "xxx"},
            {"location_id": l2.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 1,
             "expansion": 1,
             "source_url_root": "xxx"},
            {"location_id": l3.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 1,
             "expansion": 1,
             "source_url_root": "xxx"},
        ]

        user2_answers=[
            {"location_id": l1.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 0,
             "expansion": 0,
             "source_url_root": "xxx"},
            {"location_id": l2.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 1,
             "expansion": 1,
             "source_url_root": "xxx"},
            {"location_id": l3.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 0,
             "expansion": 0,
             "source_url_root": "xxx"},
        ]

        user3_answers=[
            {"location_id": l1.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 1,
             "expansion": 1,
             "source_url_root": "xxx"},
            {"location_id": l2.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 1,
             "expansion": 1,
             "source_url_root": "xxx"},
            {"location_id": l3.id,
             "year_new": 2000,
             "year_old": 1997,
             "zoom_level": 0,
             "left_top_lat": 0,
             "left_top_lng": 0,
             "bbox_left_top_lat": 0,
             "bbox_left_top_lng": 0,
             "bbox_bottom_right_lat": 0,
             "bbox_bottom_right_lng": 0,
             "land_usage": 0,
             "expansion": 0,
             "source_url_root": "xxx"},
        ]

        # User u1 passes the standard test, and submit answers to #l2 and #l3.
        result = location_operations.batch_process_answers(user1.id, user1_answers)
        assert(result==True)
        assert(l2.done_at is None)
        assert(l3.done_at is None)

        # User u2 fails the standard test, only #l2 matches u1.
        result = location_operations.batch_process_answers(user2.id, user2_answers)
        assert(result==False)
        assert(l2.done_at is None)
        assert(l3.done_at is None)

        # User u3 passes the standard test, only #l2 matches u1. #l2 Done criteria reaches.
        result = location_operations.batch_process_answers(user3.id, user3_answers)
        assert(result==True)
        assert(l2.done_at is not None)
        assert(l3.done_at is None)

        loc_count = user_operations.get_user_done_location_count(user2.id)
        assert(loc_count == len(user2_answers))


if __name__ == "__main__":
    unittest.main()
