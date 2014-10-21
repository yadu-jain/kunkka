from db import update_perms_links
from datetime import datetime
from datetime import timedelta
import table
import gds_api
import chart
from file_cache import FileCache
#from mem_client import clear_companies
from fabric_api import delete_allowed_compaies,delete_search_routes
import email_sender
reports={} ## oauth based
service_reports={} ## Key Based
##-----------------------------------Decorators------------------------##
##FOR TABLE
REFRESH_REPORT_IN_DB=False
class Create_Tables:
    def __init__(self,titles):

        if len(titles)==0:
            self.titles=[""]
        else:
            self.titles=titles        
        print self.titles
    def __call__(self,fun): 
        if hasattr(fun,'dataGenerators')== False:
            fun.dataGenerators=[]
        def getTable(response):            
            return table.jsonToTable(response)
        generator=getTable
        generator.titles=self.titles
        generator.name='tables'
        fun.dataGenerators.append(generator)
        print len(fun.dataGenerators)
        return fun

##FOR CHART
class Create_Charts:
    """
    titles:         list of string for each table return by gds_api
    chart_configs:  list of configuration tuple for each table return by gds_api
                    configuration tuple should have atleast 3 values(x,y,group).
                    X: column name on x-axis. It's value in table should be string
                    Y: column data on y-axis. It's value in table should double or int
                    group: column name different color groups. It's value in table should be string
    """
    def __init__(self,titles,chart_configs):

        if len(titles)==0:
            self.titles=["Default Title"]
        else:
            self.titles=titles
        try:               
            if chart_configs and len(chart_configs)>0:
                print "here"                
                self.initialized=True
                self.chart_configs=chart_configs
            else:            
                self.initialized=False
        except Exception as e:
            print e
            self.initialized=False
        
    def __call__(self,fun): 
        print fun        
        if hasattr(fun,'dataGenerators')== False:
            fun.dataGenerators=[]
        def wrapper(data):
            if self.initialized==True:
                return chart.getChart(data,self.chart_configs,self.titles)
            else:
                raise Exception("Invalid Chart Config")

        generator=wrapper       
        generator.titles=self.titles
        generator.name='charts'        
        fun.dataGenerators.append(generator)
        return fun


##-------------------Key based service report---------###

class Service_Reporter(object):
    def __init__(self,shared_key=None):
        self.shared_key=shared_key
    def __call__(self,fun):
        def wrapper(*args, **kwargs):
            if self.shared_key !=None and( kwargs.has_key("shared_key")==False or (kwargs.has_key("shared_key")==True and  kwargs["shared_key"]!=self.shared_key)):
                raise Exception("Invalid shared key")
            response=fun(*args, **kwargs)     
            new_response={}
            new_response["raw"]=response
            if hasattr(fun,'dataGenerators')== True:
                print fun.dataGenerators                
                for dataGenerator in fun.dataGenerators:                    
                    generatedData = dataGenerator(response)                    
                    count=0
                    resultItems=[]
                    if len(dataGenerator.titles)<len(generatedData):
                        dataGenerator.titles=dataGenerator.titles
                        dataGenerator.titles.extend(["Default Title"]*(len(generatedData)-len(dataGenerator.titles)))
                    for item in generatedData:
                        print "Preparing result"                         
                        if not len(item)==0:
                            resultItems.append({"title":dataGenerator.titles[count],"meta_content":item[0],"content":item[1]})
                        count+=1
                    print "added "+dataGenerator.name
                    new_response[dataGenerator.name]=resultItems            
            print new_response.keys()
            return new_response
        wrapper.__name__=fun.__name__
        service_reports[fun.__name__]=wrapper        
