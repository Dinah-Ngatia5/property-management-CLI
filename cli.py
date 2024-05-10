import click
from models import Expense, Owner, Tenant, Property, User, MaintenanceRequest, RentPayment, Document
import argparse

@click.group()
def cli():
    """
    Property Management System CLI
    """
    pass 

@cli.group()
def main():
    """Register or Login"""
    pass


@main.command()
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Create a new user record
    User.create(username=username, password=password)
    print("User registered successfully!")
 

@main.command()
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Check if user exists and password matches
    user = User.get_or_none(username=username)
    if user and user.password == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")


#adding commands to main group
main.add_command(register)
main.add_command(login)

#Property operations
@cli.group()
def property():
    """Manage properties"""
    pass

@property.command()
def add():
    """Add a new property"""
    address= click.prompt("Enter property address", type=str)
    city= click.prompt("Enter city", type=str)
    rent_amount= click.prompt("Enter rent_amount", type= int)
    status = click.prompt("Enter property status", type=str)
    owner_id= click.prompt("Enter owner ID", type=int)
   

    new_property= Property(address, city, rent_amount, status, owner_id)
    new_property.add()
    click.echo(f"Property added successfully: Address: {new_property.address}, City: {new_property.city}, Rent Amount: {new_property.rent_amount}, Status: {new_property.status}, Owner ID: {new_property.owner_id}")
    

@property.command()
@click.argument("property_id", type=int)
def delete(property_id):
    """Delete a property"""
    Property.delete(property_id)
    click.echo(f"Deleted property with ID {property_id}")

@property.command()
@click.argument("property_id", type=int)
def view_property(property_id):
    """View details of a property"""
    #logic for viewing property details
    click.echo(f"Viewing details of property with ID {property_id}")

@property.command()
def list_properties():
    """List all properties""" 
    properties = Property.get_all()
    if properties:
        click.echo("Here's a full list of all properties:")
        for prop in properties:
            click.echo(f"Property ID: {prop.property_id}, Address: {prop.address}, City: {prop.city}, Rent Amount: {prop.rent_amount}, Status: {prop.status}, Owner ID: {prop.owner_id}")
    else:
        click.echo("No properties found.")

@property.command()
def find_by_id():
    """Find a property by its ID."""
    property_id = click.prompt("Enter the property ID", type=int)
    property_data = Property.get_by_id(property_id)
    if property_data:
        click.echo("Property found:")
        click.echo(property_data)
    else:
        click.echo("Property not found.")

@property.command()
@click.argument('property_id', type=int)
def update(property_id):
    """Update a property"""
    new_address = click.prompt("Enter new address (leave blank to keep current)", default="", type=str)
    new_city = click.prompt("Enter new city (leave blank to keep current)", default="", type=str)
    new_rent_amount = click.prompt("Enter new price (leave blank to keep current)", default=0.0, type=float)
    new_owner_id = click.prompt("Enter new owner ID (leave blank to keep current)", default=0, type=int)
    new_status = click.prompt("Enter new property status (leave blank to keep current)", default="", type=str)

    Property.update(property_id, new_address, new_city, new_rent_amount, new_owner_id, new_status)
    click.echo("Property updated successfully.")


#Owner operations
@cli.group()
def owner():
    """Manage owners"""
    pass

@owner.command()
def add():
    """Add a new owner"""
    name = click.prompt("Enter owner name", type=str)
    email = click.prompt("Enter email", type=str)
    phone = click.prompt("Enter phone number", type=str)

    new_owner = Owner(owner_id=None, name=name, email=email, phone=phone)
    new_owner.add(name, email, phone)

    click.echo("Owner added successfully.")


@owner.command()
@click.argument("owner_id", type=int)
def update(owner_id):
    """Update an owner"""
    new_name= click.prompt("Enter new name (leave blank to keep current)", default="")
    new_email= click.prompt("Enter new email (leave blank to keep current)", default="")
    new_phone=click.prompt("Enter new phone number (leave blank to keep current)", default="")

    Owner.update(owner_id, new_name, new_email, new_phone)
    click.echo("Owner updated successfully.")


@owner.command()
@click.option("--owner-id", prompt="Enter the owner ID to delete", type=int, help="The ID of the owner to delete")
def delete(owner_id):
    """Delete an owner by ID."""
    try:
        # Call the delete method of the Owner class here passing the owner_id
        Owner.delete(owner_id)
        click.echo(f"Owner with ID {owner_id} deleted successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")


