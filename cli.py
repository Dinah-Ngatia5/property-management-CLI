import click
from models import Expense, Tenant, Property, User, MaintenanceRequest

@click.group()
def cli():
    """
    Property Management CLI
    """

@cli.command()
@click.option("--username", prompt= "Enter username", help="Your username")
@click.option("--password", prompt="Enter password", help="Your password")
def login(username, password):
    cursor.execute



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
@click.argument("property_id")
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
def add_property():
    """Add a new property"""
    pass

@cli.command()
def add_user():
    """Add a new user"""
    pass


if __name__ == "__main__":
    cli()