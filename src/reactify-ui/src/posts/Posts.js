import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'

import PostInline from './PostInline';

class Posts extends Component {
      state = {
        posts : [],
      }
  loadPosts(){ //http request
      const endpoint = '/api/posts'
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
          console.log(responseData.results)
            thisComp.setState({
                posts: responseData.results
                })
      }).catch(function(error){
          console.log("error",error)
      })
    }

  componentDidMount(){ //{
    this.setState({
        posts: []
    })
    this.loadPosts()
  }
  render() {
      const {posts} = this.state
    return (
      <div>
        <h1> Hellow world </h1>
        {posts.length > 0 ? posts.map((postItem,index)=>{
              return (
                <PostInline post={postItem.title} />
            )
        }) : <p> No Post Found </p>}
      </div>
    );
  }
}

export default Posts;
