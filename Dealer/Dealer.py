# Dealer.py
import sqlite3

class Dealer:
    @staticmethod
    def get_all_dealers():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, address, phone, email
            FROM Dealer
        ''')
        dealers = cursor.fetchall()
        conn.close()
        return dealers

    @staticmethod
    def get_dealer_details(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, address, phone, email
            FROM Dealer
            WHERE id = ?
        ''', (dealer_id,))
        dealer = cursor.fetchone()
        conn.close()
        return dealer

    @staticmethod
    def update_dealer(dealer_id, name, address, phone, email):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Dealer
            SET name = ?, address = ?, phone = ?, email = ?
            WHERE id = ?
        ''', (name, address, phone, email, dealer_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_dealer(name, address, phone, email):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Dealer (name, address, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, address, phone, email))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_dealer(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Dealer WHERE id = ?', (dealer_id,))
        conn.commit()
        conn.close()