###---------------------------------------------------###
class Reporter(object):
    def __init__(self,perm_enable=True,perm_groups=[],name=None,enable=1,category=None,parent_path="report"):
        self.perm_enable=perm_enable
        self.group_ids=perm_groups
        self.name=name
        self.enabled=enable
        self.category=category
        self.parent_path=parent_path
    def __add_to_db__(self,fun_name):
        if not self.name:
            self.name=fun_name
        if not self.group_ids:            
                self.group_ids=[]            
        self.path="/"+self.parent_path+"/"+fun_name+"/"

        response=update_perms_links(self.name,self.group_ids,self.path,self.enabled,self.category)
        print response
    def __call__(self,fun):         
        if self.perm_enable==True and REFRESH_REPORT_IN_DB==True:
                self.__add_to_db__(fun.__name__)
        def wrapper(*args, **kwargs):

            response=fun(*args, **kwargs)     
            new_response={}
            new_response["raw"]=response
            if hasattr(fun,'dataGenerators')== True:
                print fun.dataGenerators                
                for dataGenerator in fun.dataGenerators:                    
                    generatedData = dataGenerator(response)                    
                    count=0
                    resultItems=[]
                    if len(dataGenerator.titles)<len(generatedData):
                        dataGenerator.titles=dataGenerator.titles
                        dataGenerator.titles.extend(["Default Title"]*(len(generatedData)-len(dataGenerator.titles)))
                    for item in generatedData:
                        print "Preparing result"                         
                        if not len(item)==0:
                            resultItems.append({"title":dataGenerator.titles[count],"meta_content":item[0],"content":item[1]})
                        count+=1
                    print "added "+dataGenerator.name
                    new_response[dataGenerator.name]=resultItems            
            print new_response.keys()
            return new_response
        wrapper.__name__=fun.__name__
        reports[fun.__name__]=wrapper        
##----------------------------------------------------------------##
#       To Generate Report
#1.create function like this
#        
# @Reporter(perm_enable=True,perm_groups=[],name="",enable=1,category="Reports")
# @Create_Tables(titles=[""])
# @Create_Charts(titles=[""],chart_configs=[("IS_ACTIVE","$count",[]),("provider_name","$count",[])]) #(X,Y,[groups])
# def agents_details(**fields):
#     api=gds_api.Gds_Api()
#     if fields.has_key("SUB_AGENT_ID"):
#         fields["SUB_AGENT_ID"]=int(fields["SUB_AGENT_ID"])
#     if fields.has_key("FLAG_ALL_INFO"):
#         fields["FLAG_ALL_INFO"]=int(fields["FLAG_ALL_INFO"])
#     print fields
#     return api.RMS_SUB_AGENT_STATUS(**fields)
#2. @Reporter decorator must be added, perm_enable specifies whether particular permission is required for the report
#3. @Create_Tables to generate tables
#4. @Create_Charts to generate charts with configuration
# a.chart_configs is list of tuple for each table returned gds_api
# b.Each tuple in chart_configs should contains (X,Y,[groups],table_no),where
#   X is column on x-axis
#   Y is column on y-axis
#   groups is list group
#   table_no on which chart data depends(starts from 0)
#   put empty tuple in chart_configs if chart for particular table in result set, is not desired
#5. function must  return api.<SP_name>(**fields) value
#6. SP_NAME must be configured before in gds_api.json file specifying parameters details(name,type,default value)
#7. It requires server to be refreshed in order to reflect the report
##-------------------------------Reports---------------------------##
@Reporter(perm_enable=True,perm_groups=[1,8],name="Agent Details",enable=1,category="Reports",parent_path='report')
@Create_Tables(titles=["Agent Details","Company Wise Commission"])
#@Create_Charts(titles=[""],chart_configs=[("IS_ACTIVE","$count",[],0),("provider_name","$count",[],1)]) #(X,Y,[groups],table_no)
def agents_details(request,**fields):
    api=gds_api.Gds_Api()
    user_id=request.user.username            
    if user_id:        
        fields["USER_ID"]=user_id
    if fields.has_key("FLAG_ALL_INFO"):
        fields["FLAG_ALL_INFO"]=int(fields["FLAG_ALL_INFO"])
    return api.RMS_SUB_AGENT_STATUS(**fields)

@Reporter(perm_enable=True,perm_groups=[1,7],name="Agent Bookings",enable=1,category="Reports",parent_path='date_report')
@Create_Tables(titles=["SUB AGENT STATS"])
@Create_Charts(titles=["BOOKED","CANCELLED","FAILED"],chart_configs=[("BOOKING_DATE","TOTAL_BOOKED",["SUB_AGENT_NAME"],0),
                                          ("BOOKING_DATE","TOTAL_CANCELLED",["SUB_AGENT_NAME"],0),
                                          ("BOOKING_DATE","TOTAL_FAILED",["SUB_AGENT_NAME"],0)]) #(X,Y,[groups])
