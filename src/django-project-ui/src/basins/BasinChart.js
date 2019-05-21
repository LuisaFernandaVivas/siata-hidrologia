import React, { Component } from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'

class BasinChart extends Component {
  render() {
      const {show} = this.props
      const {click} = this.props

      if (show == true) {
        var margin = {top: 50, right: 60, bottom: 0, left: 300},
          width = 1100 - margin.left - margin.right,
          height = 2200 - margin.top - margin.bottom;

        function responsiveChart(svg){
          var chartWidth = width + margin.left + margin.right;
          var chartHeight = height + margin.top + margin.bottom;
          var aspect = chartWidth / chartHeight;

          svg.attr("viewBox","0 0" + chartWidth + " " +chartHeight)
            .attr("perserveAspectRatio","xMinMid")
            .call(resize);

          d3.select(window).on("resize",resize);

          function resize(){
            var parent = d3.select("div#risk_container.chart-stage")._groups[0];
            if (parent[0]==null){
              console.log('is null')
              var parentWidth = chartWidth;
            }
            else{
              var parentWidth = parent[0].clientWidth;
            }

            console.log(parentWidth)

            if (parentWidth < 1000){
              svg.attr("width",1100 + margin.left + margin.right);
              svg.attr("height",height + margin.top + margin.bottom)

            }

            else {
              svg.attr("width",1800 + margin.left + margin.right);
              svg.attr("height",height + margin.top + margin.bottom)

            }

          }
        }

        var svg = d3.select("#heatmap")
        .append("svg")
          .call(responsiveChart)
        .append("g")
          .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        var parent = (d3.select("div#risk_container.chart-stage")._groups[0])
        if (parent[0]==null){
          parWidth = 1100;
        }
        else{
          var parWidth = parent[0].clientWidth;
        }

        d3.csv("static/data.csv", function(d) {
          return {
            slug:d.slug,
            path:d.three_hours_image_path,
            water_surface_velocity:d.water_surface_velocity,
            water_level:d.water_level,
            radar_rain:d.radar_rain,
            color:d.water_level_color,
            hour:d.hour,
            date:d.date,
            name:d.nombre
          };
        }).then (function (data) {

          if (parWidth > 1000){
            var ancho = width
          }
          else{
            var ancho = 0.75*width
          }

          if (parWidth > 1000) {
            console.log("mayor que mil");
            var ancho = width
            var yticks = -50;
            var x_heat = -50;
            var y_heat = 0.8*height;
            var tooltipLeft = -300;
            var tooltipTop = 1100;
            var currentdata = data;
            var rangex = ancho;
          } else if (parWidth < 1000 && parWidth > 500) {
            console.log("menor que mil y mayor que 500");
            var ancho = 0.7*width
            var yticks = -50;
            var x_heat = -50;
            var y_heat = 0.8*height;
            var tooltipLeft = 0;
            var tooltipTop = 500;
            var currentdata = data;
            var rangex = ancho;

          } else if (parWidth < 500 && parWidth > 350) {
            var ancho = 0.3*width;
            var yticks = -50;
            var x_heat = -50;
            var y_heat = 0.7*height;
            var tooltipLeft = 0;
            var tooltipTop = 500;
            var rangex = 0.4*ancho;
            var datelimit = data[data.length-6].date
            var currentdata = data.filter(function(d){return d.date > datelimit;})
          } else {
            console.log("menor");
            var ancho = 0.001*width;
            var yticks = -90;
            var x_heat = -90;
            var y_heat = 0.7*height;
            var tooltipLeft = -100;
            var tooltipTop = -500;
            var rangex = x_heat+50;

            var datelimit = data[data.length-1].date
            var currentdata = data.filter(function(d){return d.date == datelimit;})

          }
          console.log(data)
          var myGroups = d3.map(currentdata, function(d){return d.hour;}).keys()
          var myVars = d3.map(currentdata, function(d){return d.name;}).keys()
          var myColors = d3.map(currentdata, function(d){return d.color;}).keys()


          var x = d3.scaleBand()
            .range([ x_heat, rangex]) //grafica
            .domain(myGroups)
            .padding(0.05)
            ;

          svg.append("g")
            .style("font-size", 15)
            .style("font-weight","bold")
            .attr("transform", "translate(0,-30)")
            .call(d3.axisBottom(x))
            .call(g => g.select(".domain").remove())
            .attr("class","axisRed")
            .selectAll("text")
              .style("text-anchor", "middle")
              .style("background","black")
              .attr("transform", "rotate(-45)");

          var y = d3.scaleBand()
            .range([ y_heat, 0 ])
            .domain(myVars)
            .padding(0.05);

          svg.append("g")
            .style("font-size", 15)
            .style("font-weight","bold")
            .attr("transform", "translate("+yticks+",0)")
            .call(d3.axisLeft(y).tickSize(0))
            .select(".domain").remove()

          var tooltip = d3.select("#heatmap")
            .append("div")
            .style("opacity", 20)
            .attr("class", "tooltip")

          var mouseover = function(d) {
            tooltip
              .style("opacity", 1)
            d3.select(this)
              .style("stroke", "black")
              .style("opacity", 0.5)
          }
          var mousemove = function(d) {
            tooltip
              .text(""+d.name + "- "+d.location)
              .style("left", (d3.event.pageX - 10) + "px")
              .style("top", (d3.event.pageY + 10) + "px");
          }

          var mouseleave = function(d) {
            tooltip
              .style("opacity", 0)
            d3.select(this)
              .style("stroke", "none")
              .style("opacity", 0.8)
          }

          var div = d3.select("#heatmap").append("div")   // declare the properties for the div used for the tooltips
                    .attr("class", "tooltip")               // apply the 'tooltip' class
                    .style("opacity", 0);                   // set the opacity to nil

          svg.selectAll()
            .data(currentdata, function(d) {return d.hour+':'+d.name;})
            .enter()
            .append("rect")
              .attr("x", function(d) { return x(d.hour) })
              .attr("y", function(d) { return y(d.name) })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("width", x.bandwidth() )
              .attr("height", y.bandwidth() )
              .style("fill", function(d) { return d.color} )
              .style("stroke-width", 4)
              .style("stroke", "none")
              .style("opacity", 0.8)
            .on("mouseover", function(d) {
                        div.transition()
                            .duration(200)
                            .style("opacity", 0.98);
                        var string = "<img src= " + d.path +  " width= '400' height='500' />";
                        div .html(string) //this will add the image on mouseover
                            .style("left", (d3.event.pageX + tooltipLeft) + "px")
                            .style("top", (d3.event.pageY - tooltipTop) + "px")
                            .style("font-color", "white");
                      })
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
            .on("click", function(d) { return click(d,data.filter(function(f){return f.name == d.name;}));})
      })
    }

    return (
        <div id='parent'>
          <div className="chart-wrapper">
            <div className="chart-title">
              Niveles de riesgo
            </div>
            <div id ="risk_container" className="chart-stage">
              <div id = "heatmap">
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default BasinChart;
