from flask import Flask, render_template, request
from app.models.stock_manager import StockManager
from app.models.stock_item import StockItem

app = Flask(__name__, template_folder='app/templates')
stock_manager = StockManager()

@app.route('/')
def index():
    return render_template('index.html', stock_items=stock_manager.items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = float(request.form['price'])
        category = request.form['category']
        quantity = int(request.form['quantity'])
        stock_item = StockItem(item_name, price, category, quantity)
        stock_manager.add_item(stock_item)
    return render_template('index.html', stock_items=stock_manager.items)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

