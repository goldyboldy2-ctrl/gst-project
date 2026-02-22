// Authentication Service for MyGSTIndia
// Handles all auth operations with Firebase
import { firebaseConfig } from './auth-config.js';

class AuthService {
  constructor() {
    this.user = null;
    this.initialized = false;
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
      this.auth.onAuthStateChanged(user => {
        this.user = user;
        this.handleAuthStateChange(user);
      });
      
      this.initialized = true;
      console.log('✅ Auth service initialized');
    } catch (error) {
      console.error('❌ Auth initialization failed:', error);
    }
  }

  // Handle auth state changes
  handleAuthStateChange(user) {
    if (user) {
      // User logged in
      console.log('User logged in:', user.email);
      this.createUserDocument(user);
      this.updateUI(true);
      this.loadUserPreferences();
    } else {
      // User logged out
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
      
      // Track in GA
      gtag('event', 'login', {
        method: 'Google'
      });
      
      return result.user;
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please try again.');
      return null;
    }
  }

  // Sign out
  async signOut() {
    try {
      await this.auth.signOut();
      
      // Track in GA
      gtag('event', 'logout');
      
      alert('Signed out successfully');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  // Create user document in Firestore (if doesn't exist)
  async createUserDocument(user) {
    if (!user) return;
    
    const userRef = this.db.collection('users').doc(user.uid);
    const doc = await userRef.get();
    
    if (!doc.exists) {
      // New user - create document
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
      
      console.log('✅ User document created');
    } else {
      // Existing user - update last login
      await userRef.update({
        lastLogin: firebase.firestore.FieldValue.serverTimestamp()
      });
    }
  }

  // Load user preferences from Firestore
  async loadUserPreferences() {
    if (!this.user) return null;
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      const doc = await userRef.get();
      
      if (doc.exists) {
        const data = doc.data();
        this.applyPreferences(data.preferences);
        return data.preferences;
      }
    } catch (error) {
      console.error('Failed to load preferences:', error);
    }
    
    return null;
  }

  // Save user preferences to Firestore
  async savePreferences(preferences) {
    if (!this.user) {
      // Not logged in - save to localStorage
      this.saveLocalPreferences(preferences);
      return;
    }
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      await userRef.update({
        preferences: preferences,
        'stats.lastActive': firebase.firestore.FieldValue.serverTimestamp()
      });
      
      this.applyPreferences(preferences);
      console.log('✅ Preferences saved');
      return true;
    } catch (error) {
      console.error('Failed to save preferences:', error);
      return false;
    }
  }

  // Apply preferences to UI
  applyPreferences(preferences) {
    if (!preferences) return;
    
    // Store in window for easy access
    window.userPreferences = preferences;
    
    // Apply theme
    if (preferences.theme === 'dark') {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    
    // Dispatch event for tools to listen
    window.dispatchEvent(new CustomEvent('preferencesLoaded', {
      detail: preferences
    }));
  }

  // Save preferences to localStorage (for non-logged-in users)
  saveLocalPreferences(preferences) {
    localStorage.setItem('myGSTPreferences', JSON.stringify(preferences));
    this.applyPreferences(preferences);
  }

  // Load preferences from localStorage
  loadLocalPreferences() {
    const saved = localStorage.getItem('myGSTPreferences');
    if (saved) {
      try {
        const preferences = JSON.parse(saved);
        this.applyPreferences(preferences);
        return preferences;
      } catch (e) {
        console.error('Failed to parse saved preferences');
      }
    }
    return null;
  }

  // Toggle favorite tool
  async toggleFavorite(toolId) {
    if (!this.user) {
      alert('Please sign in to save favorites');
      return false;
    }
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      const doc = await userRef.get();
      const data = doc.data();
      const favorites = data.favoriteTools || [];
      
      if (favorites.includes(toolId)) {
        // Remove from favorites
        await userRef.update({
          favoriteTools: firebase.firestore.FieldValue.arrayRemove(toolId)
        });
        return false;
      } else {
        // Add to favorites
        await userRef.update({
          favoriteTools: firebase.firestore.FieldValue.arrayUnion(toolId)
        });
        return true;
      }
    } catch (error) {
      console.error('Failed to toggle favorite:', error);
      return null;
    }
  }

  // Check if tool is favorited
  async isFavorite(toolId) {
    if (!this.user) return false;
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      const doc = await userRef.get();
      const data = doc.data();
      return (data.favoriteTools || []).includes(toolId);
    } catch (error) {
      return false;
    }
  }

  // Get user favorites
  async getFavorites() {
    if (!this.user) return [];
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      const doc = await userRef.get();
      const data = doc.data();
      return data.favoriteTools || [];
    } catch (error) {
      console.error('Failed to get favorites:', error);
      return [];
    }
  }

  // Increment tool usage count
  async trackToolUsage(toolId) {
    if (!this.user) return;
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      await userRef.update({
        'stats.toolsUsed': firebase.firestore.FieldValue.increment(1),
        'stats.lastActive': firebase.firestore.FieldValue.serverTimestamp(),
        'stats.lastTool': toolId
      });
    } catch (error) {
      console.error('Failed to track usage:', error);
    }
  }

  // Get user stats
  async getStats() {
    if (!this.user) return null;
    
    try {
      const userRef = this.db.collection('users').doc(this.user.uid);
      const doc = await userRef.get();
      const data = doc.data();
      return data.stats || { toolsUsed: 0 };
    } catch (error) {
      console.error('Failed to get stats:', error);
      return null;
    }
  }

  // Update UI based on auth state
  updateUI(isLoggedIn) {
    const loginBtn = document.getElementById('loginBtn');
    const userMenu = document.getElementById('userMenu');
    
    if (isLoggedIn && this.user) {
      // Show logged-in UI
      if (loginBtn) loginBtn.style.display = 'none';
      if (userMenu) {
        userMenu.style.display = 'flex';
        const userName = document.getElementById('userName');
        if (userName) {
          userName.textContent = this.user.displayName || this.user.email.split('@')[0];
        }
        const userPhoto = document.getElementById('userPhoto');
        if (userPhoto) {
          userPhoto.src = this.user.photoURL || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="16" fill="%233b82f6"/><text x="16" y="21" text-anchor="middle" fill="white" font-size="14" font-weight="bold">' + (this.user.displayName ? this.user.displayName[0] : 'U') + '</text></svg>';
        }
      }
    } else {
      // Show guest UI
      if (loginBtn) loginBtn.style.display = 'inline-block';
      if (userMenu) userMenu.style.display = 'none';
    }
  }

  // Check if user is logged in
  isLoggedIn() {
    return this.user !== null;
  }

  // Get current user
  getCurrentUser() {
    return this.user;
  }
}

// Create global instance
const authService = new AuthService();

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
  authService.init();
});
