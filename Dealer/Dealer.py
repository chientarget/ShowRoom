import sqlite3

class Dealer:
    def __init__(self, id=None, name="", address="", phone="", email="", open_time=None, close_time=None):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.open_time = open_time
        self.close_time = close_time

    @staticmethod
    def get_dealers():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, address, phone, email, open_time, close_time FROM Dealer')
        dealers = cursor.fetchall()
        conn.close()
        return [Dealer(*dealer) for dealer in dealers]

    @staticmethod
    def get_dealer_details(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, address, phone, email, open_time, close_time FROM Dealer WHERE id = ?', (dealer_id,))
        dealer = cursor.fetchone()
        conn.close()
        return Dealer(*dealer) if dealer else None

    def add_dealer(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Dealer (name, address, phone, email, open_time, close_time) VALUES (?, ?, ?, ?, ?, ?)',
                       (self.name, self.address, self.phone, self.email, self.open_time, self.close_time))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update_dealer(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Dealer SET name = ?, address = ?, phone = ?, email = ?, open_time = ?, close_time = ? WHERE id = ?',
                       (self.name, self.address, self.phone, self.email, self.open_time, self.close_time, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_dealer(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Dealer WHERE id = ?', (dealer_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_dealer_revenue(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(price) FROM Car
            WHERE dealer_id = ?
        ''', (dealer_id,))
        revenue = cursor.fetchone()[0] or 0
        conn.close()
        return revenue

    @staticmethod
    def get_dealer_car_count(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM Car
            WHERE dealer_id = ?
        ''', (dealer_id,))
        count = cursor.fetchone()[0] or 0
        conn.close()
        return count

    @staticmethod
    def get_dealer_employee_count(dealer_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM Human_resources
            WHERE dealer_id = ?
        ''', (dealer_id,))
        count = cursor.fetchone()[0] or 0
        conn.close()
        return count

    @staticmethod
    def format_price(price):
        if price >= 1_000_000_000:
            return f"{price / 1_000_000_000:.2f} Tỷ"
        elif price >= 1_000_000:
            return f"{price / 1_000_000:.0f} Triệu"
        else:
            return f"{price:,} vnđ"

    def __str__(self):
        return f"{self.name} - {self.address}"



