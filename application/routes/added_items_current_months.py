from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required

added_items_current_months_route = Blueprint('added_items_current_months', __name__)

@added_items_current_months_route.route('/added_items_current_months', methods=['GET', 'POST'])
@login_required
def added_items_current_months():
    """
    Route to display the added items in the current months.
    """
    # Retrieve user-id from session.
    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')

    # Accessing item_manager stored in the Flask application.
    item_manager = current_app.item_manager

    # Retrieve added items for the current from the database.
    added_items = item_manager.get_items_current_month(user_department)
    print('added_items for current months: ', added_items)

    return render_template(
            'get_items_current_month.html',
            added_items=added_items,
            user_department=user_department,
            user_role=user_role
            )
