import './App.css'
import React, { useState, useEffect } from 'react'
import Post from './Post'
import { db, auth, storage } from './firebase-config'
import { collection, onSnapshot } from 'firebase/firestore'
import Box from '@mui/material/Box';
import Button  from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Input from '@mui/material/Input';
import ImageUpload from './ImageUpload'


const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

function App() {

  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const [openSignIn, setOpenSignIn] = React.useState(false);
  const [posts, setPosts] = useState([]);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((authUser) => {
      if(authUser) {
        // user logged in
        console.log(authUser);
        setUser(authUser);
      } else {
        // user logged out
        setUser(null);
      }
    })

    return () => {
      // perform some cleanup
      unsubscribe();
    }
  }, [user, username]);

  useEffect(() => {

    db.collection('posts').orderBy('timestamp', 'desc').onSnapshot(snapshot => {
      setPosts(snapshot.docs.map(doc => ({
        id: doc.id,
        post: doc.data()
      })));
    })
  }, []);

  const signUp = (event) => {
    event.preventDefault();

    auth
    .createUserWithEmailAndPassword(email, password)
    .then((authUser) => {
      return authUser.user.updateProfile({
        displayName: username
      })
    })
    .catch((error) => alert(error.message))
  }

  const signIn = (event) => {
    event.preventDefault();
    
    auth
      .signInWithEmailAndPassword(email, password)
      .catch((error) => alert(error.message))
    setOpenSignIn(false)
  }


  return (
    <div className="App">

    



      <Modal
        open={open}
        onClose={() => setOpen(false)}
      >
        <Box sx={style}>
        <form className="app__signup"> 
          <center>
            <img 
              className="app__headerImage"
              src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png"
              alt=""
            />   
          </center>

          <Input 
            placeholder="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input 
            placeholder="email"
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input 
            placeholder="password"
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" onClick={signUp}>Sign up</Button>
          
        </form>
        </Box>
      </Modal>

      <Modal
        open={openSignIn}
        onClose={() => setOpenSignIn(false)}
      >
        <Box sx={style}>
        <form className="app__signup"> 
          <center>
            <img 
              className="app__headerImage"
              src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png"
              alt=""
            />   
          </center>
          <Input
            placeholder="email"
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input 
            placeholder="password"
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" onClick={signIn}>Sign In</Button>
          
        </form>
        </Box>
      </Modal>


      <div className="app__header">
        <img
          className="app__headerImage"
          src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png"
          alt=""
        />
        {user ? (
          <Button onClick={() => auth.signOut()}>Logout</Button>
        ): (
          <div className="app__loginContainer">
            <Button onClick={() => setOpenSignIn(true)}>Sign in</Button>          
            <Button onClick={() => setOpen(true)}>Sign up</Button>
          </div>
        )}
      </div>

      
      <div className="app__posts">
        {
          posts.map(({id, post}) => (
            <Post key={id} postId={id} user={user} username={post.username} caption={post.caption} imageUrl={post.imageUrl} />
          ))
        }
      </div>


      {user?.displayName ? (
        <ImageUpload username={user.displayName} onImageUpload={setUploadedImageUrl} />
        ): (
        <h3>Sorry, you need to login to upload.</h3>
      )}

    </div>
  );
}

export default App;
