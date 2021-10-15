from basic_tests import BasicTest
from models.model_operations import user_operations
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


if __name__ == "__main__":
    unittest.main()
