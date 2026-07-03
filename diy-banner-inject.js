/**
 * diy-banner-inject.js — 51微店 fenghan-trade.com DIY配置器首页横幅
 * Injected via: <script src="diy-banner-inject.js"></script>
 * Version: 2026-07-02
 */
(function() {
    if (window.__fenghanDIYBannerInjected) return;
    window.__fenghanDIYBannerInjected = 1;

    // Inject CSS
    var style = document.createElement('style');
    style.textContent =
        '.diy-banner{display:block;margin:24px 0;padding:32px 24px;background:linear-gradient(135deg,#0D1F3D 0%,#1a3a6b 100%);border-radius:12px;color:#fff;text-decoration:none;position:relative;overflow:hidden}' +
        '.diy-banner::before{content:"";position:absolute;top:-50%;right:-10%;width:300px;height:300px;background:radial-gradient(circle,rgba(200,155,60,0.3) 0%,transparent 70%);border-radius:50%}' +
        '.diy-banner::after{content:"";position:absolute;bottom:-30%;left:-5%;width:200px;height:200px;background:radial-gradient(circle,rgba(198,40,40,0.15) 0%,transparent 70%);border-radius:50%}' +
        '.diy-banner:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(13,31,61,0.4);transition:all 0.3s}' +
        '.diy-banner-inner{position:relative;z-index:1;display:flex;align-items:center;gap:24px;flex-wrap:wrap}' +
        '.diy-banner-icon{width:64px;height:64px;background:rgba(200,155,60,0.2);border:2px solid #C89B3C;border-radius:16px;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:32px}' +
        '.diy-banner-text{flex:1;min-width:200px}' +
        '.diy-banner-text h2{margin:0 0 6px;font-size:22px;font-weight:700;color:#C89B3C}' +
        '.diy-banner-text p{margin:0;font-size:14px;opacity:0.85;line-height:1.5}' +
        '.diy-banner-btn{display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:linear-gradient(135deg,#C62828,#e53935);color:#fff;border-radius:8px;font-size:15px;font-weight:700;text-decoration:none;white-space:nowrap;transition:all 0.3s;flex-shrink:0}' +
        '.diy-banner-btn:hover{background:linear-gradient(135deg,#b71c1c,#d32f2f);transform:scale(1.05);box-shadow:0 4px 16px rgba(198,40,40,0.5)}' +
        '.diy-banner-btn svg{width:18px;height:18px;fill:currentColor}' +
        '@media(max-width:600px){.diy-banner{padding:20px 16px}.diy-banner-text h2{font-size:18px}.diy-banner-btn{width:100%;justify-content:center}}';

    document.head.appendChild(style);

    // Wait for DOM
    function injectBanner() {
        // Try to find the main content area / hero section on the homepage
        var target = document.querySelector('.home-hero, .hero, .banner, main, .main-content, #main, .content');
        if (!target) {
            // Fallback: find first major container
            target = document.querySelector('.container, .wrapper, .page-content, .site-content');
        }
        if (!target) {
            // Last fallback: insert after body
            target = document.body;
        }

        var banner = document.createElement('a');
        banner.className = 'diy-banner';
        banner.href = 'https://charlie555666.github.io/shacman-catalog/diy-configurator/';
        banner.target = '_blank';
        banner.rel = 'noopener';
        banner.title = 'DIY Vehicle Configurator — Build Your SHACMAN Truck';

        banner.innerHTML =
            '<div class="diy-banner-inner">' +
            '<div class="diy-banner-icon">🔧</div>' +
            '<div class="diy-banner-text">' +
            '<h2>DIY Vehicle Configurator · 在线选车</h2>' +
            '<p>Choose country → pick model → swap engine & accessories → get real-time pricing. Build your perfect SHACMAN truck in 2 minutes!</p>' +
            '</div>' +
            '<span class="diy-banner-btn">' +
            '<svg viewBox="0 0 24 24"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>' +
            ' Start Configuring' +
            '</span>' +
            '</div>';

        // Insert at top of target
        if (target === document.body) {
            target.insertBefore(banner, target.firstChild);
        } else {
            target.insertBefore(banner, target.firstChild);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectBanner);
    } else {
        injectBanner();
    }
})();
