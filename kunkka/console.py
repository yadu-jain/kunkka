from db import get_query
from sqlalchemy.orm import sessionmaker
from models import MongoQuery
from mongo import Mongo
from .models import (
    Base,
    MongoQuery,
    DBSession,
    get_session
    )
import transaction
from datetime import datetime
default_text="""
/*
Hints:
Paramters: $1,$2,$3..
dbname: $db
*/

/*Example:*/
return $db.count({"method":"$1"})
"""
class Query(object):
    def __init__(self,id=None,load_query=False):
        if id:
            result = get_query(id=id,load_query=load_query)
            if len(result) >0:
                self.mongoQuery=result[0]
            else:
                raise Exception("Console Error: No Query Found !")        
        else:
            self.mongoQuery=None
    def execute(self,date_from,date_to,arguments):
        mongo=Mongo()
        dict_query=self.mongoQuery.dict_query
        db_name=dict_query["db_name"]
        coll=dict_query["coll"]
        level=self.mongoQuery.level
        #str_query="""
        #return $db.group({
        #    key: {"Module":1},
#
 #           cond:{"LogLevel":"error","Method": "HoldSeats"},
#
 #           reduce: function ( curr, result ) {result.total += 1;},
#
 #           initial:{ total : 0 }
#
 #       });
  #      """

        str_query=dict_query["str_query"]
        print len(arguments)
        if self.mongoQuery.args_count != len(arguments):
            raise Exception("Console Error: Invalid No of arguments!")
        return mongo.query(db_name,date_from,date_to,str_query,arguments,coll)
    def save(self,name,args_count,dict_query,level):
        if self.mongoQuery is None:
            self.mongoQuery= MongoQuery()  
            self.created_on= datetime.now()
        #else:
        #    self.mongoQuery= MongoQuery(id=self.mongoQuery.id)  
        db_session=sessionmaker(bind=Base.metadata.bind)
        db=db_session()
        self.mongoQuery=db.merge(self.mongoQuery)
        self.mongoQuery.name=name
        self.mongoQuery.args_count=args_count
        self.mongoQuery.dict_query=dict_query
        self.mongoQuery.level=level
        self.mongoQuery.last_updated=datetime.now()
        #=MongoQuery(id=id,name=name,args_count=args_count,dict_query=args_count,level=level,last_updated=datetime.now())            
        db.add(self.mongoQuery)                
        db.commit()        
        #Refresh
        temp= self.mongoQuery.id        
        db.close()
        #result = get_query(id=self.mongoQuery.id)
        #self.mongoQuery=result[0]                        
        return self.mongoQuery        

    def delete(self):
        pass
    @staticmethod
    def copy(copied_from_id=None):
        pass

    @staticmethod
    def execute_str(str_query,db_name,date_from,date_to,coll,arguments):
        mongo=Mongo()
        return mongo.query(db_name,date_from,date_to,str_query,arguments,coll)