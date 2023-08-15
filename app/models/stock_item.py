#!/usr/bin/python3
"""Module for defining the StockItem class."""

from app.models.base_model import BaseModel


class StockItem(BaseModel):
    """Class representing a stock item.

    Attributes:
        item_name (str): The name of the item.
        price (float): The price of the item.
        category (str): The category of the item.
        quantity (int, optional): The quantity of the item. Default is 0.
        currency (str, optional): The currency of the item's price.
                                  Default is 'RWF'.
    """
    def __init__(self, item_name, price, category, quantity=0, currency='RWF'):
        """Initialize a StockItem instance."""
        super().__init__(item_name, price, category, quantity, currency)

    def display(self):
        total_price = self.calculate_total_price()
        return (f"Item ID: {self.item_id}\n"
                f"Item Name: {self.item_name}\n"
                f"Price: {self.price} {self.currency}\n"
                f"Quantity: {self.quantity}\n"
                f"Category: {self.category}\n"
                f"Total Price: {total_price} {self.currency}")

    def calculate_total_price(self):
        return f"{self.currency} {self.price * self.quantity:.2f}"
