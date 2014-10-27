<%inherit file="base.mako"/>
<%block name="control">
    <script src="${request.static_url('kunkka:static/tran.js')}"></script>
    <div class="row">
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Trip ID:</span>
            <input type="text" class="form-control" id="trip_id">
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Service ID:</span>
            <input type="text" class="form-control" id="service_id">
        </div>
        <div class="col-md-3">
            <input type="checkbox" id="chkHardRefresh"> Hard Refresh
        </div>
        <div class="col-md-3 input-group">
            <div class="btn-group">            
               <button id="go" type="button" class="btn btn-primary" href="#" onclick='open_report();' tabindex="-1">Refresh</button>
            </div>
        </div>
    </div>
</%block>
<%block name="inner_content">
    <div class="row clearfix">
        <div class="col-md-12 column"></div>
    </div>
    <div class="row clearfix">
        <div class="col-md-2 column"></div>
    </div>
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="tables"></div>               
        <script type="text/javascript">
            function report_callback(response) {
                if (response.success==true) {
                    try {
                        $("#go").text("Fetching...");
                        console.log( response.data.meta_content);
                        generateTables(response.data.tables);
                    }catch(e){
                        console.log(e);
                    }
                    $("#go").text("Go");
                    $("#go").attr("disabled",null);
                }else{
                    $("#go").text("Go");
                    $("#go").attr("disabled",null);
                }
            }
            function open_report() {
                var trip_id=$("#trip_id").val();
                var service_id=$("#service_id").val().trim();
                var hard_refresh=$("#chkHardRefresh").prop('checked');
                var url="${refresh_pickups_path}";
                if(trip_id.length==0 && service_id.length==0) {
                    return;
                }
                if(trip_id.length!=0){
                    url+="&TRIP_ID="+trip_id;
                }
                if(service_id.length!=0){
                    url+="&SERVICE_ID="+service_id;
                }
                url+="&HARD_REFRESH="+hard_refresh;
                $("#go").attr("disabled",true);
                $("#go").text("Refreshing...");
                $.getJSON(url,report_callback);
            }
            $(document).ready(function(){
                $(function() { });
            });
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts"></div>
    </div>
</%block>
<%block name="post_content"></%block>