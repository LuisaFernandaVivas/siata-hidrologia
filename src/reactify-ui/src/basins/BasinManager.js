import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'
import BasinChart from './BasinChart';
import TimeChart from './TimeChart';
import PictureChart from './PictureChart';
import MapChart from './MapChart';
import VideoChart from './VideoChart';

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

  toogleItem(value,filter){ //http request
    const endpoint = 'api/basin/'+value.slug
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
      const gif = "http://siata.gov.co/operacional/radar/PPI/Radar_10_120/Prod_ZOOM_Radar_10_120_DBZH.gif"
      function isEmpty(obj,class_name) {
          for(var key in obj) {
              if(obj.hasOwnProperty(key))
                  return class_name;
          }
          return 'd-none';
      }
      function getName(obj) {
          for(var key in obj) {
              if(obj.hasOwnProperty(key))
                  return obj.nombre;
          }
          return 'd-none';
      }
    return (
      <div className="col-sm-12">
          <div id='title' className={isEmpty(item,'col-sm-12')}>
            <h2>{getName(item)}</h2>
          </div>
          <div className = "row">
            <div id = 'timechart-row' className ={isEmpty(item,'col-sm-5')}>
              <TimeChart data = {data} parameter = {'water_level'} color = {"#39a4a4"}/>
              <TimeChart data = {data} parameter = {'radar_rain'} color = {"#69bbbc"}/>
              <TimeChart data = {data} parameter = {'water_surface_velocity'} color = {"#4c7f80"}/>
              <VideoChart camera_path = {item.camera_path}/>
            </div>
            <div id = 'picturechart-row' className ={isEmpty(item,'col-sm-3')}>
              <PictureChart path = {gif} title={'Radar últimas 3 horas'}/>
              <PictureChart path={item.water_level_history_path} title={"Histórico de hidrógrafas"}/>
              <PictureChart path={item.radar_rain_history_path} title={"Histórico de eventos de lluvia"}/>
              <PictureChart path={item.statistical_model_path} title={"Modelo estadístico"}/>
            </div>
            <div id = 'container' className ={isEmpty(item,'col-sm-4')}>
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
