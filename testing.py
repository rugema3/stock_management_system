from app.models.database_manager import Database

# Database configuration (replace with your actual configuration)
db_config = {
    'user': 'rugema3',
    'password': 'Shami@2020',
    'host': 'localhost',
    'database': 'stock',
}

# Create a Database instance
db = Database(db_config)

# Test the get_all_items method
def test_get_all_items():
    try:
        items = db.get_all_items()
        if items:
            for item in items:
                print(f"Item ID: {item[0]}")
                print(f"Item Name: {item[1]}")
                print(f"Price: {item[2]}")
                print(f"Category: {item[3]}")
                print(f"Quantity: {item[4]}\n")
        else:
            print("No items found in the database.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_get_all_items()

