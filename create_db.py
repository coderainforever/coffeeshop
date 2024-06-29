import sqlite3

conn = sqlite3.connect('coffeeshop.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE MenuItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
)
''')

cur.execute('''
CREATE TABLE Ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity REAL NOT NULL
)
''')

cur.execute('''
CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price REAL
)
''')

cur.execute('''
CREATE TABLE OrderItems (
    order_id INTEGER,
    menu_item_id INTEGER,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, menu_item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id)
)
''')

cur.execute('''
CREATE TABLE MenuItemIngredients (
    menu_item_id INTEGER,
    ingredient_id INTEGER,
    quantity_needed REAL NOT NULL,
    PRIMARY KEY (menu_item_id, ingredient_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
)
''')

cur.execute('''
INSERT INTO MenuItems (name, description, price) VALUES
    ('Espresso', 'Strong and bold coffee', 2.50),
    ('Latte', 'Coffee with milk', 3.00),
    ('Cappuccino', 'Coffee with steamed milk foam', 3.50)
''')

cur.execute('''
INSERT INTO Ingredients (name, quantity) VALUES
    ('Coffee Beans', 1000),
    ('Milk', 500),
    ('Sugar', 200)
''')

cur.execute('''
INSERT INTO MenuItemIngredients (menu_item_id, ingredient_id, quantity_needed) VALUES
    (1, 1, 10),  -- Espresso uses 10 units of Coffee Beans
    (2, 1, 8),   -- Latte uses 8 units of Coffee Beans
    (2, 2, 20),  -- Latte uses 20 units of Milk
    (2, 3, 20),  -- Latte uses 20 units of Sugar
    (3, 1, 8),   -- Cappuccino uses 8 units of Coffee Beans
    (3, 2, 30),  -- Cappuccino uses 30 units of Milk
    (3, 3, 20)   -- Cappuccino uses 20 units of Sugar
''')

conn.commit()
conn.close()
