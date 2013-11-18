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
	var url="/tran/?from="+from.value+"&to="+to.value+"#"+type;
	console.log(url);
	document.location.href=url;
}
