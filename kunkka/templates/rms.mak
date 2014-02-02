<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Bootstrap 3, from LayoutIt!</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">

	<!--link rel="stylesheet/less" href="less/bootstrap.less" type="text/css" /-->
	<!--link rel="stylesheet/less" href="less/responsive.less" type="text/css" /-->
	<!--script src="js/less-1.3.3.min.js"></script-->
	<!--append ‘#!watch’ to the browser URL, then refresh the page. -->
	
	<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <!-- Le styles -->
    <link href="${request.static_url('kunkka:static/bootstrap/css/bootstrap.min.css')}" rel="stylesheet">
  <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
  <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
  <![endif]-->

  <!-- Fav and touch icons -->
  <link rel="apple-touch-icon-precomposed" sizes="144x144" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-144-precomposed.png')}" >
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-114-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" sizes="72x72" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-72-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-57-precomposed.png')}">
  <link rel="shortcut icon" href="${request.static_url('kunkka:static/bootstrap/img/favicon.png')}">
  	
	<script type="text/javascript" src="${request.static_url('kunkka:static/bootstrap/js/bootstrap.min.js')}"></script>
	<script type="text/javascript" src="${request.static_url('kunkka:static/bootstrap/js/scripts.js')}"></script>
</head>

<body>

<body>
<div class="container">
    <div class="row clearfix">
        <div class="col-md-12 column">
            <h3 class="text-center text-primary">
                GDS RMS
            </h3>
        </div>
    </div>
    <div class="row clearfix">        
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
              <button id="go" type="button" class="btn btn-default" href="#" onclick='go();' tabindex="-1">Go</span></button>
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
        <div class="col-md-2 column">
        </div>
    </div>
</div>
</body>
</html>
