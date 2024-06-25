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
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Human_resources (username, password, name, phone, email, address, gender, role_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, name, phone, email, address, gender, role_id))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, name, role_id FROM Human_resources WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_role_by_id(role_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM Role WHERE id = ?', (role_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else "Unknown"
