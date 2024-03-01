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

    def insert_item(
            self, item, maker_id=None, description=None, 
            purchase_date=None, expiration_date=None):
        """
        Insert an item into the database.

        Args:
            item (StockItem): The StockItem object to be inserted into the database.
            maker_id (int, optional): The ID of the user who added the item. Default is None.
            dectription(str, optional): The description of an item when entered in the db.
            purchade_date(date, optional): The date of the purchase of an item
            expiration_date(date, optional): The date of an item is set to expire.

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
                    INSERT INTO stock_items(item_name, price, category, quantity, department, maker_id, description, purchase_date, expiration_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    item.item_name, 
                    item.price, 
                    item.category, 
                    item.quantity, 
                    department, 
                    maker_id, 
                    description, 
                    purchase_date, 
                    expiration_date))

        self.db_connection.commit()
        cursor.close()



    def get_all_items(self):
        """
        Retrieve all items from the database.

        Returns:
            list: A list of tuples containing the item records.
        """
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM stock_items WHERE status='approved'")
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
        """
        Checkout an item for a user.

        Args:
            user_id (int): The ID of the user performing the checkout.
            item_name (str): The name of the item to be checked out.
            quantity (int): The quantity of the item to be checked out.

        Returns:
            bool: True if the checkout is successful, False otherwise.
        """
        cursor = self.db_connection.cursor()

        try:
            # Retrieve department information based on user_id
            department_query = "SELECT department FROM users WHERE id = %s"
            cursor.execute(department_query, (user_id,))
            department_result = cursor.fetchone()

            if department_result:
                department = department_result[0]

                # Create a checkout transaction record with user_id, 
                # department, and pending status
                checkout_query = """
                    INSERT INTO checkout_transactions (
                    item_name, quantity, user_id, department, approval_status)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                cursor.execute(
                        checkout_query, 
                        (item_name, quantity, user_id, department, 'pending')
                        )

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

    def insert_user(self, email, password, department, role='user', name=None):
        """
        Insert a new user into the 'users' table.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            department (str): The user's department.
            role (str, optional): The user's role (default is 'user').
            name (str, optional): The user's name.

        Returns:
            None
        """
        cursor = self.db_connection.cursor()
        insert_query = """
            INSERT INTO users(email, password, department, role, name)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (email, password, department, role, name))
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
            return user_data
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


    def get_pending_items(self, department=None):
        """
        Retrieve a list of all pending items from the database with selected fields.

        Args:
            department (str): The department for which to retrieve pending items. If None, retrieve all pending items.

        Returns:
            list: A list of tuples containing selected pending item information.
        """
        if department:
            query = """
                SELECT id,
                item_name,
                price, 
                category,
                quantity, 
                created_at, 
                currency, 
                status,
                maker_id,
                description
                FROM stock_items WHERE status = 'pending' AND department = %s
                """
            params = (department,)
        else:
            query = "SELECT id, item_name, price, category, quantity, created_at, currency, status, maker_id, description FROM stock_items WHERE status = 'pending'"
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
            query = "SELECT id, email, role, department, name FROM users WHERE department = %s"
            params = (department,)
        else:
            query = "SELECT id, email, role, department, name FROM users"
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

    def get_pending_items_count(self, department=None):
        """
        Retrieve the count of pending items from the database.

        Args:
            department (str): The department for which to retrieve the count of pending items.
                             If None, retrieve the count for all pending items.

        Returns:
            int: The count of pending items.
        """
        if department:
            query = "SELECT COUNT(*) as count FROM stock_items WHERE status = 'pending' AND department = %s"
            params = (department,)
        else:
            query = "SELECT COUNT(*) as count FROM stock_items WHERE status = 'pending'"
            params = None

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        count = cursor.fetchone()[0]  # Access the count using [0]
        cursor.close()
        return count


    def get_users_count_by_department(self, department):
        """
        Retrieve the count of users based on their roles and department from the database.

        Args:
            department (str): The department for which to retrieve user counts.

        Returns:
            dict: A dictionary containing user counts for each role.
        """
        query = """
        SELECT 
            (SELECT COUNT(*) FROM users WHERE department = %s AND role = 'user') as user_count,
            (SELECT COUNT(*) FROM users WHERE department = %s AND role = 'admin') as admin_count,
            (SELECT COUNT(*) FROM users WHERE department = %s AND role = 'approver') as approver_count
        """
        params = (department, department, department)

        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        user_counts = cursor.fetchone()
        cursor.close()
        return user_counts

    def get_total_cost_of_stock(self, department=None, status='approved'):
        """
        Calculate the total cost of approved items in the stock.

        Args:
            department (str): The department for which to calculate the total cost.
                             If None, calculate the total cost for all items.
            status (str): The status of items to include in the calculation. Default is 'approved'.

        Returns:
            float: The total cost of approved items in the stock.
        """
        if department:
            query = "SELECT SUM(price * quantity) as total_cost FROM stock_items WHERE department = %s AND status = %s"
            params = (department, status)
        else:
            query = "SELECT SUM(price * quantity) as total_cost FROM stock_items WHERE status = %s"
            params = (status,)

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        total_cost = cursor.fetchone()[0] or 0  # Access the total cost using [0] and handle None result
        cursor.close()
        return total_cost

    def get_items_by_department(self, department):
        """
        Retrieve items from the database based on the specified department.

        Args:
            department (str): The department for which to retrieve items.

        Returns:
            list: A list of tuples containing the item records for the specified department.
        """
        query = "SELECT * FROM stock_items WHERE status='approved' AND department = %s"
        params = (department,)

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        items = cursor.fetchall()
        cursor.close()

        return items

    def get_checkout_items_by_department(self, department):
        """
        Retrieve pending checkout items for a specific department.

        Args:
            department (str): The department for which to retrieve checkout items.

        Returns:
            list: A list of dictionaries representing checkout items.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve checkout items for the department
            query = """
                SELECT * FROM checkout_transactions 
                WHERE department = %s AND (approval_status = 'pending' 
                OR approval_status = 'rejected')
            """
            cursor.execute(query, (department,))
            checkout_items = cursor.fetchall()

            return checkout_items
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
    
    def update_checkout_status(self, checkout_id, status, approver_id):
        """
        Update the status of a checkout transaction and, if approved, deduct the quantity from the stock.

        Args:
            checkout_id (int): The ID of the checkout transaction to be updated.
            status (str): The desired status ('approved' or 'rejected').
            approver_id (int): The ID of the user updating the checkout status.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        cursor = self.db_connection.cursor()

        try:
            # Retrieve checkout details
            checkout_query = """
                SELECT item_name, quantity, department 
                FROM checkout_transactions 
                WHERE checkout_id = %s AND approval_status = 'pending'
            """
            cursor.execute(checkout_query, (checkout_id,))
            checkout_details = cursor.fetchone()

            if checkout_details:
                item_name, quantity, department = checkout_details

                # Update checkout status and approver_id
                update_query = """
                    UPDATE checkout_transactions 
                    SET approval_status = %s, 
                    approver_id = %s WHERE checkout_id = %s
                """
                cursor.execute(update_query, (status, approver_id, checkout_id))

                if status == 'approved':
                    # Deduct the quantity from the stock if the checkout is approved
                    update_stock_query = """
                        UPDATE stock_items 
                        SET quantity = quantity - %s 
                        WHERE item_name = %s 
                        AND quantity >= %s 
                        AND department = %s
                    """
                    cursor.execute(
                            update_stock_query, 
                            (quantity, item_name, quantity, department)
                    )

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

    def update_pending_item_quantity(self, item_id, new_quantity):
        """
        Update the quantity of a pending item in the database.

        Args:
            item_id (int): The ID of the pending item to be updated.
            new_quantity (int): The new quantity.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()

        try:
            # Update the quantity of the pending item
            update_query = """
                UPDATE stock_items 
                SET quantity = %s 
                WHERE id = %s 
                AND status = 'pending'
            """
            cursor.execute(update_query, (new_quantity, item_id))

            # Commit the changes
            self.db_connection.commit()

            return True
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def update_pending_item_price(self, item_id, new_price):
        """
        Update the price of a pending item in the database.

        Args:
            item_id (int): The ID of the pending item to be updated.
            new_quantity (int): The new quantity.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()

        try:
            # Update the quantity of the pending item
            update_query = """
                UPDATE stock_items
                SET price = %s
                WHERE id = %s
                AND status = 'pending'
            """
            cursor.execute(update_query, (new_price, item_id))

            # Commit the changes
            self.db_connection.commit()

            return True
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()


    def add_item_category(self, category_name):
        """
        Add a new category to the item_category table.

        Args:
            category_name (str): The name of the category to be added.

        Returns:
            bool: True if the category was added successfully, False otherwise.
        """
        cursor = self.db_connection.cursor()

        try:
            # Use parameterized query to prevent SQL injection
            query = "INSERT INTO item_category (category_name) VALUES (%s)"
            values = (category_name.lower(),)  # Convert to lowercase

            cursor.execute(query, values)

            # Commit the transaction
            self.db_connection.commit()

            print("Category added successfully!")
            return True

        except mysql.connector.Error as err:
            print(f"Error adding category: {err}")
            return False

        finally:
            # Close the cursor
            cursor.close()

    def get_item_categories(self):
        """
        Retrieve all categories from the item_category table.

        Returns:
            list: A list of strings representing category names.
        """
        cursor = self.db_connection.cursor()

        try:
            # Retrieve all categories
            query = "SELECT category_name FROM item_category"
            cursor.execute(query)
            categories = [row[0] for row in cursor.fetchall()]

            return categories

        except mysql.connector.Error as err:
            print(f"Error retrieving categories: {err}")
            return []

        finally:
            # Close the cursor
            cursor.close()

    def get_user_name_by_id(self, user_id):
        """
        Retrieve the name of a user based on the user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            str: The name of the user.
        """
        query = "SELECT name FROM users WHERE id = %s"
        params = (user_id,)

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        user_name = cursor.fetchone()
        cursor.close()

        return user_name[0] if user_name else None
