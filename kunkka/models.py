import cryptacular.bcrypt
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,    
    )
from sqlalchemy import types

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    synonym,
    )
from pyramid.security import (
    Everyone,
    Authenticated,
    Allow,    
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def get_session():
    try:
        # suppose the database has been restarted.
        session=DBSession()
        session.execute("SELECT 1")
        session.close()
        return DBSession()
    except exc.DBAPIError, e:
        # an exception is raised, Connection is invalidated.
        if e.connection_invalidated:
            print "connection invalidated"
    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    engine = Base.metadata.bind
    DBSession.configure(bind=engine)
    return DBSession()
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
    #id              = Column(types.Integer,primary_key=True)
    booking_id      = Column(types.Integer,primary_key=True,autoincrement=False)
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
    
class Provider(Base):
    __tablename__   = 'providers'
    provider_id     = Column(types.Integer,primary_key=True)    
    name            = Column(types.String(100))    

class Tier(Base):
    __tablename__   = 'tiers'
    tier_id         = Column(types.String(10),primary_key=True)
    name            = Column(types.String(30))

class IP(Base):
    __tablename__   = 'ips'
    id              = Column(types.Integer,primary_key=True)
    ip              = Column(types.String(30))
    host            = Column(types.String(50))
    agent_id        = Column(types.Integer)

class User(Base):
    """
    For Authentication
    """
    __tablename__ = 'users'
    id = Column(types.Integer,primary_key=True)
    username = Column(Unicode(20), unique=True)
    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = password #hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return  user.password==password#crypt.check(user.password, password)