from functools import wraps
from flask import redirect, session

def login_required(f):
    """
    A decorator to protect routes and allow access only to authenticated users.

    Args:
        f (function): The route function to be protected.

    Returns:
        function: A decorated function that checks if the user is authenticated.

    Example:
        @app.route('/dashboard')
        @login_required
        def dashboard():
            # This page is only accessible to authenticated users
            return render_template('dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if 'user_email' is in the session, indicating an authenticated user
        if 'user_email' in session:
            # If authenticated, allow access to the protected route
            return f(*args, **kwargs)
        else:
            # If not authenticated, redirect the user to the login page
            return redirect('/login')
    return decorated_function

