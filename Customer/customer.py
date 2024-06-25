# customer.py
import sqlite3

class Customer:
    def __init__(self, id, name, address, phone, email):
        self._id = id
        self._name = name
        self._address = address
        self._phone = phone
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def phone(self):
        return self._phone

    @property
    def email(self):
        return self._email

    @staticmethod
    def get_all_customers():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, name, address, phone, email FROM Customer''')
        rows = cursor.fetchall()
        conn.close()
        return [Customer(*row) for row in rows]

    @staticmethod
    def get_customer_by_id(customer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, name, address, phone, email FROM Customer WHERE id = ?''', (customer_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Customer(*row)
        else:
            return None

    def update(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Customer
            SET name = ?, address = ?, phone = ?, email = ?
            WHERE id = ?
        ''', (self.name, self.address, self.phone, self.email, self.id))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Customer (name, address, phone, email)
            VALUES (?, ?, ?, ?)
        ''', (self.name, self.address, self.phone, self.email))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @staticmethod
    def delete(customer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Customer WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