@owner.command()
def list_owners():
    """List all owners."""
    owners = Owner.get_all()
    if owners:
        click.echo("Here's a list of all owners:")
        for owner in owners:
            click.echo(f"Owner ID: {owner.owner_id}, Name: {owner.name}, Email: {owner.email}, Phone: {owner.phone}")
    else:
        click.echo("No owners found.")

@owner.command()
def find_by_id():
    """Find an owner by their ID."""
    owner_id = click.prompt("Enter the owner ID", type=int)
    owner = Owner.get_by_id(owner_id)
    if owner:
        click.echo("Owner found:")
        click.echo(f"Owner ID: {owner.owner_id}, Name: {owner.name}, Email: {owner.email}, Phone: {owner.phone}")
    else:
        click.echo("Owner not found.")





#Tenant operations
@cli.group()
def tenant():
    """Manage tenants"""
    pass

@tenant.command()
def add():
    """Add a new tenant"""
    name=click.prompt("Enter tenant name", type=str)
    contact_info= click.prompt("Enter contact information", type=str)
    lease_start_date= click.prompt("Enter lease start date (YYYY-MM-DD)", type=str)
    lease_end_date = click.prompt("Enter lease end date (YYYY-MM-DD)", type=str)
    property_id = click.prompt("Enter property ID", type=int)


    new_tenant= Tenant(name, contact_info, lease_start_date, lease_end_date, property_id)
    new_tenant.save()
    click.echo("Tenant added successfully.")


@tenant.command()
@click.argument("tenant_id", type=int)
def delete(tenant_id):
    """Delete a tenant"""
    Tenant.delete(tenant_id)
    click.echo(f"Tenant with ID{tenant_id} has been deleted.")


@tenant.command()
@click.argument("tenant_id", type=int)
def update(tenant_id):
    """Update a tenant"""
    new_name=click.prompt("Enter new name (leave blank to keep current)", type="", default="")
    new_contact_info= click.prompt("Enter new contact information (leave blank to keep default)", type="", default="")
    new_lease_start_date= click.prompt("Enter new lease start date (YYYY-MM-DD) **Leave blank to keep current**", type= "", default="")
    new_lease_end_date= click.prompt("Enter new lease end date (YYYY-MM-DD) **Leave blank to keep current**", type="", default="")
    new_property_id= click.prompt("Enter new property ID (Leave blank to keep current)", type=int, default=0)

    Tenant.update(tenant_id, new_name, new_contact_info, new_lease_start_date, new_lease_end_date, new_property_id)
    click.echo("Tenant updated successfully.")


@tenant.command()
def list():
    """List of all tenants"""
    tenants= Tenant.get_all()
    if tenants:
        click.echo("Tenants")
        for tenant in tenants:
            click.echo(f"ID: {tenant[0]}, \nName: {tenant[1]}, \nContact: {tenant[2]}, \nLease Start: {tenant[3]}, \nLease_end_date: {tenant[4]}, \nProperty ID: {tenant[5]}")
        else:
            click.echo("No tenants found.")




#Rent payment operations
@cli.group()
def rent_payment():
    """Manage rent payments"""
    pass


@rent_payment.command()
def add():
    """Add a new rent payment"""
    tenant_id= click.prompt("Enter tenant ID", type=int)
    property_id= click.prompt("Enter property ID", type=int)
    payment_date= click.prompt("Enter payment date (YYYY-MM-DD)", type=str)
    amount = click.prompt("Enter payment amount", type=float)

    new_payment= RentPayment(tenant_id, property_id, payment_date, amount)
    new_payment.save()
    click.echo("Rent payment added successfully.")


@rent_payment.command()
@click.argument("payment_id", type=int)
def delete(payment_id):
    """Delete a rent payment"""
    RentPayment.delete(payment_id)
    click.echo(f"Rent payment with ID{payment_id} has been deleted.")

@rent_payment.command()
@click.argument("payment_id", type=int)
def update(payment_id):
    """Update a certain rent payment"""
    new_tenant_id= click.prompt("Enter new tenant ID **\nLeave blank to keep current\n**", default=0)
    new_property_id= click.prompt("Enter new property ID \n(leave blank to keep current)", default=0)
    new_payment_date= click.prompt("Enter new payment date (YYYY-MM-DD)\n**Leave blank to keep current**", default="")
    new_amount= click.prompt("Enter new payment amount (Leave blank to keep current)", default=0.0)

    RentPayment.update(payment_id, new_tenant_id, new_property_id, new_payment_date, new_amount)
    click.echo(f"Rent payment with ID{payment_id} successfully updated!!")


