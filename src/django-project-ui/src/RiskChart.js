import React, {Component} from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'

class RiskChart extends Component {
  componentDidMount() {
    this.drawChart();
  }

  drawChart(){
    var margin = {top: 50, right: 30, bottom: 0, left: 380},
      width = 1400 - margin.left - margin.right,
      height = 2200 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#heatmap")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Read the dataf
//    d3.csv("static/data.csv", function(data) {
    d3.csv("static/data.csv", function(d) {

      return {
        name:d.name,
        hour:d.hour,
        color:d.color,
        location:d.location,
        path:d.path
      };
    }).then (function (data) {
      var myGroups = d3.map(data, function(d){return d.hour;}).keys()
      var myVars = d3.map(data, function(d){return d.name;}).keys()
      var myColors = d3.map(data, function(d){return d.color;}).keys()
      // Build X scales and axis:
      var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(myGroups)
        .padding(0.05)
        ;

      svg.append("g")
        .style("font-size", 20)
        .style("font-weight","bold")
        .attr("transform", "translate(0,-30)")
        .call(d3.axisBottom(x))
        .call(g => g.select(".domain").remove())
        .attr("class","axisRed")
        .selectAll("text")
          .style("text-anchor", "middle")
          .style("background","black")
          .attr("transform", "rotate(-45)");
        // text label for the x axis


      // Build Y scales and axis:
      var y = d3.scaleBand()
        .range([ height, 0 ])
        .domain(myVars)
        .padding(0.05);
      svg.append("g")
        .style("font-size", 20)
        .style("font-weight","bold")
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove()

      // Build color scale
      // create a tooltip
      var tooltip = d3.select("#my_dataviz")
        .append("div")
        .style("opacity", 20)
        .attr("class", "tooltip")

      // Three function that change the tooltip when user hover / move / leave a cell
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


      // add the squares
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
        .on("mouseover", function(d) {  // the mouseover event
                    div.transition()
                        .duration(200)
                        .style("opacity", 0.90);
                    var string = "<img src= " + d.path +  " width= '400' height='500' />";
                    div .html(string) //this will add the image on mouseover
                        .style("left", (d3.event.pageX + 0) + "px")
                        .style("top", (d3.event.pageY + 0) + "px")
                        .style("font-color", "white");
                  })
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)
        .on("click", function(d) { window.open(d.path);})
    });

  }
  render(){
    return <div id="heatmap"></div>
  }
}
export default RiskChart;
