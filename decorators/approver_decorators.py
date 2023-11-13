from functools import wraps
from flask import redirect, url_for, session


def approver_required(func):
    """
    A decorator that restricts access to the wrapped function
    to users with the 'approver' role.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Checks if the user is logged in and has the 'approver' role.

        If the user is not logged in, redirects to the login page.
        If the user does not have the 'approver' role,
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

        # Check if the user has the approver role
        role = session.get('role')
        if role != 'approver':
            return redirect(url_for('home'))

        return func(*args, **kwargs)

    return decorated_function
