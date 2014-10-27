import transaction
from datetime import tzinfo
import datetime
from pyramid.renderers import *
from logger import *
from sqlalchemy import engine_from_config
from sqlalchemy import func
from sqlalchemy.sql import select
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
import json
import pickle
from .models import (
	Base,    
    Booking,
    get_session,
    User,
    Links,
    Perms
    )
from models import *
query_set={}
rest={}
engine = Base.metadata.bind
##Queries:

#Reporter Query
def update_perms_links(name,group_ids,path,enabled,category):
	"""
	Returns list of links having perm id
	"""	
	session=get_session()	

	cursor=session.query(Links).from_statement("""
			SELECT * FROM links l WHERE l.path=:path;
			""").params({"path":path})
	temp=cursor.first()
	print "saving..."
	print temp
	if not temp:
		temp=Links(path=path)
		temp.name=name
		temp.enabled=enabled
		temp.category=category	

		db_session=sessionmaker(bind=Base.metadata.bind)	
		new_session=db_session()
		new_session.add(temp)        	        	
		new_session.commit()        	
		new_session.close()
	else:
		db_session=sessionmaker(bind=Base.metadata.bind)	
		new_session=db_session()
		
		temp=new_session.merge(temp)
		temp.name=name
		temp.enabled=enabled
		temp.category=category	
		new_session.add(temp)        	        	
		new_session.commit()        	
		new_session.close()
		print temp
		
	print path
	
	session=get_session()	
	cursor=session.query(Links).from_statement("""
			SELECT * FROM links l WHERE l.path=:path;
			""").params({"path":path})
	temp=cursor.first()
	link_id=temp.link_id	
	for group_id in group_ids:
		cursor=session.query(Perms).from_statement("""
			SELECT * FROM perms p WHERE p.link_id=:link_id and p.group_id=:group_id;
			""").params({"link_id":link_id,"group_id":group_id})
		temp=cursor.first()		
		if not temp:
			temp=Perms(link_id=link_id,group_id=group_id)			
			db_session=sessionmaker(bind=Base.metadata.bind)	
			new_session=db_session()
			new_session.add(temp)        	        	
			new_session.commit()        	
			new_session.close()

	##---Disabling and enabling  perm's groups ##
	str_group_ids="("+",".join([unicode(group_id)for group_id in group_ids]) +")"
	db_session=sessionmaker(bind=Base.metadata.bind)	
	new_session=db_session()
	new_session.execute("""
		UPDATE perms 
		SET enabled=0 
		WHERE link_id=:link_id and group_id not in %s
		""" %str_group_ids,{"link_id":link_id})
	new_session.execute("""
		UPDATE perms 
		SET enabled=1 
		WHERE link_id=:link_id and group_id in %s
		""" %str_group_ids,{"link_id":link_id})	
	new_session.commit()        	
	new_session.close()

	return 1


#Permission Queries
def get_perms_links(strPerms):
	"""
	Returns list of links having perm id
	"""
	print strPerms
	session=get_session()
	if "1" in strPerms.split(","):
		cursor=session.query(Links).from_statement("""
			SELECT l.* from links l 
			inner join perms p on p.link_id=l.link_id 
			where p.enabled=1 order by l.name;			
			""")	
	else:		
		cursor=session.query(Links).from_statement("""
				SELECT l.* from links l 
				inner join perms p on p.link_id=l.link_id 
				where p.group_id in (%s) and p.enabled=1 order by l.name;			
				""" % strPerms)	
		
	return cursor.all()


#Console Queries:
def get_query_list():
	"""
	query(User).from_statement(
...                     "SELECT * FROM users where name=:name").\
...                     params(name='ed').all()
	"""
	session=get_session()

	cursor=session.query(MongoQuery).from_statement("""
			SELECT id,name,level,created_user,args_count from queries limit 100;
			""")
	temp=cursor.all()
	return temp

def get_query(id,load_query=False):
	#db_session=sessionmaker(bind=Base.metadata.bind)
	session=get_session()
	text_fields=""
	if load_query==True:
		text_fields=",_str_query,_arguments"
	query_cursor=session.query(MongoQuery).from_statement("""
			SELECT id,name,level,last_updated,created_user %s from queries where id=:id limit 1;
			""" % text_fields).params({"id":int(id)})
	temp=query_cursor.all()		
	return temp

