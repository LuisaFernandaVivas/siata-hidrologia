import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'
import BasinChart from './BasinChart';
import TimeChart from './TimeChart';

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
      <div>
      <TimeChart data = {data} parameter = {'water_level'} color = {"#4C90CD"}/>
      <TimeChart data = {data} parameter = {'radar_rain'} color = {"green"}/>
      <BasinChart show = {show} click={this.toogleItem}/>
      </div>
    );
  }
}

export default BasinManager;
