from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...models.userManagement.superAdminEntity import Super_Admin


class Credential:

    """
    Retrieves the email and password associated with the given email from the database.

    Args:
        email (str): The email of the user to retrieve credentials for.

    Returns:
        tuple: A tuple containing the email and password of the user if found, otherwise (False, False).
    """

    def get_user(self, email):
        engine = create_engine("sqlite:///monitoring-and-evaluation.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        user = session.query(Super_Admin).filter_by(Email=email).first()
        session.close()

        if user:
            return user.Email, user.Password

        return False, False
