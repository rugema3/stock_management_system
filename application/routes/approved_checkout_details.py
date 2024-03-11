from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required
import matplotlib.pyplot as plt
from collections import defaultdict
import io
import base64
from datetime import datetime, timedelta
from collections import defaultdict

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

    # Retrieve user names based on user_ids
    user_names = {}
    for approved in approved_checkouts:
        user_id = approved['user_id']
        user_names[user_id] = db.get_user_name_by_id(user_id)

    approver_names = {}
    for approver_name in approved_checkouts:
        approver_id = approver_name['approver_id']
        approver_names[approver_id] = db.get_user_name_by_id(approver_id)

    # Scenario 1: Top 5 Most Checked Out Items (Bar Chart)
    item_quantities = defaultdict(int)
    for checkout in approved_checkouts:
        item_quantities[checkout['item_name']] += checkout['quantity']

    top_items = sorted(item_quantities.items(), key=lambda x: x[1], reverse=True)[:5]
    item_names = [item[0] for item in top_items]
    quantities = [item[1] for item in top_items]

    plt.figure(figsize=(5, 3))
    plt.bar(item_names, quantities, color='skyblue')
    plt.xlabel('Item Names')
    plt.ylabel('Quantity')
    plt.title('Top 5 Most Checked Out Items')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64 and convert to a string
    summary1_url = base64.b64encode(img.getvalue()).decode()

    # Retrieve weekly checkout details
    checkouts_weekly = item_manager.get_weekly_checkouts(user_department)

    checkouts_by_week = defaultdict(list)

    return render_template(
            'approved_checkout_details.html',
            approved_checkouts=approved_checkouts,
            user_names=user_names,
            approver_names=approver_names,
            user_department=user_department,
            user_role=user_role,
            extracted_path=extracted_path,
            summary1_url=summary1_url,
            checkouts_by_week=checkouts_by_week
            )
