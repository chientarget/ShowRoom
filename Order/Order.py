# Order.py
import sqlite3

class Order:
    @staticmethod
    def get_all_orders():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, customer_id, total_price, car_id, human_resource_id, dealer_id
            FROM "Order"
        ''')
        orders = cursor.fetchall()
        conn.close()
        return orders

    @staticmethod
    def get_order_details(order_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT customer_id, total_price, car_id, human_resource_id, dealer_id
            FROM "Order"
            WHERE id = ?
        ''', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return order

    @staticmethod
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

    @staticmethod
    def add_order(customer_id, total_price, car_id, human_resource_id, dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO "Order" (customer_id, total_price, car_id, human_resource_id, dealer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, total_price, car_id, human_resource_id, dealer_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_order(order_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM "Order" WHERE id = ?', (order_id,))
        conn.commit()
        conn.close()
