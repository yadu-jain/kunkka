"""
It uses GDS's RMS Provider api to get download data from gds
"""
from httplib2 import Http
import json
import codecs
from urllib import urlencode
api_url=None
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict

api_key=""


class Gds_Api:    
    def __init__(self):
        pass
def test():
    try:
        h=Http()
        res,content=h.request(api_url+"?key="+api_key,"GET")
        if res["status"]=='200':
            response = json.loads(content)
            if len(response)==0:
                return True        
    except Exception as e:
        print "testin failed"
        print 
        return False
        
def execute(data):
    h=Http()
    print "\n\n"
    print api_url
    print data    
    res,content=h.request(
                        api_url+"?key="+api_key,
                        "POST",
                        urlencode(data),
                        headers={"content-type":"application/x-www-form-urlencoded"}
                        )        
    if res["status"]=='200':
        response = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(content)         
        if response.has_key("success") and response["success"]==True:
            return response["data"]
        elif response.has_key("success") and response["success"]==False:
            raise Exception(response["msg"])
        else:
            raise Exception("GDS Invalid Response !")

def get_api_method(method):
    def api_method(instance,**kwrds):
        param_list=[]            
        print kwrds
        for param in method["params"]:                
            param_with_val={}                 
            param_with_val.update(param)
            if param["name"] in kwrds:                    
                param_with_val["value"]=kwrds[param["name"]]
            elif "default" in param:
                param_with_val["value"]=param["default"]
            else:
                param_with_val["value"]=None
            param_list.append(json.dumps(param_with_val))
        data={method["type"]:method["name"],"params":"["+",".join(param_list)+"]"}            

        return execute(data)
    return api_method

def create_gds_api(method_list):
    for method in method_list:            
        api_method=get_api_method(method)
        print method["name"] 
        print api_method.__name__
        print (method["name"], api_method)
        setattr(Gds_Api, method["name"], api_method)    




