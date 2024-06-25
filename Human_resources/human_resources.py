import sqlite3

class HumanResource:
    def __init__(self, id, username, password, name, phone, email, address, gender, role_id):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.gender = gender
        self.role_id = role_id

    @staticmethod
    def get_all_human_resource():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, username, password, name, phone, email, address, gender, role_id FROM Human_resources''')
        human_resources = cursor.fetchall()
        conn.close()
        return human_resources

    @staticmethod
    def get_human_resource_by_id(human_resource_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT id, username, password, name, phone, email, address, gender, role_id FROM Human_resources WHERE id = ?''', (human_resource_id,))
        human_resource = cursor.fetchone()
        conn.close()
        return human_resource

    def update(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Human_resources
            SET username = ?, password = ?, name = ?, phone = ?, email = ?, address = ?, gender = ?, role_id = ?
            WHERE id = ?
        ''', (self.username, self.password, self.name, self.phone, self.email, self.address, self.gender, self.role_id, self.id))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Human_resources (username, password, name, phone, email, address, gender, role_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.username, self.password, self.name, self.phone, self.email, self.address, self.gender, self.role_id))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @staticmethod
    def delete(human_resource_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Human_resources WHERE id = ?', (human_resource_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_roles():
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM Role')
        roles = cursor.fetchall()
        conn.close()
        return roles

    @staticmethod
    def get_role_name(role_id):
        conn = sqlite3.connect('showroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM Role WHERE id = ?', (role_id,))
        role_name = cursor.fetchone()[0]
        conn.close()
        return role_name
