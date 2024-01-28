#!/usr/bin/env python3

from application.models.user_manager import UserManager
from flask import Flask, render_template, request, redirect, session, url_for, flash
from application.models.stock_manager import StockManager
from application.models.stock_item import StockItem
from application.models.database_manager import Database
from application.models.user_handler import UserHandler
from application.models.send_email import send_email
from application.helpers.random_password import random_password
from decouple import config  
import bcrypt
from application.models.user import User 
from flask_session import Session
from decorators.authentication_decorators import login_required
from decorators.admin_decorators import admin_required
from decorators.approver_decorators import approver_required
from decorators.roles import any_role_required
from flask_login import current_user
from flask_mail import Mail, Message
import os
from application.routes.edit_pending_items import edit_pending_items_route
#from application.routes.backups import backup_route
from application.routes.add_item_category import add_item_category_route
from application.routes.add_user_department import add_user_department_route
from application.routes.add_user_role import add_user_role_route

import matplotlib.pyplot as plt
import io
import base64
import subprocess


app = Flask(__name__, template_folder='application/templates',  static_folder='application/static')

stock_manager = StockManager()
#user_manager = UserManager()

# Retrieve database configuration from environment variables
db_config = {
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'database': config('DB_NAME'),
}

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  
Session(app)

# Register different Blueprints
app.register_blueprint(add_item_category_route)
app.register_blueprint(edit_pending_items_route)
app.register_blueprint(add_user_department_route)
app.register_blueprint(add_user_role_route)
#app.register_blueprint(backup_route, url_prefix='/backup')

# Create a Database instance
db = Database(db_config)
user_manager = UserManager(db_config)
user_handler = UserHandler(db_config)

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
@login_required
def home():
    # Retrieve the user's info from the session
    user_email = session.get('user_email')
    user_department = session.get('department', '')
    user_role = session.get('role')

    if user_email:
        pending_items_count = db.get_pending_items_count(department=user_department)
        user_counts = db.get_users_count_by_department(department=user_department)
        total_cost = db.get_total_cost_of_stock(department=user_department, status='approved')
        damaged_items=0
        checkout_items = session.get('checkout_items', [])
        user_name = session.get('name')


        return render_template('home.html', user_name=user_name, user_email=user_email, user_department=user_department, user_role=user_role, pending_items_count=pending_items_count, user_counts=user_counts, total_cost=total_cost, damaged_items=damaged_items, checkout_items=checkout_items)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect('/login')
@app.route('/approver')
@login_required
@approver_required
def approver_dashboard():
    """A route that handles approver dashboard home page."""
    # Retrieve the user's email from the session
    user_email = session.get('user_email')
    user_department = session.get('department')
    user_role = session.get('role')
    if user_email:
        pending_items_count = db.get_pending_items_count(department=user_department)
        user_counts = db.get_users_count_by_department(department=user_department)
        total_cost = db.get_total_cost_of_stock(department=user_department, status='approved')
        damaged_items=0
        checkout_items = session.get('checkout_items', [])
        user_name = session.get('name')

        return render_template('approver_dashboard.html', user_name=user_name, user_email=user_email, user_department=user_department, user_role=user_role, pending_items_count=pending_items_count, user_counts=user_counts, total_cost=total_cost, damaged_items=damaged_items, checkout_items=checkout_items)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect('/login')

