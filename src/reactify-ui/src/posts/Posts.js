import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'

import PostInline from './PostInline';

class Posts extends Component {
  constructor(props){
    super(props)
    this.tooglePostListClass = this.tooglePostListClass.bind(this)
  }
      state = {
        posts : [],
        postListClass : "card",
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
  tooglePostListClass(event){
    event.preventDefault()
    let currentListClass = this.state.postListClass
    if (currentListClass === ""){
      this.setState({
        postListClass:"card",
      })
    } else {
        this.setState({
          postListClass : "",
        })
    }
  }

  componentDidMount(){ //{
    this.setState({
        posts: [],
        postListClass : "card"
    })
    this.loadPosts()
  }

  render() {
      const {posts} = this.state
      const {postListClass} = this.state
      console.log(postListClass)
    return (
      <div>
        <h1> Title </h1>
        <button onClick = {this.tooglePostListClass}> Toogle Class </button>
        {posts.length > 0 ? posts.map((postItem,index)=>{
              return (
                <PostInline post={postItem} elClass={postListClass}/>
            )
        }) : <p> No Post Found </p>}
      </div>
    );
  }
}

export default Posts;
