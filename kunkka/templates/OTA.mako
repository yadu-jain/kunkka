<%inherit file="base.mako"/>
<%block name="control">
  <script type="text/javascript" src="${request.static_url('kunkka:static/tran.js')}"></script>
	<script type="text/javascript" id="chart_js" src="${request.static_url('kunkka:static/highchart/highcharts.js')}"></script>	
	<script type="text/javascript" id="chart_theme" src="${request.static_url('kunkka:static/highchart/themes/dark-green.js')}"></script>
	<div class="row">
		<div class="col-md-3 input-group input-group-sm">
			<span class="input-group-addon">From:</span>
			<input type="text" class="form-control" id="from">
		</div>
		<div class="col-md-3 input-group input-group-sm">
			<span class="input-group-addon">To:</span>
			<input type="text" class="form-control" id="to">
		</div>
		<div class="col-md-2">
			<div class="btn-group-sm">            
               <button id="go" type="button" class="btn btn-primary" href="#" onclick='go();' tabindex="-1">Go</button>
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
	</div>	
</%block>
<%block name="inner_content">
<script type="text/javascript">
var my_charts=new Object();
function go()
{
	var from=document.getElementById("from");
	var to=document.getElementById("to");	
	var url="/OTA/?from="+from.value+"&to="+to.value
	document.location.href=url;
}
function load_list(target_id)
{
	var target=document.getElementById(target_id);
	$.getJSON( "/rest/"+target_id+"/", 
	function( response ){				
		if (response["success"]==true)
		{
			data=response["data"];
			target.innerHTML="";
			var empty=document.createElement("option");
		    empty.value="-";
		    empty.innerHTML="ALL";
		    target.appendChild(empty);
		    //console.log(data);		    
			$.each( data, function( key, val ) {				
				//console.log(key);
				//console.log(val);
		    	var id=val["id"];
		    	var name=val["name"];
		    	var opt=document.createElement("option");
		    	opt.value=id;
		    	opt.innerHTML=name;
		    	target.appendChild(opt)
		  	});
		  	$( "#"+target_id).change(function() {
  				OTA_chart("OTA");
			});
		}
	});
}
function OTA_chart(target_id){
	//console.log($('#'+target_id+' div'));
	//var from_date=document.getElementById("from").value;
	//var to_date=document.getElementById("to").value;
	var str_date_from=$.datepicker.formatDate("yy-m-d",date_from);
	var str_date_to=$.datepicker.formatDate("yy-m-d",date_to);
	if(str_date_from!=str_date_to)
	{
		document.getElementById("panel_title").innerHTML="Report: " +str_date_from+" To "+str_date_to;
	}else
	{
		document.getElementById("panel_title").innerHTML="Report On: "+str_date_from;
	}
	
	var path="/chart/"+target_id+"/?from="+str_date_from+"&to="+str_date_to
	var agent=document.getElementById("agents").value;
	var provider=document.getElementById("providers").value;
	var tier=document.getElementById("tiers").value;
	var subtitle=""
	if(agent!="-")
	{
		subtitle+=" Agent=<span color=\"blue\">"+$('#agents option:selected').html()+"</span>"
		path+="&agent="+agent;
	}	
	if(provider!="-")
	{
		subtitle+=" Provider=<span color=\"blue\">"+$('#providers option:selected').html()+"</span>"
		path+="&provider="+provider;
	}	
	if(tier!="-")
	{
		subtitle+=" Tier=<span color=\"blue\">"+$('#tiers option:selected').html()+"</span>"
		path+="&tier="+tier;
	}
	var key=agent+":"+provider+":"+tier;
	
	if (my_charts[key])
	{	
		var data=my_charts[key];
		$('#'+target_id+' div').highcharts(data);
		return;
	}else
	{
		////console.log("loading chart..."+str_date_from+"->"+str_date_to+" :"+target_id);	
		$.getJSON( path, 
		function( data ){
			//console.log(subtitle);
			if(subtitle!=""){
				data["subtitle"]["text"]=subtitle;
			}else
			{
				data["subtitle"]["text"]="ALL";
			}				
			$('#'+target_id+' div').highcharts(data);
			my_charts[key]=data
		});
	}
}
$(document).ready(function(){
	//ON Load
	var str_date_from=$.datepicker.formatDate("yy-m-d",date_from)
	var str_date_to=$.datepicker.formatDate("yy-m-d",date_to)

	$('#chart_js').ready(function(){	
		OTA_chart("OTA");				  	
	  ////console.log(e.relatedTarget);// previous tab	
	});
	load_list("agents");
	load_list("tiers");
	load_list("providers");

});		
</script>
</%block>
<%block name="post_content">		
	<div class="row">
	  <div class="col-md-3">	  		  	
		  <div class="panel panel-default">
		  <div class="panel-heading"><small>Filters</small></div>
			<ul class="list-group">
			  <li class="list-group-item list-group-item-sm">
			  	 <div class="input-group input-group-sm">
			  	  	<span class="input-group-addon">			        	
					Agents
			      	</span>
			      	<select id="agents" class="form-control form-control">
				    	<option value="-">ALL</option>				    
				  	</select>
				  <!--
			      <span class="input-group-btn">
			        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown"><span class="glyphicon glyphicon-remove"></span>
	  				</button>
			      </span>
			      -->
			    </div><!-- /input-group -->			  					
			  </li>
			  <li class="list-group-item list-group-item-sm">			  	  
			  	 <div class="input-group input-group-sm">
				  	<span class="input-group-addon">
			        Tiers
			      	</span>
				    <select id="tiers" class="form-control form-control">
					    <option value="-">ALL</option>				    
					</select>
				  <!--
			      <span class="input-group-btn">
			        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown"><span class="glyphicon glyphicon-remove"></span>
	  				</button>
			      </span>
			      -->
			    </div><!-- /input-group -->			  				
			  </li>
			  <li class="list-group-item list-group-item-sm">
			  	<div class="input-group input-group-sm">
				  	<span class="input-group-addon">
					Providers
			      	</span>
			    	<select id="providers" class="form-control form-control">
				    	<option value="-">ALL</option>				    
					</select>
				  <!--
			      <span class="input-group-btn">
			        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown"><span class="glyphicon glyphicon-remove"></span>
	  				</button>
			      </span>
			      -->
			    </div><!-- /input-group -->			  				
			  </li>			 
			</ul>
	  	  </div>
	  </div><!-- /.col-md-6 -->
	  <div class="col-md-9">	  			
	     <div class="panel panel-default">
		  <div id="panel_title" class="panel-heading"></div>
		  <div id="OTA">
		  	<%include file="chart.mak"/>
		  </div>		  
		</div>
	  </div><!-- /.col-md-6 -->
	</div><!-- /.row -->
	
	<div id="test">
	</div>
</%block>
