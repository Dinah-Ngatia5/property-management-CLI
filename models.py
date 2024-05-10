import sqlite3
import re
from datetime import datetime
from contextlib import contextmanager
import datetime

conn = sqlite3.connect("property_management.db")
cursor = conn.cursor()

#creating the tables

#Users Table for Authentication
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

#Properties Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
''')

#Tenants table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
               expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
               description TEXT NOT NULL,
               amount REAL NOT NULL,
               date DATE,
               property_id INTEGER,
               FOREIGN KEY (property_id) REFERENCES properties (id)
);
""")
#Documents table
cursor.execute("""CREATE TABLE IF NOT EXISTS documents (
               document_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               file_path TEXT NOT NULL,
               property_id INTEGER NOT NULL,
               FOREIGN KEY (property_id) REFERENCES properties(id)
)
""")
#Committing changes & closing the connection 
conn.commit()
conn.close()


@contextmanager
def get_cursor():
    try:
        conn = sqlite3.connect("property_management.db")
        cursor = conn.cursor()
        yield cursor
        conn.commit()  # commit changes to the database
    except sqlite3.Error as e:
        #handle any SQLite errors that occur
        print(f"SQLite error: {e}")
    finally:
        #ensure the connection and cursor are properly closed
        if 'conn' in locals():
            conn.close()

class User:
    def __init__ (self, user_id, username, password):
        self.username= username
        self.password= password
        self.user_id= user_id

    @classmethod
    def create(cls, username, password):
        query = """
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """
        with get_cursor() as cursor:
            cursor.execute(query, (username, password))

     
     
    @classmethod
    def get_or_none(cls, username):
        query = "SELECT * FROM users WHERE username = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            else:
                return None
            


class Property:
    def __init__(self, property_id, address, city, rent_amount, status="Available", owner_id=None):
        self.address= address
        self.rent_amount= rent_amount
        self.status= status
        self.owner_id= owner_id
        self.city= city
        self.property_id = property_id

        

    def add(self):
        try:
            with get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO properties (address, city, rent_amount, status, owner_id) 
                    VALUES (?, ?, ?, ?, ?)
                """, (self.address, self.city, self.rent_amount, self.status, self.owner_id))
        except sqlite3.Error as e:
            print("SQLite error:", e)
            
       
    
    @classmethod
    def get_all(cls):
        """Get all properties."""
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM properties")
            rows = cursor.fetchall()
            properties = []
            for row in rows:
                property = cls(*row)
                properties.append(property)
            return properties
    


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


    #will add methods like delete, update later
    def delete(self, property_id):
        with get_cursor as cursor:
            cursor.execute("DELETE FROM properties WHERE id = ?", (property_id, ))


    @classmethod
    def get_by_id(cls, property_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM properties WHERE property_id = ?", (property_id,))
            property_data = cursor.fetchone()
            if property_data:
                # Unpack the property data
                property_id, address, city, rent_amount, status, owner_id = property_data
                print(f"Property ID: {property_id}, Address: {address}, City: {city}, Rent Amount: {rent_amount}, Status: {status}, Owner ID: {owner_id}")
                return cls(property_id, address, city, rent_amount, status, owner_id)
            else:
                return None


    def update(cls, property_id, new_address=None, new_city=None, new_rent_amount=None, new_owner_id=None, new_status=None):
        property_to_update = cls.get_by_id(property_id)
        if property_to_update:
            with get_cursor() as cursor:
                update_fields = []
                update_values = []

                if new_address:
                    update_fields.append("address = ?")
                    update_values.append(new_address)
                if new_city:
                    update_fields.append("city = ?")
                    update_values.append(new_city)
                if new_rent_amount:
                    update_fields.append("rent_amount = ?")
                    update_values.append(new_rent_amount)
                if new_status:
                    update_fields.append("status = ?")
                    update_values.append(new_status)
                if new_owner_id:
                    update_fields.append("owner_id = ?")
                    update_values.append(new_owner_id)

                update_values.append(property_id)

                update_query = f"UPDATE properties SET {', '.join(update_fields)} WHERE property_id = ?"
                cursor.execute(update_query, update_values)
        else:
            raise ValueError(f"Property with ID {property_id} not found.")

 

class Owner:
    def __init__(self, name, email, phone, owner_id):
        self.name = name
        self.email = email
        self.phone = phone
        self.owner_id= owner_id

    @classmethod
    def add(self, name, email, phone):
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        if not self.validate_phone(phone):
            raise ValueError("Invalid phone number format")
        
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO owners (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))

    @classmethod
    def delete( self, owner_id):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM owners WHERE owner_id = ?", (owner_id,))

    @classmethod
    def get_by_id(cls, owner_id):
        """Get an owner by their ID."""
        with get_cursor() as cursor:
            query = "SELECT * FROM owners WHERE owner_id = ?"
            cursor.execute(query, (owner_id,))
            row = cursor.fetchone()
            if row:
                owner = cls(*row) 
                return owner
            else:
                return None
        
    @staticmethod
    def validate_email(email):
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        phone_pattern = r"^\d[-\d\s]*\d$"
        return re.match(phone_pattern, phone) is not None

    
    def update(self, owner_id, new_name=None, new_email=None, new_phone=None):
        with get_cursor() as cursor:
            update_fields = []
            update_values= [] 
            if new_name:
                update_fields.append("name = ?")
                update_values.append(new_name)
            if new_email:
                update_fields.append("email = ?")
                update_values.append(new_email)

            if new_phone:
                update_fields.append("phone = ?")
                update_values.append(new_phone)
            
            update_query = "UPDATE owners SET " + ", ".join(update_fields) + "WHERE id = ?"
            update_values.append(owner_id)
            cursor.execute(update_query, update_values)


    @classmethod
    def get_all(cls):
        """Get all owners."""
        with get_cursor() as cursor:
            query = "SELECT * FROM owners"
            cursor.execute(query)
            rows = cursor.fetchall()
            owners = []
            for row in rows:
                owner = cls(*row) 
                owners.append(owner)
            return owners
            


class Tenant:
    def __init__(self,tenant_id, name, contact_info, lease_start_date, lease_end_date, property_id):
        self.name= name
        self.contact_info= contact_info
        self.lease_start_date= lease_start_date
        self.lease_end_date= lease_end_date
        self.property_id= property_id
        self.tenant_id= tenant_id
    
    
    @staticmethod
    def validate_contact_info(contact_info):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^\d{10}$'  # Assuming a 10-digit phone number format
        if re.match(email_pattern, contact_info) or re.match(phone_pattern, contact_info):
            return True
        else:
            return False

    @staticmethod
    def validate_dates(lease_start_date, lease_end_date):
        try:
            start_date = datetime.strptime(lease_start_date, '%Y-%m-%d')
            end_date = datetime.strptime(lease_end_date, '%Y-%m-%d')
            
            # check if the start date is before the end date
            if start_date < end_date:
                return True
            else:
                return False
        except ValueError:
            #if there's an error parsing the date strings, return False
            return False

    def add(self):
      if not self.validate_contact_info(self.contact_info):
          raise ValueError("Invalid contact information")
      if not self.validate_dates(self.lease_start_date, self.lease_end_date):
          raise ValueError("Invalid lease dates")
      query = """
          INSERT INTO tenants ( name, contact_info, lease_start_date, lease_end_date, property_id)
          VALUES ( ?, ?, ?, ?, ?)
      """
      with get_cursor() as cursor:
          cursor.execute(query, (self.tenant_id, self.name, self.contact_info, self.lease_start_date,
                                 self.lease_end_date, self.property_id))
    @staticmethod
    def get_by_id(tenant_id):
        query = "SELECT * FROM tenants WHERE tenant_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (tenant_id,))
            return cursor.fetchone()

    @staticmethod
    def get_all():
        query = "SELECT * FROM tenants"
        with get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def update(self):
        if not self.validate_contact_info(self.contact_info):
            raise ValueError("Invalid contact information")

        if not self.validate_dates(self.lease_start_date, self.lease_end_date):
            raise ValueError("Invalid lease dates")
        query = """
            UPDATE tenants
            SET name = ?, contact_info = ?, lease_start_date = ?, lease_end_date = ?, property_id = ?
            WHERE tenant_id = ?
        """
        with get_cursor() as cursor:
            cursor.execute(query, (self.name, self.contact_info, self.lease_start_date,
                                   self.lease_end_date, self.property_id, self.tenant_id))

    @staticmethod
    def delete(tenant_id):
        query = "DELETE FROM tenants WHERE tenant_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (tenant_id,))





class RentPayment:
    def __init__ (self,payment_id, tenant_id, property_id, payment_date, amount):
        self.tenant_id = tenant_id
        self.property_id= property_id
        self.payment_date= payment_date
        self.amount= amount
        self.payment_id= payment_id

    @staticmethod
    def validate_amount(amount):
        #amount is a positive n.o or not
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def validate_payment_date(payment_date):
        date_format = '%Y-%m-%d'
        try:
            datetime.strptime(payment_date, date_format)
            return True
        except ValueError:
            return False
        
    def add(self):
        if not self.validate_amount(self.amount):
            raise ValueError("Invalid amount")
        if not self.validate_payment_date(self.payment_date):
            raise ValueError("Invalid payment date")
        query = """
            INSERT INTO rent_payments ( payment_id, tenant_id, property_id, payment_date, amount)
            VALUES ( ?, ?, ?, ?)
        """
        with get_cursor() as cursor:
            cursor.execute(query, (self.payment_id, self.tenant_id, self.property_id,
                                   self.payment_date, self.amount))
            


    def update(self):
       if not self.validate_amount(self.amount):
           raise ValueError("Invalid amount")
       if not self.validate_payment_date(self.payment_date):
           raise ValueError("Invalid payment date")
       query = """
           UPDATE rent_payments
           SET tenant_id = ?, property_id = ?, payment_date = ?, amount = ?
           WHERE payment_id = ?
       """
       with get_cursor() as cursor:
           cursor.execute(query, (self.tenant_id, self.property_id, self.payment_date,
                                  self.amount, self.payment_id))
           


    @staticmethod
    def get_by_id(payment_id):
        query = "SELECT * FROM rent_payments WHERE payment_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (payment_id,))
            return cursor.fetchone()

    @staticmethod
    def get_all():
        query = "SELECT * FROM rent_payments"
        with get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
        
   # def add_rent_payment(property_id, tenant_id, payment_amount):
        #payment_date =  datetime.now().strftime('%Y-%m-%d')
        #with get_cursor() as cursor:
        #    cursor.execute("INSERT INTO rent_payments(property_id, tenant_id, payment_amount, payment_date) VALUES(?, ?, ?, ?)",
         #                  (property_id, tenant_id, payment_amount, payment_date))


    
    def get_rent_payments_for_property(property_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM rent_payments WHERE property_id = ?", (property_id,))
            payments= cursor.fetchall()
            for payment in payments:
                print(payment)

    def get_rent_payments_for_tenant(tenant_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM rent_payments WHERE tenant_id= ?", (tenant_id,))
            payments = cursor.fetchall()
            for payment in payments:
                print(payment)



    @staticmethod
    def delete(payment_id):
        query = "DELETE FROM rent_payments WHERE payment_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (payment_id,))



class MaintenanceRequest:
    def __init__ (self, request_id, request_description, tenant_id, property_id, request_date, request_status="open",):
        self.request_description = request_description
        self.tenant_id= tenant_id
        self.property_id= property_id
        self.request_status= request_status
        self.request_date= request_date
        self.request_id= request_id

    def validate_request_status(request_status):
        allowed_statuses = ["open", "in progress", "completed"]
        return request_status.lower() in allowed_statuses


    def add(self):
        if not self.validate_request_status(self.request_status):
            raise ValueError("Invalid request status")
        query = """
            INSERT INTO maintenance_requests (request_id, request_description, tenant_id, property_id, request_date, request_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with get_cursor() as cursor:
            cursor.execute(query, (self.request_id, self.request_description, self.tenant_id,
                                   self.property_id, self.request_date, self.request_status))

            
    def update(self):
        if not self.validate_request_status(self.request_status):
            raise ValueError("Invalid request status")
        query = """
            UPDATE maintenance_requests
            SET request_description = ?, tenant_id = ?, property_id = ?, request_date = ?, request_status = ?
            WHERE request_id = ?
        """
        with get_cursor() as cursor:
            cursor.execute(query, (self.request_description, self.tenant_id, self.property_id,
                                   self.request_date, self.request_status, self.request_id))

    @staticmethod
    def delete(request_id):
        query = "DELETE FROM maintenance_requests WHERE request_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (request_id,))

    @staticmethod
    def get_by_id(request_id):
        query = "SELECT * FROM maintenance_requests WHERE request_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (request_id,))
            return cursor.fetchone()

    @staticmethod
    def get_all():
        query = "SELECT * FROM maintenance_requests"
        with get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()




class Expense:
    def __init__ (self, expense_id, description, amount, date, property_id):
        self.description = description
        self.amount= amount
        self.date= date
        self.property_id= property_id
        self.expense_id= expense_id

    @staticmethod
    def validate_amount(amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        return True

    
    @staticmethod
    def validate_date(date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add(self):
        if not self.validate_amount(self.amount):
            raise ValueError("Invalid amount")

        if not self.validate_date(self.date):
            raise ValueError("Invalid date format")
        query = """
            INSERT INTO expenses (expense_id, description, amount, date, property_id)
            VALUES (?, ?, ?, ?, ?)
        """
        with get_cursor() as cursor:
            cursor.execute(query, (self.expense_id, self.description, self.amount, self.date, self.property_id))

    @staticmethod
    def get_by_id(expense_id):
        query = "SELECT * FROM expenses WHERE expense_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (expense_id,))
            return cursor.fetchone()

    @staticmethod
    def get_all():
        query = "SELECT * FROM expenses"
        with get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def update(self):
        query = """
            UPDATE expenses
            SET description = ?, amount = ?, date = ?, property_id = ?
            WHERE expense_id = ?
        """
        with get_cursor() as cursor:
            cursor.execute(query, (self.description, self.amount, self.date, self.property_id, self.expense_id))

    @staticmethod
    def delete(expense_id):
        query = "DELETE FROM expenses WHERE expense_id = ?"
        with get_cursor() as cursor:
            cursor.execute(query, (expense_id,))






class Document:
    def __init__ (self, document_id, name, file_path, property_id, access_level):
        self.name= name
        self.file_path= file_path
        self.property_id = property_id
        self.access_level= access_level
        self.document_id = document_id

    

    #def save(self):
      #  with get_cursor() as cursor:
   #         cursor.execute("""
#INSERT INTO documents (name, file_path, property_id, access_level) VALUES (?, ?, ?, ?)
#""", (self.name, self.file_path, self.property_id, self.access_level))
            
    def save(self):
        connection = sqlite3.connect('property_management.db')
        cursor = connection.cursor()

        query = """
        INSERT INTO documents (name, file_path, property_id, access_level) 
        VALUES (?, ?, ?, ?)
        """

        cursor.execute(query, (self.name, self.file_path, self.property_id, self.access_level))
        connection.commit()
        connection.close()
    
    @classmethod
    def get_all(cls):
        documents = []
        with sqlite3.connect('property_management.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents")
            rows = cursor.fetchall()
            for row in rows:
                document = cls(*row)  
                documents.append(document)
        #return documents
        for document in documents:
            print(document.document_id, document.name, document.file_path, document.property_id, document.access_level)

    
    @staticmethod
    def get_by_id(document_id):
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM documents WHERE id= ?", (document_id,))
            return cursor.fetchone()
        

    def delete(self, document_id):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    

    def update(self, document_id, new_name= None, new_file_path=None, new_property_id = None, new_access_level = None):
        with get_cursor() as cursor:
            update_fields = []
            update_values = []
            if new_name:
                update_fields.append("name = ?")
                update_values.append(new_name)
            if new_file_path:
                update_fields.append("file_path = ?")
                update_values.append(new_file_path)
            if new_property_id:
                update_fields.append("property_id = ?")
                update_values.append(new_property_id)
            if new_access_level:
                update_fields.append("access_level = ?")
                update_values.append(new_access_level)


            update_query = "UPDATE documents SET " + ", ".join(update_fields) + "WHERE id = ?"
            update_values.append(document_id)
            cursor.execute(update_query, update_values)

