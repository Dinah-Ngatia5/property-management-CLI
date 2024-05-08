import sqlite3
import re
from datetime import datetime
from contextlib import contextmanager

conn = sqlite3.connect("property_management.db")
cursor = conn.cursor()

#creating the tables
#Users Table for Authentication
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

#Properties Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
''')

#Tenants table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_description TEXT NOT NULL,
    request_date DATE,
    request_status TEXT NOT NULL,
    tenant_id INTEGER,
    property_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
)
""")

#Rent_payment table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rent_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    tenant_id INTEGER, 
    payment_amount REAL NOT NULL,
    payment_date DATE,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
)
""")

#Expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               description TEXT NOT NULL,
               amount REAL NOT NULL,
               property_id INTEGER,
               FOREIGN KEY (property_id) REFERENCES properties (id)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS documents (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               file_path TEXT NOT NULL,
               property_id INTEGER NOT NULL,
               access_level TEXT NOT NULL,
               FOREIGN KEY (property_id) REFERENCES properties(id)
)
""")
#Commit all the changes and close the connection 
conn.commit()
conn.close()


@contextmanager
def get_cursor():
    conn = sqlite3.connect("property_management.db")
    try:
        yield conn.cursor()
    finally:
        conn.close()

class User:
    def __init__ (self, username, password):
        self.username= username
        self.password= password


    def save(self):
        with get_cursor() as cursor:
            cursor.execute("""
            INSERT INTO users (username, password)
            VALUES(?, ?)
""", (self.username, self.password,))
            


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
            VALUES(?, ?, ?, ?, ?)
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


    def add_property():
        try:
            address = input("Enter property address: ")  
            city= input("Enter city: ")
            rent_amount= input("Enter price: ")

            #Data validation
            if not address or not city:
                raise ValueError("Address and city are required fields.")
            if not re.match(r"^\d+(\.\d{2})?$", rent_amount):
                raise ValueError("Invalid price format. Price should be a number with optional two decimal places.")
            
            price= float(rent_amount)
            owner_id= int(input("Enter owner ID: "))

            property= Property(address, city, price, owner_id)
            property.save()
            print("Property added successfully.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


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


    #function to add a new rent payment
    def add_rent_payment(property_id, tenant_id, payment_amount):
        payment_date =  datetime.now().strftime('%Y-%m-%d')
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO rent_payments(property_id, tenant_id, payment_amount, payment_date) VALUES(?, ?, ?, ?)",
                           (property_id, tenant_id, payment_amount, payment_date))


    #function to retrieve rent payments for a specific property
    def get_rent_payments_for_property(property_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM rent_payments WHERE property_id = ?", (property_id,))
            payments= cursor.fetchall()
            for payment in payments:
                print(payment)

    #function to retrieve rent payments for a specific tenant
    def get_rent_payments_for_tenant(tenant_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM rent_payments WHERE tenant_id= ?", (tenant_id,))
            payments = cursor.fetchall()
            for payment in payments:
                print(payment)


    #function to delete a rent payment
    def delete_rent_payment(payment_id):
        with get_cursor() as cursor:
            cursor.execute('DELETE FROM rent_payments WHERE id=?', (payment_id,))
            conn.commit()
            print("Rent payment deleted successfully")




class MaintenanceRequest:
    def __init__ (self, request_description, tenant_id, property_id, request_date, request_status="open",):
        self.request_description = request_description
        self.tenant_id= tenant_id
        self.property_id= property_id
        self.request_status= request_status
        self.request_date= request_date


    def save(self):
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO maintenance_requests (request_description, tenant_id, property_id, request_date, request_status) VALUES (?, ?, ?, ?)", 
                           (self.request_description, self.tenant_id, self.property_id, self.request_date, self.request_status))
            
    
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
        

    #function to add a new maintenance request
    def add_maintenance_request(property_id, tenant_id, request_description, request_date, request_status):
        request_date= datetime.now().strftime("%Y-%m-%d")
        request_status="Pending"
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO maintenance_request (property_id, tenant_id, request_date, request_description, request_status) VALUES (?, ?, ?, ?, ?)",
                           (property_id, tenant_id, request_date, request_description, request_date, request_status))
            conn.commit()
            print("Maintenance request added successfully!")


    #function to retrieve maintenance requests for a specific property
    def get_maintenance_requests_for_property(property_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM maintenance_requests WHERE property_id = ?", (property_id,))
            requests= cursor.fetchall()
            for  request in requests:
                print(request)


    #function to retrieve maintenance requests for a specific tenant
    def get_maintenance_requests_for_tenant(tenant_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM maintenance_requests WHERE tenant_id= ?", (tenant_id,))
            requests= cursor.fetchall()
            for request in requests:
                print(request)

    
    #function to update the status of a maintenance request
    def update_maintenance_request_status(request_id, new_status):
        cursor.execute("UPDATE maintenance_requests SET request_status= ? WHERE id=?", (new_status, request_id))
        conn.commit()
        print("Maintenance request status updated successfully")
    


    #function to delete a maintenance request
    def delete_maintenance_request(request_id):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM maintenance_requests WHERE id = ?", (request_id,))
            conn.commit()
            print("Maintenance request status deleted successfully!")




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
    def get_expenses_for_property(property_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE property_id = ?", (property_id,))
            expenses = cursor.fetchall()

            return expenses

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