def user_agents_report(request,**fields):
    api=gds_api.Gds_Api()    
    user_id=request.user.username            
    
    result_set=[]
    if user_id:        
        fields["USER_ID"]=user_id
        return api.RMS_GET_DAY_AGENTS_REPORT(**fields)
    else:        
        raise Exception("Mantis User Id not Specified !")

# def user_agents_report(request,**fields):
#     api=gds_api.Gds_Api()
#     print "mantis_user_id"
#     mantis_user_id=request.user.mantis_user_id    
#     print mantis_user_id
   
#     result_set=[]
#     if mantis_user_id:
#         str_from=fields["STR_FROM_DATE"]
#         str_to=fields["STR_TO_DATE"]
#         date_from=datetime.strptime(str_from,'%Y-%m-%d')       
#         date_to=datetime.strptime(str_to,'%Y-%m-%d')       
#         str_date_list=[]
#         date_curr=date_from
#         while date_curr<=date_to:
#             str_date_list.append(date_curr.strftime('%Y-%m-%d'))
#             date_curr=date_curr+timedelta(days=1)
#         n=len(str_date_list)
#         str_date_list=str_date_list[n-30:] 
#         to_refresh_list=[]
#         fileCache=FileCache("user_agents_report_"+str(mantis_user_id))
#         for str_date in str_date_list:
#             val=fileCache.get(str_date)
#             if val:
#                 result_set.append(val)
#             else:
#                 val=api.RMS_GET_DAY_AGENTS_REPORT(**{"MANTIS_ID":mantis_user_id,"DATE":str_date})
#                 if val:
#                     result_set.append(val)
#                     fileCache.save(str_date,val)
#         final_result={}
#         for result in result_set:
#             for key in result.keys():
#                 if final_result.has_key(key)==False:
#                     final_result[key]=[]
#                 final_result[key].extend(result[key])
#         return final_result
#     else:        
#         raise Exception("Mantis User Id not Specified !")

@Reporter(perm_enable=True,perm_groups=[1,2],name="Junk Pickups",enable=1,category="")                   
@Create_Tables(titles=["Junk Pickups","Main Areas","Mapped Area Stats Across India"])
def junk_pickups(request,**field):
    api=gds_api.Gds_Api()            
    return api.RMS_GET_JUNK_PICKUPS(**field)

@Reporter(perm_enable=True,perm_groups=[1,2],name="Update Junk Pickups",enable=1,category="")                       
def update_area_of_pickup(request,**field):
    api=gds_api.Gds_Api()            
    field["USER"]=request.user.username
    return api.RMS_UPDATE_AREA_OF_PICKUP(**field)
 

