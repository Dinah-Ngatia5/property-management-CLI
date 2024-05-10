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
    """python cli.py main register"""
    username = input("Enter username: ")
    password = input("Enter password: ")
   
    User.create(username=username, password=password)
    print("User registered successfully!")
 

@main.command()
def login():
    """python cli.py main login"""
    username = input("Enter username: ")
    password = input("Enter password: ")
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
    click.echo(f"Property updated with ID {property_id} successfully.")


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
@click.option('--name', prompt='Enter tenant name', required=True)
@click.option('--contact_info', prompt='Enter contact information', required=True)
@click.option('--lease_start_date', prompt='Enter lease start date (YYYY-MM-DD)', required=True)
@click.option('--lease_end_date', prompt='Enter lease end date (YYYY-MM-DD)', required=True)
@click.option('--property_id', prompt='Enter property ID', type=int, required=True)
def add(name, contact_info, lease_start_date, lease_end_date, property_id):
    """Add a new tenant"""
    new_tenant = Tenant(name=name, contact_info=contact_info, lease_start_date=lease_start_date,
                        lease_end_date=lease_end_date, property_id=property_id)
    try:
        new_tenant.add()
        click.echo("Tenant added successfully.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")


@tenant.command()
@click.option('--tenant_id', prompt='Enter the tenant ID to delete', type=int, required=True)
def delete(tenant_id):
    "Delete a tenant"
    try:
        Tenant.delete(tenant_id)
        click.echo("Tenant deleted successfully.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")


@tenant.command()
@click.argument('tenant_id', type=int)
@click.option('--name', prompt='Enter new tenant name', required=True)
@click.option('--contact_info', prompt='Enter new contact information', required=True)
@click.option('--lease_start_date', prompt='Enter new lease start date (YYYY-MM-DD)', required=True)
@click.option('--lease_end_date', prompt='Enter new lease end date (YYYY-MM-DD)', required=True)
@click.option('--property_id', prompt='Enter new property ID', type=int, required=True)
def update(tenant_id, name, contact_info, lease_start_date, lease_end_date, property_id):
    """Update a tenant"""
    updated_tenant = Tenant(tenant_id=tenant_id, name=name, contact_info=contact_info,
                            lease_start_date=lease_start_date, lease_end_date=lease_end_date,
                            property_id=property_id)
    try:
        updated_tenant.update()
        click.echo(f"Tenant with ID {tenant_id} updated successfully.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")


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

@tenant.command()
@click.option('--tenant_id', prompt='Enter the tenant ID', type=int, required=True)
def find_by_id(tenant_id):
    """find by id"""
    tenant_data = Tenant.get_by_id(tenant_id)
    if tenant_data:
        click.echo("Tenant found:")
        click.echo(tenant_data)
    else:
        click.echo("Tenant not found.")


@tenant.command()
def list_tenants():
    "list of tenants"
    all_tenants = Tenant.get_all()
    if all_tenants:
        click.echo("Here's a list of all tenants:")
        for tenant in all_tenants:
            click.echo(tenant)
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
    click.echo("Enter rent payment details:")
    payment_id=click.prompt("Enter payment ID please", type=int)
    tenant_id= click.prompt("Enter tenant ID", type=int)
    property_id= click.prompt("Enter property ID", type=int)
    payment_date= click.prompt("Enter payment date (YYYY-MM-DD)", type=str)
    amount = click.prompt("Enter payment amount", type=float)

    new_payment = RentPayment(payment_id=payment_id, tenant_id=tenant_id, property_id=property_id, payment_date=payment_date, amount=amount)

    new_payment.add()
    click.echo("Rent payment added successfully.")


@rent_payment.command()
@click.argument("payment_id", type=int)
def delete(payment_id):
    """Delete a rent payment"""
    payment_id = click.prompt("Enter the payment ID to delete", type=int)
    try:
        RentPayment.delete(payment_id)
        click.echo(f"Rent payment with ID {payment_id} has been deleted.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")


@rent_payment.command()
@click.option('--payment_id', prompt='Enter payment ID', type=int, help='The ID of the rent payment to update')
@click.option('--tenant_id', prompt='Enter tenant ID', type=int, help='The ID of the tenant')
@click.option('--property_id', prompt='Enter property ID', type=int, help='The ID of the property')
@click.option('--payment_date', prompt='Enter payment date', help='The date of the rent payment (YYYY-MM-DD)')
@click.option('--amount', prompt='Enter payment amount', type=float, help='The amount of the rent payment')
def update(payment_id, tenant_id, property_id, payment_date, amount):
    """Update a certain rent payment"""
    rent_payment = RentPayment(payment_id, tenant_id, property_id, payment_date, amount)
    try:
        rent_payment.update()
        click.echo("Rent payment updated successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")


@rent_payment.command()
@click.option('--payment_id', prompt='Enter payment ID', type=int, help='The ID of the rent payment to find')
def find_by_id(payment_id):
    """Find a rent payment by its ID"""
    try:
        rent_payment = RentPayment.get_by_id(payment_id)
        if rent_payment:
            click.echo("Rent payment found:")
            click.echo(rent_payment)
        else:
            click.echo("Rent payment not found.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")



@rent_payment.command()
def list_payments():
    """List all rent payments"""
    try:
        rent_payments = RentPayment.get_all()
        if rent_payments:
            click.echo("Rent payments:")
            for payment in rent_payments:
                click.echo(payment)
        else:
            click.echo("No rent payments found.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")



