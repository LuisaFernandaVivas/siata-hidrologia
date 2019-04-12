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
        item : {}
      }

  toogleItem(event){
    event.preventDefault()
    this.setState({
      item : event.target
    })
  }

  componentDidMount(){ //{
    this.setState({
        show: true,
        item:{}
    })
  }

  render() {
      const {show} = this.state
      const {item} = this.state
      console.log(item)
    return (
      <div>
        <BasinChart click={this.toogleItem}/>
      </div>
    );
  }
}

export default BasinManager;