@app.route('/admin')
@admin_required
def admin():
    try:
        user_email = session.get('user_email')
        user_department = session.get('department', '')
        print(type(user_department))
        user_role = session.get('role', '')
        user_name = session.get('name')
        print(f"user name is : {user_name} ")
        print(f"email: {user_email}")
        print(user_department)
        print(user_role)
        

        # Ensure user_department is not None before calling methods
        if user_department is not None:
            pending_items_count = db.get_pending_items_count(department=user_department)
            user_counts = db.get_users_count_by_department(department=user_department)

            total_cost = db.get_total_cost_of_stock(department=user_department, status='approved')
            damaged_items=0
            pending_checkout = db.get_checkout_items_by_department(user_department)
            checkout_count = len(pending_checkout) # Count pending checkouts
            print(f"Checkout count = {checkout_count}")
            print(pending_checkout)
            checkout_items = session.get('checkout_items', [])
            print("Checkout Items:", checkout_items)
             # Generate the Matplotlib graph
            categories = ['Users', 'Approvers', 'Admins']
            user_counts_data = [user_counts.get('user_count', 0), user_counts.get('approver_count', 0), user_counts.get('admin_count', 0)]
            plt.figure(figsize=(3, 4)) # Set width and height respectively<
            plt.bar(categories, user_counts_data)
            plt.xlabel('User Categories')
            plt.ylabel('Number of Users')
            plt.title('User Stats')

            # Save the plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Encode the image as base64 and convert to a string
            plot_url = base64.b64encode(img.getvalue()).decode()

        else:
            pending_items_count = 0  # Set a default count
            user_counts = {'user_count': 0, 'admin_count': 0, 'approver_count': 0}  # Set default counts
            total_cost = 0
            damaged_items= 0

        return render_template('index.html', plot_url=plot_url, pending_checkout=pending_checkout, checkout_count=checkout_count, user_email=user_email, pending_items_count=pending_items_count, user_counts=user_counts, total_cost=total_cost, damaged_items=damaged_items, user_role=user_role, user_department=user_department, user_name=user_name, checkout_items=checkout_items)

    except Exception as e:
        flash(f"Error in admin route: {str(e)}", 'error')
        return redirect('/login')


@app.route('/add_item', methods=['POST', 'GET'])
@login_required
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = float(request.form['price'])
        category = request.form['category']
        quantity = int(request.form['quantity'])
        description = request.form['description']

        # Create a StockItem object with the UUID generated
        stock_item = StockItem(item_name, price, category, quantity)

        # Get the current user's ID and department from the session
        maker_id = session.get('id')
        department = session.get('department')

        # Insert the new item into the database using the Database class
        db.insert_item(stock_item, maker_id=maker_id, description=description)

        # Flash a success message
        flash(f'The Item <b>"{item_name}"</b> has been added successfully!', 'success')

    # Fetch the updated stock items from the database
    stock_items = db.get_all_items()
    user_department = session.get('department')
    user_role = session.get('role')

    # Get all categories for the form dropdown
    categories = db.get_item_categories()
    print(categories)


    return render_template('add_item.html', stock_items=stock_items, user_department=user_department, user_role=user_role, categories=categories)


@app.route('/items')
@login_required
def all_items():
    """
    Retrieves all stock items from the database.
    And renders an HTML page to display them.

    Returns:
        str: Rendered HTML page displaying all stock items.
    """
    # Fetch all stock items from the database using the Database class
    stock_items = db.get_all_items()

    # Create a list to hold the items
    items_list = []

    for item in stock_items:
        # Create a dictionary for each item
        item_data = {
            'item_name': item[1],
            'price': item[2],
            'category': item[3],
            'quantity': item[4],
            'currency': item[6],
            'created_at': item[5],
            'total_cost': item[4] * item[2],
        }

        # Append the item dictionary to the list
        items_list.append(item_data)

    return render_template('items.html', stock_items=items_list)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_item():
    """
    Handle both form submission and displaying search results.

    - For POST requests: Retrieve search query from the form, search for items
      in the database, and display the results.
    - For GET requests: Render the search page without results.

    Returns:
        str: Rendered HTML page displaying the search form and search results (if available).
    """
    if request.method == 'POST':
        search_query = request.form['search_query']
        # Perform the database search for the item based on search_query
        search_results = db.search_item(search_query)

        # Create a list to hold the details of matching items
        items_list = []

        for item in search_results:
            # Create a dictionary for each matching item
            item_data = {
                'item_name': item[1],
                'price': item[2],
                'category': item[3],
                'quantity': item[4],
                'currency': item[6],
                'created_at': item[5],
                'total_cost': item[2] * item[4],
            }

            # Append the item dictionary to the list
            items_list.append(item_data)

        return render_template('search.html', search_results=items_list)
    else:
        # Handle GET request (initial page load)
        return render_template('search.html', search_results=[])
