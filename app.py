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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

