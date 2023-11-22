from functools import wraps
from flask import redirect, url_for, session

def any_role_required(allowed_roles):
    """
    A decorator that restricts access to the wrapped function
    to users with any of the specified roles.

    Args:
        allowed_roles (list): A list of roles that are allowed to access the route.

    Returns:
        callable: The decorated function.
    """
    def decorator(func):
        """
        Inner decorator function that performs the role check.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The decorated function.
        """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            """
            Checks if the user is logged in and has any of the allowed roles.

            If the user is not logged in, redirects to the login page.
            If the user does not have any of the allowed roles,
            redirects to the home page.

            Args:
                *args: Positional arguments passed to the wrapped function.
                **kwargs: Keyword arguments passed to the wrapped function.

            Returns:
                Any: The result of the wrapped function.
            """
            # Check if the user is logged in
            if 'user_email' not in session:
                return redirect(url_for('login'))

            # Check if the user has any of the allowed roles
            role = session.get('role')
            if role not in allowed_roles:
                return redirect(url_for('home'))

            return func(*args, **kwargs)

        return decorated_function

    return decorator
