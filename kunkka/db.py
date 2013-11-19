import transaction
from datetime import tzinfo
import datetime
from pyramid.renderers import *
from logger import *
from sqlalchemy import engine_from_config
from sqlalchemy import func
from sqlalchemy.sql import select
import json
from .models import (
	Base,
    DBSession,
    Booking,
    )

query_set={}
engine = Base.metadata.bind
##Queries:

def bookings(fields):	
	x_axis_title 	="Agents Report"
	y_axis_title 	="Total"
	result_type		="Bookings"			
	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				
	print result_type
	log(from_date)
	log(to_date)
	session=DBSession()
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
	str_chart=render('kunkka:templates/charts/ots.mak',{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={}
	for item in result_set.fetchall():
		if not temp_done.has_key(item.agent_name):
			d={"name":item.agent_name,"data":[]}
			series.append(d)
			temp_done[item.agent_name]=d
			
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time)
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
	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				
	print result_type
	log(from_date)
	log(to_date)
	session=DBSession()
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
		SELECT agent_id, agent_name,date_time,count(total_seats) AS total 
		FROM(
			SELECT DATE(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :from_date and booking_date < :to_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"from_date":from_date,"to_date_next":to_date_next})
		result_set=result
	str_chart=render('kunkka:templates/charts/ots.mak',{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={}
	for item in result_set.fetchall():
		if not temp_done.has_key(item.agent_name):
			d={"name":item.agent_name,"data":[]}
			series.append(d)
			temp_done[item.agent_name]=d
			
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time)
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
	from_date=datetime.datetime.strptime(fields["from"],'%Y-%m-%d')				
	to_date=datetime.datetime.strptime(fields["to"],'%Y-%m-%d')				
	print result_type
	log(from_date)
	log(to_date)
	session=DBSession()
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
		SELECT agent_id, agent_name,date_time,count(total_seats) AS total 
		FROM(
			SELECT DATE(B.booking_date) as date_time,B.* from bookings B 
			INNER JOIN agents ag ON ag.agent_id=B.agent_id 
			WHERE booking_date>= :from_date and booking_date < :to_date_next AND status='B' AND ag.category=1) A 
		GROUP BY agent_id, agent_name,date_time;
		""",{"from_date":from_date,"to_date_next":to_date_next})
		result_set=result
	str_chart=render('kunkka:templates/charts/ots.mak',{})
	chart=json.loads(str_chart)
	series=[]
	temp_done={}
	for item in result_set.fetchall():
		if not temp_done.has_key(item.agent_name):
			d={"name":item.agent_name,"data":[]}
			series.append(d)
			temp_done[item.agent_name]=d
			
		if same_date:
			y_axis=from_date+datetime.timedelta(hours=item.date_time)
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

query_set["Bookings"] = bookings
query_set["Seats"] =seats
query_set["Amount"]=amount




