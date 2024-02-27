#!/usr/bin/env python3
"""Get expiring items.
Description:
            This module deals with the method that checks if items
            in the stock have expired.

            It sends an email notification alerting the users of the expiring 
            items details.

            This script will be made executable and automated using a cron job
            to run daily so that we can always check the status of our 
            items in the database.
"""
import sys
sys.path.append('/home/rugema3/stock_management_system/application')
from models.item_manager import ItemManager
from decouple import config
import os
from models.send_email import send_email
from models.database_manager import Database

db_config = {
            'user': config('DB_USER'),
            'password': config('DB_PASSWORD'),
            'host': config('DB_HOST'),
            'database': config('DB_NAME'),
            }

# Create a item_manager instance.

item_manager = ItemManager(db_config)
db = Database(db_config)

def send_reminders():
    """Send reminders.
    Description:
                This function checks if items are expiring
                soon, and then sends a reminder to the users.
    """
    # Retrrive expring items.
    expiring = item_manager.get_expiring_soon('it')

    # Retrieve users from the database.
    users = db.get_all_users('it')

    # Iterate over users to send email to each of them. 
    for user in users:
        user_email = user['email']
        print("email: ", user_email)
        user_name = user['name']
        print("user_name: ", user_name)
        # Compose email message
        subject = "Expiring Items Notification"
        message = f"""<html>
        <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        h2 {{
            color: #333;
        }}
        .details {{
            margin-bottom: 20px;
        }}
        .details table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .details th, .details td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        .details th {{
            background-color: #f2f2f2;
        }}
        .logo {{
        margin-bottom: 20px;
        }}
        </style>
        </head>
        <body>
        <div class="container">
         <h2>Hi {user_name},</h2>
        <p>We wanted to inform you about the following expiring items:</p>
        <div class="details">
        <table>
            <tr>
                <th>Item Name</th>
                <th>Price</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Expiration Date</th>
            </tr>
        """

        # Iterate over each item in the list
        for item in expiring:
            message += f"""
                <tr>
                <td>{item['item_name']}</td>
                <td>{item['price']}</td>
                <td>{item['category']}</td>
                <td>{item['quantity']}</td>
                <td>{item['expiration_date']}</td>
                </tr>
            """
        message += """
            </table>
            </div>
            <p>Please take necessary action to manage these expiring items.</p>
            <p>Thank you.</p>
            </div>
        </body>
        </html>
        """
        company_email = "info@remmittance.com"

        # Retrieve email api_key.
        email_api_key = os.getenv('email_api')
        
        # Check if there are items expiring. Don's send email when empty.
        if len(expiring) > 0:
            # Sending email
            send_email(email_api_key, company_email, user_email, subject, message)

if __name__ == '__main__':
    print(send_reminders())
