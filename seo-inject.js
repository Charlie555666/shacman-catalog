/**
 * seo-inject.js — 51微店 fenghan-trade.com 首页中文SEO优化
 * 在页面顶部注入中文公司简介 + JSON-LD结构化数据，提升百度搜索排名
 * Injected via footer copyright TinyMCE or GitHub Pages
 * Version: 2026-07-08
 */
(function() {
    if (window.__fenghanSeoInjected) return;
    window.__fenghanSeoInjected = 1;

    // Update document title to be more Chinese-friendly
    var cnTitle = '陕西风瀚贸易有限公司 — 陕汽SHACMAN/SAGMOTO重卡出口 | 自卸车 牵引车 载货车 专用车工厂直供';
    if (document.title.indexOf('陕西风瀚贸易') === -1) {
        document.title = cnTitle;
    }

    // Update meta description with Chinese
    var metaDesc = document.querySelector('meta[name="description"]');
    var cnDesc = '陕西风瀚贸易有限公司是陕汽集团SHACMAN/SAGMOTO品牌授权出口经销商，专业从事中国重卡出口业务。主营自卸车、牵引车、载货车、专用车等商用车辆，200+配置，出口非洲、中东、东南亚、独联体等50+国家和地区。工厂直供价格，原厂质保，全球售后服务。';
    if (metaDesc) {
        metaDesc.setAttribute('content', cnDesc);
    } else {
        var meta = document.createElement('meta');
        meta.name = 'description';
        meta.content = cnDesc;
        document.head.appendChild(meta);
    }

    // Add keywords meta
    if (!document.querySelector('meta[name="keywords"]')) {
        var kw = document.createElement('meta');
        kw.name = 'keywords';
        kw.content = '陕西风瀚贸易,重卡出口,自卸车出口,牵引车出口,载货车出口,专用车,SHACMAN陕汽,SAGMOTO,商用车出口,中国重卡,工厂直供价格';
        document.head.appendChild(kw);
    }

    // Inject CSS for the Chinese company intro section
    var style = document.createElement('style');
    style.textContent = 
        /* 中文公司简介区域 */
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
        /* 中文业务描述区 */
        '.cn-business-desc{background:#fff;padding:36px 24px;max-width:960px;margin:0 auto;text-align:center}' +
        '.cn-business-desc h2{font-size:22px;color:#0D1F3D;margin:0 0 20px;font-weight:700}' +
        '.cn-business-desc .cn-desc-text{font-size:15px;color:#555;line-height:1.9;max-width:800px;margin:0 auto 28px;text-align:justify}' +
        '.cn-business-desc .cn-desc-text strong{color:#C62828}' +
        '.cn-business-desc .cn-product-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;max-width:880px;margin:0 auto}' +
        '.cn-business-desc .cn-prod-card{background:#f8f9fa;border-radius:10px;padding:22px 16px;text-align:center;border:1px solid #eee;transition:all .25s}' +
        '.cn-business-desc .cn-prod-card:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.1);border-color:#C89B3C}' +
        '.cn-business-desc .cn-prod-card .cn-prod-icon{font-size:36px;margin-bottom:10px}' +
        '.cn-business-desc .cn-prod-card .cn-prod-name{font-size:16px;font-weight:700;color:#0D1F3D;display:block;margin-bottom:6px}' +
        '.cn-business-desc .cn-prod-card .cn-prod-en{font-size:12px;color:#999}' +
        '@media(max-width:640px){.cn-company-intro .cn-logo-text{font-size:22px}' +
        '.cn-company-intro .cn-tagline{font-size:14px;padding:6px 16px}' +
        '.cn-company-intro .cn-features{gap:10px}' +
        '.cn-company-intro .cn-feat-item{font-size:12px;padding:4px 12px}' +
        '.cn-business-desc .cn-product-grid{grid-template-columns:1fr 1fr;gap:10px}' +
        '.cn-business-desc .cn-prod-card{padding:14px 10px}}';
    document.head.appendChild(style);

    // Wait for DOM ready
    function init() {
        var body = document.body;
        var art = document.querySelector('article') || document.querySelector('main') || body;

        // ===== SECTION 1: 中文公司简介 (inserted at the very top) =====
        var cnIntro = document.createElement('section');
        cnIntro.className = 'cn-company-intro';
        cnIntro.innerHTML = 
            '<h1 class="cn-logo-text">陕西风瀚贸易有限公司</h1>' +
            '<p class="cn-en-name">Shaanxi Fenghan Trading Co., Ltd. — SHACMAN / SAGMOTO Authorized Exporter</p>' +
            '<p class="cn-tagline">&#127464;&#127475; 陕汽集团授权出口经销商 | 中国重卡出口专家</p>' +
            '<div class="cn-features">' +
            '<span class="cn-feat-item">&#9989; <strong>200+</strong> 车型配置</span>' +
            '<span class="cn-feat-item">&#127758; <strong>50+</strong> 出口国家</span>' +
            '<span class="cn-feat-item">&#128666; <strong>自卸车/牵引车/载货车/专用车</strong></span>' +
            '<span class="cn-feat-item">&#127976; <strong>工厂直供</strong> 价格优势</span>' +
            '<span class="cn-feat-item">&#128179; <strong>原厂质保</strong> 全球售后</span>' +
            '</div>' +
            '<div class="cn-contact-strip">' +
            '<span>&#128222; +86 153 1943 1311</span>' +
            '<a href="mailto:sales@fenghan-trade.com">&#9993; sales@fenghan-trade.com</a>' +
            '<a href="https://wa.me/8615319431311" target="_blank">&#128172; WhatsApp咨询</a>' +
            '<span>&#128205; 中国·西安浐灞自贸中心</span>' +
            '</div>';

        // Insert at the VERY TOP of the page content
        var firstChild = art.firstElementChild;
        if (firstChild) {
            art.insertBefore(cnIntro, firstChild);
        } else {
            art.appendChild(cnIntro);
        }

        // ===== SECTION 2: 中文业务描述 + 产品分类 =====
        var bizDesc = document.createElement('section');
        bizDesc.className = 'cn-business-desc';
        bizDesc.innerHTML = 
            '<h2>&#128270; 主营产品 — 中国重卡出口全品类覆盖</h2>' +
            '<p class="cn-desc-text">' +
            '<strong>陕西风瀚贸易有限公司</strong>是<strong>陕汽集团SHACMAN/SAGMOTO品牌</strong>正式授权的出口经销商，' +
            '总部位于中国陕西省西安市，专业从事重型卡车及商用车辆的进出口贸易。' +
            '公司依托陕汽集团强大的生产制造能力和完善的供应链体系，向全球客户提供' +
            '<strong>自卸车（Dump Truck）、牵引车（Tractor Truck）、载货车（Cargo Truck）、' +
            '专用车（Special Vehicle）</strong>等全系列商用车产品。' +
            '主要出口市场覆盖<strong>非洲、中东、东南亚、中亚、独联体、中南美洲</strong>等区域，' +
            '服务超过50个国家和地区的客户，提供<strong>工厂直供价格、原厂整车质保、' +
            '全球配件供应和专业售后服务</strong>，致力于成为中国重卡出口领域的领先企业。' +
            '</p>' +
            '<div class="cn-product-grid">' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">&#128666;</span><span class="cn-prod-name">自卸车</span><span class="cn-prod-en">Dump Truck</span></div>' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">&#128667;</span><span class="cn-prod-name">牵引车</span><span class="cn-prod-en">Tractor Truck</span></div>' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">&#128665;</span><span class="cn-prod-name">载货车</span><span class="cn-prod-en">Cargo Truck</span></div>' +
            '<div class="cn-prod-card"><span class="cn-prod-icon">&#128737;</span><span class="cn-prod-name">专用车</span><span class="cn-prod-en">Special Vehicle</span></div>' +
            '</div>';

        // Insert after the Chinese intro
        var nextAfterIntro = cnIntro.nextSibling;
        if (nextAfterIntro) {
            art.insertBefore(bizDesc, nextAfterIntro);
        } else {
            art.appendChild(bizDesc);
        }

        // ===== SECTION 3: Baidu-friendly JSON-LD =====
        var ld = document.createElement('script');
        ld.type = 'application/ld+json';
        ld.textContent = JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "陕西风瀚贸易有限公司",
            "alternateName": "Shaanxi Fenghan Trading Co., Ltd.",
            "description": "陕汽集团SHACMAN/SAGMOTO品牌授权出口经销商，专业从事中国重卡出口。主营自卸车、牵引车、载货车、专用车，出口50+国家。",
            "url": "https://fenghan-trade.com",
            "telephone": "+86-15319431311",
            "email": "sales@fenghan-trade.com",
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "CN",
                "addressRegion": "Shaanxi",
                "addressLocality": "Xi'an",
                "streetAddress": "Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue, Chanba Ecological District"
            },
            "makesOffer": [
                {
                    "@type": "Offer",
                    "name": "自卸车",
                    "alternateName": "Dump Truck",
                    "description": "SHACMAN/SAGMOTO 自卸车出口，6x4 8x4 驱动，矿用和工程自卸"
                },
                {
                    "@type": "Offer",
                    "name": "牵引车",
                    "alternateName": "Tractor Truck", 
                    "description": "SHACMAN/SAGMOTO 牵引车出口，长途物流运输解决方案"
                },
                {
                    "@type": "Offer",
                    "name": "载货车",
                    "alternateName": "Cargo Truck",
                    "description": "SHACMAN/SAGMOTO 载货车出口，城市配送和区域物流"
                },
                {
                    "@type": "Offer",
                    "name": "专用车",
                    "alternateName": "Special Vehicle",
                    "description": "SHACMAN/SAGMOTO 专用车出口，搅拌车/油罐车/环卫车等"
                }
            ],
            "sameAs": [
                "https://www.facebook.com/profile.php?id=61591439076603",
                "https://www.youtube.com/@FenghanTrading"
            ]
        });
        document.head.appendChild(ld);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
