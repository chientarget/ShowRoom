# Car.py
import sqlite3

class Car:
    @staticmethod
    def get_all_cars():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, warranty_year, status
            FROM Car
        ''')
        cars = cursor.fetchall()
        conn.close()
        return cars

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def add_car(name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Car (name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_car(car_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Car WHERE id = ?', (car_id,))
        conn.commit()
        conn.close()
