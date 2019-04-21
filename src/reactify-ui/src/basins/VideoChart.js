import React, { Component } from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'

class VideoChart extends Component {
  render() {
    const {camera_path} = this.props
    const style = {height:150,
                   width:400}
  return (
    <div>
      <div className="chart-wrapper">
        <div className="chart-title">
          Cámara
        </div>
        <div className="chart-stage">
          <img src ={camera_path} style={style} />
        </div>
      </div>
    </div>
    );
  }
}



export default VideoChart;
