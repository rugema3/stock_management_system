from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required

search_weekly_adds_route = Blueprint('search_weekly_adds', __name__)

@search_weekly_adds_route.route('/search_weekly_adds', methods=['GET', 'POST'])
@login_required
def expiring_soon():
    """
    Route to display items expiring soon.
    """
    # Retrieve user-id, department, and role from session.
    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')

    # Retrieve information from form or any other logic for expiring items
    if request.method == 'POST':
        # Accessing item_manager stored in the Flask application.
        item_manager = current_app.item_manager

        # Logic to retrieve items expiring soon
        expiring_items = item_manager.get_expiring_soon(user_department)
        print('expiring_items: ', expiring_items)

        return render_template(
            'expiring_soon.html',
            expiring_items=expiring_items,
            user_department=user_department,
            user_role=user_role
        )
    else:
        return render_template('expiring_soon.html')
