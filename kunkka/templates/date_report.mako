<%inherit file="base.mako"/>
<%block name="control">
    <script src="${request.static_url('kunkka:static/tran.js')}"></script>
    <!--<script id="chart_js" src="${request.static_url('kunkka:static/highchart/highcharts.js')}"></script>    -->
    <!--<script id="chart_theme" src="${request.static_url('kunkka:static/highchart/themes/dark-green.js')}"></script>-->
    <div class="row">
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">From:</span>
            <input type="text" class="form-control" id="from">
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">To:</span>
            <input type="text" class="form-control" id="to">
        </div>
        <div class="col-md-2 column btn-toolbar">
            <div class="btn-group-sm">            
               <button id="go" type="button" class="btn btn-primary" href="#" onclick='open_report();' tabindex="-1">Go</button>               
          </div>            
        </div>
        <script>
            var d=new Date();
            date_from=d;
            date_to=d;
            %if not date_from==None:
                date_from=new Date('${date_from}');
            %endif
            %if not date_to==None:
                date_to=new Date('${date_to}');
            %endif          
            $(document).ready(function(){               
                $(function() {
                    $( "#from" ).datepicker({                       
                        dateFormat: 'yy-mm-dd'                      
                    });

                    $("#to" ).datepicker({                      
                        dateFormat: 'yy-mm-dd'                      
                    });
                    //console.log("${date_from}");                  
                    $("#from").datepicker( "setDate" ,date_from);
                    $("#to").datepicker( "setDate" ,date_to);
                    
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
                    $("#go").text("Go");
                    $("#go").attr("disabled",null);
                }else{
                    $("#go").text("Go");
                    $("#go").attr("disabled",null);
                    show_error(response.msg);
                }
            }
            function open_report()
            {
                $("#go").attr("disabled",true);
                $("#go").text("Fetching...");
                var str_from=$("#from").val();
                var str_to=$("#to").val();
                $.getJSON("${report_path}"+"&STR_FROM_DATE="+str_from+"&STR_TO_DATE="+str_to,report_callback);
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
