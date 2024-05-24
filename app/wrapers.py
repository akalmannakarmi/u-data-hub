from functools import wraps
from flask import session,redirect,request,abort
from app.models import User

def isNotUser(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if 'userId' in session and User.isUser(session['userId']):
			return redirect('/')
		return func(*args, **kwargs)
	return decorated_function

def isUser(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if 'userId' in session and User.isUser(session['userId']):
			return func(*args, **kwargs)
		return redirect(f'/login?next={request.url}')
	return decorated_function

def isMod(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if 'userId' in session and User.isUser(session['userId']):
			return func(*args, **kwargs)
		abort(403,"You don't have the permission to access the requested resource. Require Moderator previlages")
	return decorated_function