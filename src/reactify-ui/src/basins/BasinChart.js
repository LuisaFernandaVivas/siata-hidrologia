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
          width = 1700 - margin.left - margin.right,
          height = 2200 - margin.top - margin.bottom;

        var svg = d3.select("#heatmap")
        .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        d3.csv("static/data.csv", function(d) {
          return {
            name:d.name,
            date:d.date,
            hour:d.hour,
            color:d.color,
            location:d.location,
            path:d.path,
            water_surface_velocity:d.water_surface_velocity,
            water_level:d.water_level,
            radar_rain:d.radar_rain,
            longitude:d.longitude,
            latitude:d.latitude,
            water_level_history_path:d.water_level_history_path,
            radar_rain_history_path:d.radar_rain_history_path,
            statistical_model_path:d.statistical_model_path,
            picture_path:d.picture_path,
            camera_path:d.camera_path,
          };
        }).then (function (data) {
          var myGroups = d3.map(data, function(d){return d.hour;}).keys()
          var myVars = d3.map(data, function(d){return d.name;}).keys()
          var myColors = d3.map(data, function(d){return d.color;}).keys()
          var x = d3.scaleBand()
            .range([ 0, width ])
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
            .range([ height, 0 ])
            .domain(myVars)
            .padding(0.05);

          svg.append("g")
            .style("font-size", 15)
            .style("font-weight","bold")
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
            .data(data, function(d) {return d.hour+':'+d.name;})
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
                            .style("opacity", 0.90);
                        var string = "<img src= " + d.path +  " width= '400' height='500' />";
                        div .html(string) //this will add the image on mouseover
                            .style("left", (d3.event.pageX + 0) + "px")
                            .style("top", (d3.event.pageY - 900) + "px")
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
            <div className="chart-stage">
              <div id = "heatmap">
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default BasinChart;
