class User:
    def __init__(self, email, password):
        self.__email = email
        self.__is_authenticated = False
        self.__password = password

    """
    Gets the authentication status of the user.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """

    def get_authenticated(self):
        return self.__is_authenticated

    """
    Gets the email address of the user.

    Returns:
        str: The email address of the user.
    """

    def get_email(self):
        return self.__email

    """
    Gets the password of the user.

    Returns:
        str: The password of the user.
    """

    def get_password(self):
        return self.__password

    """
    Sets the authentication status of the user.

    Args:
        value (bool): The authentication status to be set.
    """

    def set_authenticated(self, value):
        self.__is_authenticated = value

    """
    Sets the email address of the user.

    Args:
        new_email (str): The new email address to be set.
    """

    def set_email(self, new_email):
        self.__email = new_email

    """
    Sets the password of the user.

    Args:
        new_password (str): The new password to be set.
    """

    def set_password(self, new_password):
        self.__password = new_password
