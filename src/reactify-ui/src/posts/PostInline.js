import React, { Component } from 'react';

class PostInline extends Component {
  render() {
      const {title} = this.props
      const titleABC = "asdf" // lo mismo que el anterior
    return (
      <div>
        <h1>Posts {title} - {titleABC}</h1>
      </div>
    );
  }
}

export default PostInline;
