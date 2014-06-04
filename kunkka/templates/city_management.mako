<%block name="inner_content">
<%inherit file="base.mako"/>
    <div class="row clearfix">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">
                City Management
            </h3>
        </div>
    </div>    
    <div  class="row clearfix">       
        <div class="col-md-2 column">            
        </div>
        <div class="col-md-6 input-group input-group-sm">
            <span class="input-group-addon">State: </span>
            <select id="state" class="form-control form-control">               
            </select>                        
        </div>                
    </div>    
    <div  class="row clearfix" style="padding-top:10px;">              
        <div class="col-md-2">      
        </div>
        <div class="col-md-1 col btn-toolbar merge-city">
            <div class="btn-group-sm">
              <button id="btn_merge" type="button" onclick="pre_merge();" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">
                Merge To<span class="caret"></span>
              </button>
              <ul class="dropdown-menu" role="menu">
                
              </ul>
            </div>          
        </div>
        <div class="col-md-1">      
        </div>
        <div class="col-md-6 col">
            <div class="input-group input-group-sm">
              <span class="input-group-addon">Parent City: </span>
              <select id="parent_city" class="form-control form-control">               
              </select>
              <span class="input-group-btn btn-group-sm">
                <button id="btn_set_parent" onclick="set_parent();" class="btn btn-primary" type="button">Set</button>
              </span>
            </div>
          </div>
    </div>     
    <div class="row clearfix">

        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">  

            function merge(real_city_id){
                var d=$("#tables table").dataTable().fnGetNodes();
                var cids=[];                          
                $("input:checked",d).parent().parent().each(function(index,tr_obj){
                    cids.push(tr_obj.id.split("_")[1]);
                });
                console.log(cids);
                console.log(real_city_id);
                var merge_city_path="${merge_city_path}"+"REAL_CITY_ID="+real_city_id+"&CIDS="+cids.join(",");
                $("#btn_merge").text("Merging...");
                $("#btn_merge").attr("disabled",true);
                $.ajax({
                    url:merge_city_path,
                    success:function(response){
                        if(response.success==true){
                            console.log(response);
                            get_city_list();
                        }else{
                            alert(response.msg);
                        }
                        $("#btn_merge").text("Merge To");
                        $("#btn_merge").attr("disabled",null);
                    }
                });
            }
            function pre_merge(){
                var d=$("#tables table").dataTable().fnGetNodes();
                var ul_obj=$(".merge-city ul.dropdown-menu");
                ul_obj.empty();
                $("input:checked",d).parent().parent().each(function(index,tr_obj){
                    var id=tr_obj.id.split("_")[1];
                    var name=$($(tr_obj).find("td")[2]).text();
                    var li=document.createElement("li");
                    li.innerHTML='<a onclick="merge('+id+')" href="#">'+name+'</a>';
                    ul_obj.append(li);
                });
            }
            function set_parent(){
                var d=$("#tables table").dataTable().fnGetNodes();
                var cids=[];
                var parent_city_id=$("#parent_city").val();
                $("input:checked",d).parent().parent().each(function(index,tr_obj){
                    cids.push(tr_obj.id.split("_")[1]);
                });
                console.log(cids);
                console.log(parent_city_id);
                var set_parent_city_path="${set_parent_city_path}"+"PARENT_CITY_ID="+parent_city_id+"&CIDS="+cids.join(",");
                $("#btn_set_parent").text("Setting...");
                $("#btn_set_parent").attr("disabled",true);
                $.ajax({
                    url:set_parent_city_path,
                    success:function(response){
                        if(response.success==true){
                            console.log(response);
                            get_city_list();
                        }else{
                            alert(response.msg);
                        }
                        $("#btn_set_parent").text("Set");
                        $("#btn_set_parent").attr("disabled",null);
                    }
                });
            }           
           
            function get_city_list(){
                var state_id=$("#state").val();
                var city_list_path="${city_list_path}"+"STATE_ID="+state_id;
                $.getJSON(city_list_path,function(response){
                    if(response.success==true){
                        generateTables(response.data.tables);
                        $("#parent_city").empty();
                        $(response.data.raw.Table).each(function(index,obj){
                            var option=document.createElement("option");
                            option.innerText=obj.NAME;
                            option.value=obj.id;
                            $("#parent_city").append(option);
                        });
                    }else{
                        alert(response.msg);
                    }                    
                });
            }
            function get_state_list(){
                var state_list_path="${state_list_path}";
                $.getJSON(state_list_path,function(response){
                    if(response.success==true){
                        var option=document.createElement("option");
                        $("#state").empty();                        
                        option.innerText="--Select--";
                        $("#state").append(option);
                        $(response.data.raw.Table).each(function(index,obj){
                                option=document.createElement("option");
                                option.value=obj.state_id;
                                option.innerText=obj.state_name;
                                $("#state").append(option);
                            });
                    }else{
                        
                    }
                });
            }
            $(document).ready(function(){
                get_state_list();
                $("#state").change(get_city_list);
            })
        </script>
        <style type="text/css">
            .select-check{
              display: block;
            }
        </style
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>    
<%block name="post_content">
    
</%block>    