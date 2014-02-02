from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import engine_from_config
import magnus_handler
import pymongo
from urlparse import urlparse
from mongo import Mongo
from oauth import init_oauth
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

    ##------------------OAuth----------------------##
    init_oauth()
    ##------------------MongoDB-------------------_###
    mongo_db_url = urlparse(settings['mongo_uri'])
    Mongo.conn = pymongo.Connection(
       host=mongo_db_url.hostname,
       port=mongo_db_url.port,
    )
    Mongo.username=mongo_db_url.username
    Mongo.password=mongo_db_url.password
    ###-------------------------------------------#####
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
    config.add_notfound_view(notfound, append_slash=True)
    config.add_subscriber_predicate('magnus', RequestPathStartsWith)
    config.add_subscriber_predicate('courier',RequestPathStartsWith)
    config.scan()
    return config.make_wsgi_app()
