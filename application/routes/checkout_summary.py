from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.authentication_decorators import login_required
import matplotlib.pyplot as plt
from collections import defaultdict
import io
import base64
from datetime import datetime, timedelta
from collections import defaultdict

checkout_summary_route = Blueprint('checkout_summary', __name__)

@checkout_summary_route.route('/checkout_summary', methods=['GET', 'POST'])
@login_required
def checkout_summary():
    """
    Route to display the checkout summary.
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

    # Retrieve weekly checkout details
    checkouts_weekly = item_manager.get_weekly_checkouts(user_department)

    checkouts_by_week = defaultdict(list)

    for checkout in checkouts_weekly:
        week_period = checkout['week_period']
        checkouts_by_week[week_period].append(checkout)

    # Retrieve Monthly checkout details
    checkouts_monthly = item_manager.get_monthly_checkouts(user_department)

    checkouts_by_month = defaultdict(list)
    for checkout in checkouts_monthly:
        month_period = checkout['month_period']
        checkouts_by_month[month_period].append(checkout)

    # Retrieve daily checkout details
    checkouts_daily = item_manager.get_daily_checkouts(user_department)

    checkouts_by_date = defaultdict(list)

    for checkout in checkouts_daily:
        checkout_date = checkout['checkout_date']
        checkouts_by_date[checkout_date].append(checkout)

    
    return render_template(
            'checkout_summary.html',
            approved_checkouts=approved_checkouts,
            user_names=user_names,
            approver_names=approver_names,
            user_department=user_department,
            user_role=user_role,
            extracted_path=extracted_path,
            checkouts_by_week=checkouts_by_week,
            checkouts_by_month=checkouts_by_month,
            checkouts_by_date=checkouts_by_date
            )
