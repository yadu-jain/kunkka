from pyramid.events import NewRequest
import transaction
from pyramid.events import subscriber
from logger import *
from sqlalchemy.exc import DBAPIError
import json

from .models import (
    get_session,
    DBSession,
    Booking,
    )

class RequestPathStartsWith(object):
	def __init__(self, val, config):
		self.val = val

	def text(self):
		return 'path_startswith = %s' % (self.val,)

	phash = text
	def __call__(self, event):
		return event.request.path.startswith(self.val)


@subscriber(NewRequest, magnus='/magnus')
def MagnusHandler(event):
	if event.request.method=='POST':
		log("Magnus POST")
		try:			
			data=json.loads(event.request.body, encoding=event.request.charset)
			db=DBSession()
			list_bookings=data["bookings"]
			counter=0
			for item in list_bookings:
				booking=Booking(
						booking_id =item['booking_id'],
						agent_id = item['agent_id'],
						agent_name = item['agent_name'],
						status = item['status'],
						from_city=item['from_city'],
						to_city=item['to_city'],
						journey_date=item['journey_date'],
						booking_date=item['booking_date'],
						amount=item['amount'],
						total_seats=item['total_seats'],
						customer_email=item['customer_email'],
						provider_id=item['provider_id'],
						provider_name=item['provider_name'],
						company_id=item['company_id'],
						company_name=item['company_name']
						)
				
				db.add(booking)
				count+=1
				if count>=100:
					log("Commiting...")
					db.commit()
					count=0			
			log("Commiting...")		
			try:
				db.commit()
				db.close()
				log('DONE')
        		#one = DBSession.query(Booking).filter(MyModel.name == 'one').first()        		
			except DBAPIError as e:
				#log(str(e))
				log(e)
		except Exception as e:
			#log(str(e))
			log(e)
			#log(event.request.body)
	else:
		log("Magnus GET")		

