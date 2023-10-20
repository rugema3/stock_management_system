#!/usr/bin/env python3

from app.models.user_manager import UserManager
from flask import Flask, render_template, request, redirect, session
from app.models.stock_manager import StockManager
from app.models.stock_item import StockItem
from app.models.database_manager import Database
from decouple import config  
import bcrypt
from app.models.user import User 
from flask_session import Session
from decorators.authentication_decorators import login_required

app = Flask(__name__, template_folder='app/templates',  static_folder='app/static')
stock_manager = StockManager()
#user_manager = UserManager()

# Retrieve database configuration from environment variables
db_config = {
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'database': config('DB_NAME'),
}

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  
Session(app)
# Create a Database instance
db = Database(db_config)
user_manager = UserManager(db_config)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/home')
@login_required
def home():
    # Retrieve the user's email from the session
    user_email = session.get('user_email')
    if user_email:
        # Fetch user-specific data or perform actions
        # ...
        return render_template('home.html', user_email=user_email)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect('/login')

@app.route('/add_item', methods=['POST', 'GET'])
@login_required
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

    return render_template('add_item.html', stock_items=stock_items)


@app.route('/items')
@login_required
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
@login_required
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
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve the email and password from the form data
        email = request.form['email']
        password = request.form['password']

        # Create a User object with email and password
        user = User(email=email, password=password)

        # Call the user_manager to register the user
        registration_result = user_manager.register_user(user)

        # Render the result in the HTML response
        return registration_result
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # You can call your UserManager's login_user method here
        login_result = user_manager.login_user(email, password)

        if login_result == "Login successful!":
            # Store user information in the session
            session['user_email'] = email
            # Redirect to a dashboard or home page
            return redirect('/home')
        else:
            return render_template('login.html', error=login_result)

    # For GET requests, simply render the login page
    return render_template('login.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

