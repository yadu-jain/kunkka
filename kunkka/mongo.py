from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import re
from logger import *
def getMongo(request):
       db = config.registry.db[db_url.path[1:]]
       if db_url.username and db_url.password:
           db.authenticate(db_url.username, db_url.password)
       return db
     

class Mongo:

    def __init__(self,conn=None,username=None,password=None):
        if conn:
            self.conn=conn
        elif Mongo.conn:
            self.conn=Mongo.conn
        else:
            raise Exception("No Mongo Connection Specified")

        if username:
            self.username=username
        elif Mongo.username:
            self.username=Mongo.username
        else:
            self.username=None

        if password:
            self.password=password
        elif Mongo.password:
            self.password=Mongo.password
        else:
            self.password=None    

    def query(self,str_db,date_from,date_to,str_query,args=[],collection_prefix="gds"):                     
        db=self.conn["admin"]    
        if self.username and self.password:
            db.authenticate(self.username,self.password)
        raw_result=[]
        day=date_from
        while day <= date_to:
            try:

                str_day=day.strftime("%Y_%m_%d")                
                str_query_with_db=str_query.replace("$db","db_name."+collection_prefix+"_"+str_day)
                str_args=",".join(["$"+str(i) for i in range(len(args))])

                print str_query_with_db
                str_fun="""
                function(%s){
                        /*Testing*/
                        db_name=db.getMongo().getDB( "%s" );
                        %s
                }
                """ % (str_args,str_db,str_query_with_db)

                print str_fun
                #str_query=str_query.replace("\t","")
                #str_query=str_query.replace("\n","")
                #str_query=str_query.replace(" ","")
                #return db.eval(str_query_test)
                print args
                cmd=OrderedDict([("eval",str_fun),("args",args),("nolock",True)])                   
                temp_result=db.command(cmd)            
                raw_result.append({"date":day.strftime("%Y-%m-%d"),"result":temp_result})
            except Exception as ex:
            	log(ex)
                raw_result.append({"date":day.strftime("%Y-%m-%d"),"result":str(ex)})
            finally:
                day=timedelta(days=1)+day
        result=[]    
        for item in raw_result:
            if "result" in item and "ok" in item["result"] and item["result"]["ok"]==1:            
                result.append({"success":True,"data":item["result"]["retval"],"msg":"","date":item["date"]})
            else:
                if "errmsg" in item:
                    result.append({"success":False,"msg":item["errmsg"],"date":item["date"]})
                else:
                    result.append({"success":False,"msg":"","date":item["date"]})
        return result,raw_result                
                    

    @staticmethod
    def access_logs():
        print "connecting..."
        db = config.registry.mongo_db["access_logs"]
        if mongo_db_url.username and mongo_db_url.password:
            db.authenticate(mongo_db_url.username, mongo_db_url.password)
        return db

    @staticmethod
    def gdslogs():
        print "connecting..."
        db = config.registry.mongo_db["logs"]
        if mongo_db_url.username and mongo_db_url.password:
            db.authenticate(mongo_db_url.username, mongo_db_url.password)
        return db