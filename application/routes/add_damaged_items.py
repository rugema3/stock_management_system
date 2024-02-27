# Import the redirect function
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from application.models.database_manager import Database
from decorators.authentication_decorators import login_required
from decouple import config

add_damaged_items_route = Blueprint('add_damaged_items', __name__)

@add_damaged_items_route.route('/add_damaged_items', methods=['GET', 'POST'])
@login_required
def add_damaged_items():
    """
    Add damaged items
    """

    db = current_app.db
    item_manager = current_app.db

    # Retrieve the current details of the pending item
    user_department = session.get('department')
    user_id = session.get('id')
    user_role = session.get('role')
    department_items = db.get_items_by_department(user_department)
    print(department_items)

    if request.method == 'POST':
        try:
            # Get the new details from the form
            item_id = int(request.form['item_id'])
            if 'damaged_quantity' in request.form:
                damaged_quantity = int(request.form['damaged_quantity'])
                damage_description = request.form['damage_description']
                reported_by = db.get_user_name_by_id(user_id)
                success = item_manager.add_damaged_item(item_id, damage_description, reported_by, quantity_damaged)

                if success:
                    flash('damaged item updated successfully!', 'success')
            
                else:
                    flash('Failed to update item. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template with the  item details
    return render_template('add_damaged_items.html', department_items=department_items)
