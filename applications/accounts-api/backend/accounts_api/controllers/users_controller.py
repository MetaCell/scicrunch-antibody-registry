import connexion
import six
from cloudharness.auth import AuthClient
from accounts_api.models import User, UpdatePassword  # noqa: E501
from accounts_api import util


from accounts_api.services import user_service


def create_user(user):  # noqa: E501
    """create_user

     # noqa: E501

    :param user: 
    :type user: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_user(userid):  # noqa: E501
    """get_user

     # noqa: E501

    :param userid: user id
    :type userid: str

    :rtype: User
    """
    try:
        return user_service.get_user(userid)
    except user_service.UserNotFound as e:
        return "User not found", 404


def get_users(query={}):
    """get all users

    :param query: user filter
    :type query: str

    :rtype: {}
    """

    return {'users': user_service.get_users(query)}


def update_user(userid, user=None):  # noqa: E501
    """get_user

     # noqa: E501

    :param userid: user id
    :type userid: str

    :rtype: User
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        return user_service.update_user(userid, user)
    except user_service.UserNotFound as e:
        return "User not found", 404
    except user_service.UserNotAuthorized as e:
        return "User not authorized", 401


def users_username_password_put(username, update_password: UpdatePassword = None):  # noqa: E501
    """users_userid_password_put

     # noqa: E501

    :param userid: user id
    :type userid: str
    :param update_password: 
    :type update_password: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        update_password = UpdatePassword.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        user_service.validate_password(username, update_password.old_password)
    except user_service.UserNotAuthorized as e:
        return "Wrong password", 400

    user_service.update_password(username, update_password.new_password)
    return "OK", 204
