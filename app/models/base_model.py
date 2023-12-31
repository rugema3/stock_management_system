#!/usr/bin/env python3
"""base_model module."""
import uuid


class BaseModel:
    """Define BaseModel class."""
    def __init__(self, item_name, price, category, quantity=0, currency='RWF'):
        """Define class Constructor.
        Attributes:

        item_id(str):   The unique of an item.
        item_name(str): The name of the item.
        quanity(int):   The quantity of the item.
        Price(float):   The price of the item.
        Category(str):  The category of the item.
        currency(str):  The currency of the item's price.
        """
        self.item_id = str(uuid.uuid4())
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.currency = currency

    def display(self):
        """Display items in the stock."""
        return (f"Item ID: {self.item_id}\nItem Name: {self.item_name}\n"
                "Price: {self.price}\nQuantity: {self.quantity}\n"
                "Category: {self.category}")

    def checkout(self, quantity):
        """Take items from the stock."""
        if self.quantity >= quantity:
            self.quantity -= quantity
            return True
        return False

    def update_price(self, new_price):
        """Update the price of the item in the stock."""
        try:
            new_price = float(new_price)
            self.price = new_price
            print("Price updated successfully.")
        except ValueError:
            print("The price must be a number.")

    def total(self):
        """Calculate the total of the item price."""
        total_price = self.price * self.quantity
        return f"Total price for {self.quantity} {self.item_name}(s) is: {total_price:.2f} {self.currency}"
