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

    def get_expired_items(self, department):
        """Retrieve items that have expired.
        Args:
            department (str): The department for which the current user belongs.

        Returns:
            list: A list of dictionaries showing expired items.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve added items for the department within the specified date range
            query = """
                SELECT * FROM stock_items
                WHERE department = %s
                AND status = 'approved'
                AND expiration_date <= CURDATE();
            """
            cursor.execute(query, (department,))
            added_items = cursor.fetchall()

            return added_items
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print("An error occurred:", e)
            return []

    def get_weekly_checkouts(self, department):
        """Retrieve weekly approved checkout items details.
        Args:
            department (str): The department for which to retrieve checkout items.

        Returns:
            list: A list of dictionaries showing weekly approved checkout details.

        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve weekly checkout items for the department
            query = """
            SELECT CONCAT(
                DATE_FORMAT(
                    MIN(DATE_SUB(created_at, INTERVAL (WEEKDAY(created_at) + 7) % 7 DAY)),
                    '%Y-%m-%d'
            ),
            ' - ',
            DATE_FORMAT(
            MAX(DATE_SUB(created_at, INTERVAL (WEEKDAY(created_at) + 7) % 7 - 6 DAY)),
            '%Y-%m-%d'
            )
            ) AS week_period,
            item_name,
            SUM(quantity) AS total_quantity
            FROM checkout_transactions
            WHERE department = %s AND approval_status = 'approved'
            GROUP BY WEEK(created_at, 1), item_name
            ORDER BY week_period, item_name;
            """
            cursor.execute(query, (department,))
            weekly_checkouts = cursor.fetchall()

            return weekly_checkouts
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def get_monthly_checkouts(self, department):
        """Retrieve monthly approved checkout items details.
        Args:
            department (str): The department for which to retrieve checkout items.

        Returns:
            list: A list of dictionaries showing monthly approved checkout details.

        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve monthly checkout items for the department
            query = """
            SELECT CONCAT(
            DATE_FORMAT(DATE_SUB(created_at, INTERVAL DAYOFMONTH(created_at) - 1 DAY), '%Y-%m-%d'),
            ' - ',
            LAST_DAY(created_at)
            ) AS month_period,
            item_name,
            SUM(quantity) AS total_quantity
            FROM checkout_transactions
            WHERE department = %s AND approval_status = 'approved'
            GROUP BY month_period, item_name
            ORDER BY month_period, item_name;
            """

            cursor.execute(query, (department,))
            monthly_checkouts = cursor.fetchall()

            return monthly_checkouts
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def get_daily_checkouts(self, department):
        """Retrieve daily approved checkout items details.
        Args:
            department (str): The department for which to retrieve checkout items.

        Returns:
            list: A list of dictionaries showing daily approved checkout details.

        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve monthly checkout items for the department
            query = """
            SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS checkout_date,
            item_name,
            SUM(quantity) AS total_quantity
            FROM checkout_transactions
            WHERE department = %s AND approval_status = 'approved'
            GROUP BY checkout_date, item_name
            ORDER BY checkout_date, item_name;
            """

            cursor.execute(query, (department,))
            monthly_checkouts = cursor.fetchall()

            return monthly_checkouts
        except Exception as e:
            # Handle exceptions here if needed
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def update_item_quantity(self, item_id, new_quantity):
        """
        Update the quantity of an item in the database.

        Args:
            item_id (int): The ID of the item to update.
            new_quantity (int): The new quantity of the item.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            # Execute the SQL update query
            sql_query = "UPDATE stock_items SET quantity = %s WHERE id = %s"
            self.cursor.execute(sql_query, (new_quantity, item_id))
            self.db_connection.commit()
            return True
        except Error as e:
            print("Error updating item quantity:", e)
            return False

    def add_damaged_item(self, item_id, damage_description, reported_by, quantity_damaged):
        """
        Add a damaged item to the 'damaged_items' table in the database.

        Args:
            item_id (int): The ID of the damaged item.
            damage_description (str): A description of the damage.
            reported_by (int): The ID of the person who reported the damage.
            quantity_damaged (int): The quantity of the item that was damaged.

        Returns:
            None
        """
        try:
            cursor = self.db_connection.cursor()
            # Inserting data into damaged_items table
            sql_query = """INSERT INTO damaged_items (item_id, damage_description, reported_by, quantity_damaged)
                        VALUES (%s, %s, %s, %s)
                        """
            cursor.execute(sql_query, (item_id, damage_description, reported_by, quantity_damaged))
            self.db_connection.commit()
            print("Damaged item added successfully!")

            # Create a notification for the reported damage
            message = f"Item with ID {item_id} reported as damaged. Description: {damage_description}"
            action_type = "damaged"
            try:
                self.create_notification(reported_by, message, action_type)
            except Error as e:
                print("Error while creating a notification.", e)

            return True
        except Error as e:
            print("Error while adding damaged item:", e)
        finally:
            cursor.close()

    def update_item_category(self, category_id, new_category):
        """
        Update the name of the category in the database.

        Args:
            category_id (int): The ID of the category to be updated.
            new_category (str): The new category name.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            cursor = self.db_connection.cursor()
            update_query = "UPDATE item_category SET category_name = %s WHERE category_id = %s"
            cursor.execute(update_query, (new_category, category_id))
            rows_affected = cursor.rowcount
            self.db_connection.commit()
            return rows_affected > 0
        except mysql.connector.Error as err:
            print(f"Error updating Category: {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_damaged_items(self):
        """Retrieve items that have been damaged.

        Returns:
            list: A list of dictionaries showing expired items.
        """
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Retrieve added items for the department within the specified date range
            query = """
                SELECT * FROM damaged_items;
            """
            cursor.execute(query,)
            damaged_items = cursor.fetchall()

            return damaged_items
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print("An error occurred:", e)
            return []
    
    def get_item_name_by_id(self, item_id):
        """
        Retrieve the name of a item based on the Item ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            str: The name of the item.
        """
        query = "SELECT item_name FROM stock_items WHERE id = %s"
        params = (item_id,)

        cursor = self.db_connection.cursor()
        cursor.execute(query, params)
        item_name = cursor.fetchone()
        cursor.close()

        return item_name[0] if item_name else None

    def create_notification(self, user_id, message, action_type):
        """
        Create a notification for a user.

        Args:
            user_id (int): The ID of the user for whom the notification is created.
            message (str): The notification message.
            action_type (str): The type of action that triggered the notification.

        Returns:
            bool: True if the notification was successfully created, False otherwise.
        """
        cursor = self.db_connection.cursor(dictionary=True)
        try:
            # Insert notification into the database
            query = "INSERT INTO notifications (user_id, message, action_type) VALUES (%s, %s, %s)"
            params = (user_id, message, action_type)
            cursor.execute(query, params)

            # Commit the transaction
            self.db_connection.commit()

            return True

        except mysql.connector.Error as err:
            print(f"Error creating notification: {err}")
            return False

        finally:
            # Close the cursor
            cursor.close()

    def get_unread_notifications(self):
        """
        Retrieve unread notifications for the currently logged-in user.

        Returns:
            list: A list of dictionaries representing unread notifications.
                  Each dictionary contains 'id', 'message', 'action_type', 'created_at', and 'read_status' keys.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            # Query to retrieve unread notifications
            sql_query = """SELECT id, message, action_type, created_at, read_status
                           FROM notifications
                           WHERE read_status = 0
                           ORDER BY created_at DESC"""
            cursor.execute(sql_query)
            unread_notifications = cursor.fetchall()
            return unread_notifications
        except Error as e:
            print(f"Error retrieving unread notifications: {e}")
            return []

    def mark_notification_as_read(self, notification_id):
        """
        Mark a notification as read.

        Args:
            notification_id (int): The ID of the notification to mark as read.

        Returns:
            bool: True if the notification was successfully marked as read, False otherwise.
        """
        try:
            cursor = self.db_connection.cursor()
            # Update the read_status of the notification to 1 (read)
            sql_query = """UPDATE notifications
                           SET read_status = 1
                           WHERE id = %s"""
            cursor.execute(sql_query, (notification_id,))
            self.db_connection.commit()
            return True
        except Error as e:
            print(f"Error marking notification as read: {e}")
            return False


if __name__ == '__main__':
    db_config = {
            'user': config('DB_USER'),
            'password': config('DB_PASSWORD'),
            'host': config('DB_HOST'),
            'database': config('DB_NAME'),
            }

    item = ItemManager(db_config)
    weekly_items = item.get_unread_notifications()
    print(weekly_items)
