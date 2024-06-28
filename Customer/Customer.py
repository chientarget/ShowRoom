import sqlite3

class Customer:
    def __init__(self, id, name, address, phone, email):
        self._id = id
        self._name = name
        self._address = address
        self._phone = phone
        self._email = email

    #region Properties[Getters, Setters]
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

    #endregion Properties[Getters, Setters]

    @staticmethod
    def get_all_customers():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, name, address, phone, email FROM Customer''')
        rows = cursor.fetchall()
        conn.close()
        return [Customer(*row) for row in rows]

    @staticmethod
    def get_all_customers_with_total_purchase():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
               SELECT Customer.id, Customer.name, Customer.address, Customer.phone, Customer.email, 
                      SUM("Order".total_price) as total_purchase
               FROM Customer
               LEFT JOIN "Order" ON Customer.id = "Order".customer_id
               GROUP BY Customer.id
               ORDER BY total_purchase DESC
           ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

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

    @staticmethod
    def get_purchased_car_count(customer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT COUNT(*) FROM "Order" WHERE customer_id = ?
            ''', (customer_id,))
        count = cursor.fetchone()[0] or 0
        conn.close()
        return count

    @staticmethod
    def get_total_purchase_value(customer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT SUM(total_price) FROM "Order" WHERE customer_id = ?
            ''', (customer_id,))
        total_value = cursor.fetchone()[0] or 0
        conn.close()
        return total_value

