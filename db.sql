-- Table: Car
CREATE TABLE Car
(
    id                   INTEGER PRIMARY KEY,
    produced_year        INTEGER,
    color                TEXT,
    name                 TEXT,
    car_type_id          INTEGER,
    fuel_capacity        TEXT,
    material_consumption TEXT,
    seat_num             INTEGER,
    engine_id            INTEGER,
    price                DECIMAL,
    vin                  TEXT UNIQUE,
    dealer_id            INTEGER,
    warranty_year        INTEGER,
    Partner_id           INTEGER,
    model_id             INTEGER,
    airbags              TEXT,
    status               TEXT,
    FOREIGN KEY (car_type_id) REFERENCES Car_Type (id),
    FOREIGN KEY (dealer_id) REFERENCES Dealer (id),
    FOREIGN KEY (Partner_id) REFERENCES Partner (id),
    FOREIGN KEY (engine_id) REFERENCES Engine (id),
    FOREIGN KEY (model_id) REFERENCES Model (id)

);
CREATE TABLE Car_Type
(
    id   INTEGER PRIMARY KEY,
    name TEXT
);
-- Table: Model
CREATE TABLE Model
(
    id   INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Engine
CREATE TABLE Engine
(
    id   INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Dealer
CREATE TABLE Dealer
(
    id          INTEGER PRIMARY KEY,
    name        TEXT,
    address     TEXT,
    phone       TEXT,
    zip         TEXT,
    email       TEXT,
    open_time   TIME,
    close_time  TIME,
    description TEXT
);

-- Table: Human_resources
CREATE TABLE Human_resources
(
    id       INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    name     TEXT,
    phone    TEXT,
    email    TEXT,
    address  TEXT,
    gender   BOOLEAN,
    role_id  INTEGER,
    dealer_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES Role (id),
    FOREIGN KEY (dealer_id) REFERENCES Dealer (id)
);

-- Table: Role
CREATE TABLE Role
(
    id   INTEGER PRIMARY KEY,
    name TEXT
);

-- Table: Customer
CREATE TABLE Customer
(
    id      INTEGER PRIMARY KEY,
    name    TEXT,
    phone   TEXT,
    email   TEXT,
    address TEXT,
    gender  BOOLEAN
);

-- Table: Order
CREATE TABLE "Order"
(
    id                INTEGER PRIMARY KEY,
    customer_id       INTEGER,
    dealer_id         INTEGER,
    total_price       INTEGER,
    creation_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    car_id            INTEGER,
    human_resource_id INTEGER,
    FOREIGN KEY (car_id) REFERENCES Car (id),
    FOREIGN KEY (customer_id) REFERENCES Customer (id),
    FOREIGN KEY (dealer_id) REFERENCES Dealer (id),
    FOREIGN KEY (human_resource_id) REFERENCES Human_resources (id)
);

-- Table: Partner
CREATE TABLE Partner
(
    id           INTEGER PRIMARY KEY,
    name         TEXT,
    country      TEXT,
    founded_year INTEGER,
    description  TEXT
);


-- Dữ liệu mẫu cho bảng Car (đã sửa)
INSERT INTO Car (produced_year, color, name, car_type_id, fuel_capacity, material_consumption, seat_num, engine_id, price, vin, dealer_id, warranty_year, Partner_id, model_id, airbags, status)
VALUES (2024, 'Đỏ', 'VinFast VF 6', 1, '90', '6.5L/100km', 5, 1, 675000000, 'VIN001', 1, 3, 1, 1, '6 túi khí', 'Đã bán'),
       (2024, 'Xanh', 'VinFast VF 7', 2, '90', '7.5L/100km', 5, 1, 850000000, 'VIN002', 2, 3, 1, 2, '8 túi khí', 'Đã bán'),
       (2024, 'Đen', 'VinFast VF 8', 3, '90', '8.0L/100km', 7, 1, 1050000000, 'VIN003', 2, 3, 1, 3, '10 túi khí', 'Đặt cọc'),
       (2024, 'Trắng', 'VinFast VF 9', 4, '90', '8.5L/100km', 7, 1, 1250000000, 'VIN004', 2, 3, 1, 4, '12 túi khí', 'Chưa bán'),
       (2024, 'Bạc', 'Honda City', 5, '90', '5.5L/100km', 5, 2, 529000000, 'VIN005', 3, 3, 2, 5, '6 túi khí', 'Đã bán'),
       (2024, 'Xám', 'Honda CR-V', 6, '90', '7.0L/100km', 7, 2, 998000000, 'VIN006', 4, 3, 2, 6, '8 túi khí', 'Đã bán'),
       (2024, 'Đen', 'Honda Civic', 7, '90', '6.0L/100km', 5, 2, 730000000, 'VIN007', 4, 3, 2, 7, '6 túi khí', 'Chưa bán'),
       (2024, 'Trắng', 'Rolls-Royce Ghost', 1, '90', '15.0L/100km', 5, 3, 30000000000, 'VIN008', 5, 4, 3, 8, '8 túi khí', 'Đã bán'),
       (2024, 'Đen', 'Rolls-Royce Phantom', 2, '90', '16.0L/100km', 5, 3, 40000000000, 'VIN009', 5, 4, 3, 9, '10 túi khí', 'Chưa bán'),
       (2024, 'Xanh', 'Toyota Camry', 3, '90', '6.5L/100km', 5, 2, 1105000000, 'VIN010', 6, 3, 4, 10, '7 túi khí', 'Chưa bán'),
       (2024, 'Bạc', 'Toyota Corolla Cross', 4, '90', '5.5L/100km', 5, 2, 720000000, 'VIN011', 6, 3, 4, 11, '7 túi khí', 'Chưa bán'),
       (2024, 'Đỏ', 'Mazda CX-5', 3, '90', '7.0L/100km', 5, 2, 839000000, 'VIN012', 7, 3, 5, 12, '6 túi khí', 'Chưa bán'),
       (2024, 'Trắng', 'Mazda3', 1, '90', '6.0L/100km', 5, 2, 669000000, 'VIN013', 7, 3, 5, 13, '6 túi khí', 'Chưa bán'),
       (2024, 'Xám', 'Mercedes-Benz C-Class', 6, '90', '7.0L/100km', 5, 2, 1669000000, 'VIN014', 8, 3, 6, 14, '9 túi khí', 'Chưa bán'),
       (2024, 'Đen', 'Mercedes-Benz GLC', 2, '90', '8.0L/100km', 5, 2, 1859000000, 'VIN015', 8, 3, 6, 15, '9 túi khí', 'Chưa bán'),
       (2024, 'Trắng', 'BMW 3 Series', 2, '90', '6.5L/100km', 5, 2, 1529000000, 'VIN016', 9, 3, 7, 16, '8 túi khí', 'Đã bán'),
       (2024, 'Xanh', 'BMW X3', 1, '90', '7.5L/100km', 5, 2, 1999000000, 'VIN017', 9, 3, 7, 17, '8 túi khí', 'Đặt cọc'),
       (2024, 'Đỏ', 'Audi A4', 3, '90', '6.0L/100km', 5, 2, 1700000000, 'VIN018', 10, 3, 8, 18, '8 túi khí', 'Chưa bán'),
       (2024, 'Bạc', 'Audi Q5', 3, '90', '7.5L/100km', 5, 2, 2400000000, 'VIN019', 10, 3, 8, 19, '8 túi khí', 'Đặt cọc'),
       (2024, 'Đen', 'Lexus ES', 3, '90', '6.5L/100km', 5, 2, 2540000000, 'VIN020', 11, 3, 9, 20, '10 túi khí', 'Chưa bán');


-- Dữ liệu mẫu cho bảng Car_Type

INSERT INTO Car_Type (name)
VALUES ('Sedan'),
       ('Hatchback'),
       ('SUV'),
       ('CUV'),
       ('MPV/Minivan'),
       ('Pickup'),
       ('Coupe'),
       ('Convertible/Cabriolet'),
       ('Luxury');


-- Dữ liệu mẫu cho bảng Model
INSERT INTO Model (name)
VALUES ('VF 6'),
       ('VF 7'),
       ('VF 8'),
       ('VF 9'),
       ('City'),
       ('CR-V'),
       ('Civic'),
       ('Ghost'),
       ('Phantom'),
       ('Camry'),
       ('Corolla Cross'),
       ('CX-5'),
       ('Mazda3'),
       ('C-Class'),
       ('GLC'),
       ('3 Series'),
       ('X3'),
       ('A4'),
       ('Q5'),
       ('ES');

-- Dữ liệu mẫu cho bảng Engine
INSERT INTO Engine (name)
VALUES ('Điện'),
       ('Động cơ đốt trong'),
       ('Hybrid'),
       ('4WD'),
       ('AWD');


-- Dữ liệu mẫu cho bảng Dealer
INSERT INTO Dealer (name, address, phone, zip, email, open_time, close_time, description)
VALUES ('VinFast Hà Nội', 'Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội', '0243123456', '100000', 'hanoi@vinfast.vn', '08:00:00', '20:00:00', 'Đại lý chính hãng VinFast tại Hà Nội'),
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
INSERT INTO Human_resources (username, password, name, phone, email, address, gender, role_id, dealer_id)
VALUES ('huychien', '123', 'Nguyễn Huy Chiến', '0901234567', 'huychien@vinfast.vn', 'Hà Nội', 1, 1,1),
       ('tungduong', '123', 'Trần Tùng Dương', '0912345678', 'tungduong@vinfast.vn', 'TP.HCM', 0, 2,2),
       ('thivan', '123', 'Đỗ Thị Vân', '0923456789', 'thivan@hondaoto.vn', 'Hà Nội', 1, 3,3),
       ('c4', '123', 'Phạm Thị D', '0934567890', 'ptd@toyotavn.com.vn', 'TP.HCM', 0, 2,3),
       ('c5', '123', 'Hoàng Văn E', '0945678901', 'hve@mazdavn.vn', 'Hà Nội', 1, 3,4);

-- Dữ liệu mẫu cho bảng Role
INSERT INTO Role (name)
VALUES ('Quản lý'),
       ('Nhân viên bán hàng'),
       ('Kỹ thuật viên'),
       ('Nhân viên chăm sóc khách hàng');

-- Dữ liệu mẫu cho bảng Customer
INSERT INTO Customer (name, phone, email, address, gender)
VALUES ('Đặng Văn F', '0956789012', 'dvf@gmail.com', 'Hà Nội', 1),
       ('Ngô Thị G', '0967890123', 'ntg@gmail.com', 'TP.HCM', 0),
       ('Bùi Văn H', '0978901234', 'bvh@gmail.com', 'Đà Nẵng', 1),
       ('Lý Thị I', '0989012345', 'lti@gmail.com', 'Hải Phòng', 0),
       ('Vũ Văn K', '0990123456', 'vvk@gmail.com', 'Cần Thơ', 1);

INSERT INTO "Order" (customer_id, dealer_id, total_price, creation_time, car_id, human_resource_id)
VALUES
(1, 1, 675000000, CURRENT_TIMESTAMP, 1, 1),
(2, 2, 850000000, CURRENT_TIMESTAMP, 2, 2),
(3, 2, 1050000000, CURRENT_TIMESTAMP, 3, 2),
(4, 3, 529000000, CURRENT_TIMESTAMP, 5, 3),
(5, 4, 998000000, CURRENT_TIMESTAMP, 6, 4),
(1, 5, 30000000000, CURRENT_TIMESTAMP, 8, 5),
(2, 9, 1529000000, CURRENT_TIMESTAMP, 16, 1),
(3, 9, 1999000000, CURRENT_TIMESTAMP, 17, 2),
(4, 10, 2400000000, CURRENT_TIMESTAMP, 19, 3);


-- Dữ liệu mẫu cho bảng Partner
INSERT INTO Partner (name, country, founded_year, description)
VALUES ('VinFast', 'Việt Nam', 2017, 'Nhà sản xuất ô tô và xe máy điện Việt Nam'),
       ('Honda', 'Nhật Bản', 1948, 'Nhà sản xuất ô tô, xe máy và động cơ hàng đầu thế giới'),
       ('Rolls-Royce', 'Anh', 1904, 'Nhà sản xuất xe hơi siêu sang'),
       ('Toyota', 'Nhật Bản', 1937, 'Hãng sản xuất ô tô lớn nhất thế giới'),
       ('Mazda', 'Nhật Bản', 1920, 'Nhà sản xuất ô tô nổi tiếng với công nghệ SkyActiv');



