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



@subscriber(NewRequest, courier='/courier')
def CourierHandler(event):
	if event.request.method=='POST':
		log("Courier POST")
		if (not "key" in event.request.params) or (event.request.params["key"]!="courier"):
			log("Invalid Courier POST !")
			return
		try:			
			#data=json.loads(event.request.body, encoding=event.request.charset)
			log(event.request.body)
			#db=DBSession()		
		except Exception as e:
			#log(str(e))
			log(e)
			#log(event.request.body)
	else:
		log("Courier GET")		

