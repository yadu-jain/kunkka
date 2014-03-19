"""
Author:Heera
Date: 2014-03-17
Description: To Update memcache
"""

import pylibmc
host="127.0.0.1"
behaviors={"tcp_nodelay":True,"ketama":True}
KEY_TYPES={
    "pickup":"pkps",
    "allowed_comps":"user_cmp1"
}
reuseInstance=None
class Memcache:
    """
    Wrapper for memcache use
    get_key: return key to be used, args: key_type and entities based on which the key is to be generated
    """
    def __init__(self):        
        self.mc=pylibmc.Client([host],binary=True,behaviors=behaviors)        
        try:
            temp=self.mc.get_stats()
        except:
            raise Exception("failed to connect to memcache server")            

    def get_key(self,key_type,entities):
        return KEY_TYPES[key_type]+"_"+"_".join(entities)
    def set(self,key,val):
        return self.mc.set(key,val)        
    def get(self,key):
        return self.mc.get(key)
    def delete(self,key):
        if type(key)==list:
            return self.mc.delete_multi(key)
        else:
            return self.mc.delete(key)    

################################# Wrapper Users #########################################
def clear_companies(user_ids):
    global reuseInstance    
    if reuseInstance:
        mem=reuseInstance
    else:
        mem=Memcache()
        reuseInstance=mem
    keys=list()
    key=None
    print "clearing cache..."
    counter=0
    for user_id in user_ids:
        key=mem.get_key("allowed_comps",[user_id])
        #mem.delete(key)
        #print key
        #print counter
        keys.append(key)
        counter+=1
        if len(keys)>=200:
            print "deleting.."
            mem.delete(keys)
            print keys
            keys=list()             
    print counter
    return mem.delete(keys)
