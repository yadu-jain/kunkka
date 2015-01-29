<%block name="inner_content">
<%inherit file="base.mako"/>    
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">            
            $(document).ready(function(){               
                callback=function(response)
                {
                    if (response.success==true)
                    {
                        console.log( response.data.meta_content);
                        generateTables(response.data.tables)
                        generateCharts(response.data.charts)                     
                    }else{
                        show_error(response.msg);
                    }
                }                
                $.getJSON("${report_path}",callback)
                
                });
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>    
<%block name="post_content">
    
</%block>    