<%inherit file="base.mako"/>
<%block name="control">    
    <div class="row">
        <div class="col-md-3 input-group input-group-sm">
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Sub Agent</span>
            <select class="form-control" id="sub_agents"></select>
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Sub Agent User</span>
            <select class="form-control" id="sub_agent_users">
            </select>
        </div>            
         <div class="col-md-2 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="go" type="button" class="btn btn-primary" href="#" onclick='open_user();' tabindex="-1">Open</button>               
          </div>            
        </div>
    </div>
    <div class="row" style="padding-top:50px;">
        <div class="col-md-3 input-group input-group-sm">
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Groups</span>
            <select class="form-control" id="groups"></select>
        </div>        
         <div class="col-md-2 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="add" type="button" class="btn btn-primary" href="#" onclick='add_group();' tabindex="-1">Add</button>               
          </div>            
        </div>
        <div class="col-md-1 column btn-toolbar">
        </div>        
    </div>
</%block>

<%block name="inner_content">

    <div class="row clearfix">
        <div class="col-md-12 column">
            <!--
            <h3 class="text-center text-primary">
                GDS RMS
            </h3>
            -->
        </div>
    </div>
    <div class="row clearfix">                
        
        <div class="col-md-2 column">
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">
        	var opened_uuid;            
            function open_user()
            {
                $("#go").attr("disabled",true);
                $("#go").text("Wait...");
                var sub_agent_user_uuid=$("#sub_agent_users").val().split("|")[1];
                var sub_agent_uuid=$("#sub_agents").val().split("|")[1];
                var uuid=0;
                if(sub_agent_user_uuid>0)
            	{
            		uuid=sub_agent_user_uuid;
            	}else
            	{
            		uuid=sub_agent_uuid;
            	}
            	$.getJSON("${gds_get_uuid_path}"+"&UUID="+uuid,function(response){
            			if(response.success==true){
            				generateTables(response.data.tables);
            				opened_uuid=uuid;
            			}
            			$("#go").attr("disabled",null);
                		$("#go").text("Open");
        		});

            }
            function add_group()
            {
            	if(opened_uuid && opened_uuid!=null){
            		$("#add").attr("disabled",true);
	                $("#add").text("Wait...");
	                var group_id=$("#groups").val();	                
	            	$.getJSON("${add_group_to_user_path}"+"UUID="+opened_uuid+"&GROUP_ID="+group_id,function(response){
	            			if(response.success==true){
	            				open_user();
	            			}else
	            			{
	            				alert(response.msg);
	            			}
	            			$("#add").attr("disabled",null);
	                		$("#add").text("Add");
	        		});
            	}
            }
            function load_sub_agent_users()            
            {            
                var sub_agent_id=$("#sub_agents").val().split("|")[0];
                $("#sub_agent_users").empty();
                if(sub_agent_id>0){
                    $.getJSON("${gds_users_path}"+"SUB_AGENT_ID="+sub_agent_id,function(response){
                    		var option;                           
		                    if(response.success==true){
		                    	option=document.createElement("option");
			                    $(option).text("--Default--");
			                    $(option).val("-1"+"|"+"-1");			                    
			                    $("#sub_agent_users").append(option);
			                    $(response.data.raw.Table).each(function(index,obj){
			                    		option=document.createElement("option");
					                    $(option).text(obj.NAME);
					                    $(option).val(obj.SUB_AGENT_USER_ID+"|"+obj.id);					                   
					                    $("#sub_agent_users").append(option);
			                    	});

		                    }
                        });
                }
            }
            function load_sub_agent()
            {
                $("#sub_agents").empty();
                 $.getJSON("${gds_users_path}",function(response){                                        
                    var option;                   
                    if(response.success==true){
                    	option=document.createElement("option");
	                    $(option).text("--Select--");
	                    $(option).val("-1"+"|"+"-1");			                    	                    
	                    $("#sub_agents").append(option);
                        $(response.data.raw.Table).each(function(index,obj){
                                option=document.createElement("option");
                                $(option).text(obj.NAME);
                                $(option).val(obj.SUB_AGENT_ID+"|"+obj.id);                               
                                $("#sub_agents").append(option);
                        });
                        $("#sub_agents").val("333|2");
                        load_sub_agent_users();
                    }else{
                        alert(response.msg);
                    }
                    });
            }
            function load_groups()
            {
                $("#groups").empty();                
                 $.getJSON("${get_group_list_path}",function(response){
                    var option;                   
                    if(response.success==true){   
                        option=document.createElement("option");
                        $(option).text("--Select--");
                        $(option).val("-1");                                                       
                        $("#groups").append(option);
                        $(response.data.raw.Table).each(function(index,obj){
                                option=document.createElement("option");
                                $(option).text(obj.group_id+"-"+obj.name);
                                $(option).val(obj.group_id);                               
                                $("#groups").append(option);
                            });                        
                    }else{
                        alert(response.msg);
                    }
                });
            }
            $(document).ready(function(){
                load_sub_agent();
                load_groups();
                $("#sub_agents").change(load_sub_agent_users);
                });

        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>
<%block name="post_content">
</%block>
