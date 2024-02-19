"""item_manager module.
This module has a class that handles the database operations concerning items.
"""
import mysql.connector
from decouple import config


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

    def get_items_current_month(self, department):
        """Retrieve items added in the stock for the cutrrent months.
        Args:
            department (str): The department for which the current user belongs.

        Returns:
            list: A list of dictionaries showing added items in the current months.

        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve added items for the department
            query = """
                SELECT * FROM stock_items
                WHERE department = %s 
                AND status = 'approved'
                AND YEAR(created_at) = YEAR(CURDATE())
                AND MONTH(created_at) = MONTH(CURDATE());
            """
            cursor.execute(query, (department,))
            added_items = cursor.fetchall()

            return added_items
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def retrieve_added_items_by_date(self, department, start_date, end_date):
        """Retrieve items added within a date range.
        Args:
            department (str): The department for which the current user belongs.
            start_date (str): The start date of the range (format: 'YYYY-MM-DD').
            end_date (str): The end date of the range (format: 'YYYY-MM-DD').

        Returns:
            list: A list of dictionaries showing added items within the date range.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve added items for the department within the specified date range
            query = """
                SELECT * FROM stock_items
                WHERE department = %s
                AND status = 'approved'
                AND created_at >= %s AND created_at <= %s;
            """
            cursor.execute(query, (department, start_date, end_date))
            added_items = cursor.fetchall()

            return added_items
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print("An error occurred:", e)
            return []

    def search_weekly_adds(self, department):
        """Retrieve items added within the last 7 7 days.
        Args:
            department (str): The department for which the current user belongs.

        Returns:
            list: A list of dictionaries showing added items within the date range.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve added items for the department within the specified date range
            query = """
                SELECT * FROM stock_items
                WHERE department = %s
                AND status = 'approved'
                AND created_at >= CURDATE() - INTERVAL 7 DAY
                AND created_at <= CURDATE();
            """
            cursor.execute(query, (department,))
            added_items = cursor.fetchall()

            return added_items
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print("An error occurred:", e)
            return []

    def get_expiring_soon(self, department):
        """Retrieve items expiring in the next 7 days.
        Args:
            department (str): The department for which the current user belongs.

        Returns:
            list: A list of dictionaries showing items expiring soon.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve added items for the department within the specified date range
            query = """
                SELECT * FROM stock_items
                WHERE department = %s
                AND status = 'approved'
                AND expiration_date BETWEEN CURDATE() 
                AND DATE_ADD(CURDATE(), INTERVAL 7 DAY);
            """
            cursor.execute(query, (department,))
            added_items = cursor.fetchall()

            return added_items
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print("An error occurred:", e)
            return []



if __name__ == '__main__':
    db_config = {
            'user': config('DB_USER'),
            'password': config('DB_PASSWORD'),
            'host': config('DB_HOST'),
            'database': config('DB_NAME'),
            }

    item = ItemManager(db_config)
    weekly_items = item.get_expiring_soon('it')
    print()
    for item in weekly_items:
        print("Weekly items")
        print(item['item_name'], item['created_at'], item['expiration_date'])
