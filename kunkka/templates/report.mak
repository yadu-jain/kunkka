<%inherit file="base.mak"/>
<%block name="inner_content">
	<script src="${request.static_url('kunkka:static/tran.js')}"></script>
	<script id="chart_js" src="${request.static_url('kunkka:static/highchart/highcharts.js')}"></script>	
	<script id="chart_theme" src="${request.static_url('kunkka:static/highchart/themes/dark-green.js')}"></script>
	<div class="row">
		<div class="col-lg-2 input-group">
			<span class="input-group-addon">From:</span>
			<input type="text" class="form-control" id="from">
		</div>
		<div class="col-lg-2 input-group">
			<span class="input-group-addon">To:</span>
			<input type="text" class="form-control" id="to">
		</div>
		<div class="col-lg-2">
			<div class="input-group">            
            <div class="input-group-btn">
              <button id="go" type="button" class="btn btn-default" href="#go" onclick='tran()' tabindex="-1">Go</button>
              <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" tabindex="-1">
                <span class="caret"></span>
                <span class="sr-only">Toggle Dropdown</span>
              </button>
              <ul class="dropdown-menu pull-right" role="menu">
                <li><a href="#Bookings" onclick='tran("Bookings")' >Bookings</a></li>
                <li><a href="#Seats" onclick='tran("Seats")'>Seats</a></li>                
                <li><a href="#Amount" onclick='tran("Amount")'>Amount</a></li>
              </ul>
            </div>
          </div>			
		</div>
		<script>
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
				    console.log("${date_from}");					
				   	$("#from").datepicker( "setDate" ,date_from);
					$("#to").datepicker( "setDate" ,date_to);
				   	
				  });
			});
		</script>
	</div>
	<div style="padding:10px;" class="row">
		%if error_msg <> '':
			<%return  %>
		%endif
	    <ul class="nav nav-tabs" id="myTab">	  
		  <li><a href="#Bookings">Bookings</a></li>
		  <li><a href="#Seats">Seats</a></li>
		  <li><a href="#Amount">Amount</a></li>
		</ul>		 
		<div class="tab-content">	  
		  <div class="tab-pane" id="Bookings">
		  <%include file="chart.mak"/>
		  </div>
		  <div class="tab-pane" id="Seats">
		  <%include file="chart.mak"/>
		  </div>
		  <div class="tab-pane" id="Amount">
		  <%include file="chart.mak"/>
		  </div>
		</div>	 
		<script>
		</script>
		
	</div>
	<div id="test">
	</div>
	<script>	
	var my_charts=new Object();
	function load_chart(target_id)
{
	//load chart using ajax	
	
	console.log($('#'+target_id+' div'));
	//var from_date=document.getElementById("from").value;
	//var to_date=document.getElementById("to").value;
	var str_date_from=$.datepicker.formatDate("yy-m-d",date_from)
	var str_date_to=$.datepicker.formatDate("yy-m-d",date_to)
	if (my_charts[target_id+":"+str_date_from+"->"+str_date_to])
	{	
		return;
	}else
	{
		//console.log("loading chart..."+str_date_from+"->"+str_date_to+" :"+target_id);	
		my_charts[target_id+":"+str_date_from+"->"+str_date_to]=true;	
	}
	$.getJSON( "/chart/OTS/"+target_id+"/?from="+str_date_from+"&to="+str_date_to, 
	function( data ){
		$('#'+target_id+' div').highcharts(data)
	});
      
}	
$('#chart_js').ready(function(){
	$('#myTab a').on('shown.bs.tab', function (e) {
		var target_id=e.target.href.split('#')[1];
		load_chart(target_id);				  	
	  //console.log(e.relatedTarget);// previous tab
	});				
});
$(document).ready(function(){
	//ON Load
	var id = document.location.hash.substring(1);
	console.log(id);

	$('#myTab a[href="#'+id+'"]').tab('show');
	
	

	//On Changes			
	$(window).bind("hashchange",function(event) {
	//if you're using the awesome hashchange plugin
	//$(window).hashchange(function(event) { ...				    
	    var id = document.location.hash.substring(1);
	    console.log(id);
	    $('#myTab a[href="#'+id+'"]').tab('show'); // Select tab by name				    
	});
	
});		
	</script>


</%block>
