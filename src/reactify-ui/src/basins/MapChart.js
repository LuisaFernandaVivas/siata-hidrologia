import React from 'react'
import { Map as LeafletMap, TileLayer, Marker, Popup } from 'react-leaflet';

class MapChart extends React.Component {
  render() {
    const {item} = this.props
    function ifisEmpty(obj) {
        for(var key in obj) {
            if(obj.hasOwnProperty(key))
                return [obj.latitud,obj.longitud];
        }
        return [6.264,-75.603];
    }
    const center_location = ifisEmpty(item)
    console.log(center_location)
    return (
      <LeafletMap
        center={center_location}
        zoom={12}
        maxZoom={17}
        attributionControl={true}
        zoomControl={true}
        doubleClickZoom={true}
        scrollWheelZoom={true}
        dragging={true}
        animate={true}
        easeLinearity={0.35}
      >
        <TileLayer
          url='http://{s}.tile.osm.org/{z}/{x}/{y}.png'
        />
        <Marker position={center_location}>
          <Popup>
            Popup for any custom information.
          </Popup>
        </Marker>
      </LeafletMap>
    );
  }
}

export default MapChart