# Maintenance request operations
@cli.group()
def maintenance_request():
    """Manage maintenance requests"""
    pass

@maintenance_request.command()
def add():
    """Add a new maintenance request"""
    description = click.prompt("Enter request description", type=str)
    tenant_id = click.prompt("Enter tenant ID", type=int)
    property_id= click.prompt("Enter property ID", type=int)
    request_status = click.prompt("Enter request status", type=str, default="open")

    new_request = MaintenanceRequest(description, tenant_id, property_id, request_status)
    new_request.save()
    click.echo("Maintenance request added.")


@maintenance_request.command()
@click.argument("request_id", type=int)
def delete(request_id):
    """Delete a maintenance request"""
    MaintenanceRequest.delete(request_id)
    click.echo(f"Maintenance request of ID{request_id} has been deleted.")


@maintenance_request.command()
@click.argument("request_id", type=int)
def update(request_id):
    """Update a maintenance request"""
    new_description= click.prompt("Enter a new description ::Leave blank to keep current", default="")
    new_tenant_id= click.prompt("Enter new tenant ID **Leave blank to keep current**", default=0)
    new_property_id= click.prompt("Enter new property ID  **Leave blank to keep current**", default=0)
    new_request_status= click.prompt("Enter new request_status **Leave blank to keep default**", type=str, default="open")
    
    MaintenanceRequest.update(request_id, new_description, new_tenant_id, new_property_id, new_request_status)
    click.echo(f"Maintenance request of ID{request_id} successfully updated.")




#Expense Operation 
@cli.group
def expense():
    """Manage expenses"""
    pass

@expense.command()
def add():
    """Add a new expense"""
    description= click.prompt("Enter a description", type=str)
    amount= click.prompt("Enter an amount", type=float)
    date = click.prompt("Enter today's date(YYYY-MM-DD)", type=str )
    property_id= click.prompt("Enter property ID ", type= int)

    new_expense= Expense(description, amount, date, property_id)
    new_expense.save()
    click.echo("New expense added.")

@expense.command()
@click.argument("expense_id", type=int)
def update(expense_id):
    """Update an expense"""
    new_description= click.prompt("Enter a new description **Leave blank to keep current**", type=str, default= "")
    new_amount= click.prompt("Enter a new amount (leave blank to keep current)", type=float, default=0.0)
    new_date= click.prompt("Enter new date(YYYY-MM-DD)", type=str, default="")
    new_property_id= click.prompt("Enter new property ID **Leave blank to keep current**", type=int, default=0)

    Expense.update(expense_id, new_description, new_amount, new_date, new_property_id)
    click.echo(f"Expense of ID{expense_id} successfully updated")


@expense.command()
@click.argument("expense_id", type=int)
def delete(expense_id):
    """Delete an expense Woohoo!!"""
    Expense.delete(expense_id)
    click.echo(f"Expense of ID{expense_id} has been deleted, you can now rest easy!")



# Document Operations
@cli.group
def document():
    """Manage docs"""
    pass

@document.command()
def add():
    """Add a doc"""
    name= click.prompt("Please enter a new doc name", type=str)
    file_path= click.prompt("Enter the file_path for this particular doc", type= str)
    property_id= click.prompt("Enter a property ID", type=int)
    access_level= click.prompt("Enter the access level for this particular doc", type=str)


    new_document = Document(name, file_path, property_id, access_level)

    new_document.save()
    click.echo("#New doc added!!")


@document.command()
@click.argument("document_id", type=int)
def update(document_id):
    """Update a certain doc"""
    new_name= click.prompt("Enter new doc name **Leave blank to leave it as it was**", type=str, default="")
    new_file_path =click.prompt("Enter a new file path for this doc (leave blank to keep current)", type=str, default="")
    new_property_id= click.prompt("Enter new Property ID (leave blank to keep current)", type=int, default=0)
    new_access_level = click.prompt("Enter a new access level **Leave blank to keep current", type=str, default= "")


    Document.update(document_id, new_name, new_file_path, new_property_id, new_access_level)
    click.echo(f"Doc with ID{document_id} has been updated ya'll!")


@document.command()
def delete():
    document_id = click.prompt("Enter the document ID to delete", type=int)
    """Delete a doc mehn!"""
    Document.delete(document_id)
    click.echo(f"Doc with ID{document_id} is out!!")


@document.command()
def list():
    """List all docs"""
    Document.get_all()
    click.echo("Here a list of documents")




@cli.command()
def add_user():
    """Add a new user"""
    pass


if __name__ == "__main__":
    cli()