import db
import oauth
from authorization import getAuthorizedLinks,authorizeResource
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    )
enable_admin=True
def get_username(request):
	if "username" in request.session:
		username=request.session["username"]
		if username.strip()!='':
			user=db.get_user(username.strip())
			if user:			
				request.username=user.username
				request.user=user
				getAuthorizedLinks(request)
				return username
			else:
				return None

def check_user(username,password):
	if username.strip()!='' and password.strip()!='':
		user=db.get_user(username.strip(),password.strip(),None,username.strip())
		return user
	return None
def check_admin(request):
	if "adminPwd" in request.params and request.params["adminPwd"]=="sitnam123":
		return True
	else:
		return False
def checkOAuthUser(request,code):
	try:
		service  = oauth.get_service(code)
		response = service.people().get(userId='me').execute()
		oauth_id = response["id"]		
		domain   = response["domain"]
		emails   = response["emails"]		
		username = emails[0]["value"]
		name     = response["displayName"]
		print response		
		print username
		if domain=="travelyaari.com":			
			user=db.get_user(username,None,oauth_id,name)						
			request.user=user
			getAuthorizedLinks(request)
			print request.allowed_links
			return True
		else:
			request.msg="INVALID_DOMAIN"	
			return False
	except Exception as ex:
		print ex

		request.msg="AUTHENTICATION_FAILED"
		print request.msg
		return False



class Auth(object):
	def __init__(self,type,authorize=False):
		self.type=type
		self.authorize=authorize
	def __call__(self,fun):	
		def simple_wrapper(*args, **kwargs):
			print args
			print kwargs
			request=args[1]
			request.login_url='/old_login/'
			if get_username(request):				
				return fun(*args[1:], **kwargs)							
			else:
				return HTTPFound(location=request.login_url)

		
		def oauth_wrapper(*args, **kwargs):
			print args
			print kwargs
			request=args[1]
			request.login_url='/login/'			
			if get_username(request):
				if self.authorize==False or authorizeResource(request)==True:
					return fun(*args[1:], **kwargs)
				else:
					print "Authorization Failed !"
					return HTTPNotFound("")				
			else:
				return HTTPFound(location='/login/')
		if self.type=='simple':
			return simple_wrapper	
		elif self.type=='oauth':			
			return oauth_wrapper
		else:
			return HTTPNotFound()