def get_user(username,password=None,oauth_id=None,name=""):
	session=get_session()
	db_session=None
	
	if password:
		cursor=session.execute("""
			SELECT * from users where username=:username and password=:password;
			""",{"username":username,"password":password})
		temp_user=cursor.first()
		cursor.close()
		return temp_user
	else:

		cursor=session.execute("""
			SELECT * from users where username=:username;
			""",{"username":username})
		print cursor
		temp_user=cursor.first()
		cursor.close()

		print temp_user
		if temp_user==None and oauth_id:
			print 'Creating..'
			db_session=sessionmaker(bind=Base.metadata.bind)
			print 'db_session'			
			user=User(username,oauth_id,name)			
			db=db_session()
			db.add(user)        	        	
			db.commit()        	
			db.close()
			session=get_session()
			cursor=session.execute("""
					SELECT * from users where username=:username;
				""",{"username":username})
			temp_user = cursor.first()
			print "created"
		elif temp_user==None:
			temp_user=None

		return temp_user

def get_last_booking_id():
	session=get_session()
	cursor=session.execute("""
		SELECT MAX(booking_id) id from bookings;;
		""")
	data=cursor.first()
	if data and data.id:
		return int(data.id)
	return 0
def bookings(fields):	
	x_axis_title 	="Agents Report"
	y_axis_title 	="Total"
	result_type		="Bookings"	
	chart_template	='kunkka:templates/charts/ots.mak'		
	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				
	print result_type
	log(from_date)
	log(to_date)
	session=get_session()
	result_set=None
	same_date=False
	if from_date==to_date:
		#On a date, hour wise
		same_date=True
		next_date=datetime.timedelta(days=1)+from_date
		temp_date=from_date.strftime("%y-%m-%d")
		temp_date_next=next_date.strftime("%y-%m-%d")

		result=session.execute("""
		SELECT agent_id, agent_name,date_time,count(*) AS total 
		FROM(
			SELECT HOUR(B.booking_date) as date_time,B.* from bookings B
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :temp_date and booking_date < :temp_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"temp_date":temp_date,"temp_date_next":temp_date_next})
		result_set=result

	else:
		#Range: from_date-to_date
		to_date_next=datetime.timedelta(days=1)+to_date
		result=session.execute("""
		SELECT agent_id, agent_name,date_time,count(*) AS total 
		FROM(
			SELECT DATE(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :from_date and booking_date < :to_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"from_date":from_date,"to_date_next":to_date_next})
		result_set=result
	str_chart=render(chart_template,{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={}
	for item in result_set.fetchall():
		if not temp_done.has_key(item.agent_name):
			d={"name":item.agent_name,"data":[]}
			series.append(d)
			temp_done[item.agent_name]=d
			
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time+1)
		else:
			y_axis=datetime.datetime(item.date_time.year,item.date_time.month,item.date_time.day)
		#input as IST									
		y_axis=y_axis+datetime.timedelta(hours=5,minutes=30)
		
		y_axis=int(y_axis.strftime("%s"))*1000		
		temp_done[item.agent_name]["data"].append([y_axis,int(item.total)])
	chart["series"]=series

	##Chart Properties
	chart["title"]["text"]=x_axis_title
	chart["subtitle"]["text"]=result_type
	chart["yAxis"]["title"]["text"]=y_axis_title
	startingPoint=from_date+datetime.timedelta(hours=5,minutes=30)
	chart["plotOptions"]["spline"]["pointStart"]=int(startingPoint.strftime("%s"))*1000			
	return chart

def seats(fields):	
	x_axis_title 	="Agents Report"
	y_axis_title 	="Total"
	result_type		="Seats"
	chart_template	='kunkka:templates/charts/ots.mak'			
	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				
	print result_type
	log(from_date)
	log(to_date)
	session=get_session()
	result_set=None
	same_date=False
	if from_date==to_date:
		#On a date, hour wise
		same_date=True
		next_date=datetime.timedelta(days=1)+from_date
		temp_date=from_date.strftime("%y-%m-%d")
		temp_date_next=next_date.strftime("%y-%m-%d")

		result=session.execute("""
		SELECT agent_id, agent_name,date_time,sum(total_seats) AS total 
		FROM(
			SELECT HOUR(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :temp_date and booking_date < :temp_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"temp_date":temp_date,"temp_date_next":temp_date_next})
		result_set=result

	else:
		#Range: from_date-to_date
		to_date_next=datetime.timedelta(days=1)+to_date
		result=session.execute("""
		SELECT agent_id, agent_name,date_time,sum(total_seats) AS total 
		FROM(
			SELECT DATE(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :from_date and booking_date < :to_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"from_date":from_date,"to_date_next":to_date_next})
		result_set=result
	str_chart=render(chart_template,{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={}
	for item in result_set.fetchall():
		if not temp_done.has_key(item.agent_name):
			d={"name":item.agent_name,"data":[]}
			series.append(d)
			temp_done[item.agent_name]=d
			
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time+1)
		else:
			y_axis=datetime.datetime(item.date_time.year,item.date_time.month,item.date_time.day)
		#input as IST									
		y_axis=y_axis+datetime.timedelta(hours=5,minutes=30)
		
		y_axis=int(y_axis.strftime("%s"))*1000		
		temp_done[item.agent_name]["data"].append([y_axis,int(item.total)])
	chart["series"]=series

	##Chart Properties
	chart["title"]["text"]=x_axis_title
	chart["subtitle"]["text"]=result_type
	chart["yAxis"]["title"]["text"]=y_axis_title
	startingPoint=from_date+datetime.timedelta(hours=5,minutes=30)
	chart["plotOptions"]["spline"]["pointStart"]=int(startingPoint.strftime("%s"))*1000				
	return chart

def amount(fields):	
	x_axis_title 	="Agents Report"
	y_axis_title 	="Total"
	result_type		="Amount"			
	chart_template	='kunkka:templates/charts/ots.mak'
	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				
	print result_type
	log(from_date)
	log(to_date)
	session=get_session()
	result_set=None
	same_date=False
	if from_date==to_date:
		#On a date, hour wise
		same_date=True
		next_date=datetime.timedelta(days=1)+from_date
		temp_date=from_date.strftime("%y-%m-%d")
		temp_date_next=next_date.strftime("%y-%m-%d")

		result=session.execute("""
		SELECT agent_id, agent_name,date_time,sum(amount) AS total 
		FROM(
			SELECT HOUR(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :temp_date and booking_date < :temp_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"temp_date":temp_date,"temp_date_next":temp_date_next})
		result_set=result

	else:
		#Range: from_date-to_date
		to_date_next=datetime.timedelta(days=1)+to_date
		result=session.execute("""
		SELECT agent_id, agent_name,date_time,sum(amount) AS total 
		FROM(
			SELECT DATE(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :from_date and booking_date < :to_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"from_date":from_date,"to_date_next":to_date_next})
		result_set=result
	str_chart=render(chart_template,{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={}
	for item in result_set.fetchall():
		if not temp_done.has_key(item.agent_name):
			d={"name":item.agent_name,"data":[]}
			series.append(d)
			temp_done[item.agent_name]=d
			
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time+1)
		else:
			y_axis=datetime.datetime(item.date_time.year,item.date_time.month,item.date_time.day)
		#input as IST									
		y_axis=y_axis+datetime.timedelta(hours=5,minutes=30)
		
		y_axis=int(y_axis.strftime("%s"))*1000		
		temp_done[item.agent_name]["data"].append([y_axis,int(item.total)])
	chart["series"]=series

	##Chart Properties
	chart["title"]["text"]=x_axis_title
	chart["subtitle"]["text"]=result_type
	chart["yAxis"]["title"]["text"]=y_axis_title
	startingPoint=from_date+datetime.timedelta(hours=5,minutes=30)
	chart["plotOptions"]["spline"]["pointStart"]=int(startingPoint.strftime("%s"))*1000			
	return chart

#### OTA####
def id_value_list(str_sql):
	def fun():
		session=get_session()	
		result=session.execute(str_sql())
		print str_sql()	
		return [{"id":item.id,"name":item.name} for item in result.fetchall()]
	return fun

@id_value_list
def agent_list():
	return """
		SELECT agent_id as id,name from agents;
	"""

	

@id_value_list
def provider_list():
	return """
		SELECT provider_id as id,name from providers;
	"""	

	
@id_value_list
def tier_list():
	return """
		SELECT tier_id as id,name from tiers;
	"""
	


ota_filters={
"agent":{"field_name":"agent_id"}
,"provider":{"field_name":"provider_id"}
#,"Tier":{"field_name":tier}
}
##TODO
result_types={
"booking":{"title":"Booking","select":""},
}

def OTA(fields):
	chart_template	='kunkka:templates/charts/ots.mak'
	applied_filters =[]
	applied_filter_values={}
	for key in ota_filters.keys():
		if fields.has_key(key) and fields[key]!="":
			field_name=ota_filters[key]["field_name"]
			applied_filters.append(field_name+"=:"+field_name)
			applied_filter_values[field_name]=fields[key]

	#if not result_types.has_key(result_type):
	#	return {}

	x_axis_title 	= "Booked/Cancelled/Failed Report"
	#result_type		= "Filter by "+",".join([key+"="+'<span class="info">'+applied_filter_values[key]+'</span>' for key in applied_filter_values.keys()])
	y_axis_title	= "Count"

	

	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				

	log(from_date)
	log(to_date)
	session=get_session()
	result_set=None
	same_date=False
	if from_date==to_date:
		#On a date, hour wise
		same_date=True
		next_date=datetime.timedelta(days=1)+from_date
		temp_date=from_date.strftime("%y-%m-%d")
		temp_date_next=next_date.strftime("%y-%m-%d")

		applied_filters.append("booking_date>= :temp_date")
		applied_filters.append("booking_date < :temp_date_next")

		applied_filter_str = " WHERE "+" AND ".join(applied_filters)

		applied_filter_values["temp_date"]=temp_date
		applied_filter_values["temp_date_next"]=temp_date_next
		result=session.execute("""
		SELECT status,date_time,count(*) AS total 
		FROM(
			SELECT HOUR(B.booking_date) as date_time,
			CASE B.status
				WHEN "B" THEN "B"
				WHEN "C" THEN "C"
				ELSE "F"
			END
			AS status
			FROM bookings B 			
			%s ) A 
		GROUP BY status,date_time;
		""" % applied_filter_str,applied_filter_values)
		result_set=result

	else:
		#Range: from_date-to_date
		to_date_next=datetime.timedelta(days=1)+to_date

		applied_filters.append("booking_date>= :from_date")
		applied_filters.append("booking_date < :to_date_next")

		applied_filter_str = " WHERE "+" AND ".join(applied_filters)

		applied_filter_values["from_date"]=from_date
		applied_filter_values["to_date_next"]=to_date_next

		result=session.execute("""
		SELECT status,date_time,count(*) AS total 
		FROM(
			SELECT DATE(B.booking_date) as date_time,
			CASE B.status
				WHEN "B" THEN "B"
				WHEN "C" THEN "C"
				ELSE "F"
			END
			AS status
			FROM bookings B 
			%s) A 
		GROUP BY status,date_time;
		""" % applied_filter_str,applied_filter_values)
		result_set=result
	str_chart=render(chart_template,{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={"B":[],"C":[],"F":[]}	

	for item in result_set.fetchall():					
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time+1)
		else:
			y_axis=datetime.datetime(item.date_time.year,item.date_time.month,item.date_time.day)
		#input as IST									
		y_axis=y_axis+datetime.timedelta(hours=5,minutes=30)
		
		y_axis=int(y_axis.strftime("%s"))*1000		
		temp_done[item.status].append([y_axis,int(item.total)])	
	chart["series"]=[{"name":"Booked","data":temp_done["B"],"color":"green"}, {"name":"Cancelled","data":temp_done["C"],"color":"yellow"}, {"name":"Failed","data":temp_done["F"],"color":"red"}]
	##Chart Properties
	chart["title"]["text"]=x_axis_title
	#chart["subtitle"]["text"]=result_type
	chart["yAxis"]["title"]["text"]=y_axis_title
	startingPoint=from_date+datetime.timedelta(hours=5,minutes=30)
	chart["plotOptions"]["spline"]["pointStart"]=int(startingPoint.strftime("%s"))*1000			
	return chart
def today_failed(fields):	
	return {}

##------------------Chart Data methods set-------------------##
##----name--------------------Function Name-----------##
query_set["today_failed"]	= today_failed
query_set["Bookings"] 		= bookings
query_set["Seats"] 			= seats
query_set["Amount"]			= amount
query_set["OTA"] 			= OTA

##------------------Rest Data methods set-------------------##
##----name--------------------Function Name-----------##
rest["agents"] 				= agent_list
rest["providers"] 			= provider_list
rest["query_list"] 			= get_query_list
rest["query"]				= get_query
#rest["tiers"]=tier_list


