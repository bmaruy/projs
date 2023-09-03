import React, { useState } from 'react';
import Button from '@mui/material/Button';
import { db, storage } from './firebase-config'; 
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import './ImageUpload.css';

function ImageUpload({ username, onImageUpload }) {
  const [image, setImage] = useState(null);
  const [progress, setProgress] = useState(0);
  const [caption, setCaption] = useState('');

  const handleChange = (e) => {
    if (e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  const uploadWithRetry = async (imageRef, image, maxRetries = 3, currentRetry = 0) => {
    try {
      const snapshot = await uploadBytes(imageRef, image);
      const downloadURL = await getDownloadURL(imageRef);
      return downloadURL;
    } catch (error) {
      console.error('Error uploading image:', error);
      if (currentRetry < maxRetries) {
        console.log(`Retrying upload (Retry ${currentRetry + 1})...`);
        return uploadWithRetry(imageRef, image, maxRetries, currentRetry + 1);
      } else {
        throw error; 
      }
    }
  };

  const handleUpload = async () => {
    if (!image) {
      return; 
    }

    const imageRef = storage.ref(`images/${image.name}`);

    try {
      const snapshot = await uploadWithRetry(imageRef, image);

      const downloadURL = await getDownloadURL(imageRef);

      await addDoc(collection(db, 'posts'), {
        timestamp: serverTimestamp(),
        caption: caption,
        imageUrl: downloadURL,
        username: username,
      });

      setProgress(0);
      setCaption('');
      setImage(null);

      // Pass the uploaded image URL back to the parent component
      if (onImageUpload) {
        onImageUpload(downloadURL);
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Error uploading image: ' + error.message);
    }
  };

  return (
    <div className="imageupload">
      <progress className="imageupload__progress" value={progress} max="100" />
      <input type="text" placeholder="Enter a caption..." onChange={(event) => setCaption(event.target.value)} value={caption} />
      <input type="file" onChange={handleChange} />
      <Button onClick={handleUpload}>Upload</Button>
    </div>
  );
}

export default ImageUpload;
