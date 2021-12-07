from basic_tests import BasicTest
from models.model_operations import user_operations
from models.model_operations import location_operations
from models.model_operations import answer_operations
from models.model import db
import unittest


class UserTest(BasicTest):
    """Test case for users."""
    def setUp(self):
        db.create_all()


    def test_create_user(self):
        user = user_operations.create_user("123")
        assert user in db.session


    def test_get_user_by_id(self):
        client_id = "456"
        user = user_operations.create_user(client_id)
        user_id = user.id
        retrieved_user = user_operations.get_user_by_id(user_id)
        assert retrieved_user.client_id == client_id


    def test_get_user_by_client_id(self):
        client_id = "456"
        user = user_operations.create_user(client_id)
        retrieved_user = user_operations.get_user_by_client_id(client_id)
        assert retrieved_user.id == user.id


    def test_remove_user(self):
        client_id = "789"
        user = user_operations.create_user(client_id)
        assert user in db.session
        user_id = user.id
        user_operations.remove_user(user.id)
        assert user not in db.session


    def test_get_all_users(self):
        client_id = "123"
        user1 = user_operations.create_user(client_id)
        assert user1 in db.session
        client_id = "456"
        user2 = user_operations.create_user(client_id)
        assert user2 in db.session
        users = user_operations.get_all_users()
        assert(len(users) == 2)


    def test_get_user_count(self):
        client_id = "123"
        user1 = user_operations.create_user(client_id)
        assert user1 in db.session
        client_id2 = "456"
        user2 = user_operations.create_user(client_id2)
        assert user2 in db.session
        count = user_operations.get_user_count()
        assert(count == 2)


    def test_get_user_done_location_count(self):
        """
        1. user 1 creates 3 answers to l1, and 2 answers to l2. user_admin creates 1 answer to l1.
        2. Check the return value of get_user_done_location_count for user 1. Pass if 2 returns.
        """

        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4

        client_id = "123"
        user1 = user_operations.create_user(client_id)
        user_admin = user_operations.create_user("ADMIN")
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        answer1 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer2 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer3 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 0, 0, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer4 = answer_operations.create_answer(user_admin.id, l1.id, 2000, 2010, "", 0, 0, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        

        answer4 = answer_operations.create_answer(user1.id, l2.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer5 = answer_operations.create_answer(user1.id, l2.id, 2000, 2010, "", 1, 0, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        

        done_loc_count = user_operations.get_user_done_location_count(user1.id)
        assert(done_loc_count == 2)


if __name__ == "__main__":
    unittest.main()
