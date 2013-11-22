from db import get_user
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    )
def get_username(request):
	if "username" in request.session:
		username=request.session["username"]
		if username.strip()!='':
			user=get_user(username.strip())
			request.username=user.username
			return username

def check_user(username,password):
	if username.strip()!='' and password.strip()!='':
		user=get_user(username.strip(),password.strip())
		return user
	return None

class Auth(object):
	def __init__(self,type):
		self.type=type
	def __call__(self,fun):			
		def wrapper(*args, **kwargs):
			print args
			request=args[1]
			if get_username(request):
				return fun(*args[1:], **kwargs)
			else:
				return HTTPFound(location='/login/')

		return wrapper

