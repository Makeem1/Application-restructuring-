from functools import wraps
from flask_login import current_user
from flask import flash 
from flask import redirect


def role_required(*roles):
    """Function checking for user role"""

    def decorators(f):
        @wraps(f)
        def decorated_fucntions(*args, **kwargs):
            if current_user.role not in roles:
                flash("You do not have permission to visit this page.", 'warning')
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_fucntions
    return decorators