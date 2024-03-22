from flask import Blueprint, render_template, request, flash, redirect
from flask import url_for, session, current_app
from decorators.authentication_decorators import login_required


get_notifications_route = Blueprint('get_notifications', __name__)

@get_notifications_route.route('/get_notifications', methods=['GET', 'POST'])
@login_required
def get_notifications():
    """
    get_notifications.
    """
    item_manager = current_app.item_manager

    # Retrieve the current details of loggedin user.
    user_department = session.get('department')
    user_role = session.get('role')
    user_id = session.get('id')
    user_name = session.get('name')
    extracted_path = session.get('extracted_path')


    try:
        # Fetch notifications
        notifications = item_manager.get_notifications()
        
        return render_template(
            'get_items.html', 
            user_role=user_role,
            user_department=user_department,
            user_name=user_name,
            extracted_path=extracted_path,
            notifications=notifications
            )
    except Exception as e:
        print("Exeption occured: ", e)