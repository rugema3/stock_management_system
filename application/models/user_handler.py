"""user_handler module.
This module has a class that handles the database operations concerning users.
"""
import mysql.connector
import os
from werkzeug.utils import secure_filename
import uuid


class UserHandler:
    """
    A class for managing user departments and roles in the inventory management system.

    Attributes:
        db: An instance of the Database class for interacting with the database.
    """

    def __init__(self, db_config):
        """
        Initialize the UserHandler with the provided database configuration.

        Args:
            db_config (dict): A dictionary containing database connection parameters,
                such as 'user', 'password', 'host', and 'database'.
        """
        self.db_connection = mysql.connector.connect(**db_config)
        self.cursor = self.db_connection.cursor()

    def add_user_department(self, department_name):
        """
        Add a new department to the database.

        Args:
            department_name (str): The name of the department to add.
        """
        cursor = self.db_connection.cursor()
        try:
            # Use parameterized query to prevent SQL injection
            query = "INSERT INTO user_department (department_name) VALUES (%s)"
            values = (department_name.lower(),)  # Convert to lowercase

            cursor.execute(query, values)

            # Commit the transaction
            self.db_connection.commit()

            print("Department {department_name} added successfully!")
            return True

        except mysql.connector.Error as err:
            print(f"Error adding category: {err}")
            return False

        finally:
            # Close the cursor
            cursor.close()

    def add_user_role(self, role_name):
        """
        Add a new user role to the database.

        Args:
            role_name (str): The name of the role to add.
        """
        cursor = self.db_connection.cursor()
        try:
            # Use parameterized query to prevent SQL injection
            query = "INSERT INTO user_role (role_name) VALUES (%s)"
            values = (role_name.lower(),)  # Convert to lowercase

            cursor.execute(query, values)

            # Commit the transaction
            self.db_connection.commit()

            print("{role_name} role added successfully!")
            return True

        except mysql.connector.Error as err:
            print(f"Error adding role: {err}")
            return False

        finally:
            # Close the cursor
            cursor.close()

    def get_user_department(self):
        """
        Retrieve all departments from the user_department table.

        Returns:
            list: A list of strings representing department names.
        """
        cursor = self.db_connection.cursor()

        try:
            # Retrieve all categories
            query = "SELECT department_name FROM user_department"
            cursor.execute(query)
            categories = [row[0] for row in cursor.fetchall()]

            return categories

        except mysql.connector.Error as err:
            print(f"Error retrieving roles: {err}")
            return []

        finally:
            # Close the cursor
            cursor.close()

    def get_user_role(self):
        """
        Retrieve all roles from the user_role table.

        Returns:
            list: A list of strings representing department names.
        """
        cursor = self.db_connection.cursor()

        try:
            # Retrieve all roles
            query = "SELECT role_name FROM user_role"
            cursor.execute(query)
            categories = [row[0] for row in cursor.fetchall()]

            return categories

        except mysql.connector.Error as err:
            print(f"Error retrieving roles: {err}")
            return []

        finally:
            # Close the cursor
            cursor.close()

    def update_profile_picture(self, user_id, filename, filepath):
        """
        Update the profile picture for a user.

        Args:
            user_id (int): The ID of the user.
            filename (str): The name of the uploaded profile picture file.
            filepath (str): The full path to the uploaded profile picture file.

        Returns:
            bool: True if the profile picture was updated successfully, False otherwise.
        """
        cursor = self.db_connection.cursor()
        try:
            if user_id and filename and filepath:
                # Update user's profile picture reference in the database
                query = "UPDATE users SET profile_picture = %s WHERE id = %s"
                cursor.execute(query, (filepath, user_id))
                self.db_connection.commit()

                print("Profile picture updated successfully!")
                return True
            else:
                print("User ID, filename, or filepath not provided.")
                return False
        except mysql.connector.Error as err:
            print(f"Error updating profile picture: {err}")
            return False
        finally:
            # Close the cursor
            cursor.close()
    
    def get_profile_picture_path(self, user_id):
        """
        Retrieve and extract the profile picture path for a user from the database.

        Args:
            user_id (int): The ID of the user.

        Returns:
            str or None: The extracted profile picture path if found, None otherwise.
        """
        cursor = self.db_connection.cursor()
        try:
            query = "SELECT profile_picture FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                path_pic = result[0]
                prefix = "/home/rugema3/stock_management_system/application"
                extracted_path = path_pic.replace(prefix, "")
                return extracted_path
            else:
                print("User not found.")
                return None
        except mysql.connector.Error as err:
            print(f"Error retrieving profile picture path: {err}")
            return None
        finally:
            cursor.close()

    def update_user_name(self, user_id, new_name):
        """
        Update the name of the user in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            new_name (str): The new name.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()
        update_query = "UPDATE users SET name = %s WHERE id = %s"
        cursor.execute(update_query, (new_name, user_id))
        rows_affected = cursor.rowcount
        self.db_connection.commit()
        cursor.close()
        return rows_affected > 0

    def update_user_department(self, department_id, new_department):
        """
        Update the name of the department in the database.

        Args:
            department_id (int): The ID of the department to be updated.
            new_department (str): The new department name.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            cursor = self.db_connection.cursor()
            update_query = "UPDATE user_department SET department_name = %s WHERE department_id = %s"
            cursor.execute(update_query, (new_department, department_id))
            rows_affected = cursor.rowcount
            self.db_connection.commit()
            return rows_affected > 0
        except mysql.connector.Error as err:
            print(f"Error updating department: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def update_user_role(self, role_id, new_role):
        """
        Update the name of the role in the database.

        Args:
            role_id (int): The ID of the role to be updated.
            new_role (str): The new department name.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            cursor = self.db_connection.cursor()
            update_query = "UPDATE user_role SET role_name = %s WHERE role_id = %s"
            cursor.execute(update_query, (new_role, role_id))
            rows_affected = cursor.rowcount
            self.db_connection.commit()
            return rows_affected > 0
        except mysql.connector.Error as err:
            print(f"Error updating department: {err}")
            return False
        finally:
            if cursor:
                cursor.close()


