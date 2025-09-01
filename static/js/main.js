// Main JavaScript file for NutriGuide - Personalized Meal Recommendation App

// Global utility functions and app initialization
(function() {
    'use strict';

    // Initialize app when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeApp();
    });

    function initializeApp() {
        // Initialize all components
        initializeAnimations();
        initializeNavigation();
        initializeTooltips();
        initializeFormEnhancements();
        initializeLoadingStates();
        initializeAccessibility();
        
        console.log('NutriGuide app initialized successfully');
    }

    // Animation and scroll effects
    function initializeAnimations() {
        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const animationObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    element.style.opacity = '1';
                    
                    if (element.classList.contains('slide-in-left')) {
                        element.style.transform = 'translateX(0)';
                    } else if (element.classList.contains('slide-in-right')) {
                        element.style.transform = 'translateX(0)';
                    } else {
                        element.style.transform = 'translateY(0)';
                    }
                    
                    // Add a small delay for staggered animations
                    if (element.classList.contains('meal-card') || element.classList.contains('tip-card')) {
                        const cards = document.querySelectorAll('.meal-card, .tip-card');
                        const index = Array.from(cards).indexOf(element);
                        element.style.animationDelay = `${index * 0.1}s`;
                    }
                }
            });
        }, observerOptions);

        // Observe all animated elements
        document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .meal-card, .tip-card').forEach(el => {
            animationObserver.observe(el);
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Parallax effect for hero section (if present)
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            window.addEventListener('scroll', function() {
                const scrolled = window.pageYOffset;
                const parallax = heroSection.querySelector('.hero-content');
                if (parallax) {
                    const speed = scrolled * 0.5;
                    parallax.style.transform = `translateY(${speed}px)`;
                }
            });
        }
    }

    // Navigation enhancements
    function initializeNavigation() {
        const navbar = document.querySelector('.navbar');
        
        if (navbar) {
            // Add scroll effect to navbar
            window.addEventListener('scroll', function() {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            });

            // Mobile navigation close on link click
            const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
            const navbarToggle = document.querySelector('.navbar-toggler');
            const navbarCollapse = document.querySelector('.navbar-collapse');

            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                        navbarToggle.click();
                    }
                });
            });
        }

        // Active page highlighting
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    // Initialize Bootstrap tooltips and popovers
    function initializeTooltips() {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // Form enhancements
    function initializeFormEnhancements() {
        // Auto-save form data to localStorage
        const forms = document.querySelectorAll('form[data-auto-save]');
        forms.forEach(form => {
            const formId = form.getAttribute('id') || 'form';
            
            // Load saved data
            const savedData = localStorage.getItem(`form_${formId}`);
            if (savedData) {
                try {
                    const data = JSON.parse(savedData);
                    Object.keys(data).forEach(key => {
                        const field = form.querySelector(`[name="${key}"]`);
                        if (field) {
                            if (field.type === 'checkbox' || field.type === 'radio') {
                                field.checked = data[key];
                            } else {
                                field.value = data[key];
                            }
                        }
                    });
                } catch (e) {
                    console.warn('Failed to load saved form data:', e);
                }
            }

            // Save data on change
            form.addEventListener('input', function() {
                const formData = new FormData(form);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }
                localStorage.setItem(`form_${formId}`, JSON.stringify(data));
            });

            // Clear saved data on successful submission
            form.addEventListener('submit', function() {
                localStorage.removeItem(`form_${formId}`);
            });
        });

        // Real-time form validation
        const validationForms = document.querySelectorAll('.needs-validation');
        validationForms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    validateField(this);
                });

                input.addEventListener('input', function() {
                    if (this.classList.contains('is-invalid')) {
                        validateField(this);
                    }
                });
            });
        });

        // Character counter for textareas
        const textareas = document.querySelectorAll('textarea[maxlength]');
        textareas.forEach(textarea => {
            const maxLength = textarea.getAttribute('maxlength');
            const counter = document.createElement('small');
            counter.className = 'text-muted mt-1 d-block';
            textarea.parentNode.appendChild(counter);

            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} characters remaining`;
                
                if (remaining < 10) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            }

            textarea.addEventListener('input', updateCounter);
            updateCounter();
        });
    }

    // Field validation helper
    function validateField(field) {
        const isValid = field.checkValidity();
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
        }

        return isValid;
    }

    // Loading states and skeleton screens
    function initializeLoadingStates() {
        // Create skeleton loader
        window.showSkeleton = function(container, count = 3) {
            const skeletonHTML = `
                <div class="skeleton-card">
                    <div class="skeleton skeleton-image mb-3" style="height: 200px; border-radius: 0.5rem;"></div>
                    <div class="skeleton skeleton-text mb-2" style="height: 20px; width: 80%;"></div>
                    <div class="skeleton skeleton-text mb-2" style="height: 16px; width: 60%;"></div>
                    <div class="skeleton skeleton-text" style="height: 16px; width: 40%;"></div>
                </div>
            `;

            if (typeof container === 'string') {
                container = document.querySelector(container);
            }

            if (container) {
                container.innerHTML = Array(count).fill(skeletonHTML).join('');
            }
        };

        // Hide skeleton loader
        window.hideSkeleton = function(container) {
            if (typeof container === 'string') {
                container = document.querySelector(container);
            }

            if (container) {
                const skeletons = container.querySelectorAll('.skeleton-card');
                skeletons.forEach(skeleton => {
                    skeleton.style.animation = 'fadeOut 0.3s ease forwards';
                    setTimeout(() => skeleton.remove(), 300);
                });
            }
        };

        // Global loading overlay
        window.showGlobalLoading = function(message = 'Loading...') {
            const overlay = document.createElement('div');
            overlay.id = 'globalLoadingOverlay';
            overlay.innerHTML = `
                <div class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
                     style="background: rgba(255, 255, 255, 0.9); z-index: 9999;">
                    <div class="text-center">
                        <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;"></div>
                        <h5 class="text-primary">${message}</h5>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
        };

        window.hideGlobalLoading = function() {
            const overlay = document.getElementById('globalLoadingOverlay');
            if (overlay) {
                overlay.style.animation = 'fadeOut 0.3s ease forwards';
                setTimeout(() => overlay.remove(), 300);
            }
        };
    }

    // Accessibility enhancements
    function initializeAccessibility() {
        // Skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'visually-hidden-focusable btn btn-primary position-absolute';
        skipLink.style.top = '10px';
        skipLink.style.left = '10px';
        skipLink.style.zIndex = '10000';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Add main content landmark if not present
        let mainContent = document.querySelector('main');
        if (!mainContent) {
            mainContent = document.querySelector('.container').closest('div');
            if (mainContent) {
                mainContent.setAttribute('role', 'main');
                mainContent.id = 'main-content';
            }
        }

        // Keyboard navigation for cards
        const interactiveCards = document.querySelectorAll('.card[data-href], .quick-action-card');
        interactiveCards.forEach(card => {
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
            
            card.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const href = this.getAttribute('data-href') || this.getAttribute('href');
                    if (href) {
                        window.location.href = href;
                    } else {
                        this.click();
                    }
                }
            });
        });

        // Announce page changes for screen readers
        const pageTitle = document.title;
        if (pageTitle) {
            const announcement = document.createElement('div');
            announcement.setAttribute('aria-live', 'polite');
            announcement.setAttribute('aria-atomic', 'true');
            announcement.className = 'visually-hidden';
            announcement.textContent = `Page loaded: ${pageTitle}`;
            document.body.appendChild(announcement);
        }

        // Focus management for modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', function() {
                const firstInput = this.querySelector('input, button, select, textarea');
                if (firstInput) {
                    firstInput.focus();
                }
            });
        });
    }

    // Utility functions
    window.NutriGuideUtils = {
        // Show toast notification
        showToast: function(message, type = 'success', duration = 3000) {
            const toast = document.createElement('div');
            toast.className = `toast-notification ${type}`;
            toast.textContent = message;
            
            const toastContainer = document.getElementById('toast-container');
            if (toastContainer) {
                toastContainer.appendChild(toast);
            } else {
                document.body.appendChild(toast);
            }
            
            setTimeout(() => {
                toast.style.animation = 'slideOutRight 0.3s ease forwards';
                setTimeout(() => toast.remove(), 300);
            }, duration);
        },

        // Format number with commas
        formatNumber: function(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        },

        // Truncate text
        truncateText: function(text, maxLength = 100) {
            if (text.length <= maxLength) return text;
            return text.substr(0, maxLength) + '...';
        },

        // Debounce function
        debounce: function(func, wait, immediate) {
            let timeout;
            return function executedFunction() {
                const context = this;
                const args = arguments;
                const later = function() {
                    timeout = null;
                    if (!immediate) func.apply(context, args);
                };
                const callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func.apply(context, args);
            };
        },

        // Validate email
        isValidEmail: function(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },

        // Calculate BMI
        calculateBMI: function(weight, height) {
            const bmi = weight / (height * height);
            return Math.round(bmi * 10) / 10;
        },

        // Get BMI category
        getBMICategory: function(bmi) {
            if (bmi < 18.5) return { category: 'Underweight', class: 'info' };
            if (bmi < 25) return { category: 'Normal', class: 'success' };
            if (bmi < 30) return { category: 'Overweight', class: 'warning' };
            return { category: 'Obese', class: 'danger' };
        },

        // Local storage helpers
        storage: {
            set: function(key, value) {
                try {
                    localStorage.setItem(`nutriguide_${key}`, JSON.stringify(value));
                    return true;
                } catch (e) {
                    console.warn('Failed to save to localStorage:', e);
                    return false;
                }
            },
            
            get: function(key) {
                try {
                    const item = localStorage.getItem(`nutriguide_${key}`);
                    return item ? JSON.parse(item) : null;
                } catch (e) {
                    console.warn('Failed to read from localStorage:', e);
                    return null;
                }
            },
            
            remove: function(key) {
                try {
                    localStorage.removeItem(`nutriguide_${key}`);
                    return true;
                } catch (e) {
                    console.warn('Failed to remove from localStorage:', e);
                    return false;
                }
            }
        }
    };

    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                console.log(`Page load time: ${loadTime}ms`);
                
                // Send to analytics if needed
                if (loadTime > 3000) {
                    console.warn('Page load time is slow:', loadTime + 'ms');
                }
            }
        });
    }

    // Error handling for uncaught errors
    window.addEventListener('error', function(e) {
        console.error('Global error:', e.error);
        
        // Show user-friendly error message
        if (e.error && !e.error.toString().includes('Script error')) {
            NutriGuideUtils.showToast('An error occurred. Please try again.', 'danger');
        }
    });

    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled promise rejection:', e.reason);
        
        // Prevent the default browser behavior
        e.preventDefault();
        
        // Show user-friendly error message
        NutriGuideUtils.showToast('Something went wrong. Please refresh the page.', 'danger');
    });

    // Service worker registration (for future PWA features)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // Placeholder for future service worker
            console.log('Service Worker support detected');
        });
    }

})();

// Additional animations and effects
document.addEventListener('DOMContentLoaded', function() {
    // Animate counters if present
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const increment = target / 200;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.ceil(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        // Start animation when element comes into view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(counter);
    });

    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.classList.add('fade-in');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: scale(0);
                animation: ripple 0.6s linear;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Add ripple animation CSS
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);
