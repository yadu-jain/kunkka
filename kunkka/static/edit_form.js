/*
Author: Heera
Created On: 2015-01-09
Description: to create edit forms
*/

function init_controls(){
	var div_control=$("#tables .table-responsive div.controls")
	if (div_control.length==0){
		$("#tables .table-responsive table").before('<div class="controls"></div>')
	}
}
function init_edit_forms(edit_forms){
	init_controls();	
	if (edit_forms && edit_forms.length>0){
		for (var i in edit_forms){
			var edit_form=edit_forms[i];
			var table_no=edit_form.content.table_no;		
			//TODO:
			$($(".dataTables_wrapper")[table_no]).parent().find("div.controls").append('<button type="button" table_no="'+table_no+'" id="edit" onclick="edit('+table_no+');" class="btn btn-sm btn-primary">Edit</button>');
			$($(".dataTables_wrapper")[table_no]).on("click",select_row);
		}
	}	
}

function edit(table_no){		
	var id=$($(".dataTables_wrapper")[table_no]).find("tr.row_selected")[0].id.split("_")[1]
	var form_url='/report_ajax/update_agent_details/';

    $("#edit").attr("disabled","true");        
    $("#edit").text("Loading...");        

    function edit_callback(response){
	    $("#edit").attr("disabled",null);                
	    $("#edit").text("Edit");        
	    if(response.success==true){
	    	open_edit_popup(create_form(response.data),form_url,id)	
	    }else{
	    	show_error(response.msg);
	    }
	    
	} 
    $.ajax({
    	url:form_url+'?ID='+id,
    	method:'GET',    	
    	success:edit_callback
    });
    	//"${report_path}"+"START_WITH="+start_with,report_callback);
}
function create_form(data){
    var form_data=data.raw.Table[0];
    var edit_form='<div style="width:80%;padding-left:50px" class="form-group">';
    var fields={}
    for(var field in form_data){
        fields[field]={};
    }                
    create_validation(fields,data.raw);

    for(var field in form_data){                    
        if(fields[field].type=="select"){
            edit_form+='<div class="input-group selector"><span class="input-group-addon">'+field.toUpperCase()+'</span><select name="'+field.toUpperCase()+'" class="form-control" >'            
            if(typeof(fields[field].data[0])=='string'){                            
                for (var item in fields[field].data){                            
                    if(form_data[field]==fields[field].data[i]){
                        edit_form+='<option selected value="'+fields[field].data[i]+'">'+fields[field].data[i]+'</option>'    
                    }else
                    {
                        edit_form+='<option value="'+fields[field].data[i]+'">'+fields[field].data[i]+'</option>'    
                    }                                        
                }               
            }else{
                for (var i in fields[field].data){                                                            
                    if(form_data[field]==fields[field].data[i].value){
                        edit_form+='<option selected value="'+fields[field].data[i].value+'">'+fields[field].data[i].label+'</option>'
                    }else
                    {
                        edit_form+='<option value="'+fields[field].data[i].value+'">'+fields[field].data[i].label+'</option>'
                    }                    
                }
               
            }
            edit_form+='</select></div>'  

        }else
        {
            if (field.toUpperCase()=="ID" ||field.toUpperCase()=="NAME")
            {
                edit_form+='<div class="input-group"><span class="input-group-addon">'+field.toUpperCase()+'</span><input disabled="true" name="'+field.toUpperCase()+'" type="text" class="form-control" value="'+form_data[field]+'"></div>'
            }            
            else
            {
                edit_form+='<div class="input-group"><span class="input-group-addon">'+field.toUpperCase()+'</span><input name="'+field.toUpperCase()+'" type="text" class="form-control" value="'+form_data[field]+'"></div>'
            }
            
        
        }                    
        
    }
    edit_form+='</div>';                 
    return edit_form

}
function create_validation(fields,tables){
    var n=Object.keys(tables).length;
    for (var field in fields){
        for(var i=1;i<n;i++){ 
            var field_data=tables["Table"+i];

            if(field_data[0][field]){
                fields[field].data=[];
                fields[field].type="select";
                for(var j=0;j<field_data.length;j++){
                    if (field_data[j].VALUE==undefined){
                        fields[field].data.push(field_data[j][field])  
                    }else{
                        fields[field].data.push({"value":field_data[j].VALUE,"label":field_data[j][field]})
                        
                    }
                    
                }
            }
        }    
    }
    return fields;
}
function field_changed(e){                
    $(e.target).parent().find("span.input-group-addon,input,select").addClass("data-changed");
}
function open_edit_popup(edit_form,save_url,id){
    var dialog = new BootstrapDialog({
        title: "Edit",        
        type: BootstrapDialog.TYPE_INFO,
        closable:false,                    
        closeByKeyboard: true,
        message:edit_form,
        buttons: [{
            label: 'Cancel',
            action: function(dialogRef){                
                $("#save_changes").attr("disabled",null);
                dialogRef.close();                            
            }
        }, {
            label: 'Save',
            cssClass: 'btn-warning',
            //hotkey: 13, // Enter.            
            action: function(dialogRef){
                    dialogRef.enableButtons(false);
                    dialogRef.setClosable(false);                    
                    //dialogRef.getModalBody().html('Dialog closes in 5 seconds.');
                    save_fields(save_url,id,dialogRef)
            }
        }]
    });               
    dialog.realize();        
    dialog.getModalBody().css('width', '');
    dialog.getModalBody().css('height', '');
    dialog.getModalBody().find("input,select").on("change",field_changed)                
    dialog.open();
}
function select_row(e){
	var temp=e.target.parentNode;	
	temp=$(temp).filter(".table_row");
	if (temp.length>=1){
	    $("#edit").attr("disabled",null);                       
	    var id=e.target.parentNode.id.split("_")[1];                
	    $("#tables .table_row").removeClass("row_selected");                
	    $(temp).addClass("row_selected");
	}
}  
function save_fields(save_url,id,dialogRef){                
    var name;
    var value;
    var post_data=new Object();
    dialogRef.getModalBody().find("input.data-changed,select.data-changed").each(function(index,obj){
        name=$(obj).attr("name");
        value=$(obj).val();                    
        post_data[name]=value;                    
    });
    console.log(post_data);            
    $.ajax({
        url:save_url+'?ID='+id,
        method:'POST',
        type:'JSON',
        data:post_data,
        success:function(response){
            if(response.success==false){
            	show_error(response.msg);            	
            }else
            {
            	dialogRef.close();                
            	open_report();
            }
            dialogRef.enableButtons(true);
            dialogRef.setClosable(false);                                    
        }
    });                
    
}            
