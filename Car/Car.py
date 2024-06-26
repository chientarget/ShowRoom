import sqlite3


def get_cars():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Car')
    cars = cursor.fetchall()
    conn.close()
    return cars


class Car:
    def __init__(self, id, name, produced_year, color, car_type_id, fuel_capacity, material_consumption, seat_num, drive_id, price, vin, warranty_year, status, dealer_id, partner_id, model_id, airbags):
        self._id = id
        self._name = name
        self._produced_year = produced_year
        self._color = color
        self._car_type_id = car_type_id
        self._fuel_capacity = fuel_capacity
        self._material_consumption = material_consumption
        self._seat_num = seat_num
        self._drive_id = drive_id
        self._price = price
        self._vin = vin
        self._warranty_year = warranty_year
        self._status = status
        self._dealer_id = dealer_id
        self._partner_id = partner_id
        self._model_id = model_id
        self._airbags = airbags

    # region Properties [Getter and Setter]
    # Getter and Setter for id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # Getter and Setter for name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Getter and Setter for produced_year
    @property
    def produced_year(self):
        return self._produced_year

    @produced_year.setter
    def produced_year(self, value):
        self._produced_year = value

    # Getter and Setter for color
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    # Getter and Setter for car_type_id
    @property
    def car_type_id(self):
        return self._car_type_id

    @car_type_id.setter
    def car_type_id(self, value):
        self._car_type_id = value

    # Getter and Setter for fuel_capacity
    @property
    def fuel_capacity(self):
        return self._fuel_capacity

    @fuel_capacity.setter
    def fuel_capacity(self, value):
        self._fuel_capacity = value

    # Getter and Setter for material_consumption
    @property
    def material_consumption(self):
        return self._material_consumption

    @material_consumption.setter
    def material_consumption(self, value):
        self._material_consumption = value

    # Getter and Setter for seat_num
    @property
    def seat_num(self):
        return self._seat_num

    @seat_num.setter
    def seat_num(self, value):
        self._seat_num = value

    # Getter and Setter for drive_id
    @property
    def drive_id(self):
        return self._drive_id

    @drive_id.setter
    def drive_id(self, value):
        self._drive_id = value

    # Getter and Setter for price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    # Getter and Setter for vin
    @property
    def vin(self):
        return self._vin

    @vin.setter
    def vin(self, value):
        self._vin = value

    # Getter and Setter for warranty_year
    @property
    def warranty_year(self):
        return self._warranty_year

    @warranty_year.setter
    def warranty_year(self, value):
        self._warranty_year = value

    # Getter and Setter for status
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    # Getter and Setter for dealer_id
    @property
    def dealer_id(self):
        return self._dealer_id

    @dealer_id.setter
    def dealer_id(self, value):
        self._dealer_id = value

    # Getter and Setter for partner_id
    @property
    def partner_id(self):
        return self._partner_id

    @partner_id.setter
    def partner_id(self, value):
        self._partner_id = value

    # Getter and Setter for model_id
    @property
    def model_id(self):
        return self._model_id

    @model_id.setter
    def model_id(self, value):
        self._model_id = value

    # Getter and Setter for airbags
    @property
    def airbags(self):
        return self._airbags

    @airbags.setter
    def airbags(self, value):
        self._airbags = value

    # endregion Properties [Getter and Setter]


    @staticmethod
    def get_all_cars():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status FROM Car''')
        rows = cursor.fetchall()
        conn.close()
        return [Car(*row) for row in rows]

    @staticmethod
    def get_car_by_id(car_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status FROM Car WHERE id = ?''', (car_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Car(*row)
        else:
            return None

    def update(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Car
            SET name = ?, produced_year = ?, color = ?, car_type_id = ?, fuel_capacity = ?, material_consumption = ?, 
                seat_num = ?, drive_id = ?, price = ?, vin = ?, warranty_year = ?, status = ?, 
                dealer_id = ?, partner_id = ?, model_id = ?, airbags = ?
            WHERE id = ?
        ''', (self.name, self.produced_year, self.color, self.car_type_id, self.fuel_capacity, self.material_consumption,
              self.seat_num, self.drive_id, self.price, self.vin, self.warranty_year, self.status,
              self.dealer_id, self.partner_id, self.model_id, self.airbags, self.id))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Car (name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.name, self.produced_year, self.color, self.car_type, self.fuel_capacity, self.material_consumption, self.seat_num, self.engine, self.price, self.vin, self.warranty_year, self.status))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @staticmethod
    def delete(car_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Car WHERE id = ?', (car_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_by_vin(vin):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Car WHERE vin = ?', (vin,))
        conn.commit()
        conn.close()

    def get_car_details(car_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status
            FROM Car
            WHERE id = ?
        ''', (car_id,))
        car = cursor.fetchone()
        conn.close()
        return car


    @staticmethod
    def add_car(name, produced_year, color, car_type_id, fuel_capacity, material_consumption, seat_num, drive_id, price, vin, warranty_year, status, dealer_id, partner_id, model_id, airbags):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Car (name, produced_year, color, car_type_id, fuel_capacity, material_consumption, seat_num, drive_id, price, vin, warranty_year, status, dealer_id, partner_id, model_id, airbags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, produced_year, color, car_type_id, fuel_capacity, material_consumption, seat_num, drive_id, price, vin, warranty_year, status, dealer_id, partner_id, model_id, airbags))
        conn.commit()
        conn.close()

    @staticmethod
    def get_cars():
        conn = sqlite3.connect('../showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, type, year, color, warranty, price, status FROM cars')
        cars = cursor.fetchall()
        conn.close()
        return cars

    @staticmethod
    def get_car_by_vin(vin):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute("""
                SELECT id, name, produced_year, color, car_type_id, fuel_capacity, 
                       material_consumption, seat_num, drive_id, price, vin, 
                       warranty_year, status, dealer_id, partner_id, model_id, airbags 
                FROM Car 
                WHERE vin = ?
            """, (vin,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Car(*row)
        else:
            return None

    @staticmethod
    def get_car_details_by_vin(vin):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT car.name, car.produced_year, car.color, car.car_type_id, car.fuel_capacity, 
                       car.material_consumption, car.seat_num, car.drive_id, car.price, car.vin, 
                       car.warranty_year, car.status, car.dealer_id, car.partner_id, car.model_id, car.airbags 
                FROM Car car
                WHERE car.vin = ?
            ''', (vin,))
        car = cursor.fetchone()
        conn.close()
        return car

    @staticmethod
    def get_foreign_key_data(table_name):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}

    @staticmethod
    def get_name_by_id(table_name, id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM {table_name} WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    @staticmethod
    def get_id_by_name(table_name, name):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {table_name} WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None