# order.py
import sqlite3

class Order:
    def __init__(self, id, customer_id, total_price, car_id, human_resource_id, dealer_id):
        self._id = id
        self._customer_id = customer_id
        self._total_price = total_price
        self._car_id = car_id
        self._human_resource_id = human_resource_id
        self._dealer_id = dealer_id

    @property
    def id(self):
        return self._id

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def total_price(self):
        return self._total_price

    @property
    def car_id(self):
        return self._car_id

    @property
    def human_resource_id(self):
        return self._human_resource_id

    @property
    def dealer_id(self):
        return self._dealer_id

    @staticmethod
    def get_all_orders():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, customer_id, total_price, car_id, human_resource_id, dealer_id FROM "Order"''')
        rows = cursor.fetchall()
        conn.close()
        return [Order(*row) for row in rows]

    @staticmethod
    def get_order_by_id(order_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, customer_id, total_price, car_id, human_resource_id, dealer_id FROM "Order" WHERE id = ?''', (order_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Order(*row)
        else:
            return None

    def update(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE "Order"
            SET customer_id = ?, total_price = ?, car_id = ?, human_resource_id = ?, dealer_id = ?
            WHERE id = ?
        ''', (self.customer_id, self.total_price, self.car_id, self.human_resource_id, self.dealer_id, self.id))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO "Order" (customer_id, total_price, car_id, human_resource_id, dealer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.customer_id, self.total_price, self.car_id, self.human_resource_id, self.dealer_id))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @staticmethod
    def delete(order_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM "Order" WHERE id = ?', (order_id,))
        conn.commit()
        conn.close()
