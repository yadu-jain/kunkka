<%block name="control">

</%block>>
<%block name="inner_content">
<%inherit file="base.mako"/>        
    <div style="" class="row clearfix">        
        <div class="col-md-4 column">
        </div>
        <div class="col-md-4 column btn-toolbar" role="toolbar">
            <div class="btn-group btn-group-xs">
                <button id="open_company" type="button" class="btn btn-primary" onclick="GetCompanies();" href="#company_tables">Open</button>
            </div>
            <div class="btn-group btn-group-xs">
              <button type="button" disabled="true" class="btn btn-success">Activate</button>
              <button type="button" disabled="true"  class="btn btn-danger">Deactivate</button>
            </div>
        </div>
    </div>
    <div class="row clearfix">        
        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <div class="col-md-12 column" style="padding-left:0px;"id="company_tables">
            
        </div >
        <style type="text/css">
            #contextMenu {
                position: absolute;
                display:none;
            }
        </style>
        <script type="text/javascript">           
            function GetCompanies(){
                var table=$("#tables").find("table")[0];
                var temp_str=$(table).find(".row_selected").attr("id");                
                if(temp_str==undefined){
                    alert("SELECT PROVIDER !");
                    return;
                }
                var PROVIDER_ID=temp_str.split("_")[1];
                $("#open_company").text("Opening...");
                $("#open_company").attr("disabled",true);
                GetCompanies_callback=function(response){
                    if (response.success==true)
                    {
                        generateTables(response.data.tables,"company_tables")
                        //generateCharts(response.data.charts,"company_tables")
                        location.href = "#";
                        location.href = "#company_tables";
                        $("#open_company").text("Open");
                        $("#open_company").attr("disabled",false);
                    }
                }               
                
                
                $.getJSON("${company_path}"+"PROVIDER_ID="+PROVIDER_ID,GetCompanies_callback);
                //$(".table_row").removeClass("row_selected");                
                //$("id=Table_"+PROVIDER_ID).addClass("row_selected");                

            }
            function activate_provider(){
                var PROVIDER_ID=$("tables").find(".row_selected").attr("id").split("_")[1];


            }
            function deactivate_provider(){
                var PROVIDER_ID=$("tables").find(".row_selected").attr("id").split("_")[1];

            }
            function activate_company(){
                var COMPANY_ID=$("company_tables").find(".row_selected").attr("id").split("_")[1];

            }
            function deactivate_company(){
                var COMPANY_ID=$("company_tables").find(".row_selected").attr("id").split("_")[1];

            }
            function select_it(e){
                var PROVIDER_ID=e.currentTarget.id.split("_")[1];                
                $(".table_row").removeClass("row_selected");                
                $("#Table_"+PROVIDER_ID).addClass("row_selected");
            }            
            function refresh(){
                callback=function(response)
                {
                    if (response.success==true)
                    {
                        console.log( response.data.meta_content);
                        generateTables(response.data.tables)
                        generateCharts(response.data.charts)
                        $(".table_row").on("dblclick",GetCompanies); 
                        $(".table_row").on("click",select_it);
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
</%block>    
<%block name="post_content">
    
</%block>    