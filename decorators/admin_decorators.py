"""
admin_decorators.py.

This module defines custom decorators for Flask routes to control
access based on user roles.

Decorators:
    - `admin_required`: Restricts access to routes for users
       with admin privileges.

Usage:
    Import these decorators into your Flask application to protect specific
    routes based on user roles.
    Example usage can be found in your route definitions.

"""

from functools import wraps
from flask import redirect, url_for, flash, session


def admin_required(view_func):
    """
    A decorator to protect routes and allow access only to users
    with admin privileges.

    Args:
        view_func (function): The route function to be protected.

    Returns:
        function: A decorated function that checks if the
        user has admin privileges.

    Example:
        @app.route('/admin_dashboard')
        @admin_required
        def admin_dashboard():
            # This page is only accessible to users with admin privileges
            return render_template('admin_dashboard.html')
    """
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        """
        Checks if the user has admin privileges and allows
        access to the protected route.

        Args:
            *args: Variable-length arguments.
            **kwargs: Variable-length keyword arguments.

        Returns:
            Any: The original route function or a redirect response if the
            user does not have admin privileges.
        """
        user_role = session.get('role')
        print(f"User role: {user_role}")  # Debugging
        if user_role == 'admin':
            # If the user has admin privileges, allow access to restricteds.
            return view_func(*args, **kwargs)
        else:
            flash(
                    'Permission denied. Admin privileges needed', 'error'
                    )

            return redirect(url_for('home'))  # Redirect to home
    return decorated_view
