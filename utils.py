import sqlite3

conn = sqlite3.connect("property_management.db")
cursor = conn.cursor()

# Properties table
cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
               id INTEGER PRIMARY KEY,
               address TEXT NOT NULL,
               rent_amount INTEGER NOT NULL, 
               status TEXT NOT NULL,
               owner_id INTEGER,
               FOREIGN KEY(owner_id) REFERENCES owners(id)
)
''')
# owners table
cursor.execute('''
CREATE TABLE IF NOT EXISTS owners (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL, 
               email TEXT NOT NULL, 
               phone TEXT NOT NULL
)
''')

# Tenants table
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

# Maintenance_request table
cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance_requests (
               id INTEGER PRIMARY KEY,
               description TEXT NOT NULL, 
               status TEXT NOT NULL,
               property_id INTEGER,
               FOREIGN KEY (property_id) REFERENCES properties(id)
)
""")

# this commits all the changes and closes the connection
conn.commit()
conn.close