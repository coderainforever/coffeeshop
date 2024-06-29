from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('coffeeshop.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/menu', methods=['GET'])
def get_menu():
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM MenuItems').fetchall()
    conn.close()
    menu_items = [dict(row) for row in menu_items]
    return jsonify(menu_items)

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    order_items = data['orderItems']
    total = data['total']
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('BEGIN')

        # Check if there are enough ingredients
        for item in order_items:
            ingredients = cur.execute('''
                SELECT ingredient_id, quantity_needed
                FROM MenuItemIngredients
                WHERE menu_item_id = ?
            ''', (item['id'],)).fetchall()

            for ingredient in ingredients:
                cur.execute('''
                    SELECT quantity FROM Ingredients
                    WHERE id = ?
                ''', (ingredient['ingredient_id'],))
                available_quantity = cur.fetchone()['quantity']
                required_quantity = ingredient['quantity_needed'] * item['quantity']

                if available_quantity < required_quantity:
                    conn.rollback()
                    return jsonify({'status': 'error', 'message': f'Not enough {ingredient["ingredient_id"]} to fulfill the order. Please add more ingredients.'})

        # Place the order and update ingredient quantities
        cur.execute('INSERT INTO Orders (total_price) VALUES (?)', (total,))
        order_id = cur.lastrowid

        for item in order_items:
            cur.execute('INSERT INTO OrderItems (order_id, menu_item_id, quantity) VALUES (?, ?, ?)', (order_id, item['id'], item['quantity']))

            ingredients = cur.execute('''
                SELECT ingredient_id, quantity_needed
                FROM MenuItemIngredients
                WHERE menu_item_id = ?
            ''', (item['id'],)).fetchall()

            for ingredient in ingredients:
                cur.execute('''
                    UPDATE Ingredients
                    SET quantity = quantity - ?
                    WHERE id = ?
                ''', (ingredient['quantity_needed'] * item['quantity'], ingredient['ingredient_id']))

        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        conn.close()

@app.route('/api/todays-sales', methods=['GET'])
def todays_sales():
    conn = get_db_connection()
    cur = conn.cursor()
    today = datetime.now().date()
    cur.execute('SELECT SUM(total_price) as total_sales FROM Orders WHERE DATE(order_date) = ?', (today,))
    result = cur.fetchone()
    conn.close()
    total_sales = result['total_sales'] if result['total_sales'] is not None else 0
    return jsonify({'total_sales': total_sales})

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM Ingredients').fetchall()
    conn.close()
    ingredients = [dict(row) for row in ingredients]
    return jsonify(ingredients)

@app.route('/api/ingredients', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    name = data['name']
    quantity = data['quantity']
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO Ingredients (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        conn.close()

@app.route('/api/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
    data = request.get_json()
    quantity = data['quantity']
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('UPDATE Ingredients SET quantity = quantity + ? WHERE id = ?', (quantity, id))
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
