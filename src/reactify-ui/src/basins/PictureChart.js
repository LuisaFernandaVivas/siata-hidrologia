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

  return (
    <div id='parent'>
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
