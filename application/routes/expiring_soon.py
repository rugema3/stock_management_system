from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required

expiring_soon_route = Blueprint('expiring_soon', __name__)

@expiring_soon_route.route('/expiring_soon', methods=['GET', 'POST'])
@login_required
def expiring_soon():
    """
    Route to display items expiring soon.
    """
    # Retrieve user-id, department, and role from session.
    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')
    user_name = session.get('name')
    extracted_path = session.get('extracted_path')


    # Retrieve information from form or any other logic for expiring items
    if request.method == 'GET':
        # Accessing item_manager stored in the Flask application.
        item_manager = current_app.item_manager
        db = current_app.db

        # Logic to retrieve items expiring soon
        expiring_items = item_manager.get_expiring_soon(user_department)
        print('expiring_items: ', expiring_items)

        return render_template(
            'expiring_soon.html',
            expiring_items=expiring_items,
            user_department=user_department,
            user_role=user_role,
            db=db,
            user_name=user_name,
            extracted_path=extracted_path
        )
    else:
        return render_template('expiring_soon.html')
