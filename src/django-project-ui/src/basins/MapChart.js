import React from 'react'
import { Map as LeafletMap, TileLayer, Marker, Popup, GeoJSON, Polygon,ImageOverlay} from 'react-leaflet';

class MapChart extends React.Component {
  render() {
    const {item} = this.props
    const url = ''
    function ifisEmpty(obj) {
        for(var key in obj) {
            if(obj.hasOwnProperty(key))
                return [obj.latitud,obj.longitud];
        }
        return [6.264,-75.603];
    }
    const center_location = ifisEmpty(item)
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
        <GeoJSON
           key={item.slug}
           data={item.basin_polygon}
           color='#4b898a'
           fillColor='#6cafb0'
           fillOpacity= {0.5}
           weight={1}
        />
        <ImageOverlay
          url="http://siata.gov.co/kml/00_Radar/Ultimo_Barrido/AreaMetRadar_10_120_DBZH.png"
          bounds={[[7.3000, -76.6000], [5.1000, -74.3000]]}
          alpha = {0.8}
        />
      </LeafletMap>
    );
  }
}

export default MapChart
