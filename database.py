import sqlite3

def get_cars():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, produced_year, color, warranty_year, price, fuel_capacity, status
        FROM Car
    ''')
    cars = cursor.fetchall()
    conn.close()
    return cars

def get_car_details(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, produced_year, color, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status
        FROM Car
        WHERE id = ?
    ''', (car_id,))
    car = cursor.fetchone()
    conn.close()
    return car

def update_car(car_id, name, produced_year, color, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Car
        SET name = ?, produced_year = ?, color = ?, size = ?, fuel_capacity = ?, material_consumption = ?, seat_num = ?, engine = ?, price = ?, vin = ?, warranty_year = ?, status = ?
        WHERE id = ?
    ''', (name, produced_year, color, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status, car_id))
    conn.commit()
    conn.close()

def add_car(name, produced_year, color, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Car (name, produced_year, color, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, produced_year, color, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status))
    conn.commit()
    conn.close()

def delete_car(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Car WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()