# Maintenance request operations
@cli.group()
def maintenance_request():
    """Manage maintenance requests"""
    pass

@maintenance_request.command()
@click.option('--request_description', prompt='Enter the request description')
@click.option('--tenant_id', prompt='Enter the tenant ID', type=int)
@click.option('--property_id', prompt='Enter the property ID', type=int)
@click.option('--request_date', prompt='Enter the request date')
@click.option('--request_status', prompt='Enter the request status', default='open')
def add( request_description, tenant_id, property_id, request_date, request_status):
    """Add a new maintenance request"""
    try:
        request = MaintenanceRequest(request_description, tenant_id, property_id, request_date, request_status)
        request.add()
        click.echo("Maintenance request has been sent successfully.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")


@maintenance_request.command()
@click.option('--request_id', prompt='Enter the request ID to delete', type=int)
def delete(request_id):
    try:
        MaintenanceRequest.delete(request_id)
        click.echo(f"Maintenance request with ID {request_id} has been deleted.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")

@maintenance_request.command()
@click.option('--request_id', prompt='Enter the request ID to retrieve', type=int)
def find_by_id(request_id):
    try:
        request = MaintenanceRequest.get_by_id(request_id)
        if request:
            click.echo(f"Request ID: {request.request_id}, Description: {request.request_description}, Tenant ID: {request.tenant_id}, Property ID: {request.property_id}, Date: {request.request_date}, Status: {request.request_status}")
        else:
            click.echo("Maintenance request not found.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")


@maintenance_request.command()
@click.option('--request_id', prompt='Enter the request ID to update', type=int)
@click.option('--request_description', prompt='Enter the new request description')
@click.option('--tenant_id', prompt='Enter the new tenant ID', type=int)
@click.option('--property_id', prompt='Enter the new property ID', type=int)
@click.option('--request_date', prompt='Enter the new request date')
@click.option('--request_status', prompt='Enter the new request status', default='open')
def update(request_id, request_description, tenant_id, property_id, request_date, request_status):
    """Update a maintenance request"""
    try:
        request = MaintenanceRequest.get_by_id(request_id)
        if request:
            request.request_description = request_description
            request.tenant_id = tenant_id
            request.property_id = property_id
            request.request_date = request_date
            request.request_status = request_status
            request.update()
            click.echo(f"Maintenance request of ID{request_id} updated successfully.")
        else:
            click.echo("Maintenance request not found.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")

@maintenance_request.command()
def list_or_requests():
    try:
        requests = MaintenanceRequest.get_all()
        if requests:
            for request in requests:
                click.echo(f"Request ID: {request.request_id}, Description: {request.request_description}, Tenant ID: {request.tenant_id}, Property ID: {request.property_id}, Date: {request.request_date}, Status: {request.request_status}")
        else:
            click.echo("No maintenance requests found.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")



#Expense Operation 
@cli.group
def expense():
    """Manage expenses"""
    pass

@expense.command()
def add_expense():
    """Add a new expense."""
    expense_id = click.prompt("Enter expense ID", type=int)
    description = click.prompt("Enter expense description")
    amount = click.prompt("Enter expense amount", type=float)
    date = click.prompt("Enter expense date (YYYY-MM-DD)")
    property_id = click.prompt("Enter property ID", type=int)

    expense = Expense(expense_id, description, amount, date, property_id)
    try:
        expense.add()
        click.echo("Expense added successfully.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")

@expense.command()
def update_expense():
    """Update an existing expense."""
    expense_id = click.prompt("Enter expense ID to update", type=int)
    # Retrieve existing expense
    existing_expense = Expense.get_by_id(expense_id)
    if existing_expense:
        # Display current expense information
        click.echo(f"Current Expense Details:\n{existing_expense}")
        # Prompt for updated information
        description = click.prompt("Enter new description (press Enter to keep existing)", default=existing_expense.description)
        amount = click.prompt("Enter new amount (press Enter to keep existing)", default=existing_expense.amount, type=float)
        date = click.prompt("Enter new date (press Enter to keep existing)", default=existing_expense.date)
        property_id = click.prompt("Enter new property ID (press Enter to keep existing)", default=existing_expense.property_id, type=int)

        # Update expense with new information
        updated_expense = Expense(expense_id, description, amount, date, property_id)
        try:
            updated_expense.update()
            click.echo("Expense updated successfully.")
        except ValueError as e:
            click.echo(f"An error occurred: {str(e)}")
    else:
        click.echo(f"Expense with ID {expense_id} not found.")

@expense.command()
def delete_expense():
    """Delete an expense."""
    expense_id = click.prompt("Enter expense ID to delete", type=int)
    try:
        Expense.delete(expense_id)
        click.echo(f"Expense with ID {expense_id} has been deleted.")
    except ValueError as e:
        click.echo(f"An error occurred: {str(e)}")

@expense.command()
def find_expense_by_id():
    """Find an expense by its ID."""
    expense_id = click.prompt("Enter the expense ID", type=int)
    expense = Expense.get_by_id(expense_id)
    if expense:
        click.echo(f"Expense found:\n{expense}")
    else:
        click.echo("Expense not found.")

@expense.command()
def list_all_expenses():
    """List of all expenses."""
    expenses = Expense.get_all()
    if expenses:
        click.echo("Here's a list of all the expenses:")
        for expense in expenses:
            click.echo(expense)
    else:
        click.echo("No expenses found.")







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







if __name__ == "__main__":
    cli()