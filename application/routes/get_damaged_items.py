from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from decorators.authentication_decorators import login_required

get_damaged_items_route = Blueprint('get_damaged_items', __name__)

@get_damaged_items_route.route('/get_damaged_items', methods=['GET', 'POST'])
@login_required
def get_damaged_items():
    """
    Add damaged items
    """

    db = current_app.db
    item_manager = current_app.item_manager

    # Retrieve the current details of the items
    user_department = session.get('department')
    user_role = session.get('role')
    user_id = session.get('id')
    user_name = session.get('name')
    extracted_path = session.get('extracted_path')

    try:
        # Fetch damaged items.
        damaged_items = item_manager.get_damaged_items()
        print("Damaged Itmes: ", damaged_items)

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return render_template(
            'get_damaged_items.html', 
            damaged_items=damaged_items,
            user_role=user_role,
            user_department=user_department, 
            db=db,
            item_manager=item_manager,
            extracted_path=extracted_path,
            user_name=user_name
            )
