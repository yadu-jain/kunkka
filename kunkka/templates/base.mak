<!DOCTYPE html>
<!-- saved from url=(0049)http://getbootstrap.com/2.3.2/examples/fluid.html -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>Kunkka</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="GDS Report">
    <meta name="author" content="Heera">
    <!--<script src="http://cdn.jquerytools.org/1.2.7/full/jquery.tools.min.js"></script>-->
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <!-- Le styles -->
    <link href="${request.static_url('kunkka:static/bootstrap/css/bootstrap.min.css')}" rel="stylesheet">
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
    </style>   
  <style type="text/css"></style></head>

  <body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">                   
          <span class="navbar-brand">KUNKKA</span>          
        </div>        
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav">
            <li id="nav_dashboard"><a href="/aff/">Dashboard</a></li>
            <li id="nav_OTA"><a href="/OTA/">OTA</a></li>
            <li id="nav_console"><a href="/console/">CONSOLE</a></li>
          </ul>
          <script type="text/javascript">
            var nav_id="nav_"+document.location.href.split("/")[3];            
            document.getElementById(nav_id).classList.add("active");
          </script>
          <div class="nav navbar-nav navbar-right">            
            <ul>
            <li>${request.username}</li>          
            <li><a href="/logout/">Logout</a></li>        
            </ul> 
          </div>
        </div>
      </div>

    </div>
    <div class="container fluid">
      <div class="row">
            <%block name="error">
              % if error<>'':
                <h2 style="color:red;">${error_msg}</h2>
              % endif
              
            </%block>
      </div>
       <div class="row">
          <%block name="inner_content">            
          ---------------
          </%block>     
        <div class="row">   
    </div>
      <footer>
        <p>© Mantis 2013</p>
        <p><small> Under Developement</small></p>
      </footer>

    </div><!--/.fluid-container-->
    
    <script src="${request.static_url('kunkka:static/bootstrap/js/bootstrap.min.js')}"></script>

</body></html>