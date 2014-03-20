<%block name="inner_content">
<%inherit file="base.mako"/>
    <div class="row clearfix">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">
                GDS Inventory
            </h3>
        </div>
    </div>    
    <div  class="row clearfix">       
        <div class="col-md-1 column">            
        </div>
        <div class="col-md-6 input-group input-group-sm">
            <span class="input-group-addon">From: </span>
            <select id="from_city" class="form-control form-control">               
            </select>
            <span class="input-group-addon">To: </span>
            <select id="to_city" class="form-control form-control">               
            </select>
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">JD: </span>
            <input type="text" class="form-control" id="jd">
        </div>        
        <script>
            var date_jd=new Date();                                
            $(document).ready(function(){               
                $(function() {
                    $( "#jd" ).datepicker({                       
                        dateFormat: 'yy-mm-dd'                      
                    });                                        
                    $("#jd").datepicker( "setDate" ,date_jd);                    
                    
                  });
            });           
        </script>  
        <div class="col-md-2 column btn-toolbar" role="toolbar">            
            <div class="btn-group btn-group-sm">
                <button id="go" type="button" class="btn btn-primary" onclick="get_gds_inventory();">Go</button>
            </div>            
        </div>
        <!--
        <div class="col-md-3 input-group input-group-sm">
            <div class="input-group-btn">
            <button type="button" onclick="get_junk_pickups();" class="run btn btn-primary">Go</button>
            </div>
        </div>  
        -->
    </div>    
    <div class="row clearfix">

        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">
            function report_callback(response){
                if (response.success==true)
                {
                    
                    console.log( response.data.meta_content);
                    generateTables(response.data.tables)
                    generateCharts(response.data.charts)                 
                    $("#go").text("Go");
                    $("#go").attr("disabled",null);
                }else
                {
                    $("#go").text("Go");
                    $("#go").attr("disabled",null);
                    BootstrapDialog.alert(response.msg);
                }
            }
            function get_gds_inventory(){
                var from_city_id=$("#from_city").val();
                var to_city_id=$("#to_city").val();
                if(from_city_id==to_city_id){
                    BootstrapDialog.alert('From City and To City can not be same !');
                    return;
                }
                var jd=$("#jd").val();
                $("#go").attr("disabled",true);
                $("#go").text("Fetching...");
                $.getJSON("${report_path}"+"FROM_CITY="+from_city_id+"&TO_CITY="+to_city_id+"&STR_JD="+jd,report_callback);                
            }
            $(document).ready(function(){               
                
                city_list_callback= function(response)
                {
                    if (response.success==true){
                        console.log(response.data);
                        cities=response.data.raw.Table;
                        var city_data;
                        var elem_option;
                        var elem_select_from=document.getElementById("from_city");
                        var elem_select_to=document.getElementById("to_city");
                        elem_select_from.innerHTML="";
                        elem_select_to.innerHTML="";
                        for (var i in cities)
                        {
                            city_data=cities[i];
                            elem_option_to=document.createElement("option");
                            elem_option_from=document.createElement("option");

                            elem_option_from.value=city_data.city_id;
                            elem_option_from.innerHTML=city_data.city_name[0].toUpperCase()+city_data.city_name.substring(1);

                            elem_option_to.value=city_data.city_id;
                            elem_option_to.innerHTML=city_data.city_name[0].toUpperCase()+city_data.city_name.substring(1);


                            elem_select_from.appendChild(elem_option_to);
                            elem_select_to.appendChild(elem_option_from);                            
                        }
                    }
                }
                console.log("Report")
                $.getJSON("${city_list_path}",city_list_callback);
                
                });
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>    
<%block name="post_content">
    
</%block>    