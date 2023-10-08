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

    def insert_item(self, item):
        """
        Insert an item into the database.

        Args:
            item (StockItem): The StockItem object to be inserted into the database.
        """
        cursor = self.db_connection.cursor()
        insert_query = "INSERT INTO stock_items(id, item_name, price, category, quantity) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (item.item_id, item.item_name, item.price, item.category, item.quantity))
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
