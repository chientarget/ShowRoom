import sqlite3

def get_database_connection():
    return sqlite3.connect('showroom.db')

def add_user(username, password, name, phone, email, address, gender, role_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Human_resources (username, password, name, phone, email, address, gender, role_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, name, phone, email, address, gender, role_id))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, name, phone, email, address, gender, role_id FROM Human_resources WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_role_by_id(role_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM Role WHERE id = ?', (role_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else "Unknown"

def get_monthly_revenue():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total_price) FROM "Order"')
    revenue = cursor.fetchone()[0] or 0
    conn.close()
    return revenue

def get_cars_sold():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Car WHERE status = "Đã bán"')
    sold = cursor.fetchone()[0] or 0
    conn.close()
    return sold

def get_cars_in_stock():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Car WHERE status = "Chưa bán"')
    in_stock = cursor.fetchone()[0] or 0
    conn.close()
    return in_stock

def get_top_dealers():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.name, SUM(o.total_price) as total_revenue
        FROM Dealer d
        JOIN "Order" o ON d.id = o.dealer_id
        GROUP BY d.id
        ORDER BY total_revenue DESC
        LIMIT 3
    ''')
    top_dealers = cursor.fetchall()
    conn.close()
    return top_dealers

def get_top_human_resource_weekly():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.name, SUM(o.total_price) as total_revenue
        FROM Human_resources h
        JOIN "Order" o ON h.id = o.human_resource_id
        GROUP BY h.id
        ORDER BY total_revenue DESC
        LIMIT 3
    ''')
    top_human_resource = cursor.fetchall()
    conn.close()
    return top_human_resource

def get_top_human_resource_monthly():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.name, SUM(o.total_price) as total_revenue
        FROM Human_resources h
        JOIN "Order" o ON h.id = o.human_resource_id
        GROUP BY h.id
        ORDER BY total_revenue DESC
        LIMIT 3
    ''')
    top_human_resource = cursor.fetchall()
    conn.close()
    return top_human_resource


PERMISSIONS = {
    'Quản lý': ['all'],
    'Nhân viên bán hàng': ['add_order', 'view_order', 'view_car'],
    'Kỹ thuật viên': ['add_car', 'view_dealer'],
    'Nhân viên chăm sóc khách hàng': ['view_customer', 'update_customer']
}

def has_permission(role, action):
    if 'all' in PERMISSIONS.get(role, []):
        return True
    return action in PERMISSIONS.get(role, [])

def get_user_role(user_id):
    conn = sqlite3.connect('showroom.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Role.name
        FROM Human_resources
        JOIN Role ON Human_resources.role_id = Role.id
        WHERE Human_resources.id = ?
    ''', (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else None