import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'
import BasinChart from './BasinChart';
import TimeChart from './TimeChart';
import PictureChart from './PictureChart';
import MapChart from './MapChart';
import VideoChart from './VideoChart';
import WaterLevelChart from './WaterLevelChart';
import RadarRainChart from './RadarRainChart';
import WaterSurfaceVelocityChart from './WaterSurfaceVelocityChart';

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
ClassName
  toogleItem(value,filter){ //http request
    const endpoint = 'hidrologia/api/basin/'+value.slug
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
              item: responseData,
              data: filter,
              show:false,
              })
          window.scroll({top: 600, left: 0, behavior: 'smooth' })
    }).catch(function(error){
        console.log("error",error)
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
      function isEmpty(obj) {
          for(var key in obj) {
              if(obj.hasOwnProperty(key))
                  return obj.nombre;
          }
          return '';
      }
    return (
      <div className = "full-width-div">
        <div className = "container">
          <div className = "col-sm-12">
            <div id = "banner">
              <img src="/static/banner.jpg" className="img-fluid" alt=".."/>
            </div>
            <div className="col-sm-6">
              <br/>
              <br/>
              <div className="station-title">
                {isEmpty(item)}
              </div>
            </div>
            <div className = "row">
              <div id = 'timechart-row' className ='col-sm-5'>
                <WaterLevelChart data = {data} parameter = {'water_level'} color = {"#4C90CD"} />
                <RadarRainChart data = {data} parameter = {'radar_rain'} color = {"#008b8b"}/>
                <VideoChart camera_path = {item.camera_path}/>
              </div>
              <div id = 'picturechart-row' className ='col-sm-3'>
                <PictureChart path={item.water_level_history_path} title={"Histórico de hidrógrafas"}/>
                <PictureChart path={item.radar_rain_history_path} title={"Histórico de eventos de lluvia"}/>
                <PictureChart path={item.statistical_model_path} title={"Modelo estadístico"}/>
              </div>
              <div id = 'container' className ='col-sm-4'>
                <div className="chart-wrapper">
                  <div className="chart-title">
                    Mapa
                  </div>
                  <div className="chart-stage">
                    <div>
                      <MapChart item = {item}/>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div id='basinchart'>
              <BasinChart show = {show} click={this.toogleItem}/>
            </div>
        </div>
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
