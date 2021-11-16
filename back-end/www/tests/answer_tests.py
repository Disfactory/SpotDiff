from basic_tests import BasicTest
from models.model_operations import answer_operations
from models.model_operations import location_operations
from models.model_operations import user_operations
from models.model import db
import unittest


class AnswerTest(BasicTest):
    """Test case for answers."""

    def setUp(self):
        db.create_all()

    def test_create_answer(self):
        """
          Create an answer and check if returns an answer, and its factory_id as expected. Pass if both.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"        
        BBOX_LEFT_UP_LAT = 0.1
        BBOX_LEFT_UP_LNG = 0.2
        BBOX_RIGHT_DOWN_LAT = 0.3
        BBOX_RIGHT_DOWN_LNG = 0.4

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID, 2000, "")
        user1 = user = user_operations.create_user(CLIENT_ID)

        # create answer 
        answer = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        
        assert answer in db.session
        assert answer.user_id == user1.id
        assert answer.location_id == location1.id

    def test_remove_answer(self):
        """
          Create then remove an answer. 
          Check if the answer first existed in db, then removed successfully. Pass if both.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"

        BBOX_LEFT_UP_LAT = 0.5
        BBOX_LEFT_UP_LNG = 0.6
        BBOX_RIGHT_DOWN_LAT = 0.7
        BBOX_RIGHT_DOWN_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID, 2000, "")
        user1 = user = user_operations.create_user(CLIENT_ID)

        answer = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        assert answer in db.session

        answer_id = answer.id
        answer_operations.remove_answer(answer_id)
        assert answer not in db.session

    def test_get_answer_by_id(self):
        """
          1. Create a answer, get its returned id.
          2. Check if it can be retrieved by the previously returned id. Pass if id is the same.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"
        BBOX_LEFT_UP_LAT = 0.5
        BBOX_LEFT_UP_LNG = 0.6
        BBOX_RIGHT_DOWN_LAT = 0.7
        BBOX_RIGHT_DOWN_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID, 2000, "")
        user1 = user_operations.create_user(CLIENT_ID)

        # Create an answer and retrieve back, compare the id
        answer = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)

        answer_id = answer.id
        retrieved_answer = answer_operations.get_answer_by_id(answer_id)
        assert retrieved_answer.id == answer_id


    def test_get_answers_by_user(self):
        """
          1. Create 2 answers with the same user, and create the 3rd answer with a different user.
          2. Get answers with the first user. Pass if only the first 2 answers are gotten.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"
        CLIENT_ID2 = "jjj"
        BBOX_LEFT_UP_LAT = 0.5
        BBOX_LEFT_UP_LNG = 0.6
        BBOX_RIGHT_DOWN_LAT = 0.7
        BBOX_RIGHT_DOWN_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID, 2000, "")
        user1 = user_operations.create_user(CLIENT_ID)
        user2 = user_operations.create_user(CLIENT_ID2)

        answer1 = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer2 = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer3 = answer_operations.create_answer(user2.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)

        retrieved_answers = answer_operations.get_answers_by_user(user1.id)
        assert len(retrieved_answers)==2

        assert answer1 in retrieved_answers
        assert answer2 in retrieved_answers
        assert answer3 not in retrieved_answers

    def test_get_answers_by_location(self):
        """
          1. Create 2 answers with the same location, and create the 3rd answer with a different location.
          2. Get answers with the first location. Pass if only the first 2 answers are gotten.
        """
        FACTORY_ID = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID = "kkk"
        BBOX_LEFT_UP_LAT = 0.5
        BBOX_LEFT_UP_LNG = 0.6
        BBOX_RIGHT_DOWN_LAT = 0.7
        BBOX_RIGHT_DOWN_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID, 2000, "")
        location2 = location_operations.create_location(FACTORY_ID2, 2000, "")
        user1 = user_operations.create_user(CLIENT_ID)

        answer1 = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer2 = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer3 = answer_operations.create_answer(user1.id, location2.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)

        retrieved_answers = answer_operations.get_answers_by_location(location1.id)
        assert len(retrieved_answers)==2

        assert answer1 in retrieved_answers
        assert answer2 in retrieved_answers
        assert answer3 not in retrieved_answers


    def test_get_answers_by_user_and_location(self):
        """
          1. Create 4 answers with 2 user and 2 locations respectively.
          2. Get answers with specified user and location. Pass if the exact answer is gotten.
        """
        FACTORY_ID1 = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID1 = "kkk"
        CLIENT_ID2 = "jjj"

        BBOX_LEFT_UP_LAT = 0.5
        BBOX_LEFT_UP_LNG = 0.6
        BBOX_RIGHT_DOWN_LAT = 0.7
        BBOX_RIGHT_DOWN_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID1, 2000, "")
        location2 = location_operations.create_location(FACTORY_ID2, 2000, "")
        user1 = user_operations.create_user(CLIENT_ID1)
        user2 = user_operations.create_user(CLIENT_ID2)

        # create 4 answers for the combination of users/locations
        answer1 = answer_operations.create_answer(user1.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer2 = answer_operations.create_answer(user1.id, location2.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer3 = answer_operations.create_answer(user2.id, location1.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)
        answer4 = answer_operations.create_answer(user2.id, location2.id, 1, 1, 0, BBOX_LEFT_UP_LAT, BBOX_LEFT_UP_LNG, BBOX_RIGHT_DOWN_LAT, BBOX_RIGHT_DOWN_LNG)

        # Only one should be retrieved
        retrieved_answers = answer_operations.get_answers_by_user_and_location(user2.id, location2.id)
        assert len(retrieved_answers)==1

        assert answer1 not in retrieved_answers
        assert answer2 not in retrieved_answers
        assert answer3 not in retrieved_answers
        assert answer4 in retrieved_answers


if __name__ == "__main__":
    unittest.main()
