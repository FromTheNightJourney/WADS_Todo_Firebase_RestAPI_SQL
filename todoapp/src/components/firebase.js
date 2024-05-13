// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCR7CS1GvnJinRasreVYzIipMJmw9oIsuc",
  authDomain: "fir-fastapi-todo.firebaseapp.com",
  projectId: "fir-fastapi-todo",
  storageBucket: "fir-fastapi-todo.appspot.com",
  messagingSenderId: "723597021228",
  appId: "1:723597021228:web:31e25043c505ed4f528189",
  measurementId: "G-SF2MH12LCJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export const auth =getAuth(app);
export const db = getFirestore(app);