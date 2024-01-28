from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from application.models.user_handler import UserHandler
from decorators.admin_decorators import admin_required
from decouple import config

add_user_department_route = Blueprint('add_user_department', __name__)

@add_user_department_route.route('/add_user_department', methods=['GET', 'POST'])
@admin_required
def add_user_department():
    """
    Add the department of items in the db.

    Returns:
        Flask.Response: Redirects to the add_item_department page.
    """
    # Initialize the Database
    db_config = {
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'database': config('DB_NAME'),
    }
    db = UserHandler(db_config)

    if request.method == 'POST':
        try:
            # Get the new details from the form
            department_name = request.form['department_name']
            

            # Add category in the database.:wq

            success = db.add_user_department(department_name)

            if success:
                flash(f'{department_name} department has been added successfully!', 'success')
            else:
                flash(f'Failed to add {department_name} department. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template on GET http
    return render_template('add_user_department.html')

