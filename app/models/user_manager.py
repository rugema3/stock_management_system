from app.models.database_manager import Database
from app.models.user import User

class UserManager:
    """
    A class for managing user registration and login.

    Attributes:
        db (Database): An instance of the Database class for database interactions.
    """

    def __init__(self, db_config):
        """
        Initialize the UserManager with a database connection.
        """
        self.db = Database(db_config)

    def register_user(self, email, password):
        """
        Register a new user with email and password and store their information in the database.

        Args:
            email (str): User's email address.
            password (str): User's password (plaintext).

        Returns:
            str: A registration success message or an error message.
        """
        # Check if the user already exists
        existing_user = self.db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
        if existing_user:
            return "Email already in use."

        # Create a new user with the provided plaintext password
        success = self.db.insert_user(User(email, password))

        if success:
            return "Registration successful!"
        else:
            return "Registration failed. Please try again later."


    def login_user(self, email, password):
        """
        Authenticate a user's login and return a success message or an error message.

        Args:
            email (str): User's email address.
            password (str): User's password (plaintext).

        Returns:
            str: A login success message or an error message.
        """
        # Retrieve the user's information from the database
        user_data = self.db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))

        if user_data is not None:
            if user_data.get('password', '') == password:
                return "Login successful!"
            else:
                return "Incorrect password."
        else:
            return "Email not found."

    def close_database_connection(self):
        """
        Close the database connection when it's no longer needed.
        """
        self.db.close()

