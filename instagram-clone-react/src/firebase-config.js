import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';
import 'firebase/compat/storage';
//import { getStorage } from 'firebase/storage';

const firebaseConfig = {
    apiKey: "AIzaSyAusxiLryo1ofEMrEQhowq_Q6uUe2CrypE",
    authDomain: "instagram-clone-react-6269d.firebaseapp.com",
    projectId: "instagram-clone-react-6269d",
    storageBucket: "instagram-clone-react-6269d.appspot.com",
    messagingSenderId: "446614928914",
    appId: "1:446614928914:web:45496f94a035503899e2cb",
    measurementId: "G-1PMTK99SJG"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);

const db = firebaseApp.firestore();
const auth = firebase.auth();
const storage = firebase.storage();
//const storage = getStorage();


export { db, auth, storage };
