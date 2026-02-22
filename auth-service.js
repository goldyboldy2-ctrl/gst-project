// auth-service.js
// Authentication Service for MyGSTIndia
// Handles all auth operations with Firebase

import { firebaseConfig } from './auth-config.js';
class AuthService {
  constructor() {
    this.user = null;
    this.initialized = false;
    this.auth = null;
    this.db = null;
  }

  // Initialize Firebase
  async init() {
    if (this.initialized) return;

    try {
      // Initialize Firebase with config
      firebase.initializeApp(firebaseConfig);

      // Initialize services
      this.auth = firebase.auth();
      this.db = firebase.firestore();

      // Listen for auth state changes
      this.auth.onAuthStateChanged((user) => {
        this.user = user;
        this.handleAuthStateChange(user);
      });

      this.initialized = true;
      console.log('✅ Auth service initialized successfully');
    } catch (error) {
      console.error('❌ Auth initialization failed:', error);
    }
  }

  // Handle auth state changes
  handleAuthStateChange(user) {
    if (user) {
      console.log('User logged in:', user.email);
      this.createUserDocument(user);
      this.updateUI(true);
      this.loadUserPreferences();
    } else {
      console.log('User logged out');
      this.updateUI(false);
      this.loadLocalPreferences();
    }
  }

  // Sign in with Google
  async signInWithGoogle() {
    try {
      const provider = new firebase.auth.GoogleAuthProvider();
      const result = await this.auth.signInWithPopup(provider);

      // Track in GA (if GA is set up)
      if (typeof gtag === 'function') {
        gtag('event', 'login', { method: 'Google' });
      }

      return result.user;
    } catch (error) {
      console.error('Google login failed:', error);
      alert('Google login failed. Please try again.');
      return null;
    }
  }

  // Sign out
  async signOut() {
    try {
      await this.auth.signOut();

      if (typeof gtag === 'function') {
        gtag('event', 'logout');
      }

      alert('Signed out successfully');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  // Create or update user document in Firestore
  async createUserDocument(user) {
    if (!user) return;

    const userRef = this.db.collection('users').doc(user.uid);
    const doc = await userRef.get();

    if (!doc.exists) {
      await userRef.set({
        email: user.email,
        displayName: user.displayName || user.email.split('@')[0],
        photoURL: user.photoURL || '',
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        lastLogin: firebase.firestore.FieldValue.serverTimestamp(),
        preferences: {
          defaultGSTRate: 18,
          defaultState: '',
          theme: 'light'
        },
        favoriteTools: [],
        stats: {
          toolsUsed: 0,
          lastActive: firebase.firestore.FieldValue.serverTimestamp()
        }
      });
      console.log('✅ New user document created');
    } else {
      await userRef.update({
        lastLogin: firebase.firestore.FieldValue.serverTimestamp()
      });
      console.log('✅ Existing user updated');
    }
  }

  // ... (rest of your methods like loadUserPreferences, savePreferences, toggleFavorite, etc.)
  // Copy-paste the remaining functions from your original file here.
  // They look correct — no syntax issues in them.
}

// Create global instance
const authService = new AuthService();

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
  authService.init();
});
