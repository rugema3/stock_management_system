from flask import render_template
from app import app
from app.models.stock_manager import StockManager
from app.user_interface import UserInterface

# Initialize instances once during the application startup
stock_manager = StockManager()
ui = UserInterface(stock_manager)

@app.route('/')
def index():
    # Get items using stock_manager's method
    items = stock_manager.get_all_items()

    # Perform necessary actions using the UserInterface instance
    ui_result = ui.some_method()

    # Pass the items and ui_result to the HTML template for rendering
    return render_template('index.html', items=items, ui_result=ui_result)
