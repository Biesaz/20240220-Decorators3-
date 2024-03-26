# Create a shop item  manage system. The program main aim is to take inputs (create) from user 
# (item name, amount, price, best_before if aplicable, date entered, item_type (electronic etc)):
#  - The name should be converted all capitals  
#  - amount can't be negative
#  - price should be float.
#  - best bofore should be a date (YYYY-MM-DD)
#  - date entered should be (YYYY-MM-DD hh:mm:ss)
#  - total price value of entered items

# All methods in a class should have a error handling and logging handling through decorators. 
# All data must be saved and retrieved from sql database.
# After submiting data I should be able to retreive all data from database based on item_type.

import sqlite3
from datetime import datetime

class ShopItemManager:
    def __init__(self, db_name='shop_items.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shop_items (
                            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            item_name TEXT,
                            amount INTEGER,
                            price REAL,
                            best_before DATE,
                            date_entered DATETIME,
                            item_type TEXT
                            )''')
        self.conn.commit()

    def error_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error occurred: {e}")
        return wrapper

    def log_handler(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"Logging: {func.__name__} executed")
            return result
        return wrapper

    @error_handler
    @log_handler
    def add_item(self, item_name, amount, price, best_before, date_entered, item_type):
        item_name = item_name.upper()
        if amount < 0:
            raise ValueError("Amount can't be negative")
        if not isinstance(price, float):
            raise ValueError("Price should be a float")
        if not datetime.strptime(best_before, '%Y-%m-%d'):
            raise ValueError("Invalid best before date format. Should be YYYY-MM-DD")
        if not datetime.strptime(date_entered, '%Y-%m-%d %H:%M:%S'):
            raise ValueError("Invalid date entered format. Should be YYYY-MM-DD HH:MM:SS")

        self.cursor.execute('''INSERT INTO shop_items (item_name, amount, price, best_before, date_entered, item_type)
                            VALUES (?, ?, ?, ?, ?, ?)''', (item_name, amount, price, best_before, date_entered, item_type))
        self.conn.commit()

    @error_handler
    @log_handler
    def get_items_by_type(self, item_type):
        self.cursor.execute('''SELECT * FROM shop_items WHERE item_type = ?''', (item_type,))
        items = self.cursor.fetchall()
        return items
    
    def calculate_total_price(self):
        self.cursor.execute('''SELECT price FROM shop_items''')
        prices = self.cursor.fetchall()
        total_price = sum(price[0] for price in prices)
        return total_price

manager = ShopItemManager()

def get_user_input():
    item_name = input("Enter item name: ")
    amount = int(input("Enter amount: "))
    price = float(input("Enter price: "))
    best_before = input("Enter best before date (YYYY-MM-DD): ")
    date_entered = input("Enter date entered (YYYY-MM-DD HH:MM:SS): ")
    item_type = input("Enter item type: ")

    return item_name, amount, price, best_before, date_entered, item_type

item_name, amount, price, best_before, date_entered, item_type = get_user_input()
manager.add_item(item_name, amount, price, best_before, date_entered, item_type)

items = manager.get_items_by_type(item_type)
for item in items:
    print(item)

total_price = manager.calculate_total_price()
print(f"Total price of all items: {total_price}")
