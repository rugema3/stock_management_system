from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required
from decouple import config

store_approval_details_route = Blueprint('store_approval_details', __name__)

@store_approval_details_route.route('/store_approval_details', methods=['GET', 'POST'])
@login_required
def store_approval_details():
    """
    Route to store approval details with item_id in the database.
    """
    # Retrieve user-id from session.
    user_id = session.get('id')
    item_manager = current_app.item_manager
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        approval_status = request.form.get('status')
        approver_id = user_id
        approval_comment = request.form.get('approval_comment')

        # Call the method to store approval details with item_id
        item_manager.store_approval_details(item_id, approval_status, approver_id, approval_comment)

        return "Approval details with item_id stored successfully"
    else:
        return "Method not allowed"