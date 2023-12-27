"""
Module: user

This module defines the User class, which represents a user in the stock management system.
"""

class User:
    """
    Represents a user in the stock management system.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        phone (str): The user's phone number.
        department (str): The user's department or division.
        role (str): The user's role or position.
        username (str): The user's username.
        password (str): The user's password.
    """

    def __init__(self, email, password, first_name=None, last_name=None, phone=None, department=None, role=None, username=None):
        """
        Initialize a User object.

        Args:
            first_name (str, optional): The user's first name.
            last_name (str, optional): The user's last name.
            email (str, optional): The user's email address.
            phone (str, optional): The user's phone number.
            department (str, optional): The user's department or division.
            role (str, optional): The user's role or position.
            username (str, optional): The user's username.
            password (str, optional): The user's password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.department = department
        self.role = role
        self.username = username
        self.password = password

