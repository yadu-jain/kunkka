function tran(type)
{
	var from=document.getElementById("from");
	var to=document.getElementById("to");
	if(!type)
	{
		type=document.location.hash.substring(1);
		console.log(type);
		if(!type)
		{
			type="Bookings";
		}
	}	
	var url="/aff/?from="+from.value+"&to="+to.value+"#"+type;
	console.log(url);
	document.location.href=url;
}

function load_chart(target_id)
{
	//load chart using ajax	
	//target_id is type
	console.log($('#'+target_id+' div'));
	//var from_date=document.getElementById("from").value;
	//var to_date=document.getElementById("to").value;
	var str_date_from=$.datepicker.formatDate("yy-m-d",date_from)
	var str_date_to=$.datepicker.formatDate("yy-m-d",date_to)
	console.log(str_date_from);
	if (my_charts[target_id+":"+str_date_from+"->"+str_date_to])
	{	
		return;
	}else
	{
		//console.log("loading chart..."+str_date_from+"->"+str_date_to+" :"+target_id);	
		my_charts[target_id+":"+str_date_from+"->"+str_date_to]=true;	
	}
	$.getJSON( "/chart/"+target_id+"/?from="+str_date_from+"&to="+str_date_to, 
	function( data ){
			console.log(data)
		$('#'+target_id+' div').highcharts(data)
	});
      
}	
