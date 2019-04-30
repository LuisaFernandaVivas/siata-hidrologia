import React, { Component } from 'react';
import * as d3 from "d3";
import 'whatwg-fetch'
import cookie from 'react-cookies'

class PictureChart extends Component {
  render() {
  const {path} = this.props
  const {title} = this.props
  const style = {height:150,
                 width:250};
  function emptyField(path) {
    if (path == null || path == ''){
      return 'd-none'
    }
    else{
      return 'd-block'
    }
  }
  console.log(path)
  const class_name = emptyField(path)
  return (
    <div id='parent' className={class_name}>
      <div className="chart-wrapper">
        <div className="chart-title">
          {title}
        </div>
        <div className="chart-stage">
          <div>
            <img src ={path} style={style} />
          </div>
        </div>
      </div>
    </div>
    );
  }
}


export default PictureChart;
