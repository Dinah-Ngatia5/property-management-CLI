
import time 
import smtplib
import re
import locale
import time
import smtplib
import sqlite3
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart



def validate_email(email):
    """
    Validate the format of an email address
    """
    #email validation regular expression
    pattern= r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def format_currency(amount):
    """
    Format a numeric amount as currency
    """
    #setting locale to user's default
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    #format amount as currency
    formatted_amount = locale.currency(amount, grouping=True)
    return formatted_amount

def generate_invoice(property_id, tenant_id, amount):
    """
    Generate an invoice for rent payment
    """
    #constructing invoice data
    invoice = {
        "property_id": property_id,
        "tenant_id": tenant_id,
        "amount":format_currency(amount),
        "due_date": "2024-08-04", #an example of a due date

    }
    return invoice

#usage
email= "dinahngatia86@gmail.com"
if validate_email(email):
    print("Email is valid")
else:
    print("Email is invalid")

amount= 1000
formatted_amount = format_currency(amount)
print("Formatted amount:", formatted_amount)

invoice_data= generate_invoice(1, 1, 1200)
print("Generated invoice:", invoice_data)

#more utility functions, incase i wanna add more


#PS i don't think i will be using any of the code i've written above, just learning some new stuff, ** Extra extra Terrified of bugs haha***
