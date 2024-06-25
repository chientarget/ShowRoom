import sqlite3

def get_cars():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, warranty_year, status
        FROM Car
    ''')
    cars = cursor.fetchall()
    conn.close()
    return cars


def get_car_details(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status
        FROM Car
        WHERE id = ?
    ''', (car_id,))
    car = cursor.fetchone()
    conn.close()
    return car

def update_car(car_id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Car
        SET name = ?, produced_year = ?, color = ?, car_type = ?, fuel_capacity = ?, material_consumption = ?, seat_num = ?, engine = ?, price = ?, vin = ?, warranty_year = ?, status = ?
        WHERE id = ?
    ''', (name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status, car_id))
    conn.commit()
    conn.close()

def add_car(name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Car (name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status))
    conn.commit()
    conn.close()

def delete_car(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Car WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()

def add_user(username, password, name, phone, email, address, gender, role_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Human_resources (username, password, name, phone, email, address, gender, role_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, name, phone, email, address, gender, role_id))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, name, phone, email, address, gender, role_id FROM Human_resources WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user(user_id, username, password, name, phone, email, address, gender, role_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Human_resources
        SET username = ?, password = ?, name = ?, phone = ?, email = ?, address = ?, gender = ?, role_id = ?
        WHERE id = ?
    ''', (username, password, name, phone, email, address, gender, role_id, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Human_resources WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_users():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, name, phone, email, address, gender, role_id FROM Human_resources')
    users = cursor.fetchall()
    conn.close()
    return users

def get_roles():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM Role')
    roles = cursor.fetchall()
    conn.close()
    return roles

def get_role_by_id(role_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM Role WHERE id = ?', (role_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else "Unknown"


def get_database_connection():
    return sqlite3.connect('showroom.db')

def get_monthly_revenue():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total_price) FROM "Order"')
    revenue = cursor.fetchone()[0] or 0
    conn.close()
    return revenue

def get_cars_sold():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Car WHERE status = "Đã bán"')
    sold = cursor.fetchone()[0] or 0
    conn.close()
    return sold

def get_cars_in_stock():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Car WHERE status = "Chưa bán"')
    in_stock = cursor.fetchone()[0] or 0
    conn.close()
    return in_stock

def get_top_dealers():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.name, SUM(o.total_price) as total_revenue
        FROM Dealer d
        JOIN "Order" o ON d.id = o.dealer_id
        GROUP BY d.id
        ORDER BY total_revenue DESC
        LIMIT 3
    ''')
    top_dealers = cursor.fetchall()
    conn.close()
    return top_dealers

def get_top_human_resource_weekly():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.name, SUM(o.total_price) as total_revenue
        FROM Human_resources h
        JOIN "Order" o ON h.id = o.human_resource_id
        GROUP BY h.id
        ORDER BY total_revenue DESC
        LIMIT 3
    ''')
    top_human_resource = cursor.fetchall()
    conn.close()
    return top_human_resource

def get_top_human_resource_monthly():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.name, SUM(o.total_price) as total_revenue
        FROM Human_resources h
        JOIN "Order" o ON h.id = o.human_resource_id
        GROUP BY h.id
        ORDER BY total_revenue DESC
        LIMIT 3
    ''')
    top_human_resource = cursor.fetchall()
    conn.close()
    return top_human_resource


def get_order_columns():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info("Order")')
    columns = cursor.fetchall()
    conn.close()
    return columns


def get_orders():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, customer_id, total_price, car_id, human_resource_id, dealer_id
        FROM "Order"
    ''')
    orders = cursor.fetchall()
    conn.close()
    return orders


def add_order(customer_id, total_price, car_id, human_resource_id, dealer_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
         INSERT INTO "Order" (customer_id, total_price, car_id, human_resource_id, dealer_id)
         VALUES (?, ?, ?, ?, ?)
     ''', (customer_id, total_price, car_id, human_resource_id, dealer_id))
    conn.commit()
    conn.close()


def update_order(order_id, customer_id, total_price, car_id, human_resource_id, dealer_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
         UPDATE "Order"
         SET customer_id = ?, total_price = ?, car_id = ?, human_resource_id = ?, dealer_id = ?
         WHERE id = ?
     ''', (customer_id, total_price, car_id, human_resource_id, dealer_id, order_id))
    conn.commit()
    conn.close()


def delete_order(order_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "Order" WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()

