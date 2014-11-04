try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
#import aggregator
   


class TableAggregators(object):

    def __init__(self,aggregators,table_no):        
        self.__aggregators_config__=[]
        self.__table_no__=table_no
        for aggregator in aggregators:
            if len(aggregator)<3:
                raise Exception("Invalid Aggregator Configuration %s",str(aggregator))
            if aggregator[2]==self.__table_no__:
                self.__aggregators_config__.append({"field":aggregator[0],"aggregator":aggregator[1]()})


    def update_aggregators(self,row):        
        for aggregator_config in self.__aggregators_config__:
            try:
                if aggregator_config["field"] in row:
                    aggregator_config["aggregator"].aggregate(row[aggregator_config["field"]])
            except Exception as e:
                print aggregator_config,e

    def get_aggregators_tr(self,fields):
        aggagated_data=[""]*len(fields)              
        print self.__aggregators_config__
        for aggregator_config in self.__aggregators_config__:            
            try:
                index=fields.index(aggregator_config["field"])
                print aggregator_config["aggregator"].get_value()
                if aggagated_data[index]=="":
                    aggagated_data[index]=aggregator_config["aggregator"].get_name()+": "+str(aggregator_config["aggregator"].get_value())
                else:
                    aggagated_data[index]+="\n"+aggregator_config["aggregator"].get_name()+": "+str(aggregator_config["aggregator"].get_value())
            except Exception as e:
                print e
        if len(aggagated_data)>0:
            tr='<tr>'                
            tr+='<th><div style="color: rgb(211, 114, 25);">'+'</div></th><th><div style="color: rgb(211, 114, 25);">'.join(aggagated_data)+'</div></th>'
            tr+='</tr>'            
            return tr
        else:
            return ''

def jsonToTable(dictObj,aggregators):
    tables=[]    
    tableCounter = -1    
    if aggregators==None:
        aggregators=[]
    for table_name in dictObj.keys():                
        tableCounter+=1
        table=dictObj[table_name]
        headers=OrderedDict()
        thead=''
        tfoot=''
        tbody=''         
        tableAggregators = TableAggregators(aggregators,tableCounter)
        if len(table)>0:
            item=OrderedDict(table[0])
            print item
            for key in item:
                if key not in headers:
                    headers[key]={}
                    headers[key]["name"]=key
                    if type(item[key])==int:
                        headers[key]["type"]="int"
                    ##TODO: Date##
                    elif type(item[key])==float:
                        headers[key]["type"]="float"
                    else:
                        headers[key]["type"]="str"
            #if headers.has_key("id"):
            #    thead='<thead><tr class="gradeA"><th class="select-check"><span class="glyphicon glyphicon-ok"></span></th><th>'+'</th><th>'.join(headers)+'</th></tr></thead>'
            #else:
            thead='<thead><tr class="gradeA"><th>'+'</th><th>'.join(headers)+'</th></tr></thead>'
            tfoot='<tfoot><tr>'
            ip_index=0
            #print headers
            for key in headers.keys():
                #tfoot+='<th><div class="input-group-sm"><input name="'+"search"+key+'" type="text" class="search_init form-control" placeholder="'+key+'"></div></th>'
                #tfoot+='<th><input ip_index='+str(ip_index)+' type="text" name="'+"search"+key+'" value="Search '+key+'" class="search_init" /></th>'
                ip_index+=1
            tfoot+='</tr></tfoot>'            
            
            listTbody=[]
            for row in table:                
                values=[(unicode(val)) for key,val in row.items()]                
                is_active=None
                is_active_class=""
                if row.has_key("IS_ACTIVE"):
                    is_active=str(row["IS_ACTIVE"])                    
                if is_active:
                    if is_active=="1" or is_active.lower()=="true":                                            
                        is_active_class="activated"
                    else:
                        is_active_class="deactivated"                
                if row.has_key("id"):
                    #Removed
                    #<td class="select-check"><input type="checkbox"></td>
                    listTbody.append('<tr id='+table_name+'_'+str(row["id"])+' class=" '+is_active_class+' table_row gradeA"><td>'+'</td><td>'.join(values)+'</td></tr>')                
                else:    
                    listTbody.append('<tr class="gradeA"><td>'+'</td><td>'.join(values)+'</td></tr>')
                tableAggregators.update_aggregators(row)

            tfoot+=tableAggregators.get_aggregators_tr(headers.keys())
            tbody='<tbody>'+''.join(listTbody)+'</tbody>'
            

        tables.append((headers,'<table>'+thead+tbody+tfoot+'</table>'))
    print len(tables)
    return tables

def getTable(response):
    print response.keys()
    return jsonToTable(response)





