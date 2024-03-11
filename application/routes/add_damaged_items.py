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
    item_manager = current_app.item_manager

    # Retrieve the current details of loggedin user.
    user_department = session.get('department')
    user_role = session.get('role')
    user_id = session.get('id')
    user_name = session.get('name')
    extracted_path = session.get('extracted_path')


    # Fetch items as tuples
    department_items = db.get_items_by_department(user_department)

    if request.method == 'POST':
        try:
            # Get the details from the form
            item_id = int(request.form['item_id'])
            damaged_quantity = int(request.form['quantity_damaged'])
            damage_description = request.form['damage_description']
            reported_by = session.get('id')
            item_name = request.form['item_name']
            print("Item name: ", item_name)

            # Debugging: Print form data
            print("Form Data - item_id:", item_id)
            print("Form Data - damaged_quantity:", damaged_quantity)
            print("Form Data - damage_description:", damage_description)

            # Find the item in department_items by item_id
            current_item = next((item for item in department_items if item[0] == item_id), None)
            if current_item:
                current_quantity = int(current_item[4])
                print("current quantity: ", current_quantity)

                # Check if the damaged quantity is valid
                if damaged_quantity > current_quantity:
                    flash('Damaged quantity exceeds available quantity', 'error')
                else:
                    # Update the quantity in the database
                    new_quantity = current_quantity - damaged_quantity
                    item_manager.update_item_quantity(item_id, new_quantity)

                    # Add damaged item to the damaged_items table
                    success = item_manager.add_damaged_item(item_id, damage_description, reported_by, damaged_quantity)
                
                    if success:
                        flash(f'{damaged_quantity} units of {item_name} have been  reported as damaged. Update successfull!', 'success')
                    else:
                        flash("Something went wrong and we couldn't update the damage report.", "error")
            else:
                flash('Item not found', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    return render_template(
            'add_damaged_items.html', 
            department_items=department_items,
            user_role=user_role,
            user_department=user_department,
            user_name=user_name,
            extracted_path=extracted_path
            )
