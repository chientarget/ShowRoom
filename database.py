import sqlite3

def init_db():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            year INTEGER,
            color TEXT,
            size TEXT,
            engine TEXT,
            max_power TEXT,
            fuel_capacity TEXT,
            transmission TEXT,
            fuel_consumption TEXT,
            drivetrain TEXT,
            seats INTEGER,
            airbags INTEGER,
            warranty TEXT,
            price TEXT,
            dealer TEXT,
            status TEXT
        )
    ''')

    # Insert sample data
    sample_data = [
        ("VINFAST LUX A2.0", "Sedan", 2021, "Trắng", "4,973 x 1,900 x 1,464 mm", "2.0L", "228 HP", "70L", "Tự động 8 cấp", "8.5L/100km", "RWD", 5, 6, "5 năm", "2.114.000.000 VND", "Vinfast Dealer 1", "Đã bán"),
        ("VINFAST VF 9", "SUV", 2022, "Trắng", "5,120 x 2,000 x 1,721 mm", "Electric", "402 HP", "90 kWh", "Single-speed", "N/A", "AWD", 7, 6, "10 năm", "2.114.000.000 VND", "Vinfast Dealer 2", "Chưa bán"),
        ("VINFAST President", "SUV", 2022, "Trắng", "4,750 x 1,900 x 1,660 mm", "Electric", "402 HP", "90 kWh", "Single-speed", "N/A", "AWD", 5, 6, "10 năm", "2.114.000.000 VND", "Vinfast Dealer 3", "Đặt cọc")
    ]

    cursor.executemany('''
        INSERT INTO cars (name, type, year, color, size, engine, max_power, fuel_capacity, transmission, fuel_consumption, drivetrain, seats, airbags, warranty, price, dealer, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()

def get_cars():
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, type, year, color, warranty, price, status FROM cars')
    cars = cursor.fetchall()
    conn.close()
    return cars

def get_car_details(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, type, year, color, size, engine, max_power, fuel_capacity, transmission, fuel_consumption, drivetrain, seats, airbags, warranty, price, dealer, status FROM cars WHERE id = ?', (car_id,))
    car = cursor.fetchone()
    conn.close()
    return car

def update_car(car_id, name, car_type, year, color, size, engine, max_power, fuel_capacity, transmission, fuel_consumption, drivetrain, seats, airbags, warranty, price, dealer, status):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cars
        SET name = ?, type = ?, year = ?, color = ?, size = ?, engine = ?, max_power = ?, fuel_capacity = ?, transmission = ?, fuel_consumption = ?, drivetrain = ?, seats = ?, airbags = ?, warranty = ?, price = ?, dealer = ?, status = ?
        WHERE id = ?
    ''', (name, car_type, year, color, size, engine, max_power, fuel_capacity, transmission, fuel_consumption, drivetrain, seats, airbags, warranty, price, dealer, status, car_id))
    conn.commit()
    conn.close()

def delete_car(car_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    conn.commit()
    conn.close()
