"""item_manager module.
This module has a class that handles the database operations concerning items.
"""
import mysql.connector


class ItemManager:
    """
    A class for managing item operations in the inventory management system.

    Attributes:
        db: An instance of the Database class for interacting with the database.
    """

    def __init__(self, db_config):
        """
        Initialize the ItemManager with the provided database configuration.

        Args:
            db_config (dict): A dictionary containing database connection parameters,
                such as 'user', 'password', 'host', and 'database'.
        """
        self.db_connection = mysql.connector.connect(**db_config)
        self.cursor = self.db_connection.cursor()

    def get_item_category(self):
        """
        The method for retrieving the item category.

        Returns:
                List: A list of Strings representing item categories.
        """
        cursor = self.db_connection.cursor()
        try:
            # Retrieve all categories
            query = "SELECT category FROM stock_items"
            cursor.execute(query)
            categories = [row[0] for row in cursor.fetchall()]

            return categories

        except  mysql.connector.Error as err:
            print(f"Error retrieving roles: {err}")
            return []

        finally:
            # Close the cursor
            cursor.close()

    def get_categories(self):
        """
        The method that retrieves the list of categories in the 
        item_category_table in database.

        Returns:
                list: A list of strings of categories.
        """
        cursor = self.db_connection.cursor()
        try:
            # Retrieve all categories
            query = "SELECT category_name FROM item_category"
            cursor.execute(query)
            categories = [row[0] for row in cursor.fetchall()]

            return categories

        except mysql.connector.Error as err:
            print(f"Error retrieving roles: {err}")
            return []

        finally:
            # Close the cursor
            cursor.close()

    def get_category_counts(self, department):
        """
        Retrieve the count of items in the stock_items table for each category.

        Returns:
            dict: A dictionary where keys are category names and values are the counts of items in each category.
        """
        cursor = self.db_connection.cursor()
        try:
            if department:
                # Retrieve category counts for the specified department
                query = "SELECT category, COUNT(*) FROM stock_items WHERE department = %s GROUP BY category"
                cursor.execute(query, (department,))
            else:
                # Retrieve category counts for all departments
                query = "SELECT category, COUNT(*) FROM stock_items GROUP BY category"
                cursor.execute(query)

            category_counts = {row[0]: row[1] for row in cursor.fetchall()}

            return category_counts

        except mysql.connector.Error as err:
            print(f"Error retrieving category counts by department: {err}")
            return {}

        finally:
            # Close the cursor
            cursor.close()

    def store_approval_details(self, item_id, approval_status, approver_id, approval_comment):
        """
        Store approval details for added items in the approval_details table.

        Args:
            
            item_id (int): The ID of the item associated with the approval.
            approval_status (str): The status of the approval (e.g., 'approved', 'rejected').
            approver_id (int): The ID of the user who approved/rejected the transaction.
            approval_comment (str): Any comment provided by the approver.

        Returns:
            None
        """
        cursor = self.db_connection.cursor()
        try:
            query = "INSERT INTO approval_details (item_id, approval_status, approver_id, approval_comment) VALUES (%s, %s, %s, %s)"
            params = (item_id, approval_status, approver_id, approval_comment)

            cursor.execute(query, params)
            self.db_connection.commit()

        except mysql.connector.Error as err:
            print(f"Error updating the approval details: {err}")

        finally:
            cursor.close()

    def get_approved_checkouts(self, department):
        """Retrieve approved checkout items details.
        Args:
            department (str): The department for which to retrieve checkout items.

        Returns:
            list: A list of dictionaries showing approved checkout details.

        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve checkout items for the department
            query = """
                SELECT * FROM checkout_transactions
                WHERE department = %s AND (approval_status = 'approved')
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


