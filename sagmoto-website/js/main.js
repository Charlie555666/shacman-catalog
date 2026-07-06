/**
 * SAGMOTO Commercial Vehicle — Main JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {

  // ============================================
  // MOBILE MENU TOGGLE
  // ============================================
  const menuToggle = document.querySelector('.menu-toggle');
  const mainNav = document.querySelector('.main-nav');
  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
      mainNav.classList.toggle('open');
      menuToggle.classList.toggle('open');
    });

    // Mobile dropdown toggle
    const navItems = mainNav.querySelectorAll('li');
    navItems.forEach(item => {
      const dropdown = item.querySelector('.dropdown');
      if (dropdown) {
        item.querySelector('a').addEventListener('click', (e) => {
          if (window.innerWidth <= 768) {
            e.preventDefault();
            item.classList.toggle('open');
          }
        });
      }
    });
  }

  // ============================================
  // BANNER SLIDER
  // ============================================
  const banner = document.querySelector('.banner');
  if (banner) {
    const slides = banner.querySelectorAll('.banner-slide');
    const dots = banner.querySelectorAll('.dots span');
    let current = 0;
    const total = slides.length;
    let interval;

    function goTo(index) {
      slides[current].classList.remove('active');
      dots[current]?.classList.remove('active');
      current = (index + total) % total;
      slides[current].classList.add('active');
      dots[current]?.classList.add('active');
    }

    function next() { goTo(current + 1); }

    dots.forEach(dot => {
      dot.addEventListener('click', () => {
        const index = parseInt(dot.dataset.index);
        goTo(index);
        resetTimer();
      });
    });

    function resetTimer() {
      clearInterval(interval);
      interval = setInterval(next, 5000);
    }

    if (total > 1) {
      resetTimer();
    }
  }

  // ============================================
  // SCROLL ANIMATION
  // ============================================
  const animatedEls = document.querySelectorAll('.animate-on-scroll');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  animatedEls.forEach(el => observer.observe(el));

  // ============================================
  // STICKY HEADER SHADOW
  // ============================================
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        header.style.boxShadow = '0 2px 16px rgba(0,0,0,0.1)';
      } else {
        header.style.boxShadow = '0 1px 4px rgba(0,0,0,0.04)';
      }
    });
  }

  // ============================================
  // PRODUCT FILTER (Products Page)
  // ============================================
  const filterBtns = document.querySelectorAll('.filter-bar .filter-btn');
  const productCards = document.querySelectorAll('.product-grid .product-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const category = btn.dataset.filter;
      productCards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // ============================================
  // SMOOTH SCROLL
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
