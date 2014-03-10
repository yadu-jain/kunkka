import cryptacular.bcrypt
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,    
    )
from sqlalchemy import types
from sqlalchemy import exc

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
import json

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def get_session():
    global DBSession
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
    __tablename__   = 'users'
    id              = Column(types.Integer,primary_key=True)
    username        = Column(Unicode(100), unique=True)
    _password       = Column('password', Unicode(60))
    perms           = Column(types.String(100))
    oauth_id        = Column(types.Integer)
    mantis_user_id  = Column(types.Integer)
    name =Column(types.String(100))
    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = password #hash_password(password)

    password        = property(_get_password, _set_password)
    password        = synonym('_password', descriptor=password)
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __init__(self, username, oauth_id,name):
        self.username = username
        self.oauth_id = oauth_id
        self.name     = name
    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return  user.password==password#crypt.check(user.password, password)
class MongoQuery(Base):
    """
    Mongo Query
    """
    __tablename__   = 'queries'
    id              = Column(types.Integer,primary_key=True)
    name            = Column(types.String(50))
    #Wrapper=dict_query
    _str_query      = Column(types.Text)
    created_user    = Column(types.String(50))
    creaded_on      = Column(types.DateTime)
    last_updated    = Column(types.DateTime)
    level           = Column(types.Integer,default=0)
    args_count      = Column(types.Integer,default=0)
    #Wrapper=arguments
    #_arguments      =Column(types.Text)

    ##Dict Wrapper for _str_query
    @property
    def dict_query(self):
        return json.loads(self._str_query)

    @dict_query.setter
    def dict_query(self,value):        
        self._str_query=json.dumps(value)        
    dict_query=synonym('_str_query',descriptor=dict_query)
    
    ##Dict Wrapper for _arguments
    #@property
    #def arguments(self):
    #    return json.loads(self._arguments)

    #@arguments.setter
    #def arguments(self,value):
    #    self._arguments=json.dumps(value)
    #arguments=synonym('_arguments',descriptor=arguments)


class Execution(Base):
    """
    Mongo Query Execution
    """
    __tablename__   = 'executions'
    id              = Column(types.Integer,primary_key=True)
    query_id        = Column(types.Integer)
    count           = Column(types.Integer,default=0)
    last_executed   = Column(types.DateTime)
    #Wrapper=last_result
    _str_last_result     = Column(types.Text)

    @property
    def last_result(self):
        return json.loads(self._str_last_result)

    @last_result.setter
    def last_result(self,value):    
        self._str_last_result=json.dumps(value)        
    last_result=synonym('_str_last_result',descriptor=last_result)

class Links(Base):
    __tablename__   = 'links'
    link_id         = Column(types.Integer,primary_key=True)
    name            = Column(types.String(50),nullable=False)    
    path            = Column(types.String(100),unique=True)
    method          = Column(types.String(30),default='GET')
    enabled         = Column(types.Integer,default=1)
    category        = Column(types.String(50))
class Perms(Base):
    """
    User Permissions    
    """
    __tablename__   = 'perms'
    id         = Column(types.Integer,primary_key=True)
    group_id        = Column(types.Integer,default=0)
    link_id         = Column(types.Integer)
    enabled         = Column(types.Integer,default=1)