from flask import render_template
from app import app
from app.models.stock_manager import StockManager
from app.user_interface import UserInterface

stock_manager = StockManager()
ui = UserInterface(stock_manager)

@app.route('/')
def index():
    return render_template('index.html')

