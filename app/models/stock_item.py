#!/usr/bin/python3
from app.models.base_model import BaseModel

class StockItem(BaseModel):
    def __init__(self, item_name, price, category, quantity=0):
        super().__init__(item_name, price, category, quantity)

    def display(self):
        return f"Item ID: {self.item_id}\nItem Name: {self.item_name}\nPrice: {self.price}\nQuantity: {self.quantity}\nCategory: {self.category}"

