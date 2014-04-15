<%block name="control">

</%block>>
<%block name="inner_content">
<%inherit file="base.mako"/>        
    <div style="" class="row clearfix">        
        <div class="col-md-3 column">
        </div>
        <div class="col-md-7 column btn-toolbar" role="toolbar">
            <div class="btn-group btn-group-xs">
                <button id="get_companies" type="button" class="btn btn-primary" onclick="GetCompanies();"  disabled="true" href="#company_tables">Open Provider</button>
            </div>
            <div class="btn-group btn-group-xs">
              <button type="button" id="btn_activate_prov" onclick="activate_provider();" disabled="true" class="btn btn-success">Activate Provider</button>
              <button type="button" id="btn_deactivate_prov" onclick="deactivate_provider();" disabled="true"  class="btn btn-danger">Deactivate Provider</button>
            </div>
        </div>
    </div>
    <div class="row clearfix">        
        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>                       
        <style type="text/css">
            #contextMenu {
                position: absolute;
                display:none;
            }
        </style>
        <script type="text/javascript">           
            function select_comp(e){
                var COMPANY_ID=e.target.parentNode.id.split("_")[1];                
                $("#company_tables .table_row").removeClass("row_selected");                
                var temp =$("#company_tables #Table_"+COMPANY_ID).addClass("row_selected");
                if (temp.length>=1){
                    $("#open_company").attr("disabled",null)
                    $("#btn_activate_comp").attr("disabled",null);   
                    $("#btn_deactivate_comp").attr("disabled",null);
                }else
                {
                    $("#open_company").attr("disabled",true)
                    $("#btn_activate_comp").attr("disabled",true);   
                    $("#btn_deactivate_comp").attr("disabled",true);
                }
            }

            function GetCompanies(){
                var table=$("#tables").find("table")[0];
                var temp_str=$(table).find(".row_selected").attr("id");                
                if(temp_str==undefined){
                    alert("SELECT PROVIDER !");
                    return;
                }
                var PROVIDER_ID=temp_str.split("_")[1];
                $("#get_companies").text("Opening...");
                $("#get_companies").attr("disabled",true);
                GetCompanies_callback=function(response){
                    if (response.success==true)
                    {
                        generateTables(response.data.tables,"company_tables")
                        //generateCharts(response.data.charts,"company_tables")
                        $("#company_tables").click(select_comp);
                        location.href = "#";
                        location.href = "#company_tables";
                        $("#get_companies").text("Open");
                        $("#get_companies").attr("disabled",false);
                    }
                }               
                
                
                $.getJSON("${company_path}"+"PROVIDER_ID="+PROVIDER_ID,GetCompanies_callback);
                //$(".table_row").removeClass("row_selected");                
                //$("id=Table_"+PROVIDER_ID).addClass("row_selected");                

            }
            function activate_provider(){
                $("#btn_activate_prov").attr("disabled",true);
                var PROVIDER_ID=$("#tables").find(".row_selected").attr("id").split("_")[1];
                var PROVIDER_NAME=$("#tables").find(".row_selected").find("td")[1].innerHTML;
                BootstrapDialog.show({
                    title: 'Activate '+PROVIDER_NAME +' (ID='+PROVIDER_ID+')',
                    type: BootstrapDialog.TYPE_SUCCESS,
                    closable:false,
                    message: $('<textarea id="comment" class="form-control" placeholder="Write a comment..."></textarea>'),                    
                    buttons: [{
                        label: 'Cancel',
                        action: function(dialogRef){
                            console.log("Cancelled");
                            $("#btn_activate_prov").attr("disabled",null);
                            dialogRef.close();                            
                        }
                    }, {
                        label: 'Confirm',
                        cssClass: 'btn-warning',
                        hotkey: 13, // Enter.
                        action: function(dialogRef){
                            // You can also use BootstrapDialog.closeAll() to close all dialogs.
                            var comment=document.getElementById("comment").value;
                            $("#btn_activate_prov").text("Activating...");                                                        
                            $.getJSON("${update_provider_status}"+"&ACTIVE=1&ID="+PROVIDER_ID+"&PROVIDER_NAME="+PROVIDER_NAME+"&COMMENT="+comment
                            ,function(res){
                                if(res.success==true){
                                    refresh();
                                }
                                $("#btn_activate_prov").text("Activate");                            
                                $("#btn_activate_prov").attr("disabled",null);
                            })
                            dialogRef.close();
                        }
                    }]
                });
/*
                $.getJSON("${update_provider_status}"+"&ACTIVE=1&ID="+PROVIDER_ID+"&PROVIDER_NAME="+PROVIDER_NAME+"&COMMENT="+"Testing provider activation/deactivation, please ignore"
                    ,function(res){console.log(res)})
*/
            }
            function deactivate_provider(){
                $("#btn_deactivate_prov").attr("disabled",true);
                var PROVIDER_ID=$("#tables").find(".row_selected").attr("id").split("_")[1];
                var PROVIDER_NAME=$("#tables").find(".row_selected").find("td")[1].innerHTML;
                BootstrapDialog.show({
                    title: 'Deactivate '+PROVIDER_NAME +' (ID='+PROVIDER_ID+')',
                    type: BootstrapDialog.TYPE_DANGER,
                    closable:false,
                    message: $('<textarea id="comment" class="form-control" placeholder="Write a comment..."></textarea>'),                    
                    buttons: [{
                        label: 'Cancel',
                        action: function(dialogRef){
                            console.log("Cancelled");
                            $("#btn_deactivate_prov").attr("disabled",null);
                            dialogRef.close();                            
                        }
                    }, {
                        label: 'Confirm',
                        cssClass: 'btn-warning',
                        hotkey: 13, // Enter.
                        action: function(dialogRef){
                            // You can also use BootstrapDialog.closeAll() to close all dialogs.
                            var comment=document.getElementById("comment").value;
                            $("#btn_deactivate_prov").text("Deactivating...");                                                        
                            $.getJSON("${update_provider_status}"+"&ACTIVE=0&ID="+PROVIDER_ID+"&PROVIDER_NAME="+PROVIDER_NAME+"&COMMENT="+comment
                            ,function(res){
                                if(res.success==true){
                                    refresh();
                                }
                                $("#btn_deactivate_prov").text("Deactivate");                            
                                $("#btn_deactivate_prov").attr("disabled",null);
                            })
                            dialogRef.close();
                        }
                    }]
                });

            }
            function activate_company(){
                var COMPANY_ID=$("#company_tables").find(".row_selected").attr("id").split("_")[1];
                $("#btn_activate_comp").attr("disabled",true);                
                var COMPANY_NAME=$("#company_tables").find(".row_selected").find("td")[1].innerHTML;
                BootstrapDialog.show({
                    title: 'Activate '+COMPANY_NAME +' (ID='+COMPANY_ID+')',
                    type: BootstrapDialog.TYPE_SUCCESS,
                    closable:false,
                    message: $('<textarea id="comment" class="form-control" placeholder="Write a comment..."></textarea>'),                    
                    buttons: [{
                        label: 'Cancel',
                        action: function(dialogRef){
                            console.log("Cancelled");
                            $("#btn_activate_comp").attr("disabled",null);
                            dialogRef.close();                            
                        }
                    }, {
                        label: 'Confirm',
                        cssClass: 'btn-warning',
                        hotkey: 13, // Enter.
                        action: function(dialogRef){
                            // You can also use BootstrapDialog.closeAll() to close all dialogs.
                            var comment=document.getElementById("comment").value;
                            $("#btn_activate_comp").text("Activating "+COMPANY_NAME+"..");                                                        
                            $.getJSON("${update_company_status}"+"&ACTIVE=1&ID="+COMPANY_ID+"&COMPANY_NAME="+COMPANY_NAME+"&COMMENT="+comment
                            ,function(res){
                                if(res.success==true){
                                    GetCompanies();
                                }
                                $("#btn_activate_comp").text("Activate Company");                            
                                $("#btn_activate_comp").attr("disabled",null);
                            })
                            dialogRef.close();
                        }
                    }]
                });


            }

            function deactivate_company(){
                var COMPANY_ID=$("#company_tables").find(".row_selected").attr("id").split("_")[1];
                $("#btn_deactivate_comp").attr("disabled",true);                
                var COMPANY_NAME=$("#company_tables").find(".row_selected").find("td")[1].innerHTML;
                BootstrapDialog.show({
                    title: 'Deactivate '+COMPANY_NAME +' (ID='+COMPANY_ID+')',
                    type: BootstrapDialog.TYPE_DANGER,
                    closable:false,
                    message: $('<textarea id="comment" class="form-control" placeholder="Write a comment..."></textarea>'),                    
                    buttons: [{
                        label: 'Cancel',
                        action: function(dialogRef){
                            console.log("Cancelled");
                            $("#btn_deactivate_comp").attr("disabled",null);
                            dialogRef.close();                            
                        }
                    }, {
                        label: 'Confirm',
                        cssClass: 'btn-warning',
                        hotkey: 13, // Enter.
                        action: function(dialogRef){
                            // You can also use BootstrapDialog.closeAll() to close all dialogs.
                            var comment=document.getElementById("comment").value;
                            $("#btn_deactivate_comp").text("Deactivating "+COMPANY_NAME+"..");                                                        
                            $.getJSON("${update_company_status}"+"&ACTIVE=0&ID="+COMPANY_ID+"&COMPANY_NAME="+COMPANY_NAME+"&COMMENT="+comment
                            ,function(res){
                                if(res.success==true){
                                    GetCompanies();
                                }
                                $("#btn_deactivate_comp").text("Deactivate Company");                            
                                $("#btn_deactivate_comp").attr("disabled",null);
                            })
                            dialogRef.close();
                        }
                    }]
                });

            }
            function select_prov(e){
                var PROVIDER_ID=e.target.parentNode.id.split("_")[1];                
                $("#tables .table_row").removeClass("row_selected");                
                var temp =$("#Table_"+PROVIDER_ID).addClass("row_selected");
                if (temp.length>=1){
                    $("#get_companies").attr("disabled",null);   
                    $("#btn_activate_prov").attr("disabled",null);   
                    $("#btn_deactivate_prov").attr("disabled",null);
                }else
                {
                    $("#get_companies").attr("disabled",true);   
                    $("#btn_activate_prov").attr("disabled",true);   
                    $("#btn_deactivate_prov").attr("disabled",true);
                }
            }            
            function refresh(){
                callback=function(response)
                {
                    if (response.success==true)
                    {
                        console.log( response.data.meta_content);
                        var temp=generateTables(response.data.tables)
                        generateCharts(response.data.charts)
                        $("#tables").on("click",select_prov);
                        //$(".table_row").on("dblclick",GetCompanies); 
                        //$(".table_row").on("click",select_it);
                        
                        //$("#tables").on("dblclick",GetCompanies);
                        //process_active_providers();
                        /*
                        var table=response.data.tables[0];
                        var div=document.getElementById("content");
                        div.innerHTML=table.content;
                        $(div).ready(function() {
                            var tables=$(div).find("table");
                            tables.dataTable();
                        } );
*/
                    }
                }
                console.log("Report")
                $.getJSON("${provider_path}",callback)
            }
            $(document).ready(function(){                               
                refresh();    
            });
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">                        
        </div> 
        <div id="contextMenu" class="dropdown clearfix">
        <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">
          <li><a tabindex="-1" href="#">Action</a></li>
          <li><a tabindex="-1" href="#">Another action</a></li>
          <li><a tabindex="-1" href="#">Something else here</a></li>
          <li class="divider"></li>
          <li><a tabindex="-1" href="#">Separated link</a></li>
        </ul>
        </div>

    </div>
    <div style="" class="row clearfix">        
        <div class="col-md-3 column">
        </div>
        <div class="col-md-7 column btn-toolbar" role="toolbar">
            <div class="btn-group btn-group-xs" style="display:none;">
                <button id="open_company" type="button" class="btn btn-primary" onclick="GetDetails();"  disabled="true" href="#">Open Company</button>
            </div>
            <div class="btn-group btn-group-xs">
              <button type="button" id="btn_activate_comp" onclick="activate_company();" disabled="true" class="btn btn-success">Activate Company</button>
              <button type="button" id="btn_deactivate_comp" onclick="deactivate_company();" disabled="true"  class="btn btn-danger">Deactivate Company</button>
            </div>
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="company_tables">
            
        </div >
    </div>
</%block>    
<%block name="post_content">
    
</%block>    