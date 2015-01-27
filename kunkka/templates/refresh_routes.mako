<%inherit file="base.mako"/>
<%block name="control">
    <script src="${request.static_url('kunkka:static/tran.js')}"></script>
    <!--<script id="chart_js" src="${request.static_url('kunkka:static/highchart/highcharts.js')}"></script>    -->
    <!--<script id="chart_theme" src="${request.static_url('kunkka:static/highchart/themes/dark-green.js')}"></script>-->
    <div class="row">
        <div class="col-md-2 input-group input-group-sm">
            <span class="input-group-addon">Trip ID:</span>
            <input type="text" class="form-control" id="trip_id">
        </div>
        <div class="col-md-2 input-group input-group-sm">
            <span class="input-group-addon">Service ID:</span>
            <input type="text" class="form-control" id="service_id">
        </div>
    </div>
    <br/>
    <div class="row">        
        <div class="col-md-2 input-group input-group-sm">
            <span class="input-group-addon">From:</span>
            <input type="text" class="form-control" id="jd_from">
        </div>
        <div class="col-md-2 input-group input-group-sm">
            <span class="input-group-addon">To:</span>
            <input type="text" class="form-control" id="jd_to">
        </div>
        <div class="col-md-2">
            <input type="checkbox" id="chkHardRefresh"> Hard Refresh
        </div>
        <div class="col-md-1 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="go" type="button" class="btn btn-primary" href="#" onclick='open_report();' tabindex="-1">Refresh</button>               
          </div>            
        </div>
        <script>
            var d=new Date();
            date_from=d;
            date_to=d;           
            $(document).ready(function(){               
                $(function() {
                    $( "#jd_from" ).datepicker({                       
                        dateFormat: 'yy-mm-dd'                      
                    });

                    $("#jd_to" ).datepicker({                      
                        dateFormat: 'yy-mm-dd'                      
                    });                    
                    $("#jd_from").datepicker( "setDate" ,date_from);
                    $("#jd_to").datepicker( "setDate" ,date_to);
                    
                  });
            });           
        </script>  
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
            function report_callback(response)
            {
                if (response.success==true)
                {
                    try{
                        $("#go").text("Fetching...");
                        console.log( response.data.meta_content);
                        generateTables(response.data.tables);
                        generateCharts(response.data.charts) ;                
                    }catch(e){

                    }
                    $("#go").text("Refresh");
                    $("#go").attr("disabled",null);
                }else{
                    $("#go").text("Refresh");
                    $("#go").attr("disabled",null);
                    show_error(response.msg);
                }
            }
            function open_report()
            {
               
                var trip_id=$("#trip_id").val();
                var service_id=$("#service_id").val().trim();
                
                var jd_from=$("#jd_from").val().trim();
                var jd_to=$("#jd_to").val();
                var url="${refresh_routes_path}";
                var hard_refresh=$("#chkHardRefresh").prop('checked');
                if(trip_id.length==0 && service_id.length==0)
                {
                        return;
                }
                if(trip_id.length!=0){
                    url+="&TRIP_ID="+trip_id;
                }
                if(service_id.length!=0){
                    url+="&SERVICE_ID="+service_id;    
                }
                if(hard_refresh==true){
                    url+="&HARD_REFRESH="+1;                    
                }else{
                    url+="&HARD_REFRESH="+0;                    
                }
                
                url+="&STR_FROM_JOURNEY_DATE="+jd_from+"&STR_TO_JOURNEY_DATE="+jd_to;
                $("#go").attr("disabled",true);
                $("#go").text("Refreshing...");
                $.getJSON(url,report_callback);
            }            
            
            $(document).ready(function(){            
                });

        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>
<%block name="post_content">
</%block>
