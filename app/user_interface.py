#!/usr/bin/env python3

from app.models.stock_manager import StockManager
from app.models.stock_item import StockItem

class UserInterface:
    def __init__(self, stock_manager):
        self.stock_manager = stock_manager

    def run(self):
        while True:
            print("Please select what you want to do:")
            print("1 for add_item")
            print("2 for display")
            print("3 for checkout")
            print("4 for update price")
            print("5 for total value")
            print("6 to set currency")
            print("7 to stop the program.")
            choice = input("Please enter your choice: ")

            if choice == '1':
                while True:
                    item_name = input("Please enter the item name or 'done' to quit: ")
                    item_name = item_name.lower()
                    if item_name.lower() == "done":
                        break
                    price = float(input("Please enter the price of the item: "))
                    category = input("Please enter the item category: ")
                    category = category.lower()
                    quantity = int(input("Please enter the quantity: "))
                    item = StockItem(item_name, price, category, quantity)
                    self.stock_manager.add_item(item)

            elif choice == '2':
                self.stock_manager.display_items()

            elif choice == '3':
                name = input("Please enter the name of the product: ")
                name = name.lower()
                quantity = int(input("Please enter the quantity to be checked-out: "))
                item = self.stock_manager.find_item_by_name(name)
                if item:
                    if item.checkout(quantity):
                        print(f"{quantity} {item.item_name} checked out successfully.")
                    else:
                        print("Insufficient quantity in stock.")
                else:
                    print("Item not found in stock.")

            elif choice == '4':
                update_item_name = input("Enter the name of the item to update the price: ")
                update_item_name = update_item_name.lower()
                item = self.stock_manager.find_item_by_name(update_item_name)
                if item:
                    new_price = float(input("Enter the new price: "))
                    item.update_price(new_price)
                else:
                    print("Item not found in stock.")

            elif choice == '5':
                total_value = sum(item.price * item.quantity for item in self.stock_manager.items)
                print(f"Total value of items in stock: {total_value} ")

            elif choice == '6':
                new_currency = input("Enter the new currency: ")
                item.currency = new_currency

            elif choice == '7':
                break

            else:
                print("Invalid choice. Please choose again.")
