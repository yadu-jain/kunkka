import shelve
from contextlib import contextmanager
from datetime import datetime
@contextmanager
def closing(obj):
    try:
        yield obj
    finally:
        obj.close()

class FileCache:
    """
    """
    def __init__(self,name):
        self.name=name
    def save(self,key,val):        
        with closing(shelve.open(self.name)) as cache:                        
            cache[key]=val        
            cache["last_modified"]=datetime.now()

    def get(self,key):
        temp=None
        with closing(shelve.open(self.name)) as cache:            
            if cache.has_key(key):
                temp=cache[key]
        return temp     
