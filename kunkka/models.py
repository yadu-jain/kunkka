from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text
    )
from sqlalchemy import types

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


#class MyModel(Base):
#    __tablename__ = 'models'
    #id = Column(Integer, primary_key=True)
    #name = Column(Text)
    #value = Column(Integer)

#    def __init__(self, name, value):
 #       self.name = name
  #      self.value = value

#Index('my_index', MyModel.name, unique=True, mysql_length=255)


## For Magnus Data to mysql-->username:kunkka, database:
class Booking(Base):
    __tablename__   = 'bookings'
    id              = Column(types.Integer,primary_key=True)
    booking_id      = Column(types.Integer)
    agent_id        = Column(types.Integer)
    agent_name      = Column(types.String(50))
    status          = Column(types.String(2))
    from_city       = Column(types.String(100))
    to_city         = Column(types.String(100))
    journey_date    = Column(types.DateTime)
    booking_date    = Column(types.DateTime)
    amount          = Column(types.Float(10,True))
    total_seats     = Column(types.Integer)
    customer_email  = Column(types.String(100))
    provider_id     = Column(types.Integer)
    provider_name   = Column(types.String(50))
    company_id      = Column(types.Integer)
    company_name    = Column(types.String(50))


class Agent(Base):
    __tablename__   = 'agents'
    agent_id        = Column(types.Integer,primary_key=True)    
    name            = Column(types.String(100))    
    category        = Column(types.Integer,default=0)

class IP(Base):
    __tablename__   = 'ips'
    id              = Column(types.Integer,primary_key=True)
    ip              = Column(types.String(30))
    host            = Column(types.String(50))
    agent_id        = Column(types.Integer)
