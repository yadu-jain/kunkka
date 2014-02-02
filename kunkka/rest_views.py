from datetime import datetime
from pyramid.response import Response
from pyramid.view import view_config
from datetime import datetime
from sqlalchemy.exc import DBAPIError
from logger import *
from mongo import Mongo
from collections import OrderedDict
import console
from authentication import (
    Auth,
    check_admin,
    enable_admin
    )
from .models import (
    get_session,
    )    
import db
def row2dict(row):
	d=OrderedDict()
	if type(row)==dict:
		return OrderedDict(row)
	print row.__table__.columns
	print "Converting"
	for column in row.__table__.columns:
		val=getattr(row, column.name)
		if val and type(val)==datetime:
			d[column.name]=val.strftime("%y-%M-%d %h-%m-%s")
		else:
			d[column.name] = val
	return d

def JSON_NOT_FOUND(request,msg=None):
	if msg==None:
		msg="Invalid rest url !"
	return {"success":"false","msg":msg}

@view_config(route_name='chart',renderer='json')
@Auth('simple')
def chart(request):
	rest_name=request.matchdict["type"]	
	fields=request.params
	if db.query_set.has_key(rest_name):
		return db.query_set[rest_name](fields)
	else:
		return JSON_NOT_FOUND(request)

@view_config(route_name='rest',renderer='json')
@Auth('simple')
def rest(request):
	rest_name=request.matchdict["fun"]	
	fields={i:request.params[i] for i in request.params}
	print fields
	if db.rest.has_key(rest_name):
		try:
			result=db.rest[rest_name](**fields)			
			if result:
				print result
				data= [row2dict(row) for row in result]
				return {"success":True,"data":data}
			else:
				return {"success":False,"msg":"Not found !"}
		except Exception as e:
			print e
			return JSON_NOT_FOUND(request)
	else:
		return JSON_NOT_FOUND(request)

@view_config(route_name='run_query',renderer='json')
@Auth('simple')
def run_query(request):	
	log(request.params)
	str_from=request.params["from"]
	str_to=request.params["to"]
	date_from=datetime.strptime(str_from,"%Y-%m-%d")
	date_to=datetime.strptime(str_to,"%Y-%m-%d")	

	###Validation
	
	arguments=[]
	if "args" in request.params and len(request.params["args"])>0:
		arguments=request.params["args"].split(",")
	if  date_from > date_to:
		return {"success":False,"msg":"Invalid From-to Date"}
	#####

	if "query" in request.params:
		if "db_name" in request.params:
			db_name=request.params["db_name"]
		else:
			return {"success":False,"msg":"db_name not specified!"}
		if "coll" in request.params:
			coll=request.params["coll"]	
		else:
			return {"success":False,"msg":"coll(collection name) not specified!"}		
		str_query=request.params["query"]
		if enable_admin==True and check_admin(request)==False:
			return {"success":False,"msg":"Invalid Admin password!"}		
		data,raw_data=console.Query.execute_str(str_query,db_name,date_from,date_to,arguments,coll)
		try:
			return {"success":True,"data":data,"raw_data":raw_data}
		except Exception as ex:
			return {"success":False,"msg":str(ex)}	
		
	elif "id" in request.params:		
		str_query_id=request.params["id"]
		if len(str_query_id) >0:
			try:
				query=console.Query(id=str_query_id)
				if query and query.mongoQuery.level==1:
					if enable_admin==True and check_admin(request)==False:
						return {"success":False,"msg":"Invalid Admin password!"}					
				data,raw_data=query.execute(date_from,date_to,arguments)
			except Exception as ex:
				return {"success":False,"msg":str(ex)}					
			return {"success":True,"data":data,"raw_data":raw_data}
		else:
			return {"success":False,"msg":"Invalid Query"}
	else:
		return {"success":False,"msg":"Query not specified !"}

@view_config(route_name='new_query',renderer='json')
@Auth('simple')
def new_query(request):		
	return {"success":True,"default_text":console.default_text}

@view_config(route_name='save_query',renderer='json')
@Auth('simple')
def save_query(request):
	try:
		if enable_admin==True and check_admin(request)==False:
			return {"success":False,"msg":"Invalid Admin password!"}	
		query_id=int(request.params["id"])
		name=request.params["name"]
		str_query=request.params["query"]
		db_name=request.params["db_name"]
		coll=request.params["coll"]
		args_count=request.params["args_count"]
		level=request.params["level"]
		dict_query={"db_name":db_name,"coll":coll,"str_query":str_query}
		if query_id==-1:
			query=console.Query()
			updated_result=query.save(name,args_count,dict_query,level)			
			return {"success":True,"query":row2dict(updated_result)}
		else:
			query=console.Query(query_id)
			updated_result=query.save(name,args_count,dict_query,level)
			return {"success":True,"query":row2dict(updated_result)}
	except Exception as e:
		return {"success":False,"msg":str(e)}

