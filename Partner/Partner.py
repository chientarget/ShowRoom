# Partner.py
import sqlite3

class Partner:
    @staticmethod
    def get_all_partners():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, address, phone, email
            FROM Partner
        ''')
        partners = cursor.fetchall()
        conn.close()
        return partners

    @staticmethod
    def get_partner_details(partner_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, address, phone, email
            FROM Partner
            WHERE id = ?
        ''', (partner_id,))
        partner = cursor.fetchone()
        conn.close()
        return partner

    @staticmethod
    def update_partner(partner_id, name, address, phone, email):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Partner
            SET name = ?, address = ?, phone = ?, email = ?
            WHERE id = ?
        ''', (name, address, phone, email, partner_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_partner(name, address, phone, email):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Partner (name, address, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, address, phone, email))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_partner(partner_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Partner WHERE id = ?', (partner_id,))
        conn.commit()
        conn.close()
