<%inherit file="base.mako"/>
<%block name="inner_content">
    <div class="row">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">Payments Reports</h3>
        </div>
    </div>
    <div class="row">
        <div class="col-md-4"></div>
        <div class="col-md-2 input-group input-group-sm">
            <div class="radio">
              <label>Journey Date: <input type="radio" name="datewise" value="JD" checked="checked"></label>
            </div>
        </div>
        <div class="col-md-2 input-group input-group-sm">
            <div class="radio">
              <label>Booking Date: <input type="radio" name="datewise" value="BD"></label>
            </div>
        </div>
        <div class="col-md-4"></div>
    </div>
    <div class="row">
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Provider:</span>
            <select id="provider" class="form-control form-control"></select>
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Company:</span>
            <select id="company" class="form-control form-control"></select>
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">From:</span>
            <input type="text" class="form-control" id="from">
        </div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">To:</span>
            <input type="text" class="form-control" id="to">
        </div>
    </div>
    <div class="row" style="padding-top:10px;">
        <div class="col-md-4"></div>
        <div class="col-md-4 column btn-toolbar">
            <div class="btn-group-sm">            
                <button id="go" type="button" class="btn btn-primary" href="#" onclick='open_report();' tabindex="-1">Fetch Operators Payment</button>
            </div>            
        </div>
        <div class="col-md-4"></div>
    </div>
    <div class="row clearfix"><div class="col-md-12 column" style="padding-left:0px;"id="tables"></div></div>  
    <script>
        var report_callback = function(response)
        {
            if (response.success==true)
            {
                try
                {
                    $("#go").text("Fetching...");
                    console.log( response.data.meta_content);
                    generateTables(response.data.tables);
                    generateCharts(response.data.charts);
                }
                catch(e){}
                $("#go").text("Fetch Operators Payment");
                $("#go").attr("disabled",null);
            }else{
                $("#go").text("Fetch Operators Payment");
                $("#go").attr("disabled",null);
            }
        }
        var open_report = function()
        {
            $("#go").attr("disabled",true);
            $("#go").text("Fetching...");
            var str_from=$("#from").val();
            var str_to=$("#to").val();
            var company_id=$("#company").val();
            var provider_id=$("#provider").val();
            var datewise=$("input[name=datewise]:checked").val();
            $.getJSON("${operator_payments_path}"+"&FromDate="+str_from+"&ToDate="+str_to+"&ProviderId="+provider_id+"&CompanyId="+company_id+"&DateWise="+datewise,report_callback);
        }
        var get_companies_list = function()
        {
            var provider_id=$("#provider").val();
            var provider_company_list_path="${provider_company_list_path}"+"ProviderId="+provider_id;
            $.getJSON(provider_company_list_path,function(response){
                if(response.success==true){
                    var option=document.createElement("option");
                    $("#company").empty();
                    option.innerText="--All Company--";
                    option.value="0";
                    $("#company").append(option);
                    $(response.data.raw.Table).each(function(index,obj){
                        option=document.createElement("option");
                        option.value=obj.company_id;
                        option.innerText=obj.company_name;
                        $("#company").append(option);
                    });
                }else{
                    alert(response);
                }
            });
        }
        var get_provider_list = function()
        {
            var provider_list_path="${provider_list_path}";
                $.getJSON(provider_list_path,function(response){
                if(response.success==true){
                    var option=document.createElement("option");
                    $("#provider").empty();
                    option.innerText="--Select--";
                    $("#provider").append(option);
                    $(response.data.raw.Table).each(function(index,obj){
                        option=document.createElement("option");
                        option.value=obj.provider_id;
                        option.innerText=obj.provider_name;
                        $("#provider").append(option);
                    });
                }else{
                    alert(response);
                }
            });
        }
        $(document).ready(function() {
            $(function() {
                var d=new Date();
                date_from=d;
                date_to=d;
                $("#from").datepicker({ dateFormat: 'yy-mm-dd' });
                $("#to").datepicker({ dateFormat: 'yy-mm-dd' });
                $("#from").datepicker( "setDate" ,date_from);
                $("#to").datepicker( "setDate" ,date_to);
                get_provider_list();
                $("#provider").change(get_companies_list);
            });
        });
    </script>
</%block>
<%block name="post_content"></%block>
