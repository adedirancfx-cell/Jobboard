// ============ JOBBOARD MAIN JAVASCRIPT ============

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');
    
    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileNav.classList.toggle('hidden');
            const icon = mobileMenuBtn.querySelector('i');
            if (icon) {
                if (!mobileNav.classList.contains('hidden')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
    
    // Close mobile menu when clicking a link
    document.querySelectorAll('#mobileNav a').forEach(link => {
        link.addEventListener('click', () => {
            if (mobileNav) {
                mobileNav.classList.add('hidden');
                const icon = mobileMenuBtn?.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    });
    
    // Auto-hide messages after 4 seconds
    const messages = document.querySelectorAll('.fixed.top-20.right-4 > div');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });
    
    // Navbar scroll effect
    const navbar = document.querySelector('nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-black/80');
                navbar.classList.remove('bg-black/50');
            } else {
                navbar.classList.add('bg-black/50');
                navbar.classList.remove('bg-black/80');
            }
        });
    }
    
    // Counter animation for stats
    const counters = document.querySelectorAll('.counter');
    if (counters.length) {
        const observerCounter = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const updateCount = () => {
                        const target = parseInt(counter.getAttribute('data-target'));
                        const current = parseInt(counter.innerText);
                        const increment = Math.ceil(target / 50);
                        if (current < target) {
                            counter.innerText = Math.min(current + increment, target);
                            setTimeout(updateCount, 30);
                        }
                    };
                    updateCount();
                    observerCounter.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });
        counters.forEach(counter => observerCounter.observe(counter));
    }
    
    // Scroll reveal animation for cards
    const cards = document.querySelectorAll('.feature-card, .testimonial-card, .stat-card, .category-card, .career-card');
    if (cards.length) {
        const observerOptions = { threshold: 0.2, rootMargin: '0px 0px -50px 0px' };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    const delay = index * 150;
                    setTimeout(() => {
                        entry.target.classList.remove('opacity-0', 'translate-y-8', 'translate-y-12');
                        entry.target.classList.add('opacity-100', 'translate-y-0');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        cards.forEach(card => observer.observe(card));
    }
    
    // Scroll to section function
    window.scrollToSection = function(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };
    
    // Character counter for cover letter
    const coverLetter = document.querySelector('textarea[name="cover_letter"]');
    if (coverLetter) {
        coverLetter.addEventListener('input', function() {
            const remaining = 1000 - this.value.length;
            const counter = document.getElementById('char-counter');
            if (counter) {
                counter.textContent = `${remaining} characters remaining`;
                if (remaining < 0) {
                    counter.classList.add('text-red-400');
                } else {
                    counter.classList.remove('text-red-400');
                }
            }
        });
    }
    
    // Update application status (employers)
    window.updateStatus = function(applicationId, status) {
        fetch(`/update-status/${applicationId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `status=${status}`,
        })
        .then(response => {
            if (response.ok) {
                showToast('Application status updated!', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        })
        .catch(error => console.error('Error:', error));
    };
    
    // Show toast notification
    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `fixed top-20 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transition-all duration-300 ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'error' ? 'bg-red-500 text-white' : 'bg-blue-500 text-white'
        }`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    // Get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    console.log('JobBoard JavaScript loaded successfully!');
});


// desk profilr drop down
 
        // ========== DESKTOP PROFILE DROPDOWN ==========
const profileBtn = document.getElementById('profileBtn');
const profileDropdown = document.getElementById('profileDropdown');

if (profileBtn && profileDropdown) {
    profileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (profileDropdown.classList.contains('opacity-0')) {
            profileDropdown.classList.remove('opacity-0', 'invisible');
            profileDropdown.classList.add('opacity-100', 'visible');
        } else {
            profileDropdown.classList.add('opacity-0', 'invisible');
            profileDropdown.classList.remove('opacity-100', 'visible');
        }
    });
}

// Close desktop dropdown when clicking outside
document.addEventListener('click', function(event) {
    if (profileDropdown && !profileDropdown.classList.contains('opacity-0')) {
        if (!profileBtn?.contains(event.target) && !profileDropdown.contains(event.target)) {
            profileDropdown.classList.add('opacity-0', 'invisible');
            profileDropdown.classList.remove('opacity-100', 'visible');
        }
    }
});

// ========== MOBILE PROFILE SUBMENU ==========
const mobileProfileBtn = document.getElementById('mobileProfileBtn');
const mobileSubmenu = document.getElementById('mobileSubmenu');
const mobileDropdownIcon = document.getElementById('mobileDropdownIcon');

if (mobileProfileBtn && mobileSubmenu) {
    mobileProfileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (mobileSubmenu.classList.contains('hidden')) {
            mobileSubmenu.classList.remove('hidden');
            if (mobileDropdownIcon) {
                mobileDropdownIcon.style.transform = 'rotate(180deg)';
            }
        } else {
            mobileSubmenu.classList.add('hidden');
            if (mobileDropdownIcon) {
                mobileDropdownIcon.style.transform = 'rotate(0deg)';
            }
        }
    });
}

// ========== MOBILE MAIN MENU TOGGLE ==========
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuIcon = document.getElementById('mobileMenuIcon');

if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', function() {
        if (mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.remove('hidden');
            mobileMenuIcon.classList.remove('fa-bars');
            mobileMenuIcon.classList.add('fa-times');
        } else {
            mobileMenu.classList.add('hidden');
            mobileMenuIcon.classList.remove('fa-times');
            mobileMenuIcon.classList.add('fa-bars');
            // Also close the submenu when main menu closes
            if (mobileSubmenu && !mobileSubmenu.classList.contains('hidden')) {
                mobileSubmenu.classList.add('hidden');
                if (mobileDropdownIcon) {
                    mobileDropdownIcon.style.transform = 'rotate(0deg)';
                }
            }
        }
    });
}

// Close mobile menu when clicking a link
document.querySelectorAll('#mobileMenu a').forEach(link => {
    link.addEventListener('click', () => {
        if (mobileMenu) {
            mobileMenu.classList.add('hidden');
            if (mobileMenuIcon) {
                mobileMenuIcon.classList.remove('fa-times');
                mobileMenuIcon.classList.add('fa-bars');
            }
        }
    });
});

// Close menus when clicking outside
document.addEventListener('click', function(event) {
    // Close mobile main menu
    if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
        if (!mobileMenuBtn?.contains(event.target) && !mobileMenu.contains(event.target)) {
            mobileMenu.classList.add('hidden');
            if (mobileMenuIcon) {
                mobileMenuIcon.classList.remove('fa-times');
                mobileMenuIcon.classList.add('fa-bars');
            }
            // Close mobile submenu as well
            if (mobileSubmenu && !mobileSubmenu.classList.contains('hidden')) {
                mobileSubmenu.classList.add('hidden');
                if (mobileDropdownIcon) {
                    mobileDropdownIcon.style.transform = 'rotate(0deg)';
                }
            }
        }
    }
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('bg-black/80');
            navbar.classList.remove('bg-black/50');
        } else {
            navbar.classList.add('bg-black/50');
            navbar.classList.remove('bg-black/80');
        }
    }
});

// Auto-hide messages after 4 seconds
setTimeout(() => {
    const messages = document.querySelectorAll('.fixed.top-20.right-4 > div');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });
}, 1000);