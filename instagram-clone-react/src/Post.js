import './Post.css';
import Avatar from '@mui/material/Avatar';
import { db } from './firebase-config';
import React, { useState, useEffect } from 'react'
import { Postcard } from 'react-bootstrap-icons';
import firebase from 'firebase/compat/app';
import 'firebase/compat/firestore';


function Post({ postId, user, username, caption, imageUrl }) {
  const [comments, setComments] = useState([]);
  const [comment, setComment] = useState('');

  useEffect(() => {
    let unsubscribe;
    if(postId) {
      unsubscribe = db
        .collection("posts")
        .doc(postId)
        .collection("comments")
        .orderBy('timestamp', 'desc')
        .onSnapshot((snapshot) => {
          setComments(snapshot.docs.map((doc) => doc.data()))
        });
    }

    return () => {
      if(unsubscribe) {
        unsubscribe();
      }
    };
  }, [postId]);


  const postComment = (event) => {
    event.preventDefault();

    db.collection("posts").doc(postId).collection("comments").add({
      text: comment,
      username: user.displayName,
      timestamp: firebase.firestore.FieldValue.serverTimestamp()
    });
    setComment('');
  }

  return (
    <div className="post">
        <div className="post__header">
        <Avatar 
                className="post__avatar"
                alt={username}
                src="/static/images/avatar/1.jpg" 
        />
            <h3>{username}</h3>
        </div>
        
        <img className="post__image" src={imageUrl}/>

        <h4 className="post__text"><strong>{username}:</strong> {caption} </h4>

        <div className="post__comments">
          {comments.map((comment) => (
            <p>
              <strong>{comment.username}</strong> {comment.text}
            </p>
          ))}
        </div>

        {user&& (
          <form>
            <input 
              className="post__input"
              type="text"
              placeholder="Add a comment..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}

            />
            <button 
              disabled={!comment}
              className="post__button"
              type="submit"
              onClick={postComment}
            >
              Post
            </button>
          </form>
        )}

        
    </div>
  )
}

export default Post