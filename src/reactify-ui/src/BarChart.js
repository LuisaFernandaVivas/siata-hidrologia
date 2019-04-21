import React, {Component} from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'


class BarChart extends Component {
  componentDidMount() {
    this.drawChart();
  }

  drawChart() {
    const data = [23,21];
    d3.csv("static/data.csv", function(data) {
      
    })
    const svg = d3.select("body").append("svg")
      .attr("width", this.props.width)
      .attr("height", this.props.height);

    svg.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("width", 65)
      .attr("fill", "green")
  }

  render(){
    return <div id={"#" + this.props.id}></div>
  }
}

export default BarChart;
