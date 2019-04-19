import React, { Component } from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'

class TimeChart extends Component {
  render() {
    const {data} = this.props
    const {parameter} = this.props
    // Define margins, dimensions, and some line colors
    const margin = {top: 40, right: 120, bottom: 30, left: 40};
    const width = 1400 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    function isEmpty(obj) {
        for(var key in obj) {
            if(obj.hasOwnProperty(key))
                return false;
        }
        return true;
    }

    if (isEmpty(data)){
      console.log("is empty")
    } else {
    data.forEach(function(d){
        //console.log(typeof(d.date)); //check the type before it changes
        var orgDate = new Date(d.date); // changes the string date into origional date type
        d.date = orgDate;
    }); //

    var minDate = data[0]["date"]
    var maxDate = data[30]["date"]
    var maxValue = Math.max.apply(Math, data.map(function(o) { return o[parameter]; }))
    var xScale = d3.scaleTime().domain([new Date(minDate),new Date(maxDate)]).range([0,width]);
    var yScale = d3.scaleLinear().domain([0,maxValue]).range([height,0]);
    var lineGenerator = d3.line()
    	.x(function(d, i) {
          return xScale(d.date);
        })
    	.y(function(d) {
          return yScale(d[parameter]);
        })
      .defined(function(d) {
          return (typeof d[parameter] != 'undefined' && d[parameter]);
        });

    var line = lineGenerator(data);
    var x_axis = d3.axisBottom().scale(xScale);
    var y_axis = d3.axisLeft().scale(yScale);
    d3.select("#timechart").selectAll("*").remove();
    var svg = d3.select("#timechart")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    svg.append("path")
      .attr("d",line)
      .style("stroke", "red")
      .style("fill","none");

    var axG = svg.append("g")
         .attr("class", "x axis")
         .attr("transform", "translate(0," + height + ")")
         .call(x_axis);

    svg.append("g")
      .attr("class", "y axis")
     	.attr("transform", "translate(15,0)")
      .call(y_axis);
    }

    return (
        <div id="timechart" ></div>
    );
  }
}

export default TimeChart;
