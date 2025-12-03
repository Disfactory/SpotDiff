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
        Create an answer and check if returns an answer and its factory_id as expected. Pass if both.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"
        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4
        PASS_GOLD_TEST = 1

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user = user_operations.create_user(CLIENT_ID)

        # Create answer
        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                PASS_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        assert answer in db.session
        assert answer.user_id == user1.id
        assert answer.location_id == location1.id
        assert answer.gold_standard_status == PASS_GOLD_TEST

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

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user = user_operations.create_user(CLIENT_ID)

        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                1, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        assert answer in db.session

        answer_id = answer.id
        answer_operations.remove_answer(answer_id)
        assert answer not in db.session

    def test_get_answer_by_id(self):
        """
        Create a answer, get its returned id.
        Check if it can be retrieved by the previously returned id. Pass if id is the same.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user_operations.create_user(CLIENT_ID)

        # Create an answer and retrieve back, compare the id
        answer = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                1, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        answer_id = answer.id
        retrieved_answer = answer_operations.get_answer_by_id(answer_id)
        assert retrieved_answer.id == answer_id

    def test_get_answers_by_user(self):
        """
        Create 2 answers with the same user, and create the 3rd answer with a different user.
        Get answers with the first user. Pass if only the first 2 answers are gotten.
        """
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"
        CLIENT_ID2 = "jjj"
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        user1 = user_operations.create_user(CLIENT_ID)
        user2 = user_operations.create_user(CLIENT_ID2)

        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                1, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                1, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user2.id, location1.id, 2000, 2010, "", 1, 1,
                1, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        retrieved_answers = answer_operations.get_answers_by_user(user1.id)
        assert len(retrieved_answers)==2

        assert answer1 in retrieved_answers
        assert answer2 in retrieved_answers
        assert answer3 not in retrieved_answers

    def test_get_answers_by_location(self):
        """
        Create 2 answers with the same location, and create the 3rd answer with a different location.
        Get answers with the first location. Pass if only the first 2 answers are gotten.
        """
        FACTORY_ID = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID = "kkk"
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        location2 = location_operations.create_location(FACTORY_ID2)
        user1 = user_operations.create_user(CLIENT_ID)

        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        retrieved_answers = answer_operations.get_answers_by_location(location1.id)
        assert len(retrieved_answers)==2

        assert answer1 in retrieved_answers
        assert answer2 in retrieved_answers
        assert answer3 not in retrieved_answers

    def test_get_answers_by_user_and_location(self):
        """
        Create 4 answers with 2 users and 2 locations respectively.
        Get answers with specified user and location. Pass if the exact answer is gotten.
        """
        FACTORY_ID1 = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID1 = "kkk"
        CLIENT_ID2 = "jjj"

        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID1)
        location2 = location_operations.create_location(FACTORY_ID2)
        user1 = user_operations.create_user(CLIENT_ID1)
        user2 = user_operations.create_user(CLIENT_ID2)

        # Create 4 answers for the combination of users/locations
        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user2.id, location1.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer4 = answer_operations.create_answer(user2.id, location2.id, 2000, 2010, "", 1, 1, 1,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        # Only one should be retrieved
        retrieved_answers = answer_operations.get_answers_by_user_and_location(user2.id, location2.id)
        assert len(retrieved_answers)==1

        assert answer1 not in retrieved_answers
        assert answer2 not in retrieved_answers
        assert answer3 not in retrieved_answers
        assert answer4 in retrieved_answers

    def test_get_answer_count(self):
        """
        Create 4 non-gold answers and 1 gold answer
        Get answer count. Pass if the count matches 5.
        """
        FACTORY_ID = "aaa"
        FACTORY_ID2 = "bbb"
        CLIENT_ID = "kkk"
        CLIENT2_ID = "mmm"
        IS_GOLD_STANDARD = 0
        PASS_GOLD_TEST = 1
        FAIL_GOLD_TEST = 2
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        location2 = location_operations.create_location(FACTORY_ID2)
        user1 = user_operations.create_user(CLIENT_ID)
        user2 = user_operations.create_user(CLIENT2_ID)

        # Create 4 non-golden and 1 golden answer
        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                PASS_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1,
                IS_GOLD_STANDARD, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                PASS_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer4 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                FAIL_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer5 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                PASS_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer6 = answer_operations.create_answer(user2.id, location1.id, 2000, 2010, "", 1, 1,
                PASS_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        user_answer_count = answer_operations.get_answer_count()
        assert(user_answer_count == 6)

        user_answer_count = answer_operations.get_answer_count(user2.id)
        assert(user_answer_count == 1)

    def test_get_gold_answer_by_location(self):
        """
        Create 4 answers. Only 1 of them is gold answer which belongs to the target location.
        Get gold answer for the target location. Pass if the expected answer successfully retrieved.
        """
        IS_GOLD_STANDARD = 0
        PASS_GOLD_TEST = 1
        FAIL_GOLD_TEST = 2
        FACTORY_ID = "aaa"
        CLIENT_ID = "kkk"
        CLIENT_ID_ADMIN = "admin"
        BBOX_LEFT_TOP_LAT = 0.5
        BBOX_LEFT_TOP_LNG = 0.6
        BBOX_BOTTOM_RIGHT_LAT = 0.7
        BBOX_BOTTOM_RIGHT_LNG = 0.8

        # Create user and location first for db consistency
        location1 = location_operations.create_location(FACTORY_ID)
        location2 = location_operations.create_location(CLIENT_ID_ADMIN)
        user1 = user_operations.create_user(CLIENT_ID)
        user_admin = user_operations.create_user(CLIENT_ID_ADMIN)
        answer1 = answer_operations.create_answer(user1.id, location1.id, 2000, 2010, "", 1, 1,
                PASS_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer2 = answer_operations.create_answer(user1.id, location2.id, 2000, 2010, "", 1, 1,
                FAIL_GOLD_TEST, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer3 = answer_operations.create_answer(user_admin.id, location1.id, 2000, 2010, "", 1, 1,
                IS_GOLD_STANDARD, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        answer4 = answer_operations.create_answer(user_admin.id, location2.id, 2000, 2010, "", 1, 1,
                IS_GOLD_STANDARD, BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        my_answer = answer_operations.get_gold_answer_by_location(location2.id)

        assert(my_answer is not None)
        assert(my_answer.user_id == user_admin.id)
        assert(my_answer.location_id == location2.id)
        assert(my_answer.gold_standard_status == IS_GOLD_STANDARD)

    def test_exam_gold_standard(self):
        """
        User admin create 1 gold standard, A_gold.
        User 1 creates A1, which pass the quality test with A_gold. Pass if the result is 1.
        User 1 creates A2, which has different expansion result with A_gold. Pass if the result is 2.
        User 1 creates A3, which have no gold standard to the location. Pass if the result is 0.
        """
        IS_GOLD_STANDARD = 0
        PASS_GOLD_TEST = 1
        FAIL_GOLD_TEST = 2
        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4
        user1 = user_operations.create_user("123")
        user_admin = user_operations.create_user("ADMIN")
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")

        A_gold = answer_operations.create_answer(user_admin.id, l1.id, 2000, 2010, "", 0, 1, IS_GOLD_STANDARD,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        A1 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 0, 1, PASS_GOLD_TEST,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        A2 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)
        A3 = answer_operations.create_answer(user1.id, l2.id, 2000, 2010, "", 1, 1, FAIL_GOLD_TEST,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)

        result = answer_operations.exam_gold_standard(A1.location_id, A1.land_usage, A1.expansion)
        assert(result==1)
        result = answer_operations.exam_gold_standard(A2.location_id, A2.land_usage, A2.expansion)
        assert(result==2)
        result = answer_operations.exam_gold_standard(A3.location_id, A3.land_usage, A3.expansion)
        assert(result==0)

    def test_is_answer_reliable(self):
        """
        u1 failed the gold standard, but still submit answer a1 to location #l1.
        u2 passes the gold standard test, and submit the same result with u1. Fail if is_answer_reliable True.
        u3 passes the gold standard test, but have different answer with u1 or u2. Fail if is_answer_reliable true.
        u4 passes the gold standard test, and have the same result with u1 and u2. Fail if is_answer_reliable false.
        """
        PASS_GOLD_TEST = 1
        FAIL_GOLD_TEST = 2
        user1 = user_operations.create_user("123")
        user2 = user_operations.create_user("456")
        user3 = user_operations.create_user("789")
        user4 = user_operations.create_user("000")
        l1 = location_operations.create_location("AAA")

        # u1 failed the gold standard.
        a1 = answer_operations.create_answer(user1.id, l1.id, 2000, 2010, "", 1, 1, FAIL_GOLD_TEST,
                0, 0, 0, 0, 0)

        # u2 pass the gold test.
        result = answer_operations.is_answer_reliable(l1.id, 1, 1)
        assert(result == False)
        a2 = answer_operations.create_answer(user2.id, l1.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST,
                0, 0, 0, 0, 0)

        # u3 passes the gold test, but have different answer with u2.
        result = answer_operations.is_answer_reliable(l1.id, 1, 0)
        assert(result == False)
        a3 = answer_operations.create_answer(user3.id, l1.id, 2000, 2010, "", 1, 0, PASS_GOLD_TEST,
                0, 0, 0, 0, 0)

        # u4 passes the gold test, and have the same answer with u2.
        result = answer_operations.is_answer_reliable(l1.id, 1, 1)
        assert(result == True)
        a4 = answer_operations.create_answer(user4.id, l1.id, 2000, 2010, "", 1, 1, PASS_GOLD_TEST,
                0, 0, 0, 0, 0)


    def test_set_answer(self):
        """
        Create a gold answer then change it to disabled. 
        Get it again and check if the gold_standard_status updated.
        """
        IS_GOLD_STANDARD = 0
        IS_DISABLED_GOLD_STANDARD = 3
        BBOX_LEFT_TOP_LAT = 0.1
        BBOX_LEFT_TOP_LNG = 0.2
        BBOX_BOTTOM_RIGHT_LAT = 0.3
        BBOX_BOTTOM_RIGHT_LNG = 0.4
        user_admin = user_operations.create_user("ADMIN")
        l1 = location_operations.create_location("AAA")

        A_gold = answer_operations.create_answer(user_admin.id, l1.id, 2000, 2010, "", 0, 1, IS_GOLD_STANDARD,
                BBOX_LEFT_TOP_LAT, BBOX_LEFT_TOP_LNG, BBOX_BOTTOM_RIGHT_LAT, BBOX_BOTTOM_RIGHT_LNG, 0)            
        
        assert(A_gold.gold_standard_status==IS_GOLD_STANDARD)
        
        A_updated = answer_operations.set_answer(A_gold.id, IS_DISABLED_GOLD_STANDARD, 2, 0)

        assert(A_updated.gold_standard_status==IS_DISABLED_GOLD_STANDARD)
        assert(A_updated.land_usage==2)
        assert(A_updated.expansion==0)
        

    def test_batch_process_answers(self):
        """
        Location #l1 has gold standard.
        User u1 passes the standard test, and submit answers to #l2 and #l3.
        User u2 fails the standard test, only #l2 matches u1's answer.
        User u3 passes the standard test, only #l2 matches u1's answer.
        User u4 passes the standard test, only #l4 matches u1's answer.
        User u5 submits an answer without source root.
        Pass if location done_at correct after each user's answer submit, and individual_done_count correct, 
        and u5's answer sends assertion.
        """
        IS_GOLD_STANDARD = 0
        user1 = user_operations.create_user("123")
        user2 = user_operations.create_user("456")
        user3 = user_operations.create_user("789")
        user4 = user_operations.create_user("000")
        user_admin = user_operations.create_user("ADMIN")
        l1 = location_operations.create_location("AAA")
        l2 = location_operations.create_location("BBB")
        l3 = location_operations.create_location("CCC")
        l4 = location_operations.create_location("DDD")
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

        # missing "source_url_root"
        user4_answers=[
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
             "expansion": 1},
            {"location_id": l4.id,
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
            {"location_id": l4.id,
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
        result = answer_operations.batch_process_answers(user1.id, user1_answers)
        assert(result==True)
        assert(l2.done_at is None)
        assert(l3.done_at is None)

        # User u2 fails the standard test, only #l2 matches u1.
        result = answer_operations.batch_process_answers(user2.id, user2_answers)
        assert(result==False)
        assert(l2.done_at is None)
        assert(l3.done_at is None)

        # User u3 passes the standard test, only #l2 matches u1. #l2 Done criteria reaches.
        result = answer_operations.batch_process_answers(user3.id, user3_answers)
        assert(result==True)
        assert(l2.done_at is not None)
        assert(l3.done_at is None)

        loc_count = user_operations.get_user_done_location_count(user2.id)
        assert(loc_count == len(user2_answers))

        # User u4 creates invalid answers, missing parameters
        with self.assertRaises(Exception) as context:        
            result = answer_operations.batch_process_answers(user4.id, user4_answers)

if __name__ == "__main__":
    unittest.main()
