#!/usr/bin/env python3
from flask import Flask, render_template, request
from app.models.stock_manager import StockManager
from app.models.stock_item import StockItem
from app.models.database_manager import Database
from decouple import config  

app = Flask(__name__, template_folder='app/templates')
stock_manager = StockManager()

# Retrieve database configuration from environment variables
db_config = {
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'database': config('DB_NAME'),
}

# Create a Database instance
db = Database(db_config)

@app.route('/')
def index():
    # Fetch stock items from the database using the Database class
    stock_items = db.get_all_items()
    return render_template('index.html', stock_items=stock_items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = float(request.form['price'])
        category = request.form['category']
        quantity = int(request.form['quantity'])

        # Create a StockItem object with the UUID generated
        stock_item = StockItem(item_name, price, category, quantity)

        # Insert the new item into the database using the Database class
        db.insert_item(stock_item)

    # Fetch the updated stock items from the database
    stock_items = db.get_all_items()

    return render_template('index.html', stock_items=stock_items)


@app.route('/items')
def all_items():
    """
    Retrieves all stock items from the database.
    And renders an HTML page to display them.

    Returns:
        str: Rendered HTML page displaying all stock items.
    """
    # Fetch all stock items from the database using the Database class
    stock_items = db.get_all_items()

    # Create a list to hold the items
    items_list = []

    for item in stock_items:
        # Create a dictionary for each item
        item_data = {
            'item_name': item[1],
            'price': item[2],
            'category': item[3],
            'quantity': item[4],
            'currency': item[5],
            'created_at': item[6],
            'total_cost': item[5] * item[3],
        }

        # Append the item dictionary to the list
        items_list.append(item_data)

    return render_template('items.html', stock_items=items_list)

@app.route('/search', methods=['GET', 'POST'])
def search_item():
    """
    Handle both form submission and displaying search results.

    - For POST requests: Retrieve search query from the form, search for items
      in the database, and display the results.
    - For GET requests: Render the search page without results.

    Returns:
        str: Rendered HTML page displaying the search form and search results (if available).
    """
    if request.method == 'POST':
        search_query = request.form['search_query']
        # Perform the database search for the item based on search_query
        search_results = db.search_item(search_query)

        # Create a list to hold the details of matching items
        items_list = []

        for item in search_results:
            # Create a dictionary for each matching item
            item_data = {
                'item_name': item[1],
                'price': item[5],
                'category': item[2],
                'quantity': item[3],
                'currency': item[4],
                'created_at': item[6],
                'total_cost': item[5] * item[3],
            }

            # Append the item dictionary to the list
            items_list.append(item_data)

        return render_template('search.html', search_results=items_list)
    else:
        # Handle GET request (initial page load)
        return render_template('search.html', search_results=[])



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

