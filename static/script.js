// Initialize AOS (Animate On Scroll)
document.addEventListener('DOMContentLoaded', function() {
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });
});

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Scroll to query section
function scrollToQuery() {
    const querySection = document.getElementById('query');
    querySection.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Scroll to features section
function scrollToFeatures() {
    const featuresSection = document.getElementById('features');
    featuresSection.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Form submission handling
document.getElementById('optimizationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitButton = this.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.innerHTML = '<div class="loading"></div> Processing...';
    submitButton.disabled = true;
    
    try {
        const problemDescription = formData.get('problemDescription');
        const constraints = formData.get('constraints');
        
        console.log('Submitting problem:', problemDescription);
        
        // Store form data in localStorage for results page
        const optimizationData = {
            problemDescription: problemDescription,
            constraints: constraints,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('optimizationData', JSON.stringify(optimizationData));
        
        // Call FastAPI endpoints
        const apiConfig = window.API_CONFIG || {
            baseURL: window.location.origin,
            endpoints: {
                solver: '/solver/solve',
                planner: '/planner/plan',
                explainer: '/explainer/solve'
            }
        };
        
        console.log('API Config:', apiConfig);
        
        // Test API connectivity first
        try {
            const healthResponse = await fetch(`${apiConfig.baseURL}/health`);
            if (!healthResponse.ok) {
                throw new Error(`Health check failed: ${healthResponse.status}`);
            }
            console.log('API health check passed');
        } catch (healthError) {
            console.error('API health check failed:', healthError);
            throw new Error('API server is not responding. Please check if the FastAPI server is running.');
        }
        
        // Call APIs with better error handling
        const apiCalls = [
            fetch(`${apiConfig.baseURL}${apiConfig.endpoints.solver}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ problem_description: problemDescription })
            }).then(async res => {
                if (!res.ok) {
                    const errorText = await res.text();
                    throw new Error(`Solver API error (${res.status}): ${errorText}`);
                }
                return res.json();
            }),
            
            fetch(`${apiConfig.baseURL}${apiConfig.endpoints.planner}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ problem_description: problemDescription })
            }).then(async res => {
                if (!res.ok) {
                    const errorText = await res.text();
                    throw new Error(`Planner API error (${res.status}): ${errorText}`);
                }
                return res.json();
            }),
            
            fetch(`${apiConfig.baseURL}${apiConfig.endpoints.explainer}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ problem_description: problemDescription })
            }).then(async res => {
                if (!res.ok) {
                    const errorText = await res.text();
                    throw new Error(`Explainer API error (${res.status}): ${errorText}`);
                }
                return res.json();
            })
        ];
        
        console.log('Making API calls...');
        const [solverResult, plannerResult, explainerResult] = await Promise.all(apiCalls);
        
        console.log('API Results:', { solverResult, plannerResult, explainerResult });
        
        // Store API results
        const apiResults = {
            solver: solverResult,
            planner: plannerResult,
            explainer: explainerResult
        };
        
        localStorage.setItem('apiResults', JSON.stringify(apiResults));
        
        // Redirect to results page
        window.location.href = 'results.html';
        
    } catch (error) {
        console.error('Error calling API:', error);
        
        // Show error message but still redirect to results page with fallback data
        const errorMessage = error.message || 'Unknown error occurred';
        console.log('API failed, using fallback data. Error:', errorMessage);
        
        // Store error information
        localStorage.setItem('apiError', JSON.stringify({
            message: errorMessage,
            timestamp: new Date().toISOString()
        }));
        
        // Show brief error message
        submitButton.innerHTML = '<i class="fas fa-exclamation-triangle"></i> API Error - Using Demo Data';
        submitButton.style.background = 'var(--warning-color)';
        
        // Still redirect to results page (will show mock data)
        setTimeout(() => {
            window.location.href = 'results.html';
        }, 1000);
    }
});

// Parallax effect for floating shapes
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const shapes = document.querySelectorAll('.shape');
    
    shapes.forEach((shape, index) => {
        const speed = 0.5 + (index * 0.1);
        shape.style.transform = `translateY(${scrolled * speed}px) rotate(${scrolled * 0.1}deg)`;
    });
});

// Interactive hover effects for feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Dynamic typing effect for hero title
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing effect when page loads
window.addEventListener('load', function() {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.innerHTML;
        typeWriter(heroTitle, originalText, 50);
    }
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all elements with fade-in class
document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Button ripple effect
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add ripple CSS dynamically
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation
function validateForm() {
    const form = document.getElementById('optimizationForm');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--error-color)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--glass-border)';
        }
    });
    
    return isValid;
}

// Real-time form validation
document.querySelectorAll('input, select, textarea').forEach(field => {
    field.addEventListener('blur', function() {
        if (this.hasAttribute('required') && !this.value.trim()) {
            this.style.borderColor = 'var(--error-color)';
        } else {
            this.style.borderColor = 'var(--glass-border)';
        }
    });
    
    field.addEventListener('input', function() {
        if (this.style.borderColor === 'rgb(239, 68, 68)') {
            this.style.borderColor = 'var(--glass-border)';
        }
    });
});

// Smooth reveal animation for query section
const querySection = document.getElementById('query');
if (querySection) {
    const queryObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.3 });
    
    queryObserver.observe(querySection);
}

// Add loading states to buttons
function addLoadingState(button, text = 'Loading...') {
    const originalContent = button.innerHTML;
    button.innerHTML = `<div class="loading"></div> ${text}`;
    button.disabled = true;
    
    return function removeLoadingState() {
        button.innerHTML = originalContent;
        button.disabled = false;
    };
}

// Mobile menu toggle (if needed)
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Add mobile menu functionality
const mobileMenuButton = document.createElement('button');
mobileMenuButton.innerHTML = '<i class="fas fa-bars"></i>';
mobileMenuButton.className = 'mobile-menu-toggle';
mobileMenuButton.style.display = 'none';
mobileMenuButton.onclick = toggleMobileMenu;

// Show mobile menu button on small screens
function checkScreenSize() {
    if (window.innerWidth <= 768) {
        mobileMenuButton.style.display = 'block';
        document.querySelector('.nav-container').appendChild(mobileMenuButton);
    } else {
        mobileMenuButton.style.display = 'none';
    }
}

window.addEventListener('resize', checkScreenSize);
checkScreenSize();

// Add smooth transitions to all interactive elements
document.querySelectorAll('a, button, .feature-card, .nav-link').forEach(element => {
    element.style.transition = 'all 0.3s ease';
});

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debounced scroll handler
const debouncedScrollHandler = debounce(function() {
    // Handle scroll events here
}, 10);

window.addEventListener('scroll', debouncedScrollHandler);
