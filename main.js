/**
 * GST COMPLIANCE PRO - MAIN.JS
 * Centralized JavaScript for all pages
 * Version: 3.0 Production (February 2026)
 * Optimized for 100k+ monthly traffic
 */

/* ============================================================
   MOBILE MENU TOGGLE
   ============================================================ */

function initMobileMenu() {
  const toggle = document.querySelector('.mobile-menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (!toggle || !navLinks) return;
  
  toggle.addEventListener('click', function() {
    navLinks.classList.toggle('active');
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', function(e) {
    if (!toggle.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('active');
    }
  });
  
  // Close menu when clicking a link
  const links = navLinks.querySelectorAll('a');
  links.forEach(link => {
    link.addEventListener('click', function() {
      navLinks.classList.remove('active');
    });
  });
}

/* ============================================================
   READING PROGRESS BAR (for blog posts)
   ============================================================ */

function initReadingProgress() {
  const article = document.querySelector('article');
  const progressBar = document.getElementById('progressBar');
  
  if (!article || !progressBar) return;
  
  window.addEventListener('scroll', function() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    
    progressBar.style.width = Math.min(scrolled, 100) + '%';
  });
}

/* ============================================================
   SMOOTH SCROLL TO ANCHOR LINKS
   ============================================================ */

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      
      // Skip if href is just "#"
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

/* ============================================================
   RADIO BUTTON STYLING (for forms)
   ============================================================ */

function initRadioStyling() {
  const radios = document.querySelectorAll('input[type="radio"]');
  
  radios.forEach(radio => {
    radio.addEventListener('change', function() {
      const name = this.name;
      
      // Reset all labels in same group
      document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
        const label = r.closest('label');
        if (label) {
          label.style.background = 'var(--slate-50)';
          label.style.borderColor = 'var(--color-border)';
        }
      });
      
      // Highlight selected
      const selectedLabel = this.closest('label');
      if (selectedLabel) {
        selectedLabel.style.background = 'var(--indigo-bg)';
        selectedLabel.style.borderColor = 'var(--indigo-primary)';
      }
    });
  });
}

/* ============================================================
   COPY TO CLIPBOARD UTILITY
   ============================================================ */

function copyToClipboard(text, button) {
  navigator.clipboard.writeText(text).then(() => {
    const originalText = button.innerHTML;
    const originalBg = button.style.background;
    const originalColor = button.style.color;
    const originalBorder = button.style.borderColor;
    
    // Show success feedback
    button.innerHTML = '✓ Copied!';
    button.style.background = 'var(--green-bg)';
    button.style.color = 'var(--green-success)';
    button.style.borderColor = 'var(--green-success)';
    
    // Reset after 2 seconds
    setTimeout(() => {
      button.innerHTML = originalText;
      button.style.background = originalBg;
      button.style.color = originalColor;
      button.style.borderColor = originalBorder;
    }, 2000);
  }).catch(() => {
    // Fallback for browsers that don't support clipboard API
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
      document.execCommand('copy');
      alert('Copied to clipboard!');
    } catch (err) {
      alert('Failed to copy. Please try again.');
    }
    
    document.body.removeChild(textarea);
  });
}

/* ============================================================
   DEBOUNCE UTILITY (for search inputs)
   ============================================================ */

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func.apply(this, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/* ============================================================
   FORM VALIDATION HELPER
   ============================================================ */

function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return false;
  
  const requiredFields = form.querySelectorAll('[required]');
  let isValid = true;
  
  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.style.borderColor = 'var(--color-error, #ef4444)';
      isValid = false;
    } else {
      field.style.borderColor = 'var(--color-border)';
    }
  });
  
  return isValid;
}

/* ============================================================
   SHOW/HIDE RESULT BOX
   ============================================================ */

function showResultBox(boxId) {
  const box = document.getElementById(boxId);
  if (!box) return;
  
  box.classList.add('show');
  box.style.display = 'block';
  
  // Smooth scroll to result
  setTimeout(() => {
    box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, 100);
}

function hideResultBox(boxId) {
  const box = document.getElementById(boxId);
  if (!box) return;
  
  box.classList.remove('show');
  box.style.display = 'none';
}

/* ============================================================
   ACTIVE PAGE DETECTION (for navigation highlighting)
   ============================================================ */

function highlightActivePage() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a');
  
  navLinks.forEach(link => {
    const linkPath = new URL(link.href).pathname;
    
    // Remove active class from all
    link.classList.remove('active');
    
    // Add active class to current page
    if (currentPath === linkPath || 
        (currentPath.includes('/blog/') && linkPath.includes('/blog/')) ||
        (currentPath.includes('/tools/') && linkPath.includes('tools'))) {
      link.classList.add('active');
    }
  });
}

/* ============================================================
   MOBILE ACTION BAR ACTIVE STATE
   ============================================================ */

function highlightMobileAction() {
  const currentPath = window.location.pathname;
  const actionBtns = document.querySelectorAll('.mobile-action-btn');
  
  actionBtns.forEach(btn => {
    btn.classList.remove('active');
    
    // Tools pages
    if (currentPath.includes('calculator') || 
        currentPath.includes('finder') || 
        currentPath.includes('penalty')) {
      if (btn.querySelector('.icon').textContent === '🔍') {
        btn.classList.add('active');
      }
    }
    
    // Deadlines page
    if (currentPath.includes('deadline')) {
      if (btn.querySelector('.icon').textContent === '📅') {
        btn.classList.add('active');
      }
    }
  });
}

/* ============================================================
   LOCAL STORAGE HELPER (for user preferences)
   ============================================================ */

function savePreference(key, value) {
  try {
    localStorage.setItem(`gst_${key}`, JSON.stringify(value));
  } catch (e) {
    console.warn('LocalStorage not available:', e);
  }
}

function getPreference(key, defaultValue = null) {
  try {
    const value = localStorage.getItem(`gst_${key}`);
    return value ? JSON.parse(value) : defaultValue;
  } catch (e) {
    console.warn('LocalStorage not available:', e);
    return defaultValue;
  }
}

/* ============================================================
   FORMAT CURRENCY (Indian Rupees)
   ============================================================ */

function formatINR(amount) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount);
}

/* ============================================================
   PRINT HANDLER (for results)
   ============================================================ */

function printResult() {
  window.print();
}

/* ============================================================
   ANALYTICS HELPER (placeholder for Google Analytics)
   ============================================================ */

function trackEvent(category, action, label) {
  // Google Analytics 4 event tracking
  if (typeof gtag !== 'undefined') {
    gtag('event', action, {
      'event_category': category,
      'event_label': label
    });
  }
}

/* ============================================================
   INITIALIZE ALL ON PAGE LOAD
   ============================================================ */

document.addEventListener('DOMContentLoaded', function() {
  // Core functionality
  initMobileMenu();
  initReadingProgress();
  initSmoothScroll();
  initRadioStyling();
  highlightActivePage();
  highlightMobileAction();
  
  // Log page load for debugging
  console.log('GST Compliance Pro - Page loaded successfully');
});

/* ============================================================
   EXPOSE UTILITIES TO GLOBAL SCOPE
   ============================================================ */

window.gstTools = {
  copyToClipboard,
  debounce,
  validateForm,
  showResultBox,
  hideResultBox,
  savePreference,
  getPreference,
  formatINR,
  printResult,
  trackEvent
};
