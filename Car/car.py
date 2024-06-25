# car.py
import sqlite3

class Car:
    def __init__(self, id, name, produced_year, color, car_type, fuel_capacity, material_consumption, seat_num, engine, price, vin, warranty_year, status):
        self._id = id
        self._name = name
        self._produced_year = produced_year
        self._color = color
        self._car_type = car_type
        self._fuel_capacity = fuel_capacity
        self._material_consumption = material_consumption
        self._seat_num = seat_num
        self._engine = engine
        self._price = price
        self._vin = vin
        self._warranty_year = warranty_year
        self._status = status

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

    # Getter and Setter for car_type
    @property
    def car_type(self):
        return self._car_type

    @car_type.setter
    def car_type(self, value):
        self._car_type = value

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

    # Getter and Setter for engine
    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

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
            SET name = ?, produced_year = ?, color = ?, car_type = ?, fuel_capacity = ?, material_consumption = ?, seat_num = ?, engine = ?, price = ?, vin = ?, warranty_year = ?, status = ?
            WHERE id = ?
        ''', (self.name, self.produced_year, self.color, self.car_type, self.fuel_capacity, self.material_consumption, self.seat_num, self.engine, self.price, self.vin, self.warranty_year, self.status, self.id))
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
