# Customer.py
import sqlite3

class Customer:
    @staticmethod
    def get_all_customers():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, phone, email, address, gender, date_of_birth, customer_type
            FROM Customer
        ''')
        customers = cursor.fetchall()
        conn.close()
        return customers

    @staticmethod
    def get_customer_details(customer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, phone, email, address, gender, date_of_birth, customer_type
            FROM Customer
            WHERE id = ?
        ''', (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return customer

    @staticmethod
    def update_customer(customer_id, name, phone, email, address, gender, date_of_birth, customer_type):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Customer
            SET name = ?, phone = ?, email = ?, address = ?, gender = ?, date_of_birth = ?, customer_type = ?
            WHERE id = ?
        ''', (name, phone, email, address, gender, date_of_birth, customer_type, customer_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_customer(name, phone, email, address, gender, date_of_birth, customer_type):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Customer (name, phone, email, address, gender, date_of_birth, customer_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, address, gender, date_of_birth, customer_type))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_customer(customer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Customer WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
