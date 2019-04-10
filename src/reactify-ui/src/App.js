import React, { Component } from 'react';
import './App.css';

import RiskChart from './RiskChart.js';

class App extends Component {

  state = {
    data: [12, 5, 6, 6, 9, 10],
    width: 700,
    height: 500,
  }

  render() {
    return (
      <div className="App">
        <RiskChart />
      </div>
    );
  }
}
export default App;
