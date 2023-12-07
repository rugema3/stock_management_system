"""
Module: database_manager

This module defines the Database class, which provides functionality for interacting
with a MySQL database for a stock management system.
"""

import mysql.connector

class Database:
    """
    A class for interacting with a MySQL database.

    Attributes:
        db_connection: The MySQL database connection.
    """

    def __init__(self, db_config):
        """
        Initialize the Database class with the provided database configuration.

        Args:
            db_config (dict): A dictionary containing database connection parameters,
                such as 'user', 'password', 'host', and 'database'.
        """
        self.db_connection = mysql.connector.connect(**db_config)
        self.cursor = self.db_connection.cursor()

    def insert_item(self, item, maker_id=None):
        """
        Insert an item into the database.

        Args:
            item (StockItem): The StockItem object to be inserted into the database.
            maker_id (int, optional): The ID of the user who added the item. Default is None.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        if maker_id is not None:
            # Fetch the department information based on the maker_id
            department_query = "SELECT department FROM users WHERE id = %s"
            cursor.execute(department_query, (maker_id,))
            department_result = cursor.fetchone()

            if department_result:
                department = department_result['department']

                # Insert the item with the fetched department information
                insert_query = """
                    INSERT INTO stock_items(item_name, price, category, quantity, department, maker_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (item.item_name, item.price, item.category, item.quantity, department, maker_id))

        self.db_connection.commit()
        cursor.close()



    def get_all_items(self):
        """
        Retrieve all items from the database.

        Returns:
            list: A list of tuples containing the item records.
        """
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM stock_items")
        items = cursor.fetchall()
        cursor.close()
        return items

    def search_item(self, item_name):
        """
        Search for an item in the database by its name.

        Args:
            item_name (str): The name of the item to search for.

        Returns:
            list: A list of tuples containing the item records that match the search criteria.
        """
        cursor = self.db_connection.cursor()
        search_query = "SELECT * FROM stock_items WHERE item_name = %s"
        cursor.execute(search_query, (item_name,))
        matching_items = cursor.fetchall()
        cursor.close()
        return matching_items

    def checkout_item(self, user_id, item_name, quantity):
        cursor = self.db_connection.cursor()

        try:
            # Retrieve department information based on user_id
            department_query = "SELECT department FROM users WHERE id = %s"
            cursor.execute(department_query, (user_id,))
            department_result = cursor.fetchone()

            if department_result:
                department = department_result['department']

                
                update_query = "UPDATE stock_items SET quantity = quantity - %s WHERE item_name = %s AND quantity >= %s"
                cursor.execute(update_query, (quantity, item_name, quantity))

                # Create a checkout transaction record with user_id and department
                checkout_query = "INSERT INTO checkout_transactions (item_name, quantity, user_id, department, approval_status) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(checkout_query, (item_name, quantity, user_id, department, 'pending'))

                # Commit the changes
                self.db_connection.commit()

                return True
            else:
                return False
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()




    def delete_item(self, item_name):
        """
        Delete an item from the database by its name.

        Args:
            item_name (str): The name of the item to be deleted.

        Returns:
            bool: True if the item was successfully deleted, False otherwise.
        """
        cursor = self.db_connection.cursor()
        delete_query = "DELETE FROM stock_items WHERE item_name = %s"
        cursor.execute(delete_query, (item_name,))
        rows_affected = cursor.rowcount
        self.db_connection.commit()
        cursor.close()
        return rows_affected > 0

    def insert_user(self, user):
        """
       Insert a new user into the database.

        Args:
            user (User): The User object to be inserted into the database.
        """
        cursor = self.db_connection.cursor()
        insert_query = """
            INSERT INTO users(first_name, last_name, email, phone, department, role, username, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user.first_name, user.last_name, user.email, user.phone,
                                      user.department, user.role, user.username, user.password))
        self.db_connection.commit()
        cursor.close()


    def find_user_by_email(self, email):
        """
        Find a user in the database by their email address.

        Args:
            email (str): The email address of the user to search for.

        Returns:
            User: The User object if found, or None if not found.
        """
        cursor = self.db_connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            # You can create a User object from user_data and return it
            user = User(**user_data)
            return user
        else:
            return None

    def fetch_one(self, query, params=None):
        """
        Execute a SQL query and fetch a single row.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            dict: A dictionary representing a single row from the result.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.db_connection.commit()  # Update this line
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            self.db_connection.rollback()  # Update this line
            return None


    def insert_user(self, user):
        """
        Insert a new user into the database.

        Args:
            user (User): The User object to be inserted into the database.
        """
        insert_query = """
            INSERT INTO users(email, password, department, role)
            VALUES (%s, %s, %s, %s)
         """
        with self.db_connection.cursor() as cursor:
            cursor.execute(insert_query, (user.email, user.password, user.department, user.role))
        self.db_connection.commit()

    def get_pending_items(self, department=None):
        """
        Retrieve a list of all pending items from the database with selected fields.

        Args:
            department (str): The department for which to retrieve pending items. If None, retrieve all pending items.

        Returns:
            list: A list of tuples containing selected pending item information.
        """
        if department:
            query = "SELECT id, item_name, price, category, quantity, created_at, currency, status, maker_id FROM stock_items WHERE status = 'pending' AND department = %s"
            params = (department,)
        else:
            query = "SELECT id, item_name, price, category, quantity, created_at, currency, status, maker_id FROM stock_items WHERE status = 'pending'"
            params = None

        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        pending_items = cursor.fetchall()
        cursor.close()
        return pending_items

    def update_item_status(self, id, status):
        """
        Update the status of an item in the database.

        Args:
            item_id (int): The ID of the item to be updated.
            status (str): The new status of the item.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()
        update_query = "UPDATE stock_items SET status = %s WHERE id = %s"
        cursor.execute(update_query, (status, id))
        rows_affected = cursor.rowcount
        self.db_connection.commit()
        cursor.close()
        return rows_affected > 0  

    def update_user_password(self, user_id, new_password):
        """
        Update the password of a user in the database with plain text password.

        Args:
            user_id (int): The ID of the user to be updated.
            new_password (str): The new password (plain text).

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()
        update_query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(update_query, (new_password, user_id))
        rows_affected = cursor.rowcount
        self.db_connection.commit()
        cursor.close()
        return rows_affected > 0


    def update_user_email(self, user_id, new_email):
        """
        Update the email of a user in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            new_email (str): The new email address.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()
        update_query = "UPDATE users SET email = %s WHERE id = %s"
        cursor.execute(update_query, (new_email, user_id))
        rows_affected = cursor.rowcount
        self.db_connection.commit()
        cursor.close()
        return rows_affected > 0

    def get_all_users(self, department=None):
        """
        Retrieve a list of all users from the database with selected fields.

        Args:
            department (str): The department for which to retrieve users. If None, retrieve all users.

        Returns:
            list: A list of tuples containing selected user information.
        """
        if department:
            query = "SELECT email, role, department FROM users WHERE department = %s"
            params = (department,)
        else:
            query = "SELECT email, role, department FROM users"
            params = None

        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()
        return users

    def get_pending_checkouts(self, department=None):
        """
        Retrieve a list of all pending checkout requests from the database with selected fields.

        Args:
            department (str): The department for which to retrieve pending checkout requests. 
            If None, retrieve all pending requests.

        Returns:
            list: A list of tuples containing selected checkout request
            information.
        """
        if department:
            query = """
                SELECT 
                ct.checkout_id, 
                ct.item_name, 
                ct.quantity, 
                ct.user_id, 
                ct.created_at
                FROM checkout_transactions ct
                INNER JOIN users u ON ct.user_id = u.id
                WHERE ct.approval_status = 'pending' AND u.department = %s
            """
            params = (department,)
        else:
            query = """
                SELECT 
                checkout_id, 
                item_name, 
                quantity, 
                user_id, 
                created_at 
                FROM checkout_transactions WHERE approval_status = 'pending'
            """
            params = None

        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        pending_checkouts = cursor.fetchall()
        cursor.close()
        return pending_checkouts

