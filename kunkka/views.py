from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.view import view_config
from datetime import datetime
from sqlalchemy.exc import DBAPIError
from logger import *
from db import get_last_booking_id
from pyramid.threadlocal import get_current_registry
from urllib import urlencode
from authentication import (
    get_username,
    check_user,
    Auth,
    checkOAuthUser
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
from oauth import auth_uri
@view_config(route_name='doc', renderer='josn')
def doc(request):
    try:
        session=get_session()
        one = session.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'kunkka'}


###----------------------------------OAuth Login---------------------------------------##    
@view_config(route_name='login', renderer='kunkka:templates/login.mako')
def login(request):
    data={'msg':'','project_name':'Kunkka'}        
    data["oauth_url"]=auth_uri
    if request.GET.has_key("code")==True:
        code=request.GET["code"]
        #password=request.POST["password"]
        #user=check_user(username,password)        
        #if user:
        #    request.session["username"]=user.username
        #    #headers = remember(request, username)    
        if checkOAuthUser(request,code)==True:
            user=request.user                        
            request.session["username"]=user.username
            return HTTPFound(location="/")    
        else:
            return data
    else:
        #log(request.session)              
        return data

###----------------------------------Old Login---------------------------------------##    
@view_config(route_name='old_login', renderer='kunkka:templates/login.mako')
def old_login(request):
    data={'msg':'','project_name':'Kunkka'}
    data["oauth_url"]=auth_uri
    print request.session
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=check_user(username,password)        
        if user:
            request.session["username"]=user.username
            #headers = remember(request, username)    
            return HTTPFound(location="/")
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

@view_config(route_name='transaction',renderer='kunkka:templates/aff.mako')
@Auth('oauth',authorize=True)
def transaction(request):
    username =""
    print request.session
    data={'name':'OTA Report','project_name':'Kunkka','error_msg':'','date_from':None,'date_to':None}
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

@view_config(route_name='OTA',renderer='kunkka:templates/OTA.mako')
@Auth('simple')
def OTA(request):
    log(request.default_data)
    data={'name':'OTA:Custom Report','project_name':'Kunkka','username':'heera','error_msg':'','date_from':None,'date_to':None}
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

@view_config(route_name='console',renderer='kunkka:templates/console.mako')
@Auth('oauth',authorize=True)
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


#----------------Magnus-----------------------------------------------#
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
#---------------------------------------------------------------------#

#----------------Courier----------------------------------------------#
@view_config(route_name='courier',renderer='json')
def courier_ack(request):
    #log(request.params)
    if request.params.has_key("key"):
        key=request.params["key"]
        if key=='courier':
            if request.method=="POST":
                return {'success':'true'}
            else:
                return {'success':True}
    return {'success':'false'}    
#--------------------------------------------------------------------#

# @view_config(route_name='rms',renderer='kunkka:templates/rms.mako')
# @Auth('oauth')
# def rms(request):
#     data={'msg_type':'success','message':'Pyramid is having a problem using your SQL database.  The problemmight be caused by one of the following things:','name':'Console:Custom Report','project_name':'Kunkka','username':'heera','error_msg':'Test error','date_from':None,'date_to':None}
#     return data
################################# GENERIC REPORT #####################################################

@view_config(route_name='report',renderer='kunkka:templates/report.mako')
@Auth('oauth',authorize=True)
def report(request):
    report_name=request.matchdict["fun"]    
    print report_name
    if report_name:
        report_path="/report_ajax/"+report_name+"/?"+urlencode(request.params)        
        data={'msg_type':'success','message':'','name':request.link.name,
            'project_name':'Kunkka',
            "report_path":report_path}
        return data
    else:
        return HTTPNotFound()


#################################GENERIC REPORT WITH DATE RANGE SEARCH ################################
@view_config(route_name='date_report',renderer='kunkka:templates/date_report.mako')
@Auth('oauth',authorize=True)
def date_report(request):
    report_name=request.matchdict["fun"]    
    print report_name
    if report_name:
        report_path="/report_ajax/"+report_name+"/?"+urlencode(request.params)
        date_from=None
        date_to=None
        if "from" in request.params:
            date_from=request.params["from"]
        if "to" in request.params:
            date_to=request.params["to"]
        data={'msg_type':'success','message':'','name':request.link.name,
            'project_name':'Kunkka',
            'date_from':date_from,'date_to':date_to,"report_path":report_path}
        return data
    else:
        return HTTPNotFound()





########################################################################################
## CUSTOM REPORTS

##VALIDATE PICKUPS
@view_config(route_name='junked_pickups',renderer='kunkka:templates/junk_pickups.mako')
@Auth('oauth',authorize=True)
def junk_pickups(request):
    
    pickups_path="/report_ajax/"+'junk_pickups/'
    city_list_path="/report_ajax/"+'get_area_city_list/'
    update_area_path="/report_ajax/"+'update_area_of_pickup/'

    data={'msg_type':'success','message':'','name':request.link.name,
        'project_name':'Kunkka',
        "pickups_path":pickups_path,
        "city_list_path":city_list_path,
        "update_area_path":update_area_path
        }
    return data

@view_config(route_name='providers',renderer='kunkka:templates/providers.mako')
@Auth('oauth',authorize=True)
def providers(request):    
    provider_path="/report_ajax/get_provider_status/?"+urlencode(request.params)        
    company_path="/report_ajax/get_company_status/?"+urlencode(request.params)        
    update_provider_status="/report_ajax/update_provider_status/?"+urlencode(request.params)        
    data={'msg_type':'success','message':'','name':request.link.name,
        'project_name':'Kunkka','username':'heera',
        "provider_path":provider_path,
        "company_path":company_path,
        "update_provider_status":update_provider_status
        }
    return data   

@view_config(route_name='home',renderer='kunkka:templates/home.mako')
@Auth('oauth')
def home(request):    
    provider_path="/report_ajax/get_provider_status/?"+urlencode(request.params)        
    print request.user
    data={'msg_type':'success','message':'','name':'Home',
        'project_name':'Kunkka','username':'heera'
        }
    return data

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

