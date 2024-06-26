from ..authZicationManagement.credentialsDB import Credential
import bcrypt


class Authenticator:
    def __init__(self):

        self.__credential = Credential()

    """
    Checks the credentials of a user against the system.

    Args:
        user (User): An instance of the User class representing the user trying to log in.

    Returns:
        bool: True if the login is successful, False otherwise.
    """

    def login(self, user):
        email, password = self.__credential.get_user(user.get_email())
        if email and password:
            entered_password_hash = bcrypt.hashpw(
                user.get_password().encode('utf-8'), password.encode('utf-8'))
            if entered_password_hash == password.encode('utf-8'):
                user.set_authenticated(True)
                return True
        return False

    """
    Logs out a user from the system.

    Args:
        user (User): An instance of the User class representing the user to log out.

    Returns:
        bool: True if the user was successfully logged out, False if the user was not authenticated.
    """

    def logout(self, user):
        if user.get_authenticated():
            user.set_authenticated(False)
            return True
        return False
