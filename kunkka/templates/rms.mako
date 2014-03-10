<%block name="inner_content">
<%inherit file="base.mako"/>
    <div class="row clearfix">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">
                GDS RMS
            </h3>
        </div>
    </div>
    <div class="row clearfix">        
        <div class="col-md-3 input-group">
            <span class="input-group-addon">From:</span>
            <input type="text" class="form-control" id="from">
        </div>
        <div class="col-md-3 input-group">
            <span class="input-group-addon">To:</span>
            <input type="text" class="form-control" id="to">
        </div>
        <div class="col-md-1">
            <div class="input-group">            
            <div class="input-group-btn">
              <button id="go" type="button" class="btn btn-default" href="#" onclick='go();' tabindex="-1">Go</span></button>
            </div>
          </div>            
        </div>
        <script type="text/javascript">
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
        <div class="col-md-2 column">
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">
            var allTableObjects;
            function getHandler(oTable){
                return function () {
                    /* Filter on the column (the index) of this element */
                    console.log(this);                                            
                    console.log($(this).parent().parent().parent().find("input").index(this));                        
                    oTable.fnFilter( this.value,$(this).parent().parent().find("input").index(this));
                }    
            }
            var asInitValsList;
            function generateTables(tables)
            {
                var content;
                var meta_content;
                var title;
                var div;
                var h1;
                var table;
                var rendered_tables;
                
                allTableObjects= new Array();
                document.getElementById("tables").innerHTML="";
                for(var i=0;i<tables.length;i++)
                {
                    div=document.createElement("div");
                    $(div).addClass("shodow_box");
                    h3=document.createElement("h3");
                    table_div=document.createElement("div");                                        
                    content=tables[i].content;
                    meta_content=tables[i].meta_content;
                    title=tables[i].title;
                    columns=[];
                    var sType;
                    console.log(meta_content);
                    var index=0;
                    for(var col in meta_content)
                    {
                        console.log(col);
                        if(meta_content[col].type=="float")
                        {
                            sType="numeric";
                        }else if(meta_content[col].type=="int"){
                            sType="numeric";
                        }else if(meta_content[col].type=="str"){
                            //TODO:Date type
                            sType="html";
                        }
                        columns.push({"sType":sType,"aTargets":[index],"bSearchable": true,"sName":col,"bSortCellsTop":true})
                        index++;
                    }
                    /*Content Rendering*/               
                    h3.innerHTML=title;
                    table_div.innerHTML=content;
                    div.appendChild(h3);
                    div.appendChild(table_div);
                    document.getElementById("tables").appendChild(div);
                    $(table_div).addClass("table-responsive");
                    rendered_tables=$(table_div).find("table");
                    rendered_tables.addClass("table");
                    rendered_tables.addClass("table-bordered")
                    rendered_tables.addClass("table-striped")
                    

                    var oTables=$(rendered_tables).dataTable({
                        "aoColumnDefs": columns,
                         "sDom": "<'row'<'col-xs-6'T><'col-xs-6'f>r>t<'row'<'col-xs-6'i><'col-xs-6'p>>"                                             
                        
                    });
                    console.log(oTables)
                    console.log(i);
                    allTableObjects[i]=oTables;                                        
                    $(oTables).find("tfoot").find("input").keyup(getHandler(oTables));
                    $(oTables).find("tfoot").find("input").css("font-size","smaller");
                }
                $(".dataTables_filter").css("padding","10px");
                $(".dataTables_filter").find("input").addClass("form-control");
                $(".dataTables_filter").addClass("input-group-sm");                                    
            }
            $(document).ready(function(){               
                callback=function(response)
                {
                    if (response.success==true)
                    {
                        console.log( response.data.meta_content);
                        generateTables(response.data.tables)
                        generateCharts(response.data.charts)
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
                $.getJSON("/report/agents_details/?SUB_AGENT_ID=333",callback)
                
                });
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>    
        <script type="text/javascript">
            var allChartObjects;
            function generateCharts(charts)
            {
                var content;
                var meta_content;
                var title;
                var div;
                var h1;
                var table;
                var rendered_tables;
                allChartObjects=new Array();                
                for(var i=0;i<charts.length;i++)
                {                    
                    
                    div=document.createElement("div");
                    $(div).addClass("shodow_box");
                    h3=document.createElement("h3");
                    chart_div=document.createElement("div");                                        
                    content=
                    meta_content=charts[i].meta_content;                    
                    h3.innerHTML=charts[i].title;                    
                    
                    div.appendChild(h3);
                    div.appendChild(chart_div);
                    document.getElementById("charts").appendChild(div);
                    $(chart_div).highcharts(charts[i].content)
                    allChartObjects.push(charts[i].content)
                }
            }            
        </script>
    </div>
</%block>    
<%block name="post_content">
    
</%block>    