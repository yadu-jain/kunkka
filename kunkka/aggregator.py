
class Aggregator(object):
    __curr_value__ = None
    __name__ = None
    def __init__(self,name="Sum"):
        self.__name__ = name    
    def aggregate(self,value):
        self.__curr_value__+=value
    def init_value(self,value):
        self.__curr_value__=value
    def get_value(self):
        return self.__curr_value__
    def get_name(self):
        return self.__name__

class Sum(Aggregator):
    def __init__(self):
        super(Sum,self).__init__(name=self.__class__.__name__)
        self.init_value(0) 


class Count(Aggregator):
    def __init__(self):
        super(Count,self).__init__(name=self.__class__.__name__)
        self.init_value(0)   
    def aggregate(self,value):
        self.__curr_value__+=1