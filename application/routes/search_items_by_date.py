"""
search_items_by_date module.

Description:
            This module represents a flask blueprint where the route
            for handling searching items from the database that have been
            added based on a range of dates provided by the user.
"""
from flask import request, render_template, redirect, url_for, flash
from flask import Blueprint, current_app, session
from decorators.authentication_decorators import login_required
from datetime import datetime

search_items_by_date_route = Blueprint('search_items_by_date', __name__)


@search_items_by_date_route.route(
        '/search_items_by_date',
        methods=['GET', 'POST']
        )
@login_required
def search_items_by_date():
    """
    Route to display items by date.
    """
    # Retrieve user-id from session.
    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')
    extracted_path = session.get('extracted_path')

    # Retrieve information from form.
    if request.method == 'POST':
        # Accessing item_manager stored in the Flask application.
        item_manager = current_app.item_manager

        # Retrieve information from user input.
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Convert start_date and end_date to datetime objects
        start_date_formatted = datetime.strptime(
                start_date,
                '%Y-%m-%d').strftime('%b-%d-%Y')
        end_date_formatted = datetime.strptime(
                end_date,
                '%Y-%m-%d').strftime('%b-%d-%Y')

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
                user_role=user_role,
                extracted_path=extracted_path,
                start_date=start_date_formatted,
                end_date=end_date_formatted
                )
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            # Convert start_date and end_date to datetime objects
            start_date_formatted = datetime.strptime(
                    start_date,
                    '%Y-%m-%d').strftime('%b-%d-%Y'
                                         )
            end_date_formatted = datetime.strptime(
                    end_date,
                    '%Y-%m-%d').strftime('%b-%d-%Y'
                                         )
        else:
            start_date_formatted = None
            end_date_formatted = None
        return render_template(
                'search_items_by_date.html',
                extracted_path=extracted_path,
                user_department=user_department,
                start_date=start_date,
                end_date=end_date,
                user_role=user_role
                )
