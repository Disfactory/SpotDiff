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
        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user = user_operations.create_user(CLIENT_ID)

        # create answer 
        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        
        assert answer in db.session
        assert answer.user_id == user1.id
        assert answer.location_id == location1.id


    def test_create_answer_with_result(self):
        """
          1. Create a gold answer
          2. Create a wrong answer, an answer without gold answer reference, and a correct answer. Pass if the compare result as expected.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "ADMIN"        
        CLIENT_ID2 = "KKK"        
        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user = user_operations.create_user(CLIENT_ID)
        user2 = user = user_operations.create_user(CLIENT_ID2)

        # create a gold answer for reference
        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        

        # create a wrong answer
        result = answer_operations.create_answer_with_result(user2.id, location1.id, 2000, 2010, "", 0, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        assert result == 1

        # create an answer which has no golden answer mapping
        result = answer_operations.create_answer_with_result(user2.id, location1.id, 2000, 2011, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        assert result == -1

        # create a correct answer
        result = answer_operations.create_answer_with_result(user2.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        assert result == 0


    def test_remove_answer(self):
        """
          Create then remove an answer. 
          Check if the answer first existed in db, then removed successfully. Pass if both.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"

        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user = user_operations.create_user(CLIENT_ID)

        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
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
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user_operations.create_user(CLIENT_ID)

        # Create an answer and retrieve back, compare the id
        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        

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
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user_operations.create_user(CLIENT_ID)
        user2 = user_operations.create_user(CLIENT_ID2)

        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user2.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

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
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        location2 = location_operations.create_location(FACTORY_ID2)
        user1 = user_operations.create_user(CLIENT_ID)

        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        retrieved_answers = answer_operations.get_answers_by_location(location1.id)
        assert len(retrieved_answers)==2

        assert answer1 in retrieved_answers
        assert answer2 in retrieved_answers
        assert answer3 not in retrieved_answers


    def test_get_answers_by_user_and_location(self):
        """
          1. Create 4 answers with 2 users and 2 locations respectively.
          2. Get answers with specified user and location. Pass if the exact answer is gotten.
        """
        FACTORY_ID1 = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID1 = "kkk"
        CLIENT_ID2 = "jjj"

        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID1)
        location2 = location_operations.create_location(FACTORY_ID2)
        user1 = user_operations.create_user(CLIENT_ID1)
        user2 = user_operations.create_user(CLIENT_ID2)

        # create 4 answers for the combination of users/locations
        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer2 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer3 = answer_operations.create_answer(user2.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer4 = answer_operations.create_answer(user2.id, location2.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        # Only one should be retrieved
        retrieved_answers = answer_operations.get_answers_by_user_and_location(user2.id, location2.id)
        assert len(retrieved_answers)==1

        assert answer1 not in retrieved_answers
        assert answer2 not in retrieved_answers
        assert answer3 not in retrieved_answers
        assert answer4 in retrieved_answers


    def test_get_answer_count(self):
        """
            1. Create 4 non-gold answers and 1 gold answer
            2. Get answer count. Pass if the count matches 4.
        """
        FACTORY_ID = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID = "kkk"
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        location2 = location_operations.create_location(FACTORY_ID2)
        user1 = user_operations.create_user(CLIENT_ID)

        # create 4 non-golden and 1 golden answer
        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer4 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer5 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        user_answer_count = answer_operations.get_answer_count()
        assert(user_answer_count == 4)


    def test_get_gold_answer(self):
        """
            1. Create 4 answers. Only 1 of them is gold answer which belongs to the target location.
            2. Get gold answer for the target location. Pass if the expected answer successfully retrieved.
        """
        FACTORY_ID = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID = "kkk"
        CLIENT_ID_ADMIN = "admin"
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # create user and location first for db consistency.
        location1 = location_operations.create_location(FACTORY_ID)
        location2 = location_operations.create_location(CLIENT_ID_ADMIN)
        user1 = user_operations.create_user(CLIENT_ID)
        user_admin = user_operations.create_user(CLIENT_ID_ADMIN)
        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user_admin.id, location1.id, 2000, 2010, "", 1, 1, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer4 = answer_operations.create_answer(user_admin.id, location2.id, 2000, 2010, "", 1, 1, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        
        my_answer = answer_operations.get_gold_answer_by_location(location2.id)
        
        assert(my_answer is not None)
        assert(my_answer.user_id == user_admin.id)
        assert(my_answer.location_id == location2.id)
        assert(my_answer.is_gold_standard == True)



    def test_is_answer_passed(self):
        """
        1. user 1 creates 1 incorrect answer and 1 incorrect answer to different locations. (Admin creates 2 gold answers.)
        2. Pass if the test is correct.
        """        
        user1 = user_operations.create_user("123")
        user_admin = user_operations.create_user("ADMIN")
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")

        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4
        answer1 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer1_gold = answer_operations.create_answer(user_admin.id, l1.id, 2000, 2010, "", 0, 1, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer2 = answer_operations.create_answer(user1.id, l2.id, 2000, 2010, "", 1, 1, False, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        
        answer2_gold = answer_operations.create_answer(user_admin.id, l2.id, 2000, 2010, "", 1, 1, True, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)        

        is_answer1_passed = answer_operations.is_answer_passed(answer1.id)
        assert(is_answer1_passed==False)
        is_answer2_passed = answer_operations.is_answer_passed(answer2.id)
        assert(is_answer2_passed==True)

        
if __name__ == "__main__":
    unittest.main()
