from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import engine_from_config
import magnus_handler
#import pymongo
from urlparse import urlparse
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

    ##------------------MongoDB-------------------_###
    #db_url = urlparse(settings['mongo_uri'])
    #config.registry.mongo_db = pymongo.Connection(
    #   host=db_url.hostname,
    #   port=db_url.port,
    #)
    #def add_db(request):
    #   db = config.registry.db[db_url.path[1:]]
    #   if db_url.username and db_url.password:
    #       db.authenticate(db_url.username, db_url.password)
    #   return db
    ###-------------------------------------------#####
    #config.add_request_method(add_db, 'db', reify=True)
    config.add_static_view('static', 'kunkka:static', cache_max_age=3600)
    config.include('pyramid_mako')
    config.add_route('home', '/')
    config.add_route('login', '/login/')
    config.add_route('logout', '/logout/')
    config.add_route('transaction', '/aff/')    
    config.add_route('chart', '/chart/{type}/')    
    config.add_route('doc', '/doc/')
    config.add_route('magnus', '/magnus/')
    config.add_route('courier', '/courier/')
    config.add_route('OTA','/OTA/')
    config.add_route('rest','/rest/{fun}/')
    config.add_notfound_view(notfound, append_slash=True)
    config.add_subscriber_predicate('magnus', RequestPathStartsWith)
    config.add_subscriber_predicate('courier',RequestPathStartsWith)
    config.scan()
    return config.make_wsgi_app()
