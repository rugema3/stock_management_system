import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_item(self, item_id, item_name, price, quantity, category, currency):
        sql = "INSERT INTO stock_items (item_id, item_name, price, quantity, category, currency) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (item_id, item_name, price, quantity, category, currency)
        self.cursor.execute(sql, values)
        self.connection.commit()
