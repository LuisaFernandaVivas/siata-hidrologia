import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'

import BasinChart from './BasinChart';

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
      console.log(data)
    return (
      <div>
      <h1>{item.name}</h1>
      <BasinChart show = {show} click={this.toogleItem}/>
      </div>
    );
  }
}

export default BasinManager;
