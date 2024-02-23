from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
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
    # Retrieve the item_handler instance
    user_handler = current_app.user_handler
    user_department = session.get('department')
    user_role = session.get('role')
    roles = user_handler.get_user_role()

    if request.method == 'POST':
        try:
            # Get the new details from the form
            role_name = request.form['role_name']
            

            # Check if the role name already exists in the list of retrieved roles
            if role_name.lower() in [role.lower() for role in roles]:
                flash(f'Role "{role_name}" already exists.', 'error')
            else:
                # Add role in the database.
                success = user_handler.add_user_role(role_name)

            if success:
                flash(f'{role_name} role has been added successfully!', 'success')
            else:
                flash(f'Failed to add {role_name} role. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template on GET http
    return render_template('add_user_role.html', roles=roles, user_department=user_department, user_role=user_role)

