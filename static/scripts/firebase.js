
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
import { getDatabase, ref, set, get } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyB7pYE_d97yWvBFwhuqO1OnfcxRYOtTqnE",
    authDomain: "shade-example.firebaseapp.com",
    projectId: "shade-example",
    storageBucket: "shade-example.appspot.com",
    messagingSenderId: "465651478438",
    appId: "1:465651478438:web:ce3d17015847333b222967",
    measurementId: "G-T4H48EJ8KH",
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

export { db, ref, set, get}