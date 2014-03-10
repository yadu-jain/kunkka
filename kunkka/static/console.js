

var changed=false;
var dict_queries=null;
var date_wise_data=null;
var raw_data=null;
function to_csv(){
	var date_key=document.getElementById("dates").value;
	var data=date_wise_data[date_key];
	if (data.type=="sheet"){
		ToCSV(data.rows,data.headers.names,data.title);		
	}
	
}
function to_json(){
	var date_key=document.getElementById("dates").value;
	var data=date_wise_data[date_key];		
	ToJSON({"data":data.rows},data.title);
}
function to_raw_json(){
	var date_key=document.getElementById("dates").value;
	var data=date_wise_data[date_key];			
	ToJSON(raw_data,data.title);	
}
/****Render Data***/
function add_to_table(str_date){
	document.getElementById("report_window").style.display="block";
	var data=date_wise_data[str_date];
	if (data.type=="sheet" && data.headers && data.rows){
		document.getElementById("result_title").innerHTML='<span class="just_pretty">'+data.title+'</span>';
		set_grid(data.headers,data.rows);		
	}else if (data.type){
		document.getElementById("result_title").innerHTML=data.title;
	}else{
		alert("no result found !");
	}
	
}
function render(data,title)
{
	/*
	result_data={
				headers:{names=[]},
				rows:[
						{data:[],id=1}
						,{data:[],id=1}
						,{data:[],id=1}
					]
				title:"title"
				}

	*/
	var date_wise_result=new Object();
	if (data && data!=null)
	{
		for (var j=0;j<data.length;j++ ){
			var date_data=data[j].data;
			var result_data=new Object();		
			result_data.rows=[];

			if (date_data instanceof Array){
				result_data.type="sheet";
				for(var i=0;i<date_data.length;i++){
					var obj=date_data[i];
					var temp_arr=[];					
					for (var key in obj){
						temp_arr.push(obj[key]);
					}
					if(result_data.headers==undefined){
						result_data.headers={"names":[]};
						for (var key in obj){
							result_data.headers.names.push(key);
						}
					}
					result_data.rows.push({"data":temp_arr,"id":i+1});
					result_data.title=title;
					
				}
			}else if(date_data instanceof Object){
				var str_data='<span class="just_pretty">'+title+'</span>: ';
				for (var key in date_data){
					str_data+=key+": "+date_data[key]+'<br/>'
				}
				console.log("TODO");
				result_data.title=str_data;
				result_data.type="object";
			}
			else{
				result_data.title='<span class="just_pretty">'+title+'</span>: '+date_data;
				result_data.type="string";
			}		
			date_wise_result[data[j].date]=result_data;
		}

		
	}
	console.log(date_wise_result)
	return date_wise_result
}
function getAdminPwd(){
	return prompt("Enter Admin Password:");
}
function create_args(val)
{
	var arguments=document.getElementById("arguments");
	if(val<=0)
	{
		arguments.innerHTML=""
		return;
	}
	//arguments.innerHTML="";
	arguments.innerHTML='<div class="col-lg-1 input-group input-group-sm"><span class="input-group-addon">Arguments:</span></div>';
	/*
	var div=document.createElement("div");
	div.innerHTML='<span class="input-group-addon">Arguments:</span>';
	div.classList.add("col-lg-"+val+1);
	div.classList.add("input-group");
	div.classList.add("input-group-sm");
	arguments.appendChild(div);
	*/
	for (var i=0;i<val;i++)
	{

		var arg_div=document.createElement("div");  					
		arg_div.classList.add("col-lg-1");  					 
		arg_div.classList.add("input-group");
		arg_div.classList.add("input-group-sm");
		arg_div.innerHTML='<input id ="arg'+i+'" type="text" class="form-control" placeholder="arg '+i+'">'
		arguments.appendChild(arg_div);
		/*
		var arg_ip=document.createElement("input");  					
		//arg_div.classList.add("col-lg-1");  					 
		arg_ip.classList.add("form-control");
		//arg_div.classList.add("input-group-sm");
		arg_ip.id="arg"+i;
		arg_ip.type="text"
		arg_ip.placeholder="arg "+i;
		div.appendChild(arg_ip);
		*/
	}
}
function open_editor(id)
{
	if (id)
	{

		$.getJSON("/rest/query/?id="+id,function(res){
			if(res.success==true)
			{
				document.getElementById("editor_window").style.display="block";				
				var query =JSON.parse(res.data[0]._str_query);
				var session=ace.createEditSession(query.str_query, "ace/mode/javascript")
				var editor = ace.edit("editor");				
			    editor.setTheme("ace/theme/monokai");
			    session.on("change", function(obj){
			    	if (changed==false){
			    		var save=document.getElementById("save");
			    		save.innerText="*Save";
			    		changed=true;
			    		return true;	
			    	}
			    	
			    });
			    editor.setSession(session);			    
			    var d=document.getElementById("editor");
			    d.setAttribute("query_id",id);
			    var args_count_options=document.getElementById("test_args_count");
			    document.getElementById("coll").value=query.coll;
			    document.getElementById("db_name").value=query.db_name;
			    document.getElementById("query_name").value=res.data[0].name;
			    if (res.data[0].level==1){
			    	document.getElementById("only_admin").checked=true;
			    }else
			    {
			    	document.getElementById("only_admin").checked=false;
			    }
			    args_count_options.value=res.data[0].args_count;
			    create_test_args();
			}else
			{
				alert(res.msg);
			}
		});

	}else
	{
		$.getJSON("/mongo/new/",function(res){
			if (res.success==true)
			{				
				document.getElementById("editor_window").style.display="block";				
				var session=ace.createEditSession(res.default_text, "ace/mode/javascript")
				var editor = ace.edit("editor");				
			    editor.setTheme("ace/theme/monokai");
			    session.on("change", function(obj){
			    	if (changed==false){
			    		var save=document.getElementById("save");
			    		save.innerText="*Save";
			    		changed=true;
			    		return true;	
			    	}
			    	
			    });
			    editor.setSession(session);		
			    document.getElementById("query_name").value=""
			    var d=document.getElementById("editor");
			    d.setAttribute("query_id",-1);
			    var args_count_options=document.getElementById("test_args_count");
			    args_count_options.value=0;
			    create_test_args();

			}else
			{
				alert(res.msg)
			}
		});
	
	}
}
function open_query()
{
	var query_id=document.getElementById("queries").value;
	open_editor(query_id);

}
function select_query()
{
	var queries=document.getElementById("queries");
	var id=queries.value;	
	create_args(dict_queries[id].args_count);
}
function get_queries()
{
//TODO:
	$.getJSON("/rest/query_list/",function(res){
			if (res.success==true)
			{				
				var queries=document.getElementById("queries");
				queries.innerHTML="";
				dict_queries=new Object();
				for (var i=0;i<res.data.length;i++)
				{
					var op=document.createElement("option");
					op.value=res.data[i].id;
					op.innerText=res.data[i].name;
					queries.appendChild(op);
					dict_queries[res.data[i].id]=res.data[i];
				}
				queries.onchange=select_query;
				select_query();
			}else{
				alert(res.msg);
			}
		}
	);
}

