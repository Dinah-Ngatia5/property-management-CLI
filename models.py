import sqlite3

conn = sqlite3.connect('property_management.db')
cursor = conn.cursor()

#Properties Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    rent_amount INTEGER NOT NULL,
    status TEXT NOT NULL,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES owners(id)
)
""")

#Owners Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS owners (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
''')

#Tenants table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    lease_start_date TEXT NOT NULL,
    lease_end_date TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    property_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
""")

#Maintenance_requests table
cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance_requests (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    property_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
""")

conn.commit()
conn.close()

class Property:
    def __init__(self, address, rent_amount, status="Available", owner_id=None):
        self.address= address
        self.rent_amount= rent_amount
        self.status= status
        self.owner_id= owner_id

    def save(self):
        conn = sqlite3.connect("property_management.db")
        cursor= conn.cursor()
        cursor.execute("""
            INSERT INTO properties (address, rent_amount, status, owner_id)
            VALUES(?, ?, ?, ?)
""", (self.address, self.rent_amount, self.status, self.owner_id))
        conn.commit()
        conn.close()



class Owner:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def save(self):
        conn = sqlite3.connect("property_management.db")
        cursor= conn.cursor()
        cursor.execute("""
INSERT INTO owners (name, email, phone)
                       VALUES(?, ?, ?)
""", (self.name, self.email, self.phone))
        conn.commit()
        conn.close()

       