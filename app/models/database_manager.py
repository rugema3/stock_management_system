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

    def insert_item(self, item):
        """
        Insert an item into the database.

        Args:
            item (StockItem): The StockItem object to be inserted into the database.
        """
        cursor = self.db_connection.cursor()
        insert_query = "INSERT INTO stock_items(item_name, price, category, quantity) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (item.item_name, item.price, item.category, item.quantity))
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

    def checkout_item(self, item_name, quantity):
        """
        Checkout a specified quantity of an item from the stock.

        Args:
            item_name (str): The name of the item to be checked out.
            quantity (int): The quantity of the item to be checked out.

        Returns:
            bool: True if the checkout was successful, False otherwise.
        """
        cursor = self.db_connection.cursor()
        update_query = "UPDATE stock_items SET quantity = quantity - %s WHERE item_name = %s AND quantity >= %s"
        cursor.execute(update_query, (quantity, item_name, quantity))
        rows_affected = cursor.rowcount
        self.db_connection.commit()
        cursor.close()
        return rows_affected > 0

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

    def get_pending_items(self):
        """Retrieve all the pending items from the db."""
        cursor = self.db_connection.cursor(dictionary=True)
        search_query = "SELECT * FROM stock_items WHERE status = 'pending'"
        cursor.execute(search_query)
        matching_items = cursor.fetchall()
        cursor.close()
        return matching_items

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


if __name__ == '__main__':
    # Create an instance of the Database class with your configuration
    db_config = {
        'user': 'rugema3',
        'password': 'Shami@2020',
        'host': 'localhost',
        'database': 'stock'
    }
    
    database = Database(db_config)

    while True:
        print("\n1. Update Item Status")
        print("2. Exit")

        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            # Fetch all pending items
            pending_items = database.get_pending_items()

            if not pending_items:
                print("No pending items found.")
                continue

            print("\nPending Items:")
            for item in pending_items:
                print(f"{item['id']}. Item: {item['item_name']}, Price: {item['price']}, Category: {item['category']}, Staus: {item['status']}, Quantity: {item['quantity']}")


            item_id = input("Enter the ID of the item to update: ")
            new_status = input("Enter the new status: ")
            
            # Call the update_item_status method from your Database class
            success = database.update_item_status(item_id, new_status)

            if success:
                print("Item status updated successfully.")
            else:
                print("Failed to update item status.")
                
        elif choice == '2':
            print("Exiting the Item Status Updater. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