function close_editor()
{
	document.getElementById("editor_window").style.display="none";
}
function save()
{
	var ed=document.getElementById("editor")
	console.log(ed.getAttribute("query_id"));
	var query_id=ed.getAttribute("query_id");
	var editor = ace.edit("editor");				
	var query_str=editor.getValue();
	var args_count=document.getElementById("test_args_count").value;
	var coll=document.getElementById("coll").value;
	var db_name=document.getElementById("db_name").value;
	var level=0;
	var only_admin=document.getElementById("only_admin");
	var adminPwd=getAdminPwd();
	if (only_admin.checked==true){
		level=1;
	}
	
	var name=document.getElementById("query_name").value;
	if (name.length==0)
	{
		name="default";
	}
	var data={"id":query_id
				,"name":name
				,"query":query_str
				,"args_count":args_count
				,"db_name":db_name
				,"coll":coll
				,"level":level
				,"adminPwd":adminPwd
				};
	$.ajax({
		url:"/mongo/save/",
		data:data,
		method:"POST",
		dataType:"JSON",
		type:"JSON",
		success:function(res){
			if (res.success==true)
			{
				id=res.query.id;
				ed.setAttribute("query_id",id);
				var save=document.getElementById("save");
		    	save.innerText="Save";
		    	changed=false;
		    	get_queries();
			}else{
				alert(res.msg);
			}
		}
	});
}

