#!/usr/bin/python3

from app.models.stock_manager import StockManager
from app.user_interface import UserInterface

if __name__ == "__main__":
    stock_manager = StockManager()
    ui = UserInterface(stock_manager)
    ui.run()
