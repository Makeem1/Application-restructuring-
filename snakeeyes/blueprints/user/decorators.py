from flask import redirect, flash 
from functools import wraps

from flask_login import current_user

def anonymous_required(url='/settings'):
	"""This function help to prevent the user to visit the login page after login"""  

	def decorator(f):
		@wraps(f)
		def decorated_functions(*args, **kwargs):
			if current_user.is_authenticated:
				flash("Operation already performed", 'info')
				return redirect(url)
			return f(*args, **kwargs)
		return decorated_functions
	return decorator









