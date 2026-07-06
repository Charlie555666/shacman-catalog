/**
 * SAGMOTO Website - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {

    // ===== Banner Swiper (全屏轮播) =====
    if (document.querySelector('.hero-slider.swiper-container')) {
        new Swiper('.hero-slider.swiper-container', {
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            speed: 800,
            autoHeight: false,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            effect: 'fade',
            fadeEffect: {
                crossFade: true,
            },
            on: {
                init: function() {
                    // 强制设置全屏高度
                    var container = this.el;
                    container.style.height = '100vh';
                    var wrapper = container.querySelector('.swiper-wrapper');
                    if (wrapper) wrapper.style.height = '100vh';
                    var slides = container.querySelectorAll('.swiper-slide');
                    slides.forEach(function(s) { s.style.height = '100vh'; });
                },
            },
        });
    }

    // ===== Header Shrink on Scroll =====
    var header = document.querySelector('.e_container-2');
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                header.classList.add('shrink');
            } else {
                header.classList.remove('shrink');
            }
        });
    }

    // ===== Mobile Menu Toggle =====
    var mobileToggle = document.querySelector('.mobile-toggle');
    var mainNav = document.querySelector('.main-nav');

    if (mobileToggle && mainNav) {
        mobileToggle.addEventListener('click', function() {
            mobileToggle.classList.toggle('active');
            mainNav.classList.toggle('mobile-open');
            document.body.style.overflow = mainNav.classList.contains('mobile-open') ? 'hidden' : '';
        });

        // Close mobile menu when clicking a nav link
        var navLinks = mainNav.querySelectorAll('a');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                mobileToggle.classList.remove('active');
                mainNav.classList.remove('mobile-open');
                document.body.style.overflow = '';
            });
        });

        // Mobile dropdown toggle for ALL has-dropdown items
        var dropdownItems = mainNav.querySelectorAll('.has-dropdown');
        dropdownItems.forEach(function(item) {
            item.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    // Only prevent default if clicking the parent link, not a child
                    if (e.target.closest('.dropdown-menu a') || e.target.closest('.mega-inner a')) return;
                    e.preventDefault();
                    this.classList.toggle('mobile-sub-open');
                }
            });
        });
    }

    // ===== Tab Switching =====
    var tabBtns = document.querySelectorAll('.tab-btn');
    var tabPanels = document.querySelectorAll('.tab-panel');

    tabBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var target = this.getAttribute('data-tab');

            // Update active button
            tabBtns.forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');

            // Show target panel
            tabPanels.forEach(function(panel) {
                panel.classList.remove('active');
                if (panel.getAttribute('data-panel') === target) {
                    panel.classList.add('active');
                }
            });
        });
    });

    // ===== Recommended Model Tab Switching (.tab-item / .tab-content) =====
    var tabItems = document.querySelectorAll('.tab-item[data-tab]');
    var tabContents = document.querySelectorAll('.tab-content[id]');

    tabItems.forEach(function(item) {
        item.addEventListener('click', function() {
            var targetId = this.getAttribute('data-tab');

            // Update active tab
            tabItems.forEach(function(t) { t.classList.remove('active'); });
            this.classList.add('active');

            // Show target content
            tabContents.forEach(function(content) {
                content.classList.remove('active');
                if (content.getAttribute('id') === targetId) {
                    content.classList.add('active');
                }
            });
        });
    });

    // ===== Filter Tabs (Products Page) =====
    var filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            var filter = this.getAttribute('data-filter');

            filterTabs.forEach(function(t) { t.classList.remove('active'); });
            this.classList.add('active');

            var items = document.querySelectorAll('.filter-item');
            items.forEach(function(item) {
                if (filter === 'all' || item.getAttribute('data-category') === filter) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });

            // Animate visible cards
            setTimeout(function() {
                var visible = document.querySelectorAll('.filter-item[style*="block"], .filter-item:not([style*="none"])');
                visible.forEach(function(v, i) {
                    v.style.animation = 'fadeInUp 0.3s ease forwards';
                    v.style.animationDelay = (i * 0.05) + 's';
                });
            }, 50);
        });
    });

    // ===== Smooth Scroll for Anchor Links =====
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var targetId = this.getAttribute('href');
            if (targetId === '#') return;

            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                var headerHeight = header ? header.offsetHeight : 0;
                var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight - 20;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===== Contact Form Submit =====
    var contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            var name = this.querySelector('[name="name"]');
            var email = this.querySelector('[name="email"]');
            var phone = this.querySelector('[name="phone"]');
            var message = this.querySelector('[name="message"]');

            // Simple validation
            var valid = true;
            [name, email, message].forEach(function(field) {
                if (field && !field.value.trim()) {
                    field.style.borderColor = '#c41230';
                    valid = false;
                } else if (field) {
                    field.style.borderColor = '#e5e5e5';
                }
            });

            if (email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
                email.style.borderColor = '#c41230';
                valid = false;
            }

            if (!valid) {
                alert('Please fill in all required fields correctly.');
                return;
            }

            // Show success
            var btn = this.querySelector('.btn-submit');
            var originalText = btn.textContent;
            btn.textContent = 'Sending...';
            btn.disabled = true;

            setTimeout(function() {
                btn.textContent = 'Message Sent!';
                btn.style.background = '#28a745';
                contactForm.reset();

                setTimeout(function() {
                    btn.textContent = originalText;
                    btn.style.background = '#c41230';
                    btn.disabled = false;
                }, 2000);
            }, 1000);
        });
    }

    // ===== Scroll Reveal Animation =====
    var revealElements = document.querySelectorAll('.product-card, .recommend-card, .news-card, .stat-item, .video-card, .product-grid-item');

    function checkReveal() {
        revealElements.forEach(function(el, index) {
            var rect = el.getBoundingClientRect();
            var windowHeight = window.innerHeight;

            if (rect.top < windowHeight - 50) {
                setTimeout(function() {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, index * 50);
            }
        });
    }

    // Initial state
    revealElements.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });

    // Check on load and scroll
    checkReveal();
    window.addEventListener('scroll', checkReveal);

    // ===== Active Navigation Highlight =====
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';

    var navLinksAll = document.querySelectorAll('.main-nav a');
    navLinksAll.forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href === currentPage) {
            link.classList.add('active');
        } else if (currentPage === 'index.html' && href && href.includes('#')) {
            // Don't mark as active on index
        }
    });

    // ===== Language Selector =====
    var langLinks = document.querySelectorAll('.lang-selector a');
    langLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            langLinks.forEach(function(l) { l.classList.remove('active'); });
            this.classList.add('active');
        });
    });

});

// Add keyframe animation if not in CSS
var styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(styleSheet);
