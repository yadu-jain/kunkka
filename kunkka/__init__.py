from pyramid.renderers import JSON
from pyramid.config import Configurator
from pyramid.renderers import render
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import engine_from_config
import magnus_handler
import pymongo
import gds_api
import json
from urlparse import urlparse
from mongo import Mongo
import oauth
import mem_client
import email_sender
import fabric_api
from .models import (
    DBSession,
    Base,
    )

#authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
#authz_policy = ACLAuthorizationPolicy()



#--------------------Subscriber Filter-------------
class RequestPathStartsWith(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'path_startswith = %s' % (self.val,)

    phash = text
    def __call__(self, event):
        return event.request.path.startswith(self.val)
#----------------------------------------------

def notfound(request):
    return HTTPNotFound('Kunkka raises tide !!')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['session.secret']
        )
    
    config = Configurator(
        settings=settings,
        #root_factory=RootFactory,
        #authentication_policy=authn_policy,
        #authorization_policy=authz_policy,
        session_factory=session_factory
        )
    #config.set_authentication_policy(authn_policy)
    #config.set_authorization_policy(authz_policy)
    
    #config.include('pyramid_chameleon')    
    #config.set_default_permission()
    
    ##----------------- RMS EMAIL LIST-------------##
    try:
        email_sender.username   =settings['email_sender.username'].strip()
        email_sender.password   =settings['email_sender.password'].strip()
        email_sender.html_file  =settings['email_sender.template'].strip()
        email_sender.PROVIDER_UPDATE_LIST=[email.strip() for email in settings['email_list.PROVIDER_UPDATE_LIST'].split(",")]
    except Exception as e:
        print e

    ##---------------------------------------------------##

    
    ##-----------------Fabric----------------------##
    fabric_api.temp_path=settings['fabric_api.temp_path'].strip()
    ##---------------------------------------------##


    ##-----------------gds Memcache Server---------##
    try:
        mem_client.host = settings['gds_memcache']
    except Exception as e:
        print e
    ##---------------------------------------------##


    
    ##------------------gds_api--------------------##
    try:
        gds_api.api_key = settings['gds.api_key']
        gds_api.api_url = settings['gds.api_url']
        gds_api.api_file= settings['gds.api_file']
        #if gds_api.test()==True:            
        with open(gds_api.api_file,'rb') as gds_api_file:
            api=json.load(gds_api_file)                
            gds_api.create_gds_api(api["methods"])
        #else:
        #    print "Failed to connect gds !"

    except Exception as e:
        print e
    ##---------------------------------------------##



    ##------------------OAuth----------------------##
    oauth.CLIENT_ID=settings['oauth.CLIENT_ID']
    oauth.CLIENT_SECRET=settings['oauth.CLIENT_SECRET']
    oauth.REDIRECT_URI=settings['oauth.REDIRECT_URI']
    oauth.SCOPES=settings['oauth.SCOPES'].split(",")    
    oauth.init_oauth()
    ##---------------------------------------------##


    ##------------------MongoDB-------------------_###
    # mongo_db_url = urlparse(settings['mongo_uri'])
    # Mongo.conn = pymongo.Connection(
    #    host=mongo_db_url.hostname,
    #    port=mongo_db_url.port,
    # )
    # Mongo.username=mongo_db_url.username
    # Mongo.password=mongo_db_url.password
    ###-------------------------------------------#####


    ##--------------------Default Data------------#####
    def default_data(request):
        return {"message":"","msg_type":""}
    config.add_request_method(default_data, 'default_data', property=True)    
    print default_data
    ##--------------------------------------------#####



    #config.add_request_method(Mongo, 'mongo', reify=True)    
    config.add_static_view('static', 'kunkka:static', cache_max_age=3600)
    config.include('pyramid_mako')
    config.add_route('home', '/')
    config.add_route('rms', '/rms/')    
    config.add_route('login', '/login/')
    config.add_route('old_login', '/old_login/')
    config.add_route('logout', '/logout/')
    config.add_route('transaction', '/aff/')    
    config.add_route('OTA','/OTA/')
    config.add_route('console','/console/')
    config.add_route('chart', '/chart/{type}/')    
    config.add_route('doc', '/doc/')
    config.add_route('magnus', '/magnus/')
    config.add_route('courier', '/courier/')
    config.add_route('run_query','/mongo/run/')
    config.add_route('new_query','/mongo/new/')
    config.add_route('save_query','/mongo/save/')
    config.add_route('rest','/rest/{fun}/')
    config.add_route('report_ajax','/report_ajax/{fun}/')    
    config.add_route('report','/report/{fun}/')
    config.add_route('date_report','/date_report/{fun}/')
    config.add_route('junked_pickups','/junk_pickups/')
    config.add_route('providers','/providers/')    
    config.add_route('gds_inventory','/gds_inventory/')    
    config.add_route('city_management','/city_management/')    
    config.add_route('user_management','/user_management/')    
    config.add_route('group_management','/group_management/')    
    config.add_route('refresh_routes','/refresh_routes/')    
    config.add_route('service_report_ajax','/service_report_ajax/{fun}')    
    config.add_route('refresh_route_pickups','/refresh_route_pickups/')
    # config.add_route('company_details','/company_details/')
    config.add_route('operators_payment','/operators_payment/')
    #config.add_route('admin','/admin/')
    config.add_notfound_view(notfound, append_slash=True)
    config.add_subscriber_predicate('magnus', RequestPathStartsWith)
    config.add_subscriber_predicate('courier',RequestPathStartsWith)
    config.add_renderer('prettyjson', JSON(indent=4,sort_keys=False))
    config.scan()
    return config.make_wsgi_app()
