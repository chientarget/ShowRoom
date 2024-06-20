-- Table: Car
CREATE TABLE Car (
    id INTEGER PRIMARY KEY,
    produced_year INTEGER,
    color TEXT,
    name TEXT,
    size TEXT,
    fuel_capacity TEXT,
    material_consumption TEXT,
    seat_num INTEGER,
    engine TEXT,
    price DECIMAL,
    vin TEXT UNIQUE,
    dealer_id INTEGER,
    warranty_year INTEGER,
    series_id INTEGER,
    manu_facturer_id INTEGER,
    drive_id INTEGER,
    model_id INTEGER,
    airbags TEXT,
    status TEXT,
--     Chưa bán", "Đã bán", "Chờ mở bán
    FOREIGN KEY (dealer_id) REFERENCES Dealer(id),
    FOREIGN KEY (series_id) REFERENCES Series(id),
    FOREIGN KEY (manu_facturer_id) REFERENCES Manu_facturer(id),
    FOREIGN KEY (drive_id) REFERENCES Drive(id),
    FOREIGN KEY (model_id) REFERENCES Model(id)
);

-- Table: Model
CREATE TABLE Model (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Drive
CREATE TABLE Drive (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Series
CREATE TABLE Series (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Dealer
CREATE TABLE Dealer (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    phone TEXT,
    zip TEXT,
    email TEXT,
    open_time TIME,
    close_time TIME,
    description TEXT
);

-- Table: Human_resources
CREATE TABLE Human_resources (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    gender BOOLEAN,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES Role(id)
);

-- Table: Role
CREATE TABLE Role (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Customer
CREATE TABLE Customer (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    gender BOOLEAN
);

-- Table: Car_image
CREATE TABLE Car_image (
    id INTEGER PRIMARY KEY,
    image_data BLOB,
    car_id INTEGER,
    FOREIGN KEY (car_id) REFERENCES Car(id)
);

-- Table: Dealer_image
CREATE TABLE Dealer_image (
    id INTEGER PRIMARY KEY,
    image_data BLOB,
    dealer_id INTEGER,
    FOREIGN KEY (dealer_id) REFERENCES Dealer(id)
);

-- Table: Order
CREATE TABLE "Order" (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    dealer_id INTEGER,
    total_price INTEGER,
    car_id INTEGER,
    employee_id INTEGER,
    FOREIGN KEY (car_id) REFERENCES Car(id),
    FOREIGN KEY (customer_id) REFERENCES Customer(id),
    FOREIGN KEY (dealer_id) REFERENCES Dealer(id),
    FOREIGN KEY (employee_id) REFERENCES Human_resources(id)
);

-- Table: Manu_facturer
CREATE TABLE Manu_facturer (
    id INTEGER PRIMARY KEY,
    logo TEXT,
    name TEXT,
    country TEXT,
    founded_year INTEGER,
    description TEXT
);

-- Table: History
CREATE TABLE History (
    id INTEGER PRIMARY KEY,
    bill_id INTEGER,
    FOREIGN KEY (bill_id) REFERENCES "Order"(id)
);



-- Dữ liệu mẫu cho bảng Car
INSERT INTO Car (produced_year, color, name, size, fuel_capacity, material_consumption, seat_num, engine, price, vin, dealer_id, warranty_year, series_id, manu_facturer_id, drive_id, model_id, airbags) VALUES
(2024, 'Đỏ', 'VinFast VF 6', 'Crossover', '90', '6.5L/100km', 5, 'Điện', 675000000, 'VIN001', 1, 3, 1, 1, 1, 1, '6 túi khí'),
(2024, 'Xanh', 'VinFast VF 7', 'SUV', '90', '7.5L/100km', 5, 'Điện', 850000000, 'VIN002', 1, 3, 1, 1, 1, 2, '8 túi khí'),
(2024, 'Đen', 'VinFast VF 8', 'SUV', '90', '8.0L/100km', 7, 'Điện', 1050000000, 'VIN003', 2, 3, 1, 1, 1, 3, '10 túi khí'),
(2024, 'Trắng', 'VinFast VF 9', 'SUV', '90', '8.5L/100km', 7, 'Điện', 1250000000, 'VIN004', 2, 3, 1, 1, 1, 4, '12 túi khí'),
(2024, 'Bạc', 'Honda City', 'Sedan', '90', '5.5L/100km', 5, 'Xăng 1.5L', 529000000, 'VIN005', 3, 3, 2, 2, 2, 5, '6 túi khí'),
(2024, 'Xám', 'Honda CR-V', 'SUV', '90', '7.0L/100km', 7, 'Xăng 1.5L Turbo', 998000000, 'VIN006', 3, 3, 2, 2, 2, 6, '8 túi khí'),
(2024, 'Đen', 'Honda Civic', 'Sedan', '90', '6.0L/100km', 5, 'Xăng 1.5L Turbo', 730000000, 'VIN007', 4, 3, 2, 2, 2, 7, '6 túi khí'),
(2024, 'Trắng', 'Rolls-Royce Ghost', 'Sedan', '90', '15.0L/100km', 5, 'V12 6.75L', 30000000000, 'VIN008', 5, 4, 3, 3, 3, 8, '8 túi khí'),
(2024, 'Đen', 'Rolls-Royce Phantom', 'Sedan', '90', '16.0L/100km', 5, 'V12 6.75L', 40000000000, 'VIN009', 5, 4, 3, 3, 3, 9, '10 túi khí'),
(2024, 'Xanh', 'Toyota Camry', 'Sedan', '90', '6.5L/100km', 5, 'Xăng 2.5L', 1105000000, 'VIN010', 6, 3, 4, 4, 2, 10, '7 túi khí'),
(2024, 'Bạc', 'Toyota Corolla Cross', 'Crossover', '90', '5.5L/100km', 5, 'Hybrid 1.8L', 720000000, 'VIN011', 6, 3, 4, 4, 2, 11, '7 túi khí'),
(2024, 'Đỏ', 'Mazda CX-5', 'SUV', '90', '7.0L/100km', 5, 'Xăng 2.0L', 839000000, 'VIN012', 7, 3, 5, 5, 2, 12, '6 túi khí'),
(2024, 'Trắng', 'Mazda3', 'Sedan', '90', '6.0L/100km', 5, 'Xăng 1.5L', 669000000, 'VIN013', 7, 3, 5, 5, 2, 13, '6 túi khí'),
(2024, 'Xám', 'Mercedes-Benz C-Class', 'Sedan', '90', '7.0L/100km', 5, 'Xăng 1.5L Turbo', 1669000000, 'VIN014', 8, 3, 6, 6, 2, 14, '9 túi khí'),
(2024, 'Đen', 'Mercedes-Benz GLC', 'SUV', '90', '8.0L/100km', 5, 'Xăng 2.0L Turbo', 1859000000, 'VIN015', 8, 3, 6, 6, 2, 15, '9 túi khí'),
(2024, 'Trắng', 'BMW 3 Series', 'Sedan', '90', '6.5L/100km', 5, 'Xăng 2.0L Turbo', 1529000000, 'VIN016', 9, 3, 7, 7, 2, 16, '8 túi khí'),
(2024, 'Xanh', 'BMW X3', 'SUV', '90', '7.5L/100km', 5, 'Xăng 2.0L Turbo', 1999000000, 'VIN017', 9, 3, 7, 7, 2, 17, '8 túi khí'),
(2024, 'Đỏ', 'Audi A4', 'Sedan', '90', '6.0L/100km', 5, 'Xăng 2.0L Turbo', 1700000000, 'VIN018', 10, 3, 8, 8, 2, 18, '8 túi khí'),
(2024, 'Bạc', 'Audi Q5', 'SUV', '90', '7.5L/100km', 5, 'Xăng 2.0L Turbo', 2400000000, 'VIN019', 10, 3, 8, 8, 2, 19, '8 túi khí'),
(2024, 'Đen', 'Lexus ES', 'Sedan', '90', '6.5L/100km', 5, 'Xăng 2.5L', 2540000000, 'VIN020', 11, 3, 9, 9, 2, 20, '10 túi khí');


-- Dữ liệu mẫu cho bảng Model
INSERT INTO Model (name) VALUES
('VF 6'), ('VF 7'), ('VF 8'), ('VF 9'),
('City'), ('CR-V'), ('Civic'),
('Ghost'), ('Phantom'),
('Camry'), ('Corolla Cross'),
('CX-5'), ('Mazda3'),
('C-Class'), ('GLC'),
('3 Series'), ('X3'),
('A4'), ('Q5'),
('ES');

-- Dữ liệu mẫu cho bảng Drive
INSERT INTO Drive (name) VALUES
('Điện'),
('Động cơ đốt trong'),
('Hybrid'),
('4WD'),
('AWD');



-- Dữ liệu mẫu cho bảng Series
INSERT INTO Series (name) VALUES
('VinFast EV'),
('Honda Sedan'),
('Rolls-Royce Luxury'),
('Toyota Hybrid'),
('Mazda SUV'),
('Mercedes-Benz Luxury'),
('BMW Performance'),
('Audi Premium'),
('Lexus Luxury');


-- Dữ liệu mẫu cho bảng Dealer
INSERT INTO Dealer (name, address, phone, zip, email, open_time, close_time, description) VALUES
('VinFast Hà Nội', 'Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội', '0243123456', '100000', 'hanoi@vinfast.vn', '08:00:00', '20:00:00', 'Đại lý chính hãng VinFast tại Hà Nội'),
('VinFast TP.HCM', '123 Nguyễn Văn Linh, Quận 7, TP.HCM', '0283123456', '700000', 'hcm@vinfast.vn', '08:00:00', '20:00:00', 'Đại lý chính hãng VinFast tại TP.HCM'),
('Honda Ôtô Giải Phóng', '831 Giải Phóng, Hoàng Mai, Hà Nội', '0243555666', '100000', 'giaiphong@hondaoto.vn', '08:00:00', '18:00:00', 'Đại lý Honda Ôtô Giải Phóng'),
('Honda Ôtô Phước Thành', '63 Võ Văn Tần, Quận 3, TP.HCM', '0283987654', '700000', 'phuocthanh@hondaoto.vn', '08:00:00', '18:00:00', 'Đại lý Honda Ôtô Phước Thành'),
('Rolls-Royce Motor Cars Hanoi', '8 Phạm Hùng, Nam Từ Liêm, Hà Nội', '0243111222', '100000', 'hanoi@rolls-roycemotorcars.com', '09:00:00', '18:00:00', 'Đại lý Rolls-Royce chính hãng tại Hà Nội'),
('Toyota Thăng Long', '316 Cầu Giấy, Cầu Giấy, Hà Nội', '0243123789', '100000', 'thanglong@toyotavn.com.vn', '08:00:00', '17:30:00', 'Đại lý Toyota Thăng Long'),
('Mazda Phạm Văn Đồng', '68 Phạm Văn Đồng, Bắc Từ Liêm, Hà Nội', '0243456789', '100000', 'pvd@mazdavn.vn', '08:00:00', '18:00:00', 'Đại lý Mazda Phạm Văn Đồng'),
('Mercedes-Benz Vietnam Star', '2 Trường Chinh, Tân Bình, TP.HCM', '0283666777', '700000', 'star@mercedesvietnam.com', '08:00:00', '19:00:00', 'Đại lý Mercedes-Benz Vietnam Star'),
('BMW Long Biên', 'Số 1 Ngô Gia Tự, Long Biên, Hà Nội', '0243777888', '100000', 'longbien@bmw.com.vn', '08:00:00', '18:30:00', 'Đại lý BMW Long Biên'),
('Audi Hà Nội', '8A Phạm Hùng, Nam Từ Liêm, Hà Nội', '0243999000', '100000', 'hanoi@audi.vn', '08:00:00', '18:00:00', 'Đại lý Audi chính hãng tại Hà Nội'),
('Lexus Thảo Điền', '264 Mai Chí Thọ, Quận 2, TP.HCM', '0283222333', '700000', 'thaodien@lexus.com.vn', '08:00:00', '19:00:00', 'Đại lý Lexus Thảo Điền');

-- Dữ liệu mẫu cho bảng Human_resources
INSERT INTO Human_resources (username, password, name, phone, email, address, gender, role_id) VALUES
('nv001', 'pass123', 'Nguyễn Văn A', '0901234567', 'nva@vinfast.vn', 'Hà Nội', 1, 1),
('nv002', 'pass234', 'Trần Thị B', '0912345678', 'ttb@vinfast.vn', 'TP.HCM', 0, 2),
('nv003', 'pass345', 'Lê Văn C', '0923456789', 'lvc@hondaoto.vn', 'Hà Nội', 1, 3),
('nv004', 'pass456', 'Phạm Thị D', '0934567890', 'ptd@toyotavn.com.vn', 'TP.HCM', 0, 2),
('nv005', 'pass567', 'Hoàng Văn E', '0945678901', 'hve@mazdavn.vn', 'Hà Nội', 1, 3);

-- Dữ liệu mẫu cho bảng Role
INSERT INTO Role (name) VALUES
('Quản lý'),
('Nhân viên bán hàng'),
('Kỹ thuật viên'),
('Nhân viên hành chính'),
('Nhân viên chăm sóc khách hàng');

-- Dữ liệu mẫu cho bảng Customer
INSERT INTO Customer (name, phone, email, address, gender) VALUES
('Đặng Văn F', '0956789012', 'dvf@gmail.com', 'Hà Nội', 1),
('Ngô Thị G', '0967890123', 'ntg@gmail.com', 'TP.HCM', 0),
('Bùi Văn H', '0978901234', 'bvh@gmail.com', 'Đà Nẵng', 1),
('Lý Thị I', '0989012345', 'lti@gmail.com', 'Hải Phòng', 0),
('Vũ Văn K', '0990123456', 'vvk@gmail.com', 'Cần Thơ', 1);

-- Dữ liệu mẫu cho bảng Car_image (giả định đường dẫn ảnh)
INSERT INTO Car_image (image_data, car_id) VALUES
(X'89504E470D0A1A0A', 1),
(X'89504E470D0A1A0A', 2),
(X'89504E470D0A1A0A', 3),
(X'89504E470D0A1A0A', 4),
(X'89504E470D0A1A0A', 5);

-- Dữ liệu mẫu cho bảng Dealer_image (giả định đường dẫn ảnh)
INSERT INTO Dealer_image (image_data, dealer_id) VALUES
(X'89504E470D0A1A0A', 1),
(X'89504E470D0A1A0A', 2),
(X'89504E470D0A1A0A', 3),
(X'89504E470D0A1A0A', 4),
(X'89504E470D0A1A0A', 5);

-- Dữ liệu mẫu cho bảng "Order"
INSERT INTO "Order" (customer_id, dealer_id, total_price, car_id, employee_id) VALUES
(1, 1, 675000000, 1, 1),
(2, 2, 850000000, 2, 2),
(3, 3, 529000000, 5, 3),
(4, 4, 998000000, 6, 4),
(5, 5, 30000000000, 8, 5);

-- Dữ liệu mẫu cho bảng Manu_facturer
INSERT INTO Manu_facturer (logo, name, country, founded_year, description) VALUES
('vinfast_logo.png', 'VinFast', 'Việt Nam', 2017, 'Nhà sản xuất ô tô và xe máy điện Việt Nam'),
('honda_logo.png', 'Honda', 'Nhật Bản', 1948, 'Nhà sản xuất ô tô, xe máy và động cơ hàng đầu thế giới'),
('rolls_royce_logo.png', 'Rolls-Royce', 'Anh', 1904, 'Nhà sản xuất xe hơi siêu sang'),
('toyota_logo.png', 'Toyota', 'Nhật Bản', 1937, 'Hãng sản xuất ô tô lớn nhất thế giới'),
('mazda_logo.png', 'Mazda', 'Nhật Bản', 1920, 'Nhà sản xuất ô tô nổi tiếng với công nghệ SkyActiv');

-- Dữ liệu mẫu cho bảng History
INSERT INTO History (bill_id) VALUES
(1),
(2),
(3),
(4),
(5);

