function getHideHandler(chart_div,hide_a){
                return function(){
                    var chart = $(chart_div).highcharts();
                    var val=hide_a.getAttribute("all");
                    if (val=="1"){
                        $(chart.series).each(function(){
                        //this.hide();
                        this.setVisible(false, false);
                        });
                        hide_a.setAttribute("all","0");
                        hide_a.innerHTML="Show All";                        
                    }else
                    {
                        $(chart.series).each(function(){
                        //this.hide();
                        this.setVisible(true, false);
                        });
                        hide_a.setAttribute("all","1");
                        hide_a.innerHTML="Hide All";                        
                    }
                    chart.redraw();    
                    event.preventDefault();
                }    
            }
function generateCharts(charts,add_to)
            {
                if(charts==undefined){
                    return;
                }
                var content;
                var meta_content;
                var title;
                var div;
                var h1;
                var table;
                var rendered_tables;
                var hide_a;
                var obj_chart;
                if (add_to==undefined){
                    
                    add_to="charts";
                    
                }   
                if(allChartObjects==undefined|| allChartObjects==null){
                    allChartObjects=new Array();
                }
                document.getElementById(add_to).innerHTML="";    
                for(var i=0;i<charts.length;i++)
                {                    
                    
                    div=document.createElement("div");
                    $(div).addClass("shodow_box");
                    /*
                    h3=document.createElement("h3");
                    $(h3).addClass("text-center");
                    $(h3).addClass("text-primary");
                    */
                    chart_div=document.createElement("div");                                        
                    hide_a=document.createElement("a");
                    hide_a.innerHTML="Hide All";
                    hide_a.setAttribute("all","1");
                    hide_a.href="#";
                    meta_content=charts[i].meta_content;                    
                    //h3.innerHTML=charts[i].title;                    
                    hide_a.onclick=getHideHandler(chart_div,hide_a);

                    //div.appendChild(h3);
                    div.appendChild(chart_div);
                    div.appendChild(hide_a);
                    document.getElementById(add_to).appendChild(div);
                    obj_chart=$(chart_div).highcharts(charts[i].content);
                    
                    allChartObjects.push(charts[i].content)
                }
            }               