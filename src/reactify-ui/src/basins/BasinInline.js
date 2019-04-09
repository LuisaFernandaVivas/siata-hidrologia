import React, { Component } from 'react';

class BasinInline extends Component {
  render() {
      const {basin} = this.props
      const {elClass} = this.props
      const showContent = elClass === 'card' ? 'd-block' : 'd-none'
      const {click} = this.props


    return (
      <div>
      {basin !== undefined ?
        <div onClick={click} className={elClass} id={basin.slug}>
          <a><h1>{basin.slug}</h1></a>
          <p className = {showContent}>{basin.nombre}</p>
        </div>
      : ""}
      </div>
    );
  }
}

export default BasinInline;
