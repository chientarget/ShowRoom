# Partner.py
import sqlite3

class Partner:
    def __init__(self, id, logo, name, country, founded_year, description):
        self._id = id
        self._logo = logo
        self._name = name
        self._country = country
        self._founded_year = founded_year
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def logo(self):
        return self._logo

    @property
    def name(self):
        return self._name

    @property
    def country(self):
        return self._country

    @property
    def founded_year(self):
        return self._founded_year

    @property
    def description(self):
        return self._description

    @staticmethod
    def get_all_partners():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, logo, name, country, founded_year, description FROM Partner''')
        rows = cursor.fetchall()
        conn.close()
        return [Partner(*row) for row in rows]

    @staticmethod
    def get_partner_by_id(partner_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, logo, name, country, founded_year, description FROM Partner WHERE id = ?''', (partner_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Partner(*row)
        else:
            return None

    def update(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Partner
            SET logo = ?, name = ?, country = ?, founded_year = ?, description = ?
            WHERE id = ?
        ''', (self.logo, self.name, self.country, self.founded_year, self.description, self.id))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Partner (logo, name, country, founded_year, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.logo, self.name, self.country, self.founded_year, self.description))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @staticmethod
    def delete(partner_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Partner WHERE id = ?', (partner_id,))
        conn.commit()
        conn.close()
