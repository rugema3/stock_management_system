#!/usr/bin/env python3
class StockManager:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def display_items(self):
        for item in self.items:
            print(item.display())

    def find_item_by_name(self, name):
        for item in self.items:
            if item.item_name == name:
                return item
        return f"The item is not available"

    def set_currency(self, currency):
        self.currency = currency
        for item in self.items:
            item.currency = currency
