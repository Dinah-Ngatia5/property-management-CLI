import sqlite3
from datetime import datetime
from contextlib import contextmanager

conn = sqlite3.connect('property_management.db')
cursor = conn.cursor()

#Properties Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
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


@contextmanager
def get_cursor():
    conn = sqlite3.connect("property_management.db")
    try:
        yield conn.cursor()
    finally:
        conn.close()

class Property:
    def __init__(self, address, city, rent_amount, status="Available", owner_id=None):
        self.address= address
        self.rent_amount= rent_amount
        self.status= status
        self.owner_id= owner_id
        self.city= city

    def save(self):
       with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO properties (address, city, rent_amount, status, owner_id)
            VALUES(?, ?, ?, ?)
""", (self.address, self.city, self.rent_amount, self.status, self.owner_id))
       
    
    @staticmethod
    def get_all():
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM properties")
            return cursor.fetchall
        
    
    def get_by_id(property_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM properties WHERE id= ?", (property_id,))
            return cursor.fetchone()
        
    #will add methods like delete, update, etc later
 

class Owner:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def save(self):
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO owners (name, email, phone) VALUES(?, ?, ?)",
                            (self.name, self.email, self.phone))
       
       
       
    @staticmethod
    def get_all():
        with get_cursor as cursor:
            cursor.execute("SELECT * FROM owners")
            return cursor.fetchall()
        

    @staticmethod
    def get_by_id(owner_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM owner WHERE id = ?", (owner_id,))
            return cursor.fetchone()
        


class Tenant:
    def __init__(self, name, contact_info, lease_start_date, lease_end_date, property_id):
        self.name= name
        self.contact_info= contact_info
        self.lease_start_date= lease_start_date
        self.lease_end_date= lease_end_date
        self.property_id= property_id

    
    def save(self):
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO tenants (name, contact_info, lease_start_date, lease_end_date, property_id VALUES (?, ?, ?, ?, ?)",
                           (self.name, self.contact_info, self.lease_start_date, self.lease_end_date, self.property_id))
            
    

    @staticmethod
    def get_all():
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM tenants")
            return cursor.fetchall()
    

    @staticmethod
    def get_by_id(tenant_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM tenants WHERE id=?", (tenant_id,))
            return cursor.fetchone()



    #Section for adding methods like delete, update etc


class RentPayment:
    def __init__ (self, tenant_id, property_id, payment_date, amount):
        self.tenant_id = tenant_id
        self.property_id= property_id
        self.payment_date= payment_date
        self.amount= amount


    def save(self):
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO rent_payments (tenant_id, property_id, payment_date, amount) VALUES(?, ?, ?, ? )", 
                           (self.tenant_id, self.property_id, self.payment_date, self.amount))
            


    @staticmethod
    def get_all():
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM rent_payments")
            return cursor.fetchall()
        

    @staticmethod
    def get_by_id(payment_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM rent_payment WHERE id= ?", (payment_id,))
            return cursor.fetchone()


    # add methods (delete, update, etc)



class MaintenanceRequest:
    def __init__ (self, description, tenant_id, property_id, status="open"):
        self.description = description
        self.tenant_id= tenant_id
        self.property_id= property_id
        self.status= status


    def save(self):
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO maintenance_requests (description, tenant_id, property_id, status) VALUES (?, ?, ?, ?)", 
                           (self.description, self.tenant_id, self.property_id, self.status))
            
    
    @staticmethod
    def get_all():
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM maintenance_requests")
            return cursor.fetchall()
        

    @staticmethod
    def get_by_id(request_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM maintenance_requests WHERE id= ?", (request_id,))
            return cursor.fetchone()
        

    # add other methods (delete, update etc)



class Expense:
    def __init__ (self, description, amount, date, property_id):
        self.description = description
        self.amount= amount
        self.date= date
        self.property_id= property_id


    def save(self):
        with get_cursor() as cursor:
            cursor.execute("""
INSERT INTO expenses (description, amount, date, property_id) VALUES(?, ?, ?, ?)
""", (self.description, self.amount, self.date, self.property_id))
            
    
    @staticmethod
    def get_all():
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM expenses")
            return cursor.fetchall()
        

    @staticmethod
    def get_by_id(expense_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            return cursor.fetchone()
        


    # add methods as needed (delete, update)


class Document:
    def __init__ (self, name, file_path, property_id, access_level):
        self.name= name
        self.file_path= file_path
        self.property_id = property_id
        self.access_level= access_level

    

    def save(self):
        with get_cursor() as cursor:
            cursor.execute("""
INSERT INTO documents (name, file_path, property_id, access_level) VALUES (?, ?, ?, ?)
""", (self.name, self.file_path, self.property_id, self.access_level))
            

    
    @staticmethod
    def get_all():
        with get_cursor as cursor:
            cursor.execute("SELECT * FROM documents ")
            return cursor.fetchall()


    
    @staticmethod
    def get_by_id(document_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM documents WHERE id= ?", (document_id,))
            return cursor.fetchone()
        

    #add other methods(delete, update)


