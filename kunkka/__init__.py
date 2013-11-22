from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import engine_from_config
import magnus_handler
from .models import (
    DBSession,
    Base,
    )

#authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
#authz_policy = ACLAuthorizationPolicy()

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
    config.add_static_view('static', 'kunkka:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login/')
    config.add_route('logout', '/logout/')
    config.add_route('transaction', '/aff/')    
    config.add_route('chart', '/chart/OTS/{type}/')    
    config.add_route('doc', '/doc/')
    config.add_route('magnus', '/magnus/')
    config.add_route('console','/console/')
    config.add_route('rest','/rest/{fun}/')
    config.add_notfound_view(notfound, append_slash=True)
    config.add_subscriber_predicate('magnus', magnus_handler.RequestPathStartsWith)
    config.scan()
    return config.make_wsgi_app()