@Reporter(perm_enable=True,perm_groups=[1,2],name="Area City List",enable=1,category="")                   
def get_area_city_list(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GET_AREA_CITY_LIST()



@Reporter(perm_enable=True,perm_groups=[1,3],name="COMPANY/ROUTE BOOKING REPORT",enable=1,category="Reports",parent_path='date_report')                   
@Create_Tables(titles=["COMPANY WISE BOOKINGS(TY+CONSOLE)","ROUTE WISE BOOKINGS(TY+CONSOLE)"])
def get_company_wise_mis(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_COMPANY_WISE_MIS(**field)


@Reporter(perm_enable=True,perm_groups=[1,4],name="DAY WISE TY+CONSOLE BOOKINGS",enable=1,category="Reports",parent_path='date_report')                   
@Create_Tables(titles=["DAY WISE TY+CONSOLE BOOKINGS"])
@Create_Charts(titles=["BOOKINGS","CANCELLED","RETURN BOOKINGS"],chart_configs=[("BOOKING_DATE","BOOKINGS",["NAME"],0),
                                          ("BOOKING_DATE","CANCELLED",["NAME"],0),
                                          ("BOOKING_DATE","RETURN_BOOKINGS",["NAME"],0)]) #(X,Y,[groups])
def get_day_ty_console_bookings(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_DAY_TY_CONSOLE_BOOKINGS(**field)


@Reporter(perm_enable=True,perm_groups=[1,5],name="AGENT MIS REPORT",enable=1,category="Reports",parent_path='date_report')                   
@Create_Tables(titles=["SUB-AGENT WISE","TY USER WISE","API PARTNER WISE","TY OVER ALL","CONSOLE OVER ALL","API PARTNER OVER ALL","AGENTS OVER ALL","GDS OVER ALL"])
def get_agent_wise_mis(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_AGENT_WISE_REPORT(**field)

@Reporter(perm_enable=True,perm_groups=[1,6],name="PROVIDERS STATUS",enable=1,category="")                   
@Create_Tables(titles=["PROVIDERS STATUS"])
def get_provider_status(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GET_PROVIDER_STATUS(**field)

@Reporter(perm_enable=True,perm_groups=[1,6],name="COMPANIES STATUS",enable=1,category="")
@Create_Tables(titles=["COMPANIES STATUS"])
def get_company_status(request,**field):
    api=gds_api.Gds_Api()    
    return api.RMS_GET_COMPANY_STATUS(**field)

@Reporter(perm_enable=True,perm_groups=[1,6],name="PROVIDER ACTIVATE/DEACTIVATE",enable=1,category="")
def update_provider_status(request,**field):
    api=gds_api.Gds_Api()    
    field["TYPE"]="PROVIDER"
    field["USER"]=request.user.username
    provider_name=field["PROVIDER_NAME"]
    comment=field["COMMENT"]
    ##-------------Updating status in GDS DB----------------##
    temp_response = api.RMS_UPDATE_STATUS(**field)
    ##------------------------------------------------------##    
    
    ##----Clear cache of  allowed companies for each agent--##
    agents_field={"FLAG_ALL_INFO":0}
    all_agents=api.RMS_SUB_AGENT_STATUS(**agents_field)["Table"]
    chunk_ids=[]
    for agent in all_agents:
        chunk_ids.append(str(agent["id"]))                   
    flag_status=delete_allowed_compaies(chunk_ids)
    ##------------------------------------------------------##

    ##------Notify team through mail------------------------##
    ACTIVATION_STATUS=""
    if field["ACTIVE"]=="1":
        ACTIVATION_STATUS='<span style="color:darkGreen"><b>Activated</b></span><br/><br/>'
    elif field["ACTIVE"]=="0":
        ACTIVATION_STATUS='<span style="color:red"><b>Deactivated</b></span><br/><br/>'

    msg_body=ACTIVATION_STATUS
    msg_body+='<span>By: '+request.user.name+'</span><br/>'
    msg_body+='<span>Date: '+str(datetime.now())+'</span><br/>'
    msg_body+='<span>comment: '+comment+'</span><br/>'
    msg_body='<div>'+msg_body+'</div>'
    flag_status=email_sender.sendmail(email_sender.PROVIDER_UPDATE_LIST,"RMS: "+provider_name+" Changed",msg_body,provider_name)
    ##-------------------------------------------------------##
    return temp_response

@Reporter(perm_enable=True,perm_groups=[1,6],name="COMPANY ACTIVATE/DEACTIVATE",enable=1,category="")
def update_company_status(request,**field):
    api=gds_api.Gds_Api()    
    field["TYPE"]="COMPANY"
    field["USER"]=request.user.username
    company_name=field["COMPANY_NAME"]
    company_id=field["ID"]
    comment=field["COMMENT"]
    ##-------------Updating status in GDS DB----------------##
    temp_response = api.RMS_UPDATE_STATUS(**field)
    ##------------------------------------------------------##    
    
    ##----Clear cache of  allowed companies for each agent--##
    agents_field={"FLAG_ALL_INFO":0}
    all_agents=api.RMS_SUB_AGENT_STATUS(**agents_field)["Table"]
    chunk_ids=[]
    for agent in all_agents:
        chunk_ids.append(str(agent["id"]))                   
    flag_status=delete_allowed_compaies(chunk_ids)
    ##------------------------------------------------------##

    ##------Notify team through mail------------------------##
    ACTIVATION_STATUS=""
    if field["ACTIVE"]=="1":
        ACTIVATION_STATUS='<span style="color:darkGreen"><b>Activated</b></span><br/><br/>'
    elif field["ACTIVE"]=="0":
        ACTIVATION_STATUS='<span style="color:red"><b>Deactivated</b></span><br/><br/>'

    msg_body=ACTIVATION_STATUS
    msg_body+='<span>Company: '+company_name+'(ID='+str(company_id)+')</span><br/>'
    msg_body+='<span>By: '+request.user.name+'</span><br/>'
    msg_body+='<span>Date: '+str(datetime.now())+'</span><br/>'
    msg_body+='<span>comment: '+comment+'</span><br/>'
    msg_body='<div>'+msg_body+'</div>'
    flag_status=email_sender.sendmail(email_sender.PROVIDER_UPDATE_LIST,"RMS: "+company_name+" Changed",msg_body,company_name)
    ##-------------------------------------------------------##
    return temp_response    


@Reporter(perm_enable=True,perm_groups=[1,10],name="GDS INVENTORY",enable=1,category="")
@Create_Tables(titles=["TOTAL INVENTORY","OPERATOR WISE INVENTORY"])
def gds_inventory(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GDS_INVENTORY_STATUS(**field)


@Reporter(perm_enable=True,perm_groups=[1,2],name="Create Area Name",enable=1,category="")                       
def create_area(request,**field):
    api=gds_api.Gds_Api()            
    field["USER"]=request.user.username
    return api.RMS_CREATE_MAIN_AREA(**field)

@Reporter(perm_enable=True,perm_groups=[1,11],name="Get State List",enable=1,category="")                       
def  get_state_list(request,**field):
    api=gds_api.Gds_Api()            
    return api.RMS_GET_STATE_LIST(**field)

@Reporter(perm_enable=True,perm_groups=[1,11],name="Get City List of the State",enable=1,category="")                       
@Create_Tables(titles=["Cities"])
def  get_state_city_list(request,**field):
    api=gds_api.Gds_Api()            
    return api.RMS_GET_STATE_CITY_LIST(**field)


@Reporter(perm_enable=True,perm_groups=[1,11],name="UPDATE CITY: MERGE CITIES",enable=1,category="")                       
def  merge_city(request,**field):
    api=gds_api.Gds_Api()            
    return api.RMS_MERGE_CITIES(**field)

@Reporter(perm_enable=True,perm_groups=[1,11],name="UPDATE CITY: SET PARENT CITY",enable=1,category="")                       
def  set_parent_city(request,**field):
    api=gds_api.Gds_Api()            
    return api.RMS_UPDATE_PARENT_CITY(**field)   

@Reporter(perm_enable=True,perm_groups=[1,12],name="GET GDS USER LIST(SUB AGENTS/SUB AGENT USERS)",enable=1,category="")                       
def get_user_list(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GET_GDS_USER_LIST(**field)      

@Reporter(perm_enable=True,perm_groups=[1,12],name="GET GDS USER LIST(SUB AGENTS/SUB AGENT USERS)",enable=1,category="")                       
@Create_Tables(titles=["User Details","User Groups","Default City"])
def get_gds_uuid(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GET_GDS_UUID(**field)          

@Reporter(perm_enable=True,perm_groups=[1,13],name="PROVIDER WISE INVENTORY STATS",enable=1,category="Reports",parent_path='date_report')
@Create_Tables(titles=["ROUTES STATS","CITY PAIRS STATS"])
@Create_Charts(titles=["ROUTES STATS","CITY PAIRS STATS"],chart_configs=[("JOURNEY_DATE","TOTAL_ROUTES",["PROVIDER_NAME"],0),
                                          ("JOURNEY_DATE","CITY_PAIRS_COUNT",["PROVIDER_NAME"],1),
                                          ("Date","total",["PROVIDER_NAME"],2)
                                          ]) #(X,Y,[groups],TABLE_NO)
def provider_inventory_stats(request,**fields):
    api=gds_api.Gds_Api()        
    return api.RMS_GDS_PROVIDER_INVENTORY(**fields)    


@Reporter(perm_enable=True,perm_groups=[1,12],name="GDS GROUPS",enable=1,category="")                       
def get_group_list(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GET_GROUP_LIST(**field)  

@Reporter(perm_enable=True,perm_groups=[1,12],name="GDS GROUP LINKs",enable=1,category="")                       
@Create_Tables(titles=["Group Links","Group Users"])
def get_group_links(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_GET_GROUP_LINKS(**field) 

@Reporter(perm_enable=True,perm_groups=[1,12],name="ADD LINK TO GROUP",enable=1,category="")                       
def add_group_link(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_ADD_GROUP_LINK (**field)  

@Reporter(perm_enable=True,perm_groups=[1,12],name="UPDATE GROUP PERMS",enable=1,category="")                       
def update_groups_perms(request,**field):
    api=gds_api.Gds_Api()
    return api.RMS_UPDATE_GROUP_PERM(**field)     

@Reporter(perm_enable=True,perm_groups=[1,12],name="CREATE GDS GROUP",enable=1,category="")                       
def  create_gds_group(request,**field):
    api=gds_api.Gds_Api() 
    return api.RMS_CREATE_GDS_GROUP(**field)         

@Reporter(perm_enable=True,perm_groups=[1,12],name="ADD GROUP TO USER",enable=1,category="")                       
def  add_group_to_user(request,**field):
    api=gds_api.Gds_Api() 
    return api.RMS_ADD_GROUP_TO_USER(**field)    
         
@Reporter(perm_enable=True,perm_groups=[1,14],name="Corporate Bookings",enable=1,category="Reports",parent_path='date_report')         
@Create_Tables(titles=["CORPORATE BOOKINGS"])
def  corporate_bookings(request,**field):
    api=gds_api.Gds_Api() 
    return api.RMS_GET_CORPORATE_BOOKINGS(**field)  

@Reporter(perm_enable=True,perm_groups=[1,15],name="RMS Report",enable=1,category="Reports",parent_path='date_report')         
@Create_Tables(titles=["RMS REPORT"])
def  rms_report(request,**field):
    api=gds_api.Gds_Api() 
    return api.RMS_GET_RMS_REPORT(**field)         


@Reporter(perm_enable=True,perm_groups=[1,16],name="Refresh Routes",enable=1,category="")
@Create_Tables(titles=["REFRESH ROUTES","INACTIVE ROUTES REFRESHED"])
def refresh_routes(request,**field):
    api=gds_api.Gds_Api() 
    response=api.RMS_GET_ROUTE_LIST(**field)      
    inactive_count=response["Table1"][0]["INACTIVE"]
    print inactive_count
    if inactive_count >0 and inactive_count<=100:
        #activating inactive routes
        api.RMS_REFRESH_INACTIVE_ROUTE(**field)
    ## Deleting cache    
    delete_search_routes(response["Table"])
    return response

@Reporter(perm_enable=True,perm_groups=[1,17],name="Karnataka Agents Report",enable=1,category="Reports",parent_path='date_report')         
@Create_Tables(titles=["KARNATAKA AGENTS REPORT"])
@Create_Charts(titles=["KARNATAKA AGENTS REPORT"],chart_configs=[("STATE","TOTAL_BOOKED",["MANTIS_USER"],0)]) #(X,Y,[groups],TABLE_NO)
def  karnataka_bookings(request,**field):
    api=gds_api.Gds_Api() 
    field["STATE_ID"]=9
    return api.RMS_GET_STATE_AGENT_BOOKINGS(**field)  

@Reporter(perm_enable=True,perm_groups=[1,18],name="PROVIDER WISE DAILY BOOKINGS",enable=1,category="Reports",parent_path='date_report')
@Create_Tables(titles=["TY BOOKINGS","OVERALL BOOKINGS"])
@Create_Charts(titles=["TY BOOKINGS","OVERALL BOOKINGS"],chart_configs=[("BOOKING_DATE","TOTAL",["PROVIDER_NAME"],0),
                                          ("BOOKING_DATE","TOTAL",["PROVIDER_NAME"],1)]) #(X,Y,[groups],TABLE_NO)
def provider_daily_bookings(request,**fields):
    api=gds_api.Gds_Api()        
    return api.RMS_PROVIDER_WISE_DAILY_BOOKINGS(**fields)   

##---------------------------------## Services for crons and other clients-----------------------------------------##
@Service_Reporter(shared_key="b218fad544980213a25ef18031c9127e")
def refresh_new_routes(request,**field):
    api=gds_api.Gds_Api() 
    response=api.RMS_GET_NEW_ROUTE_LIST(**field)          
    ## Deleting cache    
    delete_search_routes(response["Table"])
    return response    

@Service_Reporter(shared_key="abc")    
def test(request,**field):    
    return None

    
#print update_area_of_pickup.dataGenerators
#print junk_pickups.dataGenerators
#print agents_details.dataGenerators 