try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
def jsonToTable(dictObj):
    tables=[]
    for table_name in dictObj.keys():
        table=dictObj[table_name]
        headers=OrderedDict()
        thead=''
        tfoot=''
        tbody=''        
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
            thead='<thead><tr class="gradeA"><th>'+'</th><th>'.join(headers)+'</th></tr></thead>'
            tfoot='<tfoot><tr>'
            ip_index=0
            print headers
            for key in headers.keys():
                tfoot+='<th><div class="input-group-sm"><input name="'+"search"+key+'" type="text" class="search_init form-control" placeholder="'+key+'"></div></th>'
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
                    listTbody.append('<tr id='+table_name+'_'+str(row["id"])+' class=" '+is_active_class+' table_row gradeA"><td>'+'</td><td>'.join(values)+'</td></tr>')
                else:    
                    listTbody.append('<tr class="gradeA"><td>'+'</td><td>'.join(values)+'</td></tr>')
                
            tbody='<tbody>'+''.join(listTbody)+'</tbody>'
        tables.append((headers,'<table>'+thead+tbody+tfoot+'</table>'))
    print len(tables)
    return tables

def getTable(response):
    print response.keys()
    return jsonToTable(response)





