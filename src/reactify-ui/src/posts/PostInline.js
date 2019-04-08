import React, { Component } from 'react';

class PostInline extends Component {
  render() {
      const {post} = this.props
      const {elClass} = this.props
      const showContent = elClass === 'card' ? 'd-block' : 'd-none'
      const {click} = this.props


    return (
      <div>
      {post !== undefined ?
        <div onClick={click} className={elClass} id={post.slug}>
          <a><h1>{post.title}</h1></a>
          <p className = {showContent}>{post.content}</p>
        </div>
      : ""}
      </div>
    );
  }
}

export default PostInline;
