<%inherit file="base.mako"/>
<%block name="control">        
    <div class="row">        
        <div class="col-md-2"></div>
        <div class="col-md-3 input-group input-group-sm">
            <span class="input-group-addon">Start With:</span>
            <select id="start_with" class="form-control form-control">
                <option>A</option>
                <option>B</option>
                <option>C</option>
                <option>D</option>
                <option>E</option>
                <option>F</option>
                <option>G</option>
                <option>H</option>
                <option>I</option>
                <option>J</option>
                <option>K</option>
                <option>L</option>
                <option>M</option>
                <option>N</option>
                <option>O</option>
                <option>P</option>
                <option>Q</option>
                <option>R</option>
                <option>S</option>
                <option>T</option>
                <option>U</option>
                <option>V</option>
                <option>W</option>
                <option>X</option>
                <option>Y</option>
                <option>Z</option>
            </select>
        </div>    
    </div>        
    </div>
</%block>

<%block name="inner_content">

    <div class="row clearfix">
        <div class="col-md-12 column">            
        </div>
    </div>
    <div class="row clearfix">                
        
        <div class="col-md-2 column">
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-12 column" style="padding-left:0px;"id="tables">
            
        </div>               
        <script type="text/javascript">
        
        function report_callback(response)
        {                
            if (response.success==true)
            {
                try{                    
                    generateTables(response.data.tables);
                    generateCharts(response.data.charts) ;
                    init_edit_forms(response.data.edit_forms);                

                }catch(e){

                }                    
            }else{
                show_error(response.msg);
            }
            $("#start_with").attr("disabled",null);                
        }            
        function open_report()
        {                
            var start_with=$("#start_with").val();        
            $("#start_with").attr("disabled","true");        
            $.getJSON("${report_path}"+"START_WITH="+start_with,report_callback);
        }                        
        $(document).ready(function(){     
            open_report();
            $("#start_with").change(open_report);
        });
        </script>
        <div class="col-md-12 column" style="padding-left:0px;"id="charts">            
        </div>            
    </div>
</%block>
<%block name="post_content">
</%block>
