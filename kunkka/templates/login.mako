<!DOCTYPE html>
<!-- saved from url=(0040)http://getbootstrap.com/examples/signin/ -->
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">    

    <title>Login ${project_name}</title>

    <!-- Bootstrap core CSS -->
    <link href="${request.static_url('kunkka:static/bootstrap/css/bootstrap.css')}" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="${request.static_url('kunkka:static/bootstrap/css/login.css')}" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../docs-assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="container">
      <form class="form-signin" style="text-align:center;" method="POST" action="/old_login/">
        <img src="${request.static_url('kunkka:static/x_mark.png')}"/>
        <h2 class="form-signin-heading">${project_name}</h2>
        <!--
        <input name="username" type="text" class="form-control" placeholder="Login Id" required="" autofocus="">
        <input name="password" type="password" class="form-control" placeholder="Password" required="">
        <label class="checkbox">        
        </label>
        <button class="btn btn-sm btn-primary btn-block" type="submit">Login</button>
        -->
        <br/>
        <a class="btn btn-sm btn-primary btn-block" style="font-weight:bold;font-size:14px;" href="${oauth_url}">Login With TY</a>        
        <br/>
        <span style="color:red;">${msg}</span>
      </form>
    </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
  

</body></html>