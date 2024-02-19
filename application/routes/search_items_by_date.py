from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required

search_items_by_date_route = Blueprint('search_items_by_date', __name__)

@search_items_by_date_route.route('/search_items_by_date', methods=['GET', 'POST'])
@login_required
def search_items_by_date():
    """
    Route to display items by date.
    """
    # Retrieve user-id from session.
    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')

    # Retrieve information from form.
    if request.method == 'POST':
        # Accessing item_manager stored in the Flask application.
        item_manager = current_app.item_manager

        # Retrieve information from user input.
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Retrieve added items from the selected dates.
        added_items = item_manager.retrieve_added_items_by_date(
                user_department, 
                start_date, 
                end_date
                )
        print('added_items for {start_date} and {end_date}: ', added_items)

        return render_template(
                'search_items_by_date.html',
                added_items=added_items,
                user_department=user_department,
                user_role=user_role
                )
    else:
        return render_template('search_items_by_date.html')
