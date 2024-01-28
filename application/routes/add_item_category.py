from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from application.models.database_manager import Database
from decorators.authentication_decorators import login_required
from decouple import config

add_item_category_route = Blueprint('add_item_category', __name__)

@add_item_category_route.route('/add_item_category', methods=['GET', 'POST'])
@login_required
def add_item_category():
    """
    Add the category of items in the db.

    Returns:
        Flask.Response: Redirects to the add_item_category page.
    """
    # Initialize the Database
    db_config = {
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'database': config('DB_NAME'),
    }
    db = Database(db_config)
    user_department = session.get('department')
    user_role = session.get('role')

    if request.method == 'POST':
        try:
            # Get the new details from the form
            category_name = request.form['category_name']
            

            # Add category in the database.
            success = db.add_item_category(category_name)

            if success:
                flash('{category_name} added successfully!', 'success')
            else:
                flash('Failed to add {category_name}. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template on GET http
    return render_template('add_item_category.html', user_department=user_department, user_role=user_role)