@app.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    if request.method == 'POST':
        # Retrieve the email and password from the form data
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        role = request.form['role']
        name = request.form['name']
        # Print all form fields for debugging
        print(f"Received email: {email}")
        print(f"Received password: {password}")
        print(f"Received department: {department}")
        print(f"Received role: {role}")
        print(f"Received name: {name}")       

        db.insert_user(email, password, department, role, name)
        flash(f'You have successfull registered <b>"{name} <b> in <b>"{department}"</b> department with <b>"{role}"</b> priviledges!', 'success')

        # Render the result in the HTML response
        return render_template('registration_success.html', name=name, role=role, department=department)
    else:
         departments = user_handler.get_user_department()
         roles = user_handler.get_user_role()
         print(roles)
         print(departments)
         user_department = session.get('department')
         user_role = session.get('role')
         return render_template('register.html', user_department=user_department, user_role=user_role, departments=departments, roles=roles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # You can call your UserManager's login_user method here
        login_result, user_data = user_manager.login_user(email, password)

        if login_result == "Login successful!":
            # Store user information in the session
            session['user_email'] = email
            session['id'] = user_data[0]
            session['role'] = user_data[4] if user_data else None  
            session['department'] = user_data[3] if user_data else None
            session['name'] = user_data[5] if user_data else None
            print(f"name: {session['name']}")
            # Redirect to a dashboard or home page
            if session['role'] == 'admin':
                return redirect('/admin')
            elif session['role'] == 'user':
                return redirect('/home')
            elif session['role'] == 'approver':
                return redirect('/approver')
        else:
            return render_template('login.html', error=login_result)

    # For GET requests, simply render the login page
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Logout route to clear the user's session and log them out.

    Returns:
        Redirect: Redirects the user to the login page.
    """
    # Clear the user's session
    session.pop('user_email', None)
    # Redirect to the login page or any other desired page
    return render_template('logout.html')

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """
    Handle the checkout process for items.

    If the request method is POST, attempt to check out the specified quantity
    of the specified item. If successful, redirect to the items page with a
    success message; otherwise, redirect with an error message.

    If the request method is GET, render the checkout form.

    Returns:
        flask.Response: Redirects to the items page with a success or error message
                       on POST; renders the checkout form on GET.
    """
    if request.method == 'POST':
        # Get the item name and quantity from the user's input
        item_name = request.form.get('item_name')
        quantity = request.form.get('quantity')
        print(f"item name: {item_name}")
        print(f"Quanity: {quantity}")

        # Validate quantity input
        if not quantity.isdigit() or int(quantity) <= 0:
            flash('Invalid quantity input. Please enter a positive integer.', 'error')
            return redirect('/checkout')

        quantity = int(quantity)

        # Call the checkout_item method to remove the specified quantity of the item
        success = db.checkout_item(session['id'], item_name, quantity)

        if success:
            # Redirect back to the items page with a success message
            flash(f'{quantity} units of {item_name} checked out successfully', 'success')
            return redirect('/department_items')
        else:
            # Redirect back to the items page with an error message
            flash(f'Failed to check out {quantity} units of {item_name}', 'error')
            return redirect('/department_items')
    else:
        # Render the checkout form on GET
        return render_template('checkout.html')

@app.route('/pending_items')
@login_required
#@any_role_required(['admin', 'approver'])
def pending_items():
    """Display pending items.
    Descript:
                This route handles the display of pending items.
                It only displays items based on the user's department.
                It will not display items from a department different
                from the user's.
    """
    try:
        # Get the logged-in user's department from the session
        user_department = session.get('department')
        print(user_department)

        # Fetch pending items only in the user's department
        pending_items = db.get_pending_items(department=user_department)

        # Print or log the pending_items for debugging
        print("Pending Items:", pending_items)
        
        # Create an empty list of names.
        names = []
        for item in pending_items:
            maker_id = item.get('maker_id')
            user_name = db.get_user_name_by_id(maker_id)
            print(f'maker_id: {maker_id}, user_name: {user_name}')
            names.append(user_name)
            print(names)

        # Pass the pending_items directly to the template
        return render_template('pending_items.html', pending_items=pending_items, names=names)

    except Exception as e:
        # Handle exceptions, you can log the error or show a flash message
        flash(f"Error fetching pending items: {str(e)}", 'error')
        return render_template('pending_items.html', pending_items=[])

@app.route('/change_status', methods=['POST','GET'])
@login_required
@any_role_required(['admin', 'approver'])
def change_status():
    """Change the status of an item.
    Description:
                When an item is being added in the stock, it hits the db
                with a pending status by default.

                The approver will need to approve the item so that the 
                status changes from pending to approved.

                This ensures that we have items in our stock that are not
                randomly added or mistakenly added.
    """
    try:
        item_id = request.form.get('id')
        status = request.form.get('status')

        # Call a method to update the status in the database
        db.update_item_status(item_id, status)
        flash(f"Item status updated to {status}.", 'success')
    except Exception as e:
        # Handle exceptions, you can log the error or show a flash message
        flash(f"Error updating item status: {str(e)}", 'error')

    # Redirect back to the pending items page
    return redirect(url_for('pending_items'))


def approve_items():
    # Logic for approving items
    return render_template('approve_items.html')


@app.route('/update_email', methods=['GET', 'POST'])
@login_required
def update_email():
    """
    Update the user's email address.

    If the user is not authenticated, redirect to the login page.
    If the update is successful, redirect to the profile page; otherwise, handle the failure.

    Returns:
        Response: Redirects to the profile page or shows an error message.
    """
    if 'id' not in session:
        # Redirect to login if user is not authenticated
        return redirect(url_for('login'))

    user_id = session['id']  # Update to use 'id'
    new_email = request.form.get('new_email')
    if new_email is None:
        return render_template('update_email.html', error='New email Required.')
    # Call the update email method from your database class
    success = db.update_user_email(user_id, new_email)

    if success:
        flash("Email updated successfully.", 'success')
        # Redirect to a success page or back to the profile page
        return redirect(url_for('home'))
    else:
        flash("Failed to update email.", 'error')
        # Handle the failure, maybe show an error message to the user
        return render_template('update_email.html')  # Render the form again


@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    """
    Update the user's password.

    If the user is not authenticated, redirect to the login page.
    If the update is successful, redirect to the profile page; otherwise, handle the failure.

    Returns:
        Response: Redirects to the profile page or shows an error message.
    """
    if 'id' not in session:
        # Redirect to login if the user is not authenticated
        return redirect(url_for('login'))

    user_id = session['id']
    new_password = request.form.get('new_password')  # Use the correct form field name
    
    if new_password is None:
        return render_template('change_password.html', error='New password cannot be null')


    # Call the update password method from your database class
    success = db.update_user_password(user_id, new_password)

    if success:
        print("Password updated successfully.")
        # Redirect to a success page or back to the profile page
        return redirect(url_for('home'))
    else:
        print("Failed to update password.")
        # Handle the failure, maybe show an error message

@app.route('/admin/view_users')
@login_required
@admin_required
def view_users():
    try:
        # Get the admin's department from the session
        admin_department = session.get('department')

        # Get user info from session.
        user_role = session.get('role')
        user_name = session.get('name')


        # Fetch users only in the admin's department
        users = db.get_all_users(department=admin_department)
        print(users)
        user_department = admin_department

        if users:
            return render_template('view_users.html', user_name=user_name, user_department=user_department, users=users, user_role=user_role)
        else:
            return "No users found."
    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred."

@app.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    """
    Handle the forgot password functionality.

    For GET requests, render the forgot password form.
    For POST requests, check if the provided email exists in the database.
    If the email exists, generate a temporary password, update the user's password,
    and send an email with the temporary password. Redirect to the login page.

    Returns:
        render_template or redirect: Depending on the request type and the success of the operation.
    """
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email exists in the database
        user_data = db.find_user_by_email(email)
        print(user_data)

        if user_data:
            # Generate a temporary password
            temporary_password = random_password()

            # Update the user's password in the database with the temporary password
            if db.update_user_password(user_data['id'], temporary_password):
                # Send an email with the temporary password using the existing send_email function
                sender_email = 'info@remmittance.com'  # Update with your sender email
                subject = 'Temporary Password for Password Reset'
                message = f'<p>Your temporary password is: <b>{temporary_password}</b></p>'

                # Get the SendGrid API key from the environment
                api_key = os.getenv('email_api')

                # Send the email using the existing send_email function
                send_email(api_key, sender_email, email, subject, message)

                flash("Temporary password sent to your email. Please check your inbox.")
                return redirect(url_for('login'))

            flash("Error updating password. Please try again.")
        else:
            flash("Email not found. Please try again.")
    
    # For GET requests or unsuccessful POST requests, render the forgot password form
    return render_template('forgot_password.html')

@app.route('/department_items')
@login_required  
def get_items_by_department():
    """
    Fetch items based on the user's department and render the department_items.html template.

    Returns:
        str: Rendered HTML template with the items or an error message if the department is not available in the session.
    """
    # Retrieve department from the session
    user_department = session.get('department')
    print("User Department:", user_department)

    if user_department:
        # Fetch items based on the user's department
        items = db.get_items_by_department(user_department)
        print("Items:", items, user_department)
        return render_template('department_items.html', items=items, user_department=user_department)
    else:
        # Handle the case when the department is not available in the session
        return "Department information not found in the session."
@app.route('/checkout_items')
@login_required
def checkout_items():
    """
    Display checkout items for the logged-in user's department.

    Returns:
        flask.Response: Renders a template with checkout items.
    """
    department = session.get('department')

    if department:
        checkout_items = db.get_checkout_items_by_department(department)
        # Store the details in a session for future use anywhere in the app.
        session['checkout_items'] = checkout_items
        print(checkout_items)
        return render_template('checkout_items.html', checkout_items=checkout_items)
    else:
        # Handle the case when the department is not available in the session
        return "Department information not found in the session."

@app.route('/change_checkout_status', methods=['POST'])
@login_required
@approver_required
def change_checkout_status():
    """Approve a checkout. 
    Description:
                The approver or the admin will be able to change the status
                of the checkout. When the user tries to checkout an item, it 
                hits the db with a default status of pending.

                The approver or the admin will be able to approve
                the checkout. They can give it a status of approved, rejected.
    """
    # Get the id of the user from the login session.
    approver_id = session.get('id')

    # Get the checkout_id from the form
    checkout_id = int(request.form.get('checkout_id'))

    # Get the status chosen by the approver/admin
    status = request.form.get('status')

    success = db.update_checkout_status(checkout_id, status, approver_id)

    if success:
        flash(f'Checkout status updated successfully', 'success')
    else:
        flash(f'Failed to update checkout status', 'error')

    return redirect('/checkout_items')

@app.route('/backup', methods=['GET', 'POST'])
def backup():
    """
    Run the database backup script and provide the backup file for download.

    This route triggers the execution of the database backup script, and once
    the backup is complete, it provides the user with the option to download
    the backup file. After the download, a success message is flashed.

    Returns:
        Flask.Response: Flask response object containing the backup file.
    """
    print("Backup route accessed!")
    try:
        # Run the backup script
        subprocess.run(['/home/rugema3/automations/stock_backup.sh'])

        # Compose the path to the backup file
        current_date = subprocess.check_output(['date', '+%d-%m-%Y']).decode().strip()
        database_name = "stock"
        backup_path = "/home/rugema3/db_backups"
        backup_filename = f"{backup_path}/{database_name}-{current_date}.sql.tar.gz"

        # Send the file for download
        response = send_file(backup_filename, as_attachment=True)

        # Flash a success message
        flash('Database backup completed successfully! File downloaded.')

        return response

    except Exception as e:
        # Handle any exceptions and flash an error message
        flash(f'Error: {str(e)}')

    # If an error occurred, you might want to redirect to an error page or another route
    return "An Error oocured"



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

