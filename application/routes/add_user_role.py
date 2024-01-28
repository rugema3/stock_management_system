from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from application.models.user_handler import UserHandler
from decorators.admin_decorators import admin_required
from decouple import config

add_user_role_route = Blueprint('add_user_role', __name__)

@add_user_role_route.route('/add_user_role', methods=['GET', 'POST'])
@admin_required
def add_user_role():
    """
    Add the user role in the db.

    Returns:
        Flask.Response: Redirects to the add_user_role page.
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
            role_name = request.form['role_name']
            

            # Add role in the database.

            success = db.add_user_role(role_name)

            if success:
                flash(f'{role_name} role has been added successfully!', 'success')
            else:
                flash(f'Failed to add {role_name} role. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template on GET http
    return render_template('add_user_role.html')

