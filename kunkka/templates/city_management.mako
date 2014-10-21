<%block name="inner_content">
<%inherit file="base.mako"/>
    <div class="row clearfix">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">City Management</h3>
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-2 column"></div>
        <div class="col-md-6 input-group input-group-sm">
            <span class="input-group-addon">State: </span>
            <select id="state" class="form-control form-control"></select>
        </div>
        <div class="col-md-4 col btn-toolbar merge-city">
            <div class="btn-group-sm">
              <button id="btn_merge" type="button" onclick="pre_merge();" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">Merge To<span class="caret"></span></button>
              <ul class="dropdown-menu" role="menu"></ul>
            </div>
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="tables"></div>
        <script type="text/javascript">
            function selet_city(e){
                var city_id=e.target.parentNode.id.split("_")[1];
                var obj=$("#Table_"+city_id);
                if(obj.hasClass("row_selected")){
                    obj.removeClass("row_selected");
                }else{
                    obj.addClass("row_selected");
                }
            }
            function merge(city_id){
                var d=$("#tables table").dataTable().fnGetNodes();
                var cids=[];
                $(d).filter("tr.row_selected").each(function(index,tr_obj){
                    cids.push(tr_obj.id.split("_")[1]);
                });
                var merge_city_path="${merge_city_path}"+"CityId="+city_id+"&CIDS="+cids.join(",");
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
                $(d).filter("tr.row_selected").each(function(index,tr_obj){
                    var id=tr_obj.id.split("_")[1];
                    var did=$($(tr_obj).find("td")[2]).text();
                    var name=$($(tr_obj).find("td")[1]).text();
                    var li=document.createElement("li");
                    li.innerHTML='<a onclick="merge('+id+')" href="#">'+name+'</a>';
                    if(id === did){
                        $(li).children().attr("style","color:#006400;font-weight:bold;text-transform:capitalize;");
                    }
                    ul_obj.append(li);
                });
            }
            function get_city_list(){
                var state_id=$("#state").val();
                var city_list_path="${city_list_path}"+"STATE_ID="+state_id;
                $.getJSON(city_list_path,function(response){
                    if(response.success==true){
                        generateTables(response.data.tables);
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
                        alert(response);
                    }
                });
            }
            $(document).ready(function(){
                get_state_list();
                $("#state").change(get_city_list);
                $("#tables").click(selet_city);
            })
        </script>
        <style type="text/css">
            .select-check{ display: block; }
        </style>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts"></div>
    </div>
</%block>
<%block name="post_content"></%block>