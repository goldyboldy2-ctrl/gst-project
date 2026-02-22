// Firebase Configuration for MyGSTIndia
// LIVE CONFIGURATION - DO NOT SHARE PUBLICLY

const firebaseConfig = {
apiKey: “AIzaSyBqLh_rGrmfl8ug_rrWSaHKQMabQvmtyIc”,
authDomain: “mygstindia-66f81.firebaseapp.com”,
projectId: “mygstindia-66f81”,
storageBucket: “mygstindia-66f81.firebasestorage.app”,
messagingSenderId: “594387667786”,
appId: “1:594387667786:web:6d8b005fe2921938c5cfb3”,
measurementId: “G-FNZQC8S2WD”
};

// Note: These keys are safe to use in client-side code
// Firebase security is controlled by Firestore Rules, not by hiding keys
// However, you should still set proper Firestore security rules

/*
SECURITY CHECKLIST:
✅ Authentication enabled (Google)
✅ Authorized domain added (mygstindia.in)
✅ Firestore database created
⏳ Security rules set (do this next if not done)

NEXT STEPS:

1. Upload this file to your GitHub repo root
1. Upload auth-service.js to your GitHub repo root
1. Upload preferences.html to your GitHub repo root
1. Add Firebase SDK scripts to all pages (see instructions below)

FIREBASE SDK SCRIPTS TO ADD:
Add these lines BEFORE </body> on EVERY page:

<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>

<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>

<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js"></script>

<script src="auth-config.js"></script>

<script src="auth-service.js"></script>

*/