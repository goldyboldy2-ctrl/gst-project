/**
 * GST Compliance Pro - Main JavaScript
 * Centralized utilities and functions
 */

(function() {
  'use strict';

  // Create global gstTools object
  const gstTools = {
    
    /**
     * Copy text to clipboard with visual feedback
     */
    copyToClipboard: function(text, button) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          if (button) {
            const originalText = button.textContent;
            button.textContent = '✓ Copied!';
            button.style.background = 'var(--green-success, #10b981)';
            button.style.color = 'white';
            setTimeout(() => {
              button.textContent = originalText;
              button.style.background = '';
              button.style.color = '';
            }, 2000);
          }
        }).catch(err => {
          console.error('Copy failed:', err);
          this.fallbackCopy(text);
        });
      } else {
        this.fallbackCopy(text);
      }
    },

    /**
     * Fallback copy method for older browsers
     */
    fallbackCopy: function(text) {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        alert('Copied to clipboard!');
      } catch (err) {
        alert('Copy failed. Please copy manually.');
      }
      document.body.removeChild(textArea);
    },

    /**
     * Format number as Indian Rupees
     */
    formatINR: function(amount) {
      if (amount === null || amount === undefined || isNaN(amount)) {
        return '₹0.00';
      }
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(amount);
    },

    /**
     * Show result box with animation
     */
    showResultBox: function(boxId) {
      const box = document.getElementById(boxId);
      if (box) {
        box.classList.add('show');
        box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    },

    /**
     * Hide result box
     */
    hideResultBox: function(boxId) {
      const box = document.getElementById(boxId);
      if (box) {
        box.classList.remove('show');
      }
    },

    /**
     * Debounce function for search inputs
     */
    debounce: function(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    /**
     * Validate form
     */
    validateForm: function(formId) {
      const form = document.getElementById(formId);
      if (!form) return false;
      return form.checkValidity();
    },

    /**
     * Save preference to localStorage
     */
    savePreference: function(key, value) {
      try {
        localStorage.setItem('gst_' + key, JSON.stringify(value));
      } catch (e) {
        console.warn('localStorage not available:', e);
      }
    },

    /**
     * Get preference from localStorage
     */
    getPreference: function(key, defaultValue) {
      try {
        const item = localStorage.getItem('gst_' + key);
        return item ? JSON.parse(item) : defaultValue;
      } catch (e) {
        console.warn('localStorage not available:', e);
        return defaultValue;
      }
    },

    /**
     * Track event (Google Analytics ready)
     */
    trackEvent: function(category, action, label) {
      if (typeof gtag !== 'undefined') {
        gtag('event', action, {
          'event_category': category,
          'event_label': label
        });
      }
      console.log('Event:', category, action, label);
    }
  };

  // Attach to window
  window.gstTools = gstTools;

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    initMobileMenu();
    initReadingProgress();
    initSmoothScroll();
    highlightActivePage();
  }

  /**
   * Mobile menu toggle
   */
  function initMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (toggle && navLinks) {
      toggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
      });

      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !navLinks.contains(e.target)) {
          navLinks.classList.remove('active');
        }
      });
    }
  }

  /**
   * Reading progress bar for blog posts
   */
  function initReadingProgress() {
    const progressBar = document.querySelector('.reading-progress-bar');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight - windowHeight;
      const scrolled = window.scrollY;
      const progress = (scrolled / documentHeight) * 100;
      progressBar.style.width = Math.min(progress, 100) + '%';
    });
  }

  /**
   * Smooth scroll for anchor links
   */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /**
   * Highlight active page in navigation
   */
  function highlightActivePage() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
      const linkPage = link.getAttribute('href').split('/').pop();
      if (linkPage === currentPage) {
        link.classList.add('active');
      }
    });
  }

})();

console.log('✅ GST Compliance Pro - main.js loaded successfully');
console.log('✅ gstTools object available:', typeof window.gstTools);
