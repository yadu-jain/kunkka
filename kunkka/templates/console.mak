<%inherit file="base.mak"/>
<%block name="inner_content">

	<link  rel="STYLESHEET" type="text/css" href="${request.static_url('kunkka:static/dhtmlx/dhtmlxgrid.css')}">
	<link rel="STYLESHEET" type="text/css" href="${request.static_url('kunkka:static/dhtmlx/dhtmlxgrid_skins.css')}">
    <script  src="${request.static_url('kunkka:static/dhtmlx/dhtmlxcommon.js')}"></script>
    <script src="${request.static_url('kunkka:static/dhtmlx/dhtmlxgrid.js')}"></script>
    <script src="${request.static_url('kunkka:static/dhtmlx/dhtmlxgridcell.js')}"></script>
    <script src="${request.static_url('kunkka:static/dhtmlx/dhtmlxgrid_filter.js')}"></script>
    <script src="${request.static_url('kunkka:static/console.js')}"></script>
    <script async="true" src="${request.static_url('kunkka:static/export.js')}"></script>
    
    <style>
    .box_me
    {    	
    	padding: 5px;
    	border-radius: 10px;
    	margin: 5px;
    }
    #editor_window
    {
    	
    	padding: 5px;
    	margin: 5px;
    	border: solid 1px black; 
    }
    .just_pretty{
    	color:Blue;
    }
    #ui-datepicker-div{
    	z-index:10 !important;
    }
    </style>
	<div class="row">
		<div class="col-lg-2 input-group">
				<span class="input-group-addon">From:</span>
				<input type="text" class="form-control" id="from">
		</div>
		<div class="col-lg-2 input-group">
			<span class="input-group-addon">To:</span>
			<input type="text" class="form-control" id="to">
		</div>
		<script>
		$(document).ready(function(){
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
				get_queries();
			});
		})
		</script>
		<div class="col-lg-5 input-group input-group-sm">
	  	  	<span class="input-group-addon">Reports</span>
	      	<select id="queries" class="form-control form-control">		    	
		  	</select>
		  <!--
	      <span class="input-group-btn">
	        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown"><span class="glyphicon glyphicon-remove"></span>
				</button>
	      </span>
	      -->
	    </div><!-- /input-group -->		
	    <div class="col-lg-2">				
	    	<div class="btn-group">	    		
	    		<button type="button" class="run btn btn-default" onclick="run();">Run</button>
	    		<button type="button" onclick="open_query();" class="btn btn-default">Open</button>
	    	</div>	  	
	    </div>
	    <div class="col-lg-1">
	    	<button type="button" onclick="open_editor();" class="btn btn-default">New</button>
	    </div>
	</div>	
	<style type="text/css" media="screen">
	    #editor { 
	        position: relative;
	        height: 100%;
	        width: 100%;	        
	    }

	</style>
	<div class="row box_me row" id="arguments_window" style="height:50px;">

		<div id="arguments">					

		</div>
		<script>		
		//console.log(val);		
		</script>
	</div>
	<script>
  			
  	</script>
	<hr/>
	<div class="row" id="editor_window" style="height:360px;display:none;">
		<div class="col-lg-1 input-group input-group-sm" style="height:100%;">
			<div class="row">									
				<span class="input-group-addon">Arguemnt Count</span>
	  			</select>  			
			</div>
			<div class="row">									
				<select id="test_args_count" class="form-control form-control">				
	  			</select>  			
			</div>
			<div id="test_arguments">					

			</div>
			<script>
			var args_count_options=document.getElementById("test_args_count");
  			args_count_options.innerHTML="";
  			for(var i=0;i<10;i++)
  			{
  				var op=document.createElement("option");
  				op.value=i;
  				op.innerText=i;
  				args_count_options.appendChild(op);
  			}
  			function create_test_args()
  			{
  				var val=args_count_options.value;
  				//console.log(val);
  				var arguments=document.getElementById("test_arguments");
  				arguments.innerHTML='';
  				for (var i=0;i<val;i++)
  				{
  					var arg_div=document.createElement("div");  					
  					arg_div.classList.add("row");  					 
  					arg_div.classList.add("input-group");
  					arg_div.classList.add("input-group-sm");
  					arg_div.innerHTML='<input id ="test_arg'+i+'" type="text" class="form-control" placeholder="test_arg '+i+'">'
  					arguments.appendChild(arg_div);
  				}

  			}
  			create_test_args();
  			args_count_options.onchange=create_test_args;
			</script>
		</div>
		<div class="col-lg-10" style="height:100%;">
			<div class="row" style="height:40px;">
				<div class="col-lg-4 input-group input-group-sm">
					<span class="input-group-addon">Report</span>
					<input id ="query_name" type="text" class="form-control" placeholder="Default">
					<span class="input-group-addon">
						Only Admin
			        	<input id="only_admin" type="checkbox">
			      	</span>
				</div>
				<div class="col-lg-2 input-group input-group-sm">					
					<span class="input-group-addon">Log DB</span>					
					<select id="db_name" class="form-control form-control">
					<option>logs</option>					
		  			</select>
			    </div>
			    <div class="col-lg-2 input-group input-group-sm">					
					<span class="input-group-addon">Coll.</span>					
					<select id="coll" class="form-control form-control">
					<option>gds</option>					
		  			</select>
			    </div>
				<div class="col-lg-3 btn-group btn-group-sm">							    	
		    		<button type="button" class="run btn btn-default" onclick="test();">Run</button>
		    		<button type="button" class="btn btn-default" onclick="save();" id="save">Save</button>
		    		<button type="button" class="btn btn-default" onclick="save_as();">Save As</button>
			    </div>			    
			    <div class="col-lg-1 btn-group btn-group-sm">							    	
		    		<button type="button" class="btn btn-default" onclick="close_editor();">Close</button>		    		
			    </div>
			</div >
			<div class="row" style="height:300px;">
				<div class="box_me"id="editor">function foo(items) {
				    var x = "All this is syntax highlighted";
				    return x;
				}</div>
			</div>
			<script src="${request.static_url('kunkka:static/ace/src-min-noconflict/ace.js')}" type="text/javascript" charset="utf-8"></script>
			<script>
			    var editor = ace.edit("editor");
			    editor.setTheme("ace/theme/monokai");
			    editor.getSession().setMode("ace/mode/javascript");
			</script>
		</div>
	</div>	
	<div id="report_window" style="display:none;">
		<div class="row" name="toolbar" >
			<div class="btn-toolbar" role="toolbar">
			  <div class="col-lg-3 btn-group btn-group-sm input-group">		
			  	<label class="input-group-addon">Export:</label>
			  	<button onclick="to_csv();" type="button" class="btn btn-default">CSV</button>			  		
			  	<button onclick="to_json();" type="button" class="btn btn-default">JSON</button>	  	
			  	<button onclick="to_raw_json();" type="button" class="btn btn-default">Raw</button>
			  </div>
			  <div class="col-lg-3 btn-group">							  
			  </div>			  	
			  <div class="col-lg-1 btn-group">		  	    
	    
			  </div>
			</div>
		</div>	
		<div class="row">
			<div class="col-lg-3 input-group">
						<span class="input-group-addon">Date</span>
				      	<select id="dates" class="form-control form-control">
					    	<option value="-">2013-12-31</option>			    
					  	</select>
			</div>
		</div>
		<div class="row" name="result">					
				<div class="col-lg-10">			
				    <div style="height:50px" id="result_title"></div>              
					<div id="gridbox" style="height:700px">
						<script type="text/javascript">
							console.log("DHTMLX");
							function set_grid(headers,rows){
									mygrid=new dhtmlXGridObject('gridbox');
									
									mygrid.setImagePath("${request.static_url('kunkka:static/dhtmlx/imgs/')}");//path to images required //by grid
									
									mygrid.setHeader(headers.names.join(", "));
									//mygrid.makeFilter("textobject",1);
									//mygrid.attachHeader(",#text_filter,#select_filter,#numeric_filter");
									//mygrid.setHeader(headers.names.join(","));
									var n=headers.names.length;
									var str_filter="";
									for (var i=0;i<n;i++){
										str_filter+="#text_filter,";
									}
									str_filter=str_filter.slice(0,-1);
									mygrid.attachHeader(str_filter);
									//mygrid.setInitWidths("70,250,*");
									//mygrid.setColAlign("right,left,left");
									//mygrid.setColTypes("dyn,ed,ed");
									//mygrid.setColSorting("int,str,str");

									mygrid.init();//initialize grid
									mygrid.setSkin("light");//set grid skin
									//mygrid.loadXML("../common/grid.xml");//load data
									
									/*test*/									
						            mygrid.parse({"rows":rows},"json");
					        }
							/*test*/
						</script>
					</div>					
				
			</div>					
		</div>	
	</div>
</%block>
