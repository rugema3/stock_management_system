from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from decorators.admin_decorators import admin_required

add_user_department_route = Blueprint('add_user_department', __name__)

@add_user_department_route.route('/add_user_department', methods=['GET', 'POST'])
@admin_required
def add_user_department():
    """
    Add or modify departments in the db.

    Returns:
        Flask.Response: Redirects to the add_user_department page.
    """
    # Retrieve the required instances
    db = current_app.db
    user_handler = current_app.user_handler

    user_department = session.get('department')
    user_role = session.get('role')

    # Retrieve departments from the database.
    departments = user_handler.get_user_department()

    if request.method == 'POST':
        try:
            # Check if department_id is present in form data
            if 'department_id' in request.form:
                # Updating an existing department
                department_id = int(request.form['department_id'])
                new_department = request.form['new_department']
                print("department_id: ", department_id)
                print()
                print("New Department: ", new_department)

                # Update the department in the database.
                success = user_handler.update_user_department(department_id, new_department)
                print("Success before: ", success)
                print()
                if success:
                    print("Inside the success block")
                    flash(f'Department "{new_department}" has been updated successfully!', 'success')
                else:
                    flash(f'Failed to update department "{new_department}". Please try again.', 'error')
            else:
                # Adding a new department
                department_name = request.form['department_name']

                # Check if the department already exists
                if department_name.lower() in [department.lower() for department in departments]:
                    flash(f'Department "{department_name}" already exists. Please add a department that is not in the database.', 'error')
                else:
                    # Add the department in the database.
                    success = user_handler.add_user_department(department_name)
                    if success:
                        flash(f'Department "{department_name}" has been added successfully!', 'success')
                    else:
                        flash(f'Failed to add department "{department_name}". Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template with the available departments
    return render_template(
            'add_user_department.html', 
            user_department=user_department, 
            user_role=user_role,
            departments=departments
            )

