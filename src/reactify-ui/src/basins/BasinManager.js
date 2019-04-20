import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'
import BasinChart from './BasinChart';
import TimeChart from './TimeChart';
import PictureChart from './PictureChart';

class BasinManager extends Component {
  constructor(props){
    super(props)
    this.toogleItem = this.toogleItem.bind(this)
  }
      state = {
        show : true,
        item : {},
        data : {}
      }

  toogleItem(value,filter){
    this.setState({
      item : value,
      show : false,
      data : filter
      })
  }

  componentDidMount(){
    this.setState({
        show: true,
        item:{},
        data:{}
    })
  }

  render() {
      const {show} = this.state
      const {item} = this.state
      const {data} = this.state
    return (
      <div className="col-sm-12">
          <div className = "row">
            <div id = 'timechart-row' className ='col-sm-5'>
              <TimeChart data = {data} parameter = {'water_level'} color = {"#4C90CD"}/>
              <TimeChart data = {data} parameter = {'radar_rain'} color = {"black"}/>
              <TimeChart data = {data} parameter = {'water_surface_velocity'} color = {"grey"}/>
            </div>
            <div id = 'picturechart-row' className ='col-sm-3'>
              <PictureChart path={item.path}/>
              <PictureChart path={item.path}/>
              <PictureChart path={item.path}/>
            </div>
          </div>
          <div id='basinchart' className='col-sm-12'>
            <BasinChart show = {show} click={this.toogleItem}/>
          </div>
      </div>
    );
  }
}

<div class="row">
  <div class="col-sm-4" style="background-color:lavender;">.col-sm-4</div>
  <div class="col-sm-4" style="background-color:lavenderblush;">.col-sm-4</div>
  <div class="col-sm-4" style="background-color:lavender;">.col-sm-4</div>
</div>



export default BasinManager;
