import React, { Component } from 'react';
import './App.css';

import BasinManager from './basins/BasinManager.js';

class App extends Component {

  state = {
    modelo_transito: "https://siata.gov.co/hidrologia/modelo_transito_crecidas/modelo_transito.php",
    camaras: "http://siata.gov.co/hidrologia/camaras/camaras.php",
    width:  700,
    height:  500
  }

  render() {
    return (
      <div className="App">
        <BasinManager />
      </div>
    );
  }
}
export default App;
