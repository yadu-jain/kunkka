from pyramid.response import Response
from pyramid.view import view_config
from datetime import datetime
from sqlalchemy.exc import DBAPIError
from logger import *
from .models import (
    DBSession,
    )    
import db

def JSON_NOT_FOUND(request,msg=None):
	if msg==None:
		msg="Invalid rest url !"
	return {"success":"false","msg":msg}

@view_config(route_name='chart',renderer='json')
def chart(request):
	rest_name=request.matchdict["type"]	
	fields=request.params
	if db.query_set.has_key(rest_name):
		return db.query_set[rest_name](fields)
	else:
		return JSON_NOT_FOUND(request)

@view_config(route_name='rest',renderer='json')
def rest(request):
	rest_name=request.matchdict["fun"]	
	fields=request.params
	if db.rest.has_key(rest_name):
		return {"success":True,"data":db.rest[rest_name]}
	else:
		return JSON_NOT_FOUND(request)