import React, { Component } from 'react';
import 'whatwg-fetch'
import cookie from 'react-cookies'

import PostInline from './PostInline';

class Posts extends Component {
  constructor(props){
    super(props)
    this.tooglePostListClass = this.tooglePostListClass.bind(this)
    this.toogleItem = this.toogleItem.bind(this)
  }
      state = {
        posts : [],
        postListClass : "card",
        currentItem : "nuevo"
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

  toogleItem(event){
    event.preventDefault()
    this.setState({
      currentItem : event.target.offsetParent.id
    })
  }

  componentDidMount(){ //{
    this.setState({
        posts: [],
        postListClass : "card",
        currentItem:"nuevo"
    })
    this.loadPosts()
  }

  render() {
      const {posts} = this.state
      const {postListClass} = this.state
      const {currentItem} = this.state
      const item = posts.find( item => item.slug === currentItem )
      console.log(item)
    return (
      <div>
        <h1> Title </h1>
        <h1> {currentItem} </h1>
        <button onClick = {this.tooglePostListClass}> Toogle Class </button>
        {posts.length > 0 ? posts.map((postItem,index)=>{
              return (
                <PostInline post={postItem} elClass={postListClass} click={this.toogleItem}/>
            )
        }) : <p> No Post Found </p>}
      </div>
    );
  }
}

export default Posts;
