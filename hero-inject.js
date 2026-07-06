/**
 * hero-inject.js — 51微店 fenghan-trade.com 首页首屏优化 + 导航栏DIY配置器入口
 * Injected via 统计代码 as: <script src="hero-inject.js"></script>
 * Version: 2026-07-03
 */
(function() {
    if (window.__fenghanInjected) return;
    window.__fenghanInjected = 1;

    // Only run on homepage
    var path = window.location.pathname;
    var isHome = path === '/' || path === '/index' || path === '/index.html' || path.indexOf('/?') === 0 || path === '';
    if (!isHome) return;

    // Inject CSS
    var style = document.createElement('style');
    style.textContent = '.fenghan-hero-wrap{background:linear-gradient(135deg,#0D1F3D 0%,#1a3a6e 100%);padding:48px 24px;text-align:center;margin:0}' +
        '.fenghan-hero-wrap .hero-title{font-size:30px;font-weight:700;color:#fff;margin:0 0 12px;font-family:Calibri,Arial,sans-serif;line-height:1.3}' +
        '.fenghan-hero-wrap .hero-subtitle{font-size:15px;color:rgba(255,255,255,.85);margin:0 0 28px;display:flex;flex-wrap:wrap;justify-content:center;gap:12px}' +
        '.fenghan-hero-wrap .hero-subtitle span{background:rgba(255,255,255,.12);padding:6px 14px;border-radius:4px;font-size:13px;white-space:nowrap}' +
        '.fenghan-hero-wrap .hero-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}' +
        '.fenghan-hero-wrap .hero-btns a{padding:14px 36px;border-radius:6px;font-size:16px;font-weight:600;text-decoration:none;transition:all .3s;display:inline-block;cursor:pointer}' +
        '.fenghan-hero-wrap .btn-quote{background:#C62828;color:#fff;border:2px solid #C62828}' +
        '.fenghan-hero-wrap .btn-quote:hover{background:#b71c1c;transform:translateY(-2px);box-shadow:0 4px 16px rgba(198,40,40,.4)}' +
        '.fenghan-hero-wrap .btn-catalog{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.5)}' +
        '.fenghan-hero-wrap .btn-catalog:hover{border-color:#fff;transform:translateY(-2px);box-shadow:0 4px 16px rgba(255,255,255,.2)}' +
        '.fenghan-trust{display:flex;flex-wrap:wrap;justify-content:center;gap:32px;padding:48px 24px;background:#fff;border-bottom:1px solid #eee}' +
        '.fenghan-trust .stat-item{text-align:center;min-width:130px}' +
        '.fenghan-trust .stat-num{font-size:34px;font-weight:700;color:#C62828;display:block;line-height:1.1}' +
        '.fenghan-trust .stat-label{font-size:13px;color:#555;margin-top:4px;display:block}' +
        '.fenghan-brands{padding:40px 24px;text-align:center;background:#f8f9fa}' +
        '.fenghan-brands .brands-title{font-size:14px;color:#0D1F3D;font-weight:700;margin-bottom:20px;letter-spacing:2px;text-transform:uppercase}' +
        '.fenghan-brands .brands-row{display:flex;justify-content:center;align-items:center;gap:36px;flex-wrap:wrap}' +
        '.fenghan-brands .brand-name{font-size:17px;font-weight:700;color:#333;letter-spacing:1px;padding:12px 24px;background:#fff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.06)}' +
        '@media(max-width:768px){.fenghan-hero-wrap .hero-title{font-size:22px}' +
        '.fenghan-hero-wrap .hero-subtitle{gap:8px}.fenghan-hero-wrap .hero-btns{flex-direction:column;align-items:center}' +
        '.fenghan-hero-wrap .hero-btns a{width:100%;max-width:280px;text-align:center}' +
        '.fenghan-trust{gap:16px;padding:28px 12px}.fenghan-trust .stat-num{font-size:26px}.fenghan-brands .brands-row{gap:16px}}' +
        // DIY Configurator Banner Styles
        '.diy-config-banner{background:linear-gradient(90deg,#C89B3C 0%,#e0b050 50%,#C89B3C 100%);padding:10px 16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.15);z-index:100;position:relative}' +
        '.diy-config-btn{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:#0D1F3D;font-weight:700;font-size:16px;padding:10px 28px;border-radius:30px;background:rgba(255,255,255,.92);border:2px solid #fff;transition:all .25s;box-shadow:0 2px 8px rgba(0,0,0,.1)}' +
        '.diy-config-btn:hover{background:#fff;transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.2);color:#0D1F3D}' +
        '.diy-config-btn .diy-icon{font-size:24px;line-height:1;filter:drop-shadow(0 1px 1px rgba(0,0,0,.1))}' +
        '.diy-config-btn .diy-text{font-size:16px;letter-spacing:.3px}' +
        '.diy-config-btn .diy-sub{font-size:11px;font-weight:400;color:#555;opacity:.9;border-left:1px solid rgba(0,0,0,.15);padding-left:10px;margin-left:2px;white-space:nowrap}' +
        '@media(max-width:640px){.diy-config-btn{padding:8px 18px;gap:6px}.diy-config-btn .diy-icon{font-size:20px}.diy-config-btn .diy-text{font-size:14px}.diy-config-btn .diy-sub{display:none}.diy-config-banner{padding:8px 12px}}';
    document.head.appendChild(style);

    // Inject HTML sections
    function init() {
        var art = document.querySelector('article') || document.querySelector('main') || document.body;

        // 1. Hero section - insert after carousel/slider
        var carousel = art.querySelector('[class*=carousel],[class*=slider],[class*=banner],[class*=swiper],[class*=hero]');
        var hero = document.createElement('div');
        hero.className = 'fenghan-hero-wrap';
        hero.innerHTML = '<h1 class="hero-title">Official SHACMAN/SAGMOTO Heavy Truck Exporter</h1>' +
            '<div class="hero-subtitle">' +
            '<span>200+ Configurations</span>' +
            '<span>50+ Countries</span>' +
            '<span>Factory-Direct Pricing</span>' +
            '<span>LHD &amp; RHD</span>' +
            '</div>' +
            '<div class="hero-btns">' +
            '<a href="/pages/contactus" class="btn-quote">Get a Quote Now</a>' +
            '<a href="https://charlie555666.github.io/shacman-catalog/" class="btn-catalog" target="_blank">Browse Product Catalog</a>' +
            '</div>';

        if (carousel && carousel.parentNode) {
            carousel.parentNode.insertBefore(hero, carousel.nextSibling);
        } else {
            var fc = art.firstElementChild;
            if (fc) art.insertBefore(hero, fc);
            else art.appendChild(hero);
        }

        // 2. Trust stats section - insert before "COMPANY" heading
        var trust = document.createElement('div');
        trust.className = 'fenghan-trust';
        trust.innerHTML = '<div class="stat-item"><span class="stat-num">200+</span><span class="stat-label">Configurations</span></div>' +
            '<div class="stat-item"><span class="stat-num">50+</span><span class="stat-label">Countries Served</span></div>' +
            '<div class="stat-item"><span class="stat-num">100%</span><span class="stat-label">Factory Warranty</span></div>' +
            '<div class="stat-item"><span class="stat-num">24/7</span><span class="stat-label">After-Sales</span></div>';

        var h2s = art.querySelectorAll('h2');
        var inserted = false;
        for (var i = 0; i < h2s.length; i++) {
            if (h2s[i].textContent.toUpperCase().indexOf('COMPANY') > -1) {
                var container = h2s[i].closest('div,section');
                if (container && container.parentNode) {
                    container.parentNode.insertBefore(trust, container.nextSibling);
                    inserted = true;
                    break;
                }
            }
        }
        if (!inserted) {
            var sc = art.children;
            if (sc.length >= 2) art.insertBefore(trust, sc[2]);
            else art.appendChild(trust);
        }

        // 3. DIY Configurator Banner — placed below the nav bar, independent from nav links
        var navEl = document.querySelector('nav,[class*=nav],[class*=navbar],[class*=menu]');
        var headerEl = document.querySelector('header') || document.querySelector('[class*=header]') || navEl;
        var diyBanner = document.createElement('div');
        diyBanner.className = 'diy-config-banner';
        diyBanner.innerHTML = '<a href="https://charlie555666.github.io/shacman-catalog/diy-configurator/" class="diy-config-btn" target="_blank" rel="noopener" title="DIY Vehicle Configurator — Build Your SHACMAN Truck">' +
            '<span class="diy-icon">\u2699\uFE0F</span>' +
            '<span class="diy-text">DIY Configurator</span>' +
            '<span class="diy-sub">Build your truck online</span>' +
            '</a>';
        if (headerEl) {
            headerEl.insertAdjacentElement('afterend', diyBanner);
        } else if (art) {
            art.insertBefore(diyBanner, art.firstElementChild);
        }

        // 4. Brand section - insert before footer
        var brands = document.createElement('div');
        brands.className = 'fenghan-brands';
        brands.innerHTML = '<div class="brands-title">We Represent</div>' +
            '<div class="brands-row">' +
            '<span class="brand-name">SHACMAN</span>' +
            '<span class="brand-name">SAGMOTO</span>' +
            '<span class="brand-name">WEICHAI</span>' +
            '<span class="brand-name">FAST GEAR</span>' +
            '<span class="brand-name">HANDE AXLE</span>' +
            '</div>';

        var ft = art.querySelector('footer,[class*=footer]');
        if (ft) art.insertBefore(brands, ft);
        else art.appendChild(brands);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
