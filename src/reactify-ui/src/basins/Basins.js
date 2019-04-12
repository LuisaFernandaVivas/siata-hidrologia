import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'

import BasinInline from './BasinInline';

class Basins extends Component {
  constructor(props){
    super(props)
    this.toogleBasinListClass = this.toogleBasinListClass.bind(this)
    this.toogleItem = this.toogleItem.bind(this)
  }
      state = {
        basins : [],
        basinListClass : "card",
        currentItem : "puente33"
      }

  loadbasins(){ //http request
      const endpoint = '/api/basin'
      let thisComp = this
      let lookupOptions = {
          method: "GET",
          headers: {
            'Content-Type':'application/json'
          }
      }

      fetch(endpoint,lookupOptions) //fetch = recuperar, returns a promise,
      .then(function(response){
          return response.json()
      }).then(function(responseData){
            thisComp.setState({
                basins: responseData
                })
      }).catch(function(error){
          console.log("error",error)
      })
    }


  toogleBasinListClass(event){
    event.preventDefault()
    let currentListClass = this.state.basinListClass
    if (currentListClass === ""){
      this.setState({
        basinListClass:"card",
      })
    } else {
        this.setState({
          basinListClass : "",
        })
    }
  }

  toogleItem(event){
    event.preventDefault()
    this.setState({
      currentItem : event.target.offsetParent.id
    })
  }

  componentDidMount(){ //{
    this.setState({
        basins: [],
        basinListClass : "card",
        currentItem:"puente33"
    })
    this.loadbasins()
  }

  render() {
      const {basins} = this.state
      const {basinListClass} = this.state
      const {currentItem} = this.state
      const item = basins.find( item => item.slug === currentItem )
      console.log(item)
    return (
      <div>
        <h1> {currentItem} </h1>
        <button onClick = {this.toogleBasinListClass}> Presione </button>
        {basins.length > 0 ? basins.map((basinItem,index)=>{
              return (
                <BasinInline basin={basinItem} elClass={basinListClass} click={this.toogleItem}/>
            )
        }) : <p> No basin Found </p>}
      </div>
    );
  }
}

export default Basins;
