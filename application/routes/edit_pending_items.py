# application/routes/edit_pending_items.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from application.models.database_manager import Database
from decorators.authentication_decorators import login_required
from decouple import config

edit_pending_items_route = Blueprint('edit_pending_items', __name__)

@edit_pending_items_route.route('/edit_pending_item', methods=['GET', 'POST'])
@login_required
def edit_pending_item():
    """
    Edit the quantity, name, and price of a pending item.

    This route handles the submission of the form to edit the quantity,
    name, and price of a pending item. It retrieves the current details of
    the pending item, updates the database, and redirects to the pending items page.

    Args:
        item_id (int): The ID of the pending item to edit.

    Returns:
        Flask.Response: Redirects to the pending items page.
    """
    # Initialize the Database
    db_config = {
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'database': config('DB_NAME'),
    }
    db = Database(db_config)

    # Retrieve the current details of the pending item
    user_department = session.get('department')
    print(user_department)
    pending_item = db.get_pending_items(user_department)
    print(pending_item)

    if request.method == 'POST':
        try:
            # Get the new details from the form
            new_name = request.form['new_name']
            new_quantity = int(request.form['new_quantity'])
            new_price = float(request.form['new_price'])
            item_id = int(request.form['item_id'])

            # Update the pending item in the database
            updates = {
                'item_name': new_name,
                'quantity': new_quantity,
                'price': new_price
            }
            success = db.update_item(item_id, updates)

            if success:
                flash('Pending item updated successfully!', 'success')
            else:
                flash('Failed to update pending item. Please try again.', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template with the pending item details
    return render_template('edit_pending_item.html', item=pending_item)

