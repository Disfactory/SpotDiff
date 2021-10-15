"""Functions to operate the user table."""

from models.model import db
from models.model import User


def create_user(client_id):
    """
    Create a user.

    Parameters
    ----------
    client_id : str
        ID provided by an external authentication service.

    Returns
    -------
    user : User
        The newly created user.
    """
    user = User(client_id=client_id)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(user_id):
    """
    Get a user by its ID.

    Parameters
    ----------
    user_id : int
        ID of the user.

    Returns
    -------
    user : User
        The retrieved user object.
    """
    user = User.query.filter_by(id=user_id).first()

    return user


def get_user_by_client_id(client_id):
    """
    Get a user by its client ID.

    Parameters
    ----------
    client_id : int
        ID of the user.

    Returns
    -------
    user : User
        The retrieved user object.
    """
    user = User.query.filter_by(client_id=client_id).first()

    return user


def get_all_users():
    """
    Get all users.

    Returns
    -------
    users : list of User
        The list of retrieved user objects.
    """
    # TODO: need a testing case
    users = User.query.all()

    return users


def update_client_type_by_user_id(user_id, client_type):
    """
    Update client type by user ID.

    Parameters
    ----------
    user_id : int
        ID of the user.
    client_type : int
        Type of the user (see the description in the User model).

    Raises
    ------
    exception : Exception
        When no user is found.
    """
    # TODO: need a testing case
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise Exception("No user found in the database to update.")

    user.client_type = client_type

    db.session.commit()

    return user


def remove_user(user_id):
    """
    Remove a user.

    Parameters
    ----------
    user_id : int
        ID of the user.

    Raises
    ------
    exception : Exception
        When no user is found.
    """
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise Exception("No user found in the database to delete.")

    db.session.delete(user)
    db.session.commit()
