/**
 * hero-inject.js — 51微店 fenghan-trade.com 首页优化：中文SEO + 首屏 + DIY配置器
 * Injected via GitHub Pages: charlie555666.github.io/shacman-catalog/hero-inject.js
 * Version: 2026-07-09 (v4: fix CSS truncation + hero insertion order)
 */
(function() {
    if (window.__fenghanInjected) return;
    window.__fenghanInjected = 1;

    // Only run on homepage
    var path = window.location.pathname;
    var isHome = path === '/' || path === '/index' || path === '/index.html' || path.indexOf('/?') === 0 || path === '';
    if (!isHome) return;

    // ===== SEO META: 更新标题为中文友好 =====
    var cnTitle = '陕西风瀚贸易有限公司 — 陕汽SHACMAN/SAGMOTO重卡出口 | 自卸车 牵引车 载货车 专用车';
    if (document.title.indexOf('陕西风瀚贸易') === -1) document.title = cnTitle;

    // ===== SEO META: 更新 meta description 为中文 =====
    var metaDesc = document.querySelector('meta[name="description"]');
    var cnDesc = '陕西风瀚贸易有限公司是陕汽集团SHACMAN/SAGMOTO授权出口经销商，专业从事中国重卡出口。主营自卸车、牵引车、载货车、专用车，200+车型配置，出口50+国家，工厂直供价格，原厂质保。';
    if (metaDesc) { metaDesc.setAttribute('content', cnDesc); }
    else {
        var md = document.createElement('meta'); md.name = 'description'; md.content = cnDesc;
        document.head.appendChild(md);
    }

    // ===== SEO: 添加中文 keywords meta =====
    if (!document.querySelector('meta[name="keywords"]')) {
        var mk = document.createElement('meta'); mk.name = 'keywords';
        mk.content = '陕西风瀚贸易,重卡出口,自卸车,牵引车,载货车,专用车,SHACMAN陕汽,SAGMOTO,商用车出口,中国重卡';
        document.head.appendChild(mk);
    }

    // ===== SEO: 百度 JSON-LD 结构化数据 =====
    var ld = document.createElement('script');
    ld.type = 'application/ld+json';
    ld.textContent = JSON.stringify({
        "@context":"https://schema.org","@type":"Organization",
        "name":"陕西风瀚贸易有限公司","alternateName":"Shaanxi Fenghan Trading Co., Ltd.",
        "description":"陕汽集团SHACMAN/SAGMOTO授权出口经销商，专业从事中国重卡出口。主营自卸车、牵引车、载货车、专用车。",
        "url":"https://fenghan-trade.com","telephone":"+86-15319431311","email":"sales@fenghan-trade.com",
        "address":{"@type":"PostalAddress","addressCountry":"CN","addressRegion":"Shaanxi","addressLocality":"Xi'an","streetAddress":"Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue"},
        "makesOffer":[
            {"@type":"Offer","name":"自卸车 Dump Truck","description":"SHACMAN/SAGMOTO自卸车出口，6x4 8x4矿用工程"},
            {"@type":"Offer","name":"牵引车 Tractor Truck","description":"SHACMAN/SAGMOTO牵引车出口，长途物流"},
            {"@type":"Offer","name":"载货车 Cargo Truck","description":"SHACMAN/SAGMOTO载货车出口，城市配送物流"},
            {"@type":"Offer","name":"专用车 Special Vehicle","description":"SHACMAN/SAGMOTO专用车出口，搅拌车油罐车环卫车"}
        ],
        "sameAs":["https://www.facebook.com/profile.php?id=61591439076603","https://www.youtube.com/@FenghanTrading"]
    });
    document.head.appendChild(ld);

    // ===== Inject ALL CSS (CN SEO + Hero + Trust + Brands + DIY) =====
    var style = document.createElement('style');
    style.textContent = 
        /* === Chinese Company Intro === */
        '.cn-company-intro{background:linear-gradient(135deg,#0D1F3D 0%,#152a54 100%);padding:40px 24px 32px;text-align:center;border-bottom:3px solid #C62828}' +
        '.cn-company-intro .cn-logo-text{font-size:28px;font-weight:700;color:#fff;margin:0 0 6px;letter-spacing:2px}' +
        '.cn-company-intro .cn-en-name{font-size:13px;color:rgba(255,255,255,.65);margin:0 0 20px;font-family:Arial;text-transform:uppercase;letter-spacing:1px}' +
        '.cn-company-intro .cn-tagline{font-size:17px;color:#C89B3C;font-weight:600;margin:0 0 16px;padding:8px 24px;background:rgba(200,155,60,.12);border-radius:4px;display:inline-block}' +
        '.cn-company-intro .cn-features{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;max-width:900px;margin:0 auto}' +
        '.cn-company-intro .cn-feat-item{display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.9);font-size:14px;padding:6px 16px;background:rgba(255,255,255,.08);border-radius:6px}' +
        '.cn-company-intro .cn-feat-item strong{color:#C89B3C}' +
        '.cn-company-intro .cn-contact-strip{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;margin-top:20px;padding-top:18px;border-top:1px solid rgba(255,255,255,.12)}' +
        '.cn-company-intro .cn-contact-strip a,.cn-company-intro .cn-contact-strip span{color:rgba(255,255,255,.8);font-size:13px;text-decoration:none;padding:6px 16px;background:rgba(255,255,255,.05);border-radius:20px;transition:all .2s}' +
        '.cn-company-intro .cn-contact-strip a:hover{background:rgba(255,255,255,.15);color:#fff}' +
        /* === Chinese Business Description === */
        '.cn-business-desc{background:#fff;border-radius:16px;box-shadow:0 4px 24px rgba(0,0,0,.08);border:1px solid #eef1f5;margin:40px auto;max-width:960px;overflow:hidden}' +
        '.cn-collapse-header{padding:18px 24px;background:linear-gradient(135deg,#f8fafd,#fff);cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid transparent;transition:all .3s}' +
        '.cn-collapse-header:hover{background:linear-gradient(135deg,#f0f4f8,#fff)}' +
        '.cn-collapse-header h2{font-size:20px;color:#0D1F3D;margin:0;font-weight:700;display:flex;align-items:center;gap:10px}' +
        '.cn-collapse-arrow{width:28px;height:28px;border-radius:50%;background:#0D1F3D;color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;transition:transform .3s;flex-shrink:0}' +
        '.cn-collapse-body{padding:28px 24px;transition:max-height .4s ease,opacity .3s ease,padding .3s ease;max-height:2000px;opacity:1;overflow:hidden}' +
        '.cn-collapse-body.collapsed{max-height:0;opacity:0;padding:0 24px}' +
        '.cn-collapse-header.collapsed .cn-collapse-arrow{transform:rotate(-90deg)}' +
        '.cn-collapse-header.collapsed{border-bottom-color:#eef1f5}' +
        '.cn-business-desc .cn-desc-text{font-size:15px;color:#555;line-height:1.9;max-width:800px;margin:0 auto 24px;text-align:justify}' +
        '.cn-business-desc .cn-desc-text strong{color:#C62828}' +
        '.cn-business-desc .cn-product-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;max-width:880px;margin:0 auto}' +
        '.cn-business-desc .cn-prod-card{background:#f8f9fa;border-radius:10px;padding:22px 16px;text-align:center;border:1px solid #eee;transition:all .25s}' +
        '.cn-business-desc .cn-prod-card:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.1);border-color:#C89B3C}' +
        '.cn-business-desc .cn-prod-card .cn-prod-icon{font-size:36px;margin-bottom:10px}' +
        '.cn-business-desc .cn-prod-card .cn-prod-name{font-size:16px;font-weight:700;color:#0D1F3D;display:block;margin-bottom:6px}' +
        '.cn-business-desc .cn-prod-card .cn-prod-en{font-size:12px;color:#999}' +
        /* === Mobile responsive for CN sections === */
        '@media(max-width:640px){.cn-company-intro .cn-logo-text{font-size:22px}' +
        '.cn-company-intro .cn-tagline{font-size:14px;padding:6px 16px}' +
        '.cn-company-intro .cn-features{gap:10px}' +
        '.cn-company-intro .cn-feat-item{font-size:12px;padding:4px 12px}' +
        '.cn-business-desc .cn-product-grid{grid-template-columns:1fr 1fr;gap:10px}' +
        '.cn-business-desc .cn-prod-card{padding:14px 10px}' +
        '.cn-collapse-header h2{font-size:16px}' +
        '.cn-collapse-header{padding:14px 18px}' +
        '.cn-collapse-body{padding:18px 16px}}' +
        /* === Hero Wrap === */
        '.fenghan-hero-wrap{background:linear-gradient(135deg,#0D1F3D 0%,#1a3a6e 100%);padding:48px 24px;text-align:center;margin:0}' +
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

        // ===== SECTION A: 中文公司简介 (页面最顶部) =====
        var cnIntro = document.createElement('section');
        cnIntro.className = 'cn-company-intro';
        cnIntro.innerHTML = '<h1 class="cn-logo-text">陕西风瀚贸易有限公司</h1>' +
            '<p class="cn-en-name">Shaanxi Fenghan Trading Co., Ltd. \u2014 SHACMAN / SAGMOTO Authorized Exporter</p>' +
            '<p class="cn-tagline">\uD83C\uDDE8\uD83C\uDDF3 陕汽集团授权出口经销商 | 中国重卡出口专家</p>' +
            '<div class="cn-features">' +
            '<span class="cn-feat-item">\u2705 <strong>200+</strong> 车型配置</span>' +
            '<span class="cn-feat-item">\uD83C\uDF0D <strong>50+</strong> 出口国家</span>' +
            '<span class="cn-feat-item">\uD83D\uDE9B <strong>自卸车/牵引车/载货车/专用车</strong></span>' +
            '<span class="cn-feat-item">\uD83C\uDFED <strong>工厂直供</strong> 价格优势</span>' +
            '<span class="cn-feat-item">\uD83D\uDCB0 <strong>原厂质保</strong> 全球售后</span>' +
            '</div>' +
            '<div class="cn-contact-strip">' +
            '<span>\uD83D\uDCDE +86 153 1943 1311</span>' +
            '<a href="mailto:sales@fenghan-trade.com">\u2709 sales@fenghan-trade.com</a>' +
            '<a href="https://wa.me/8615319431311" target="_blank">\uD83D\uDCAC WhatsApp\u54A8\u8BE2</a>' +
            '<span>\uD83D\uDCCD \u4E2D\u56FD\xB7\u897F\u5B89\u6D60\u705E\u81EA\u8D38\u4E2D\u5FC3</span>' +
            '</div>';

        var fc = art.firstElementChild;
        if (fc) art.insertBefore(cnIntro, fc);
        else art.appendChild(cnIntro);

        // ===== SECTION B: 中文业务描述 + 产品分类 (折叠卡片) =====
        var bizDesc = document.createElement('section');
        bizDesc.className = 'cn-business-desc';
        bizDesc.innerHTML = '<div class="cn-collapse-header" role="button" aria-expanded="true" tabindex="0">' +
            '<h2>\uD83D\uDD0D \u4E3B\u8425\u4EA7\u54C1 \u2014 \u4E2D\u56FD\u91CD\u5361\u51FA\u53E3\u5168\u54C1\u7C7B\u8986\u76D6</h2>' +
            '<span class="cn-collapse-arrow">\u25BC</span>' +
            '</div>' +
            '<div class="cn-collapse-body">' +
            '<p class="cn-desc-text">' +
            '<strong>\u9655\u897F\u98CE\u7FF0\u8D38\u6613\u6709\u9650\u516C\u53F8</strong>\u662F<strong>\u9655\u6C7D\u96C6\u56E2SHACMAN/SAGMOTO\u54C1\u724C</strong>\u6B63\u5F0F\u6388\u6743\u7684\u51FA\u53E3\u7ECF\u9500\u5546\uFF0C' +
            '\u603B\u90E8\u4F4D\u4E8E\u4E2D\u56FD\u9655\u897F\u7701\u897F\u5B89\u5E02\uFF0C\u4E13\u4E1A\u4ECE\u4E8B\u91CD\u578B\u5361\u8F66\u53CA\u5546\u7528\u8F66\u8F86\u7684\u8FDB\u51FA\u53E3\u8D38\u6613\u3002' +
            '\u516C\u53F8\u4F9D\u6258\u9655\u6C7D\u96C6\u56E2\u5F3A\u5927\u7684\u751F\u4EA7\u5236\u9020\u80FD\u529B\u548C\u5B8C\u5584\u7684\u4F9B\u5E94\u94FE\u4F53\u7CFB\uFF0C' +
            '\u5411\u5168\u7403\u5BA2\u6237\u63D0\u4F9B<strong>\u81EA\u5378\u8F66\u3001\u7275\u5F15\u8F66\u3001\u8F7D\u8D27\u8F66\u3001\u4E13\u7528\u8F66</strong>\u7B49\u5168\u7CFB\u5217\u5546\u7528\u8F66\u4EA7\u54C1\u3002' +
            '\u4E3B\u8981\u51FA\u53E3\u5E02\u573A\u8986\u76D6<strong>\u975E\u6D32\u3001\u4E2D\u4E1C\u3001\u4E1C\u5357\u4E9A\u3001\u4E2D\u4E9A\u3001\u72EC\u8054\u4F53\u3001\u4E2D\u5357\u7F8E\u6D32</strong>\u7B49\u533A\u57DF\uFF0C' +
            '\u670D\u52A1\u8D85\u8FC750\u4E2A\u56FD\u5BB6\u548C\u5730\u533A\u7684\u5BA2\u6237\uFF0C\u63D0\u4F9B<strong>\u5DE5\u5382\u76F4\u4F9B\u4EF7\u683C\u3001\u539F\u5382\u6574\u8F66\u8D28\u4FDD\u3001\u5168\u7403\u914D\u4EF6\u4F9B\u5E94</strong>' +
            '\u548C\u4E13\u4E1A\u552E\u540E\u670D\u52A1\uFF0C\u81F4\u529B\u4E8E\u6210\u4E3A\u4E2D\u56FD\u91CD\u5361\u51FA\u53E3\u9886\u57DF\u7684\u9886\u5148\u4F01\u4E1A\u3002' +
            '</p>' +
            '<div class="cn-product-grid">' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">\uD83D\uDE9B</span><span class="cn-prod-name">\u81EA\u5378\u8F66</span><span class="cn-prod-en">Dump Truck</span></div>' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">\uD83D\uDE9A</span><span class="cn-prod-name">\u7275\u5F15\u8F66</span><span class="cn-prod-en">Tractor Truck</span></div>' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">\uD83D\uDE99</span><span class="cn-prod-name">\u8F7D\u8D27\u8F66</span><span class="cn-prod-en">Cargo Truck</span></div>' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">\uD83D\uDEE1</span><span class="cn-prod-name">\u4E13\u7528\u8F66</span><span class="cn-prod-en">Special Vehicle</span></div>' +
            '</div>' +
            '</div>';

        // 折叠交互
        var header = bizDesc.querySelector('.cn-collapse-header');
        var body = bizDesc.querySelector('.cn-collapse-body');
        var arrow = bizDesc.querySelector('.cn-collapse-arrow');
        function toggleCollapse() {
            var isCollapsed = body.classList.toggle('collapsed');
            header.classList.toggle('collapsed', isCollapsed);
            header.setAttribute('aria-expanded', !isCollapsed);
            arrow.textContent = isCollapsed ? '\u25B6' : '\u25BC';
        }
        header.addEventListener('click', toggleCollapse);
        header.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleCollapse(); }
        });

        if (cnIntro.nextSibling) art.insertBefore(bizDesc, cnIntro.nextSibling);
        else art.appendChild(bizDesc);

        // ===== SECTION C: Hero wrap (原有英文Hero) =====
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
            // Insert hero after cnIntro, not before the first child (which is now cnIntro)
            var heroRef = cnIntro.nextSibling;
            if (heroRef) art.insertBefore(hero, heroRef);
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
