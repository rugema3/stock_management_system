from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required

approved_checkout_details_route = Blueprint('approved_checkout_details', __name__)

@approved_checkout_details_route.route('/approved_checkout_details', methods=['GET', 'POST'])
@login_required
def approved_checkout_details():
    """
    Route to display the approved_checkouts details.
    """
    # Retrieve useful information from session.
    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')
    extracted_path = session.get('extracted_path')
    
    item_manager = current_app.item_manager
    db = current_app.db

    # Retrieve approved_checkouts from session.
    approved_checkouts = session.get('approved_checkouts')
    print('approved_checkouts: ', approved_checkouts)

    # Retrieve user names based on user_ids
    user_names = {}
    for approved in approved_checkouts:
        user_id = approved['user_id']
        user_names[user_id] = db.get_user_name_by_id(user_id)

    approver_names = {}
    for approver_name in approved_checkouts:
        approver_id = approver_name['approver_id']
        approver_names[approver_id] = db.get_user_name_by_id(approver_id)
        print('approvers: ', approver_names[approver_id])


    return render_template(
            'approved_checkout_details.html',
            approved_checkouts=approved_checkouts,
            user_names=user_names,
            approver_names=approver_names,
            user_department=user_department,
            user_role=user_role,
            extracted_path=extracted_path
            )
