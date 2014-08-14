<%inherit file="base.mako"/>
<%block name="control">    
    <div class="row">
        <div class="col-md-3 input-group input-group-sm">
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Groups</span>
            <select class="form-control" id="groups"></select>
        </div>        
         <div class="col-md-2 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="go" type="button" class="btn btn-primary" href="#" onclick='open_group();' tabindex="-1">Open</button>               
          </div>            
        </div>
        <div class="col-md-1 column btn-toolbar">
        </div>
        <div class="col-md-2 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="new" type="button" class="btn btn-primary" href="#" onclick='new_group();' tabindex="-1">New</button>               
          </div>            
        </div>
    </div>
    <div class="row" style="padding-top:50px;">   
        <div class="col-md-3 input-group input-group-sm">
        </div>     
        <div class="col-md-4 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="activate" type="button" class="btn btn-primary" href="#" onclick='activate();' tabindex="-1">Activate</button>               
               <button id="deactivate" type="button" class="btn btn-primary" href="#" onclick='deactivate();' tabindex="-1">Deactivate</button>               
            </div>                      
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Add Links</span>
            <select class="form-control" id="links"></select>
        </div>        
         <div class="col-md-2 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="add_link" type="button" class="btn btn-primary" href="#" onclick='add_link();' tabindex="-1">Add</button>               
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
        function load_groups()
        {
            $("#groups").empty();
            $("#links").empty();
             $.getJSON("${get_group_list_path}",function(response){
                var option;                   
                if(response.success==true){
                    option=document.createElement("option");
                    $(option).text("--Select--");
                    $(option).val("-1");                                                       
                    $("#links").append(option);

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
                    $(response.data.raw.Table1).each(function(index,obj){
                            option=document.createElement("option");
                            $(option).text(obj.LINK_NAME);
                            $(option).val(obj.LINK_ID);                               
                            $("#links").append(option);
                        });
                }else{
                    alert(response.msg);
                }
                });
        }
        function new_group(){
            $("#new").attr("disabled",true);
            $("#new").text("Wait...");
            BootstrapDialog.show({
                    title: 'Create New GDS Group',
                    type: BootstrapDialog.TYPE_INFO,
                    closable:false,
                    message: $('<input id="group_name" class="form-control" placeholder="Enter Group Name"></input>'),                    
                    buttons: [{
                        label: 'Cancel',
                        action: function(dialogRef){                            
                            $("#new").attr("disabled",null);
                            $("#new").text("New");  
                            dialogRef.close();     
                        }
                    }, {
                        label: 'Confirm',
                        cssClass: 'btn-primary',
                        hotkey: 13, // Enter.
                        action: function(dialogRef){                            
                            var group_name=$("#group_name").val();                            
                            $.getJSON("${create_gds_group_path}"+"NAME="+group_name
                            ,function(res){
                                if(res.success==true){
                                    load_groups();    
                                }else{
                                    alert(res.msg);
                                }             
                                $("#new").attr("disabled",null);
                                $("#new").text("New");                   
                            })
                            dialogRef.close();
                        }
                    }]
                });
        }
        function add_link()
        {
            $("#add_link").attr("disabled",true);
            $("#add_link").text("Wait...");
            var group_id=$("#groups").val();
            var link_id=$("#links").val();
            var add_group_link_path="${add_group_link_path}"+"LINK_ID="+link_id+"&GROUP_ID="+group_id;
            $.getJSON(add_group_link_path,function(response){
                if(response.success==true){
                    
                }else{
                    alert(response.msg);
                }
                open_group();
                $("#add_link").attr("disabled",null);
                $("#add_link").text("Add");
            });
            
        }
        function open_group()
        {
            $("#go").attr("disabled",true);
            $("#go").text("Wait...");
            var group_id=$("#groups").val();
            var group_list_path="${get_group_links_path}"+"GROUP_ID="+group_id;
            $.getJSON(group_list_path,function(response){
                if(response.success==true){
                    generateTables(response.data.tables);                    
                }else{
                    alert(response.msg);
                }
                $("#go").attr("disabled",null);
                $("#go").text("Open");
            });
        }  
        function activate(){
            update_perm(1);
        }
        function deactivate(){
            update_perm(0);
        }
        function update_perm(status){
            var d=$("#tables table").dataTable().fnGetNodes();
            var ids=[];                          
            $(d).filter(".row_selected").each(function(index,tr_obj){
                    ids.push(tr_obj.id.split("_")[1]);
            });   
            if (status==0){
                $("#deactivate").attr("disabled",true);
                $("#deactivate").text("Wait...");
                var group_id=$("#groups").val();
                var update_groups_perms_path="${update_groups_perms_path}"+"PERM_IDS="+ids.join(",")+"&STATUS="+status;
                $.getJSON(update_groups_perms_path,function(response){
                    if(response.success==true){
                        
                    }else{
                        alert(response.msg);
                    }
                    open_group();
                    $("#deactivate").attr("disabled",null);
                    $("#deactivate").text("Deactivate");
                });
            }else{
                $("#activate").attr("disabled",true);
                $("#activate").text("Wait...");
                var group_id=$("#groups").val();
                var update_groups_perms_path="${update_groups_perms_path}"+"PERM_IDS="+ids.join(",")+"&STATUS="+status;
                $.getJSON(update_groups_perms_path,function(response){
                    if(response.success==true){
                                    
                    }else{
                        alert(response.msg);
                    }
                    open_group();
                    $("#activate").attr("disabled",null);
                    $("#activate").text("Activate");
                });
            }
            
        }
        function select_link(e){
                var link_id=e.target.parentNode.id.split("_")[1];                                
                var obj=$("#Table_"+link_id);
                if(obj.hasClass("row_selected")){
                    obj.removeClass("row_selected");
                }else{
                    obj.addClass("row_selected");
                }
        }  
        $(document).ready(function(){
                load_groups();                
                $("#tables").click(select_link);
            })             
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>
<%block name="post_content">
</%block>
