from functools import wraps
from flask import redirect, url_for, flash





def anonymous(url='/settings'):
    '''This function help to monitor activities of signed in user'''

    def decorator(f):
        @wraps(f)
        def decorated_functions(*args, **kwargs):
            if current_user.is_authenticated:
                flash("Operation already performed", 'info')
                return redirect(url)
            return f(*args, **kwargs)
        return decorated_functions
    return decorator





def username_choosed(url='/settings'):
    '''This function help to monitor activities of signed in user'''

    def decorator(f):
        @wraps(f)
        def decorated_functions(*args, **kwargs):
            if current_user.username:
                flash("Operation already performed", 'info')
                return redirect(url)
            return f(*args, **kwargs)
        return decorated_functions
    return decorator







