from flask import Blueprint, render_template, request, flash, session, current_app, redirect, url_for
from decorators.authentication_decorators import login_required

add_item_category_route = Blueprint('add_item_category', __name__)

@add_item_category_route.route('/add_item_category', methods=['GET', 'POST'])
@login_required
def add_item_category():
    """
    View function to handle adding item categories.

    Returns:
        Flask.Response: Redirects to the add_item_category page.
    """
    # Ensure the db instance is available
    if not hasattr(current_app, 'db'):
        flash('Database instance not available!', 'error')
        return "Database Instance Not available."

    # Retrieve the db instance
    db = current_app.db

    # Retrieve user info from session
    user_department = session.get('department')
    user_role = session.get('role')
    extracted_path = session.get('extracted_path')

    # Retrieve the categories from the db.
    categories = db.get_item_categories()
    print('Categories:', categories)

    if request.method == 'POST':
        try:
            # Get the new details from the form
            category_name = request.form['category_name']
            
            # Add category in the database.
            success = db.add_item_category(category_name)

            if success:
                flash(f'{category_name} added successfully!', 'success')
            else:
                flash(f'Failed to add {category_name}. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template on GET http
    return render_template(
            'add_item_category.html', 
            user_department=user_department, 
            user_role=user_role,
            categories=categories,
            extracted_path=extracted_path
            )
