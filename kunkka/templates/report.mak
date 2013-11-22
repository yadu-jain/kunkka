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
				    //console.log("${date_from}");					
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
	
$('#chart_js').ready(function(){
	//console.log("loading first time")
	$('#myTab a').on('shown.bs.tab', function (e) {
		var target_id=e.target.href.split('#')[1];
		//console.log("loading first time")
		load_chart(target_id);				  	
	  ////console.log(e.relatedTarget);// previous tab
	});				
});
$(document).ready(function(){
	//ON Load
	var id = document.location.hash.substring(1);
	////console.log(id);
	if(id==""){
		id="Bookings";
	}

	$('#myTab a[href="#'+id+'"]').tab('show');
		

	//On Changes			
	$(window).bind("hashchange",function(event) {
	//if you're using the awesome hashchange plugin
	//$(window).hashchange(function(event) { ...				    
	    var id = document.location.hash.substring(1);
	    //console.log(id);
	    $('#myTab a[href="#'+id+'"]').tab('show'); // Select tab by name				    
	});
	
});		
	</script>


</%block>
