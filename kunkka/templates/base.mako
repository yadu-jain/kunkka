<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>${name}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">
  <!--<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />-->
  <link rel="stylesheet" href="${request.static_url('kunkka:static/jquery/jquery-ui.css')}" />
  
  <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
  <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <!-- Le styles -->
    <link href="${request.static_url('kunkka:static/bootstrap/css/bootstrap.min.css')}" rel="stylesheet">    
	<!--link rel="stylesheet/less" href="less/bootstrap.less" type="text/css" /-->
	<!--link rel="stylesheet/less" href="less/responsive.less" type="text/css" /-->
	<!--script src="js/less-1.3.3.min.js"></script-->
	<!--append ‘#!watch’ to the browser URL, then refresh the page. -->
	

  <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
  <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
  <![endif]-->

  <!-- Fav and touch icons -->
  
  <link rel="apple-touch-icon-precomposed" sizes="144x144" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-144-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-114-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" sizes="72x72" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-72-precomposed.png')}">
  <link rel="apple-touch-icon-precomposed" href="${request.static_url('kunkka:static/bootstrap/img/apple-touch-icon-57-precomposed.png')}">
  <link rel="shortcut icon" href="${request.static_url('kunkka:static/img/favicon.png')}">  
  <script src="${request.static_url('kunkka:static/dataTable/js/jquery.dataTables.min.js')}"></script>    
  <link href="${request.static_url('kunkka:static/dataTable/css/jquery.dataTables.css')}" rel="stylesheet">  
  <script src="${request.static_url('kunkka:static/dataTable/DT_bootstrap.js')}"></script>    
  <link href="${request.static_url('kunkka:static/dataTable/DT_bootstrap.css')}" rel="stylesheet">      
  
  <script src="http://code.highcharts.com/highcharts.js"></script>
  <script src="http://code.highcharts.com/modules/exporting.js"></script>

  <script src="${request.static_url('kunkka:static/table.js')}"></script>
  <script src="${request.static_url('kunkka:static/chart.js')}"></script>
  <script type="text/javascript">
    var allChartObjects;
    var allTableObjects;
  </script>
  
  
  
    <meta charset=utf-8 />  	
  <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .sidebar-nav {
        padding: 9px 0;
      }

      @media (max-width: 980px) {
        /* Enable use of floated navbar text */
        .navbar-text.pull-right {
          float: none;
          padding-left: 5px;
          padding-right: 5px;
        }
      }
    .scrollable-div-outer {
        overflow:hidden;
        width:200px; 
        height:400px;
        border:1px solid #ccc;
    } 
    .scrollable-div-inner {
        overflow:auto;         
        height:400px;
    }   
    #menu {                
        width: 175px;
    } 
    .panel-default 
    {
      border-color:#428bca;
    }
    .nav-pills li a
    {
      border-radius: 0px;
    }
    /*TODO*/
    .table_row
    {
      font-size: small;

    }
    /*DataTable*/
    /*
    div.dataTables_length label {
    width: 460px;
    float: left;
    text-align: left;
    }
     
    div.dataTables_length select {
        width: 75px;
    }
     
    div.dataTables_filter label {
        float: right;
        width: 460px;
    }
     
    div.dataTables_info {
        padding-top: 8px;
    }
     
    div.dataTables_paginate {
        float: right;
        margin: 0;
    }
     
    table {
        margin: 1em 0;
        clear: both;
    }
    */
    .shodow_box
    {      
      /*border-bottom: solid 1px;*/
      border-bottom: solid 1px;      
      padding-left:15px;
      border-color:#bce8f1;
      overflow:auto;
    }
    .ui-state-focus
    {       
      
    }
    .list_link{
      margin-top:0px !important;
      border-top: 1px solid #bce8f1;
    }
    .row_selected td
    {
      background-color: #3071a9 !important;
      color:white !important;
    }
    .activated{
      color:green;
    }
    .deactivated{
      color:red;
    }
    
    </style>   
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">                   
          <span class="navbar-brand">KUNKKA</span>          
        </div>        
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <div class="row">
                <div class="col-md-1 column">            
                </div>
                <div class="col-md-7 column">
                    <%block name="msg">
                        <div id="msg" style="padding:12px;">
                      % if request.default_data["msg_type"] <> '':
                        <span class="label label-${request.default_data.msg_type}">${request.default_data.msg_type}</span>
                      % endif              
                        </div>
                    </%block>
                </div>
                <div class="col-md-2 column">
                  <ul>
                  <li><span class="label label-info">${request.user.name}</span></li>                           
                  </ul> 
                </div>
                <div class="col-md-1 column">
                  <ul>
                   % if request.user.mantis_user_id:
                    <li><span class="label label-info">Mantis Id: ${request.user.mantis_user_id}</span></li>
                   % endif
                   <li><a style="font-size:12px;" href="/logout/">Logout</a></li>        
                </ul>
                </div>                
                </div>
            </div>
        <!--
          <ul class="nav navbar-nav nav-pills">
            <li id="nav_dashboard"><a href="/aff/">Dashboard</a></li>
            <li id="nav_OTA"><a href="/OTA/">OTA</a></li>
            <li id="nav_console"><a href="/console/">CONSOLE</a></li>
          </ul>
          <script type="text/javascript">
            var nav_id="nav_"+document.location.href.split("/")[3];            
            document.getElementById(nav_id).classList.add("active");
          </script>
          -->
          
          

        </div>
      </div>

    </div>
<div class="container fluid">	
	<div class="row">
		<div class="col-md-2 column ">
            <div id="menu" class="affix">
                <div class="panel panel-default">
                  <div class="panel-heading">                    
                    <span>Resource List</span>
                  </div>
                  <div class="panel-body">                     
                     <div  class="row scrollable-div-inner">

                      <ul class="nav nav-pills nav-stacked">
                        <%block name="allowed_links">
                        % for obj in request.allowed_links:
                          % if obj.category:
                            % if obj.enabled==True:
                              <li class="list_link"><a href="${obj.path}">${obj.name}</a></li>
                            % else:
                              <li class="list_link disabled"><a href="#">${obj.name}</a></li>
                            % endif
                          %endif
                        % endfor                                    
                        </%block>
                      </ul>
                    </div>
                  </div>
                  <div class="panel-footer">
                    
                  </div>
                </div>                
                <script type="text/javascript">                
                    var strActive=document.location.pathname;
                    $("[href]").parent().removeClass("active");
                    $("[href='"+strActive+"']").parent().addClass("active");
                </script>
            </div>
		</div>
		<div class="col-md-10 column">
			<div class="panel panel-info">
				<div class="panel-heading">
					<h3 class="panel-title">            
						${name}
					</h3>
				</div>
				<div class="panel-body">
					<%block name="control">                                  
          </%block>
          <br/>
          <%block name="inner_content">            
                  Please wait loading...
          </%block>
          % if len(request.params)>0:
            <%block name="post_content">                                       
            </%block>
          % endif          
        </div>
				<div class="panel-footer">
					
				</div>
			</div>            
		</div>
	</div>
	<script src="${request.static_url('kunkka:static/bootstrap/js/bootstrap.min.js')}"></script>
</div>
</body>
</html>
