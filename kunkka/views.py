from pyramid.response import Response
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.view import view_config
from datetime import datetime
from sqlalchemy.exc import DBAPIError
from logger import *
from db import get_last_booking_id
from authentication import (
    get_username,
    check_user,
    Auth
    )
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
    )
from .models import (
    get_session,
    )

@view_config(route_name='doc', renderer='josn')
def doc(request):
    try:
        session=get_session()
        one = session.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'kunkka'}

@view_config(route_name='home')
@Auth('simple')
def home(request):    
    return HTTPMovedPermanently('/aff/')
###----------------------------------Login---------------------------------------##    
@view_config(route_name='login', renderer='kunkka:templates/login.mak')
def login(request):
    data={'msg':'','project_name':'Kunkka'}
    print request.session
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=check_user(username,password)        
        if user:
            request.session["username"]=user.username
            #headers = remember(request, username)    
            return HTTPFound(location="/aff/")
        else:
            data['msg']='Invalid Login Id and password'
    else:
        log(request.session)               
    return data
@view_config(route_name='logout')
def logout(request):
    request.session.invalidate()
    return HTTPFound(location="/login/")
##-------------------------------------------------------------------------------##

@view_config(route_name='transaction',renderer='kunkka:templates/report.mak')
@Auth('simple')
def transaction(request):
    username =""
    print request.session
    data={'name':'OTS Report','project_name':'Kunkka','error_msg':'','date_from':None,'date_to':None}
    if request.GET.has_key("from") and request.GET.has_key("to"):
        log(request.GET["from"])
        log(request.GET["to"]) 
        #date format= '2013-07-07'
        str_from=request.GET["from"]
        str_to=request.GET["to"]
        try:
            date_from=datetime.strptime(str_from,'%Y-%m-%d')       
            date_to=datetime.strptime(str_to,'%Y-%m-%d')       
            if date_to<date_from:
                data['error_msg']='Invalid Range !'
            else:
                data["date_from"]=str_from
                data["date_to"]=str_to
        except Exception as e:
            log(str(e))
            data['error_msg']=str(e)        
    else:
        today=datetime.now()
        str_today=today.strftime('%Y-%m-%d')
        data["date_from"]=str_today
        data["date_to"]=str_today     
    return data

@view_config(route_name='console',renderer='kunkka:templates/console.mak')
@Auth('simple')
def console(request):
    log(request.GET)
    data={'name':'Console:Custom Report','project_name':'Kunkka','username':'heera','error_msg':'','date_from':None,'date_to':None}
    if request.GET.has_key("from") and request.GET.has_key("to"):
        log(request.GET["from"])
        log(request.GET["to"]) 
        #date format= '2013-07-07'
        str_from=request.GET["from"]
        str_to=request.GET["to"]
        try:
            date_from=datetime.strptime(str_from,'%Y-%m-%d')       
            date_to=datetime.strptime(str_to,'%Y-%m-%d')       
            if date_to<date_from:
                data['error_msg']='Invalid Range !'
            else:
                data["date_from"]=str_from
                data["date_to"]=str_to
        except Exception as e:
            log(str(e))
            data['error_msg']=str(e)        
    else:
        today=datetime.now()
        str_today=today.strftime('%Y-%m-%d')
        data["date_from"]=str_today
        data["date_to"]=str_today        
    return data

@view_config(route_name='magnus',renderer='json')
def magnus_ack(request):
    #log(request.params)
    if request.params.has_key("key"):
        key=request.params["key"]
        if key=='magnus':
            if request.method=="POST":
                return {'success':'true'}
            else:
                return {'success':True,'id':get_last_booking_id()}
    return {'success':'false'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_kunkka_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

