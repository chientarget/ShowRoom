import sqlite3

class Dealer:
    def __init__(self, id=None, name="", address="", phone="", email=""):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email

    @staticmethod
    def get_dealers():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, address, phone, email FROM Dealer')
        dealers = cursor.fetchall()
        conn.close()
        return [Dealer(*dealer) for dealer in dealers]

    @staticmethod
    def get_dealer_details(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, address, phone, email FROM Dealer WHERE id = ?', (dealer_id,))
        dealer = cursor.fetchone()
        conn.close()
        return Dealer(*dealer) if dealer else None

    def add_dealer(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Dealer (name, address, phone, email) VALUES (?, ?, ?, ?)',
                       (self.name, self.address, self.phone, self.email))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update_dealer(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Dealer SET name = ?, address = ?, phone = ?, email = ? WHERE id = ?',
                       (self.name, self.address, self.phone, self.email, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_dealer(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Dealer WHERE id = ?', (dealer_id,))
        conn.commit()
        conn.close()

    def __str__(self):
        return f"{self.name} - {self.address}"
