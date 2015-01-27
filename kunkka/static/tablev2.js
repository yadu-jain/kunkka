function getHandler(oTable){
                return function () {
                    /* Filter on the column (the index) of this element */
                    console.log(this);                                            
                    console.log($(this).parent().parent().parent().find("input").index(this));                        
                    oTable.fnFilter( this.value,$(this).parent().parent().find("input").index(this));
                }    
            }
var flash_path="http://www.datatables.net/release-datatables/extensions/TableTools/swf/copy_csv_xls_pdf.swf";            
function generateTables(tables,add_to)
{
    var content;
    var meta_content;
    var title;
    var div;
    var h1;
    var table;
    var rendered_tables;
    
    if (add_to==undefined){                    
        add_to="tables";
    }
    if(allTableObjects==undefined ||allTableObjects==null){
        allTableObjects= new Array();
    }
    document.getElementById(add_to).innerHTML="";                                
    for(var i=0;i<tables.length;i++)
    {
        div=document.createElement("div");
        $(div).addClass("shodow_box");
        h3=document.createElement("h3");
        $(h3).addClass("text-center");
        $(h3).addClass("text-primary");                    
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
        document.getElementById(add_to).appendChild(div);
        if($(div).find("tr").length==0)
        {
            continue;
        }                    
        $(table_div).addClass("table-responsive");
        rendered_tables=$(table_div).find("table");
        rendered_tables.addClass("table");
        rendered_tables.addClass("table-bordered")
        rendered_tables.addClass("table-striped")                    
        var oTables=$(rendered_tables).dataTable({
            "aoColumnDefs": columns,
            "iDisplayLength":10,
            "sDom": 'T<"clear">lfrtip',
            "oTableTools": {
                "buttons": [
                    "copy",
                    "csv",
                    "xls",
                    "pdf",
                    { "type": "print", "buttonText": "Print me!" }
                ],
                "sSwfPath" : flash_path
            }

             //"sDom": "<'row'<'col-xs-6'T><'col-xs-6'f>r>t<'row'<'col-xs-6'i><'col-xs-6'p>>"                                             
        });
        //var tt = new $.fn.dataTable.TableTools( oTables ); 
        //$( tt.fnContainer() ).insertBefore('div.shodow_box');
        /*
        var tableTools = new $.fn.dataTable.TableTools( oTables, {
            "buttons": [
                "copy",
                "csv",
                "xls",
                "pdf",
                { "type": "print", "buttonText": "Print me!" }
            ]
        } );                      
        */
        //$( tableTools.fnContainer() ).insertAfter('div.info');
        
        
        allTableObjects[i]=oTables;                                        
        $(oTables).find("tfoot").find("input").keyup(getHandler(oTables));
        $(oTables).find("tfoot").find("input").css("font-size","smaller");
        
    }
    $(".dataTables_filter").css("padding","10px");
    $(".dataTables_filter").find("input").addClass("form-control");
    $(".dataTables_filter").addClass("input-group-sm");                                    
    return allTableObjects;
} 
