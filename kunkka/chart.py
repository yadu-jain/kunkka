try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict
import json
import copy
from pyramid.renderers import render
chart_template  ='kunkka:templates/charts/simple_chart.mako'      

def __getChartData(x_axis,y_axis,groups,table):
    
    categories=[]
    grouped_data=OrderedDict()
    for item in table:
        group_key=''
        for group_name in groups:
            if group_name in item:
                if item[group_name]:                            
                    group_key+=unicode(item[group_name])+'-'
                else:
                    group_key+=''+'-'

        if len(group_key)>0:
            group_key=group_key[:-1]                
        else:
            group_key="default"
                        
        if not group_key in grouped_data:
            grouped_data[group_key]={"name":group_key,"categories":OrderedDict()}                                                            
        if not item[ x_axis ] in grouped_data[ group_key ]["categories"]:
            grouped_data[ group_key ]["categories"][ item[ x_axis ] ] = []
        if y_axis=='$count':
            grouped_data[ group_key ]["categories"][ item[ x_axis ] ].append(1)
        else:
            grouped_data[ group_key ]["categories"][unicode(item[ x_axis ]) ].append(item[y_axis])
        if not unicode(item[x_axis]) in categories:
                categories.append(unicode(item[x_axis]))
    series=[]
    default_data=[0]*len(categories)
    print "categories"
    print categories
    for group_key,group in grouped_data.iteritems():
        obj={"name":group_key,"data":copy.copy(default_data)}                
        for category,value in group["categories"].iteritems():
            try:
                pos=categories.index(category)                        
                obj["data"][pos]=sum(value)
            except:
                pass
        series.append(obj)                            
    return ({},series,categories)

def getChart(dictObj,configs,titles):
    charts=[]
    counter=0    
    for config in configs:                
        print config        
        if len(config)<4:            
            continue
        table_name=dictObj.keys()[config[3]]
        table=dictObj[table_name]
        x_axis=config[0]
        y_axis=config[1]
        groups=config[2]
        if len(table)>0:
            item=OrderedDict(table[0])
            print item.keys()
            print config
            ## X-Axis
            if config[0] not in item.keys():
                raise Exception("X-Axis column not found")
            ## Y-Axis
            if config[1]!='$count' and not config[1] in item.keys():
                raise Exception("Y-Axis column not found")
            ## Group names
            for group_name in config[2]:
                if group_name not in item:
                    raise Exception("Group column not found")
            if config[1]!='$count' and (type(item[config[1]])!=int and type(item[config[1]])!=float):
                raise Exception("Invalid Y-Axis. It should be int or float")
            
            meta_content,series,categories=__getChartData(x_axis,y_axis,groups,table)
            meta_content["x_axis_title"]=x_axis
            meta_content["y_axis_title"]=y_axis
            if len(titles)>counter:
                meta_content["main_title"]=titles[counter]
            else:
                meta_content["main_title"]="Default Title"
            chart=renderChart(meta_content,series,categories)
            charts.append((meta_content,chart))
        else:
            
            meta_content,series,categories={},[],[]
            meta_content["x_axis_title"]=x_axis
            meta_content["y_axis_title"]=y_axis
            if len(titles)>counter:
                meta_content["main_title"]=titles[counter]
            else:
                meta_content["main_title"]="Default Title"

            chart=renderChart(meta_content,series,categories)
            charts.append((meta_content,chart))
        counter+=1    
    return charts
def renderChart(meta_content,series,categories):
    print meta_content
    str_chart=render(chart_template,{})
    chart=json.loads(str_chart)
    chart["title"]["text"]=meta_content["main_title"]
    chart["xAxis"]["title"]["text"]=meta_content["x_axis_title"]
    chart["yAxis"]["title"]["text"]=meta_content["y_axis_title"]
    chart["xAxis"]["categories"]=categories
    chart["series"]=series
    return chart


            
