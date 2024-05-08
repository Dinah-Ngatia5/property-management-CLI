import click
from models import Expense, Tenant, Property, User, MaintenanceRequest

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
    pass 

@main.command()
def login():
    pass

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
    rent_amount= click.prompt("Enter rent_amount", type= float)
    owner_id= click.prompt("Enter owner ID", type=int)
    status = click.prompt("Enter property status", type=str)

    new_property= Property(address, city, rent_amount, owner_id, status)
    new_property.save()
    click.echo("Property added successfully.")

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
    #Logic
    click.echo("Here's a full list of all properties.") 





@cli.command()
@click.option("--description", prompt="Enter expense description", help="Description of the expense")
@click.option("--amount", prompt="Enter expense amount", help="Amount of the expense")
@click.option("--property_id", prompt="Enter property ID", help="ID of the property associated with the expense")
def add_expense(description, amount, property_id):
    """Add a new expense"""
    expense= Expense(description, amount, property_id)
    expense.save()
    click.echo("Expense added successfully!")

@cli.command()
@click.argument("property_id", type=int)
def get_expenses(property_id):
    """Get all expenses for a property"""
    expenses= Expense.get_expenses_for_property(property_id)
    if expenses:
        click.echo("Expenses for property ID {}:".format(property_id))
        for expense in expenses:
            click.echo("- Description: {}".format(expenses[1]))
            click.echo('  Amount: {}'.format(expense[2]))
        
    else:
        click.echo("No expense found for property ID {}.".format(property_id))

@cli.command()
def add_tenant():
    """Add a new tenant"""
    pass



@cli.command()
def add_user():
    """Add a new user"""
    pass


if __name__ == "__main__":
    cli()