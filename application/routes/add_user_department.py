from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from application.models.user_handler import UserHandler
from decorators.admin_decorators import admin_required

add_user_department_route = Blueprint('add_user_department', __name__)

@add_user_department_route.route('/add_user_department', methods=['GET', 'POST'])
@admin_required
def add_user_department():
    """
    Add the department of items in the db.

    Returns:
        Flask.Response: Redirects to the add_item_department page.
    """
    # Retrieve the required instances
    db = current_app.db
    user_handler = current_app.user_handler

    user_department = session.get('department')
    user_role = session.get('role')

    # Retrieve departments from the database.
    departments = user_handler.get_user_department()
    print('departments: ', departments)

    if request.method == 'POST':
        try:
            # Get the new details from the form
            department_name = request.form['department_name']

            # Check if the role name already exists in the list of retrieved roles
            if department_name.lower() in [department.lower() for department in departments]:
                flash(f'Department "{department_name}" already exists.Please add A department that is not in the Database', 'error')
            else:
                # Add category in the database.
                success = user_handler.add_user_department(department_name)

            if success:
                flash(f'{department_name} department has been added successfully!', 'success')
            else:
                flash(f'Failed to add {department_name} department. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template on GET http
    return render_template(
            'add_user_department.html', 
            user_department=user_department, 
            user_role=user_role,
            departments=departments
            )

