<%inherit file="base.mak"/>
<%block name="inner_content">
	<script src="${request.static_url('kunkka:static/tran.js')}"></script>
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
			$(document).ready(function(){
				var d=new Date();
				$(function() {
				    $( "#from" ).datepicker({				    	
				    	dateFormat: 'yy-mm-dd'				    	
				    });

				    $("#to" ).datepicker({				    	
				    	dateFormat: 'yy-mm-dd'				    	
				    });
				    console.log("${date_from}");
					%if date_from==None:
				   		$("#from").datepicker( "setDate" , d);
				   	%else:
				   		$("#from").datepicker( "setDate" , new Date('${date_from}'));
				   	%endif

				   	%if date_to==None:
				   		$("#to").datepicker( "setDate" , d );
				   	%else:
				   		$("#to").datepicker( "setDate" ,new Date('${date_to}') );
				   	%endif				    
				   	
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
		  <div class="tab-pane" id="Bookings">...</div>
		  <div class="tab-pane" id="Seats">...</div>
		  <div class="tab-pane" id="Amount">...</div>
		</div>	 
		<script>
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
		
	</div>
	<div id="test">
	</div>
	<script>	
	
	</script>


</%block>
