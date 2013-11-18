from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import engine_from_config
import magnus_handler
from .models import (
    DBSession,
    Base,
    )

def notfound(request):
    return HTTPNotFound('Kunkka raises tide !!')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')    
    config.add_static_view('static', 'kunkka:static', cache_max_age=3600)
    config.add_route('home', '')
    config.add_route('transaction', '/tran/')    
    config.add_route('chart', '/chart/OTS/{type}/')    
    config.add_route('doc', '/doc/')
    config.add_route('magnus', '/magnus/')
    config.add_notfound_view(notfound, append_slash=True)
    config.add_subscriber_predicate('magnus', magnus_handler.RequestPathStartsWith)
    config.scan()
    return config.make_wsgi_app()
