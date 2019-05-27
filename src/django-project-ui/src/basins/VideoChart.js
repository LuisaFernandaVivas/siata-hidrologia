import React, { Component } from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'

class VideoChart extends Component {
  render() {
    const {camera_path} = this.props
    const style = {height:150,
                   width:400}
    function if_path_is_empty(path) {
      if (path == null || path == ''){
        return 'd-none'
      }
      else{
        return 'd-block'
      }
    }
    const class_name = if_path_is_empty(camera_path)
    console.log(class_name)
  return (
    <div className = {class_name}>
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