function save_as()
{
	var ed=document.getElementById("editor")	
	var query_id=-1;
	var editor = ace.edit("editor");				
	var query_str=editor.getValue();
	var args_count=document.getElementById("test_args_count").value;
	var coll=document.getElementById("coll").value;
	var db_name=document.getElementById("db_name").value;
	var level=0;
	var only_admin=document.getElementById("only_admin");
	if (only_admin.checked==true){
		level=1;
	}
	var adminPwd=getAdminPwd()
	var name=document.getElementById("query_name").value;
	if (name.length==0)
	{
		name="default";
	}
	var data={"id":query_id
				,"name":name
				,"query":query_str
				,"args_count":args_count
				,"db_name":db_name
				,"coll":coll
				,"level":level
				,"adminPwd":adminPwd
				}
	$.ajax({
		url:"/mongo/save/",
		data:data,
		method:"POST",
		dataType:"JSON",
		type:"JSON",
		success:function(res){
			if (res.success==true)
			{
				id=res.query.id;
				ed.setAttribute("query_id",id);
				var save=document.getElementById("save");
		    	save.innerText="Save";
		    	changed=false;
		    	get_queries();
			}else{
				alert(res.msg);
			}
		}
	});
}
function test()
{
	var ed=document.getElementById("editor")	
	var query_id=-1
	var arguments=[];
	data=null;
	var query_str=editor.getValue();	
	var args_count=document.getElementById("test_args_count").value;
	for (var i=0;i<args_count;i++)
	{
		arguments.push(document.getElementById("arg"+i).value);
	}
	var coll=document.getElementById("coll").value;
	var db_name=document.getElementById("db_name").value;
	var from=document.getElementById("from").value;
	var to=document.getElementById("to").value;
	var adminPwd=getAdminPwd();
	if (query_id==-1)
	{
		data={			
			"query":query_str
			,"db_name":db_name
			,"coll":coll
			,"args":arguments.join(",")
			,"from":from
			,"to":to
			,"adminPwd":adminPwd
			}			
		if (data!=null){
			$.ajax({
			url:"/mongo/run/",
			data:data,
			method:"POST",
			dataType:"JSON",
			type:"JSON",
			success:function(res){
				$(".run").each(function(key,val){
				val.innerText="Test";
				val.disabled=false;
				})
				if (res.success==true)
				{
					console.log(res.data);
					raw_data=res.raw_data;
					date_wise_data=render(res.data,name);
					var dates=document.getElementById("dates");
					dates.innerHTML="";
					var last=null;
					for (var dt in date_wise_data){
						var op=document.createElement("option");
						op.value=dt;
						op.innerText=dt;
						dates.appendChild(op);
						last=dt;
					}
					add_to_table(last);
					dates.onchange=function(ev){
						var val=dates.value;
						add_to_table(val);
					}

				}else{
					alert(res.msg);
				}
				}
			});
		}
	}
	
}
function run()
{
	var query_id=document.getElementById("queries").value		
	var arguments=[];
	
	var args_count=dict_queries[query_id].args_count
	var name=dict_queries[query_id].name;
	for (var i=0;i<args_count;i++)
	{
		arguments.push(document.getElementById("arg"+i).value);
	}
	data=null;
	var from=document.getElementById("from").value;
	var to=document.getElementById("to").value;
	var level=dict_queries[query_id].level;
	var adminPwd="";
	if (level==1){
		adminPwd=getAdminPwd();
	}
	if(query_id>0)
	{
		data={			
			"id":query_id			
			,"args":arguments.join(",")
			,"from":from
			,"to":to
			,"adminPwd":adminPwd
			};
		console.log(data);
		$(".run").each(function(key,val){
			val.innerText="Wait...";
			val.disabled=true;
		})
		$.ajax({
		url:"/mongo/run/",
		data:data,
		method:"POST",
		dataType:"JSON",
		type:"JSON",
		success:function(res){
			$(".run").each(function(key,val){
				val.innerText="Run";
				val.disabled=false;
			})
			if (res.success==true)
			{
				console.log(res.data);
				raw_data=res.raw_data;
				date_wise_data=render(res.data,name);
				var dates=document.getElementById("dates");
				dates.innerHTML="";
				var last=null;
				for (var dt in date_wise_data){
					var op=document.createElement("option");
					op.value=dt;
					op.innerText=dt;
					dates.appendChild(op);
					last=dt;
				}
				add_to_table(last);
				dates.onchange=function(ev){
					var val=dates.value;
					add_to_table(val);
				}

			}else{
				alert(res.msg);
			}
			}
		});
		
	}		
}
