<%block name="inner_content">
<%inherit file="base.mako"/>
    <div class="row clearfix">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">
                Junk Pickups
            </h3>
        </div>
    </div>    
    <div  class="row clearfix">
        <div class="col-md-1">
        </div>
        <div class="col-md-8 input-group input-group-sm">
            <span class="input-group-addon">                        
            Select City
            </span>
            <select id="cities" class="form-control form-control">               
            </select>
          <!--
                  <span class="input-group-btn">
                    <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown"><span class="glyphicon glyphicon-remove"></span>
                    </button>
                  </span>
                  -->
        </div>
        <div class="col-md-3 column btn-toolbar" role="toolbar">
            <div class="btn-group btn-group-sm">
                <button id="get_junk_pickups" type="button" class="btn btn-primary" onclick="get_junk_pickups();">Go</button>
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
    <div style="padding-top:10px;" class="row clearfix">
        <div class="col-md-1">
        </div>
        <div class="col-md-8 input-group input-group-sm">
            <span id="lbl_area" class="input-group-addon">Area</span>
            <input type="text" class="form-control" id="area">
            <span id="lbl_flag_address" class="input-group-addon">To Address:&nbsp<input id="map_to_address" type="checkbox"></span>
            
            <!--

            <div class="input-group-btn">
            <button type="button" class="run btn btn-primary" disabled>Update</button>
            </div>
            -->
            <!-- /btn-group -->            

        </div>               
        <!--
        <div class="col-md-3 input-group input-group-sm">
            <div class="input-group-btn">
            <button type="button" class="run btn btn-primary">Create</button>
            </div>
        </div>
        -->
        
    </div>
    
    <div style="padding-top:10px;" class="row clearfix">        
        <div class="col-md-1">
        </div>
        <div class="col-md-8 input-group input-group-sm">                
            <span class="input-group-addon">Choose Parent Area Name</span>
            <select type="text" class="form-control" id="parent_area"></select>
            <div class="input-group-btn">
                <button type="button" onclick="update_area();" disabled="true" id="update" class="run btn btn-primary">Update</button>
            </div><!-- /btn-group -->
            
        </div>
        <div class="col-md-3 column btn-toolbar" role="toolbar">
            <div class="btn-group btn-group-sm">
                <button type="button" onclick="create_area();" id="create" disabled="true" class="run btn btn-primary">New</button>
            </div><!-- /btn-group -->
        </div>
              
    </div>    

    <div class="row clearfix">

        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">
            var current_area_matcher=null;
            function create_area(){
                BootstrapDialog.show({
                    title: 'CREATE NEW AREA',
                    type: BootstrapDialog.TYPE_PRIMARY,
                    closable:false,
                    message: $('<input id="new_area_name" class="form-control" placeholder="Area Name"></textarea>'),                    
                    buttons: [{
                        label: 'Cancel',
                        action: function(dialogRef){
                            console.log("Cancelled");
                            $("#btn_activate_prov").attr("disabled",null);
                            dialogRef.close();                            
                        }
                    }, {
                        label: 'Create',
                        cssClass: 'btn-primary',
                        hotkey: 13, // Enter.
                        action: function(dialogRef){
                            // You can also use BootstrapDialog.closeAll() to close all dialogs.
                            $("#new_area_name").attr("disabled",true);                        
                            var new_area_name=document.getElementById("new_area_name").value;
                            $.ajax({
                                url:"${create_area}"+"?CITY_ID="+city_id+"&"+"AREA_NAME="+new_area_name,
                                success:function(response){console.log(response);                                    
                                    dialogRef.close();        
                                    get_junk_pickups();                                    
                                }
                            })
                            
                        }
                    }]
                });

            }
            function update_area()
            {
                var area_name=$("#area").val();
                var parent_area_id=$("#parent_area").val();
                var FLAG_TO_ADDRESS=0;
                console.log(area_name);
                console.log(parent_area_id);                
                if($("#map_to_address")[0].checked){
                    FLAG_TO_ADDRESS=1;
                }else{
                    FLAG_TO_ADDRESS=0;
                }
                $.ajax({
                    url:"${update_area_path}"+"?CITY_ID="+city_id+"&"+"AREA_NAME="+area_name+"&"+"PARENT_AREA_ID="+parent_area_id+"&"+"FLAG_TO_ADDRESS="+FLAG_TO_ADDRESS,
                    success:function(response){console.log(response);                        
                        $("#update").text("Update");
                        get_junk_pickups();
                        $("#update").attr("disabled",null);                        
                        
                    }
                })
                $("#update").text("Updating");
                $("#update").attr("disabled",true);
                
            }
            function init_area_matching(dataTable,areas)
            {               
                fun_area_match=function () {
                    /* Filter on the column (the index) of this element */
                    console.log($("#map_to_address")[0].checked);
                    var area_name=$("#area").val().toUpperCase();                  
                    if (area_name.length>2)
                    {
                        if($("#map_to_address")[0].checked){
                            dataTable.fnFilter( "",0);
                            dataTable.fnFilter( area_name,4,false,false);
                        }else{
                            dataTable.fnFilter( "",4);
                            dataTable.fnFilter( area_name,0,false,false);
                        }
                        
                        var n=dataTable.fnSettings().fnRecordsDisplay();
                        if (n>0){
                            $("#lbl_area").removeClass("label-danger").addClass("label-success").text("Area("+n+")");
                            $("#update").attr("disabled",null);
                            
                        }else{
                            $("#lbl_area").removeClass("label-success").addClass("label-danger").text("Area");
                            $("#update").attr("disabled",true);
                        }
                    }else{
                        dataTable.fnFilter( "",0);
                        dataTable.fnFilter( "",4);
                        $("#lbl_area").removeClass("label-danger").removeClass("label-success").text("Area");
                        $("#update").attr("disabled",true);
                    }
                

                }
                current_area_matcher=fun_area_match

                var area_result=[]
                var obj;
                var option;
                document.getElementById("parent_area").innerHTML="";
                option=document.createElement("option");
                option.value=0;
                option.innerHTML="INVALID_CITY";               
                $("#parent_area").append(option);


                option=document.createElement("optgroup");                
                option.label="-----";               
                $("#parent_area").append(option);
                
                for(var i in areas){
                    obj=areas[i];
                    option=document.createElement("option");
                    option.value=obj.id;
                    option.innerHTML=obj.display_name;
                    /*
                    area_result.push({
                        "label": obj.display_name,
                        "value": obj.display_name,
                        "id": obj.id
                    });                            
                    */
                    $("#parent_area").append(option);
                } 
                

                /*
                $( "#parent_area" ).autocomplete({
                        autoFocus:true,
                        select: function( event, ui ) {
                            console.log(ui.item);                            
                            $(this).attr("selected_id",ui.item.id);
                            $(this).attr("selected_text",ui.item.value);
                            $(this).removeClass("label-danger").addClass("label-success");
                        },
                        change: function(event, ui)
                       {
                       
                        try
                        {
                            console.log(event.originalEvent.type);
                            if(event.originalEvent.type != "menuselected")
                            {
                                 // Unset ID                                
                                $("#parent_area").attr("selected_id",-1);
                                //$("#parent_area").removeClass("label-success").addClass("label-danger");

                            }
                        }
                        catch(err){ 
                            // unset ID 
                            $("#parent_area").attr("selected_id",-1);
                            $("#parent_area").removeClass("label-success").addClass("label-danger");
                                                   
                       },
                        source: area_result
                    }
                );
                */
                $("#area").keyup(fun_area_match);
                $("#map_to_address").change(fun_area_match);
            }            
            function pickup_callback(response)
            {
                try{
                     if (response.success==true)
                    {
                        console.log(response.data.meta_content);                    
                        allTableObjects=generateTables(response.data.tables);
                        //Init area matching
                        init_area_matching(allTableObjects[0],response.data.raw.Table1);
                        current_area_matcher();
                        $("#create").attr("disabled",null);
                        //generateCharts(response.data.charts)
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
                }catch(error){                    
                }            
                $("#get_junk_pickups").text("Go");
                $("#get_junk_pickups").attr("disabled",null);
            }
            function get_junk_pickups()
            {
                var elem_select=document.getElementById("cities");
                city_id=elem_select.value;
                $("#get_junk_pickups").text("Fetching...");
                $("#get_junk_pickups").attr("disabled",true);
                if(city_id.length>0){
                    $.getJSON("${pickups_path}"+"?CITY_ID="+city_id,pickup_callback);

                }
            }
            $(document).ready(function(){                               
                city_list_callback= function(response)
                {
                    if (response.success==true){
                        console.log(response.data);
                        cities=response.data.raw.Table;
                        var city_data;
                        var elem_option;
                        var elem_select=document.getElementById("cities");
                        elem_select.innerHTML="";
                        for (var i in cities)
                        {
                            city_data=cities[i];
                            elem_option=document.createElement("option");
                            elem_option.value=city_data.city_id;
                            elem_option.innerHTML=city_data.city_name[0].toUpperCase()+city_data.city_name.substring(1);
                            elem_select.appendChild(elem_option);
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