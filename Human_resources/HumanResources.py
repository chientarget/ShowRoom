# HumanResources.py
import sqlite3

class HumanResources:
    @staticmethod
    def get_all_employees():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, phone, email, address, gender, date_of_birth, position, department
            FROM Human_resources
        ''')
        employees = cursor.fetchall()
        conn.close()
        return employees

    @staticmethod
    def get_employee_details(employee_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, phone, email, address, gender, date_of_birth, position, department
            FROM Human_resources
            WHERE id = ?
        ''', (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        return employee

    @staticmethod
    def update_employee(employee_id, name, phone, email, address, gender, date_of_birth, position, department):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Human_resources
            SET name = ?, phone = ?, email = ?, address = ?, gender = ?, date_of_birth = ?, position = ?, department = ?
            WHERE id = ?
        ''', (name, phone, email, address, gender, date_of_birth, position, department, employee_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_employee(name, phone, email, address, gender, date_of_birth, position, department):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Human_resources (name, phone, email, address, gender, date_of_birth, position, department)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, address, gender, date_of_birth, position, department))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_employee(employee_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Human_resources WHERE id = ?', (employee_id,))
        conn.commit()
        conn.close()
