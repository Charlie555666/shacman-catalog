// JSON-LD Structured Data Injection for fenghan-trade.com
// v4.8: Cross-link to sagmoto-trucks.com & dongfengevtrucks.com added in Organization sameAs (2026-09-04)
// Injects Organization + WebSite + Product + BlogPosting + FAQPage + WebPage + Breadcrumb structured data
(function() {
  'use strict';

  var BASE_URL = 'https://www.fenghan-trade.com';
  var path = window.location.pathname;
  var HEAD = document.head;

  // ─── 0. Search engine verification + robots + geo meta ───────────────────
  var gscMeta = document.createElement('meta');
  gscMeta.name = 'google-site-verification';
  gscMeta.content = 'ToFV2gZpfLfPuYrf8hPCWdo8VJwGuGxn5jf-UCn9YnQ';
  HEAD.appendChild(gscMeta);

  // Bing verification (runtime — may help with Bing's JS-capable crawler)
  var bingMeta = document.createElement('meta');
  bingMeta.name = 'msvalidate.01';
  bingMeta.content = 'B79A149C0CFDD0146D76B855376A72D0';
  HEAD.appendChild(bingMeta);

  // Robots meta (if missing — ensures pages are indexable)
  if (!HEAD.querySelector('meta[name="robots"]')) {
    var robotsMeta = document.createElement('meta');
    robotsMeta.name = 'robots';
    robotsMeta.content = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1';
    HEAD.appendChild(robotsMeta);
  }

  // Geo tags (local SEO signal)
  var geoTags = [
    { name: 'geo.region', content: 'CN' },
    { name: 'geo.placename', content: "Xi'an, Shaanxi, China" },
    { name: 'geo.position', content: '34.3416;108.9398' },
    { name: 'ICBM', content: '34.3416, 108.9398' }
  ];
  geoTags.forEach(function(g) {
    if (!HEAD.querySelector('meta[name="' + g.name + '"]')) {
      var m = document.createElement('meta');
      m.name = g.name;
      m.content = g.content;
      HEAD.appendChild(m);
    }
  });

  function addSchema(data) {
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(data);
    HEAD.appendChild(s);
    return s;
  }

  function safeText(sel, fallback) {
    var el = document.querySelector(sel);
    var t = el ? el.textContent.trim() : '';
    return t || (fallback || '');
  }

  // ─── 1. Organization schema (all pages) ───────────────────────────────────
  addSchema({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Shaanxi Fenghan Trading Co., Ltd.",
    "alternateName": ["Fenghan Trading", "陕西风瀚贸易有限公司"],
    "url": BASE_URL + "/",
    "logo": BASE_URL + "/company_logo.png",
    "description": "Authorized SAGMOTO / SHACMAN heavy duty truck export supplier. Tractor trucks, dump trucks, cargo trucks, and special vehicles for 50+ countries across Africa, Middle East, CIS, Southeast Asia, and Latin America. Models: X3s, E3, E1st, Z3, X6, X9, i9.",
    "foundingDate": "2018",
    "address": {
      "@type": "PostalAddress",
      "addressCountry": "CN",
      "addressLocality": "Xi'an",
      "addressRegion": "Shaanxi"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+86-15319431311",
      "contactType": "sales",
      "availableLanguage": ["English", "French", "Russian", "Spanish", "Chinese"]
    },
    "sameAs": [
      "https://www.tiktok.com/@shacmanmachelle",
      "https://charlie555666.github.io/shacman-catalog/",
      "https://sagmoto-trucks.com/",
      "https://dongfengevtrucks.com/"
    ]
  });

  // ─── 2. WebSite schema (homepage only) ────────────────────────────────────
  if (path === '/' || path === '' || path === '/index.html') {
    addSchema({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Fenghan Trading \u2014 SAGMOTO Heavy Duty Trucks",
      "url": BASE_URL + "/",
      "description": "Your trusted SAGMOTO / SHACMAN truck supplier. Browse SAGMOTO tractor trucks (X3s, E3, E1st, Z3), dump trucks, cargo trucks, mixer trucks, special vehicles and electric trucks (i9, i5) with factory-direct pricing and worldwide shipping.",
      "inLanguage": ["en", "fr", "es", "ru", "zh"],
      "publisher": { "@type": "Organization", "name": "Shaanxi Fenghan Trading Co., Ltd." },
      "potentialAction": {
        "@type": "SearchAction",
        "target": { "@type": "EntryPoint", "urlTemplate": BASE_URL + "/search?q={search_term_string}" },
        "query-input": "required name=search_term_string"
      }
    });
  }

  // ─── 3. BlogPosting schema (blog article pages) ───────────────────────────
  var isBlog = path.indexOf('/blog-news/') !== -1 || path.indexOf('/blog/') !== -1 ||
               path.indexOf('blogs') !== -1;
  if (isBlog) {
    function injectBlogSchema() {
      var headline = safeText('h1', '') ||
                     (document.title || '').split('|')[0].trim() ||
                     'SAGMOTO Truck Guide';
      var desc = safeText('meta[name="description"]', '') ||
                 safeText('.article-content p, .blog-content p, .content p', '') || '';
      if (desc.length > 300) desc = desc.substring(0, 297) + '...';

      // extract date from URL or page (blog-news/slug-123456.html)
      var datePub = '';
      var m = document.querySelector('meta[property="article:published_time"]');
      if (m) datePub = m.content;
      if (!datePub) {
        var dateEl = document.querySelector('.blog-date, .article-date, time, [class*="date"]');
        if (dateEl) datePub = dateEl.textContent.trim();
      }
      if (!datePub) datePub = new Date().toISOString().split('T')[0];

      addSchema({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": desc,
        "datePublished": datePub,
        "dateModified": datePub,
        "mainEntityOfPage": { "@type": "WebPage", "@id": window.location.href },
        "author": { "@type": "Organization", "name": "Shaanxi Fenghan Trading Co., Ltd.", "url": BASE_URL + "/" },
        "publisher": {
          "@type": "Organization",
          "name": "Shaanxi Fenghan Trading Co., Ltd.",
          "logo": { "@type": "ImageObject", "url": BASE_URL + "/company_logo.png" }
        },
        "image": BASE_URL + "/company_logo.png"
      });

      // Blog BreadcrumbList
      addSchema({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/" },
          { "@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog" },
          { "@type": "ListItem", "position": 3, "name": headline, "item": window.location.href }
        ]
      });

      // FAQPage auto-detect: look for visible Q&A blocks (h3 + following p)
      try {
        var faqBlocks = document.querySelectorAll('.faq-item, .faq, .q-and-a, [class*="faq"]');
        var mainEntity = [];
        if (faqBlocks.length > 0) {
          faqBlocks.forEach(function(blk) {
            var qEl = blk.querySelector('h2, h3, h4, .question, [class*="question"]');
            var aEl = blk.querySelector('p, .answer, [class*="answer"]');
            if (qEl && aEl && qEl.textContent.trim() && aEl.textContent.trim()) {
              mainEntity.push({
                "@type": "Question",
                "name": qEl.textContent.trim().replace(/\?$/, '?'),
                "acceptedAnswer": { "@type": "Answer", "text": aEl.textContent.trim() }
              });
            }
          });
        }
        if (mainEntity.length >= 2) {
          addSchema({ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": mainEntity });
        }
      } catch (e) { /* FAQ extraction is best-effort */ }

      console.log('[SEO] BlogPosting JSON-LD injected:', headline);
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectBlogSchema);
    } else {
      setTimeout(injectBlogSchema, 800);
    }
  }

  // ─── 4. Product schema (product detail pages only) ────────────────────────
  if (path.indexOf('/goods/') !== -1 || path.indexOf('/product/') !== -1 ||
      document.querySelector('h1.goods-name, h1[class*="product"], .product-detail h1')) {

    function injectProductSchema() {
      var nameEl = document.querySelector('h1') ||
                   document.querySelector('.goods-name') ||
                   document.querySelector('[class*="product-name"]');
      var productName = nameEl ? nameEl.textContent.trim() : (document.title.split('|')[0].trim() || 'SAGMOTO Truck');

      var priceEl = document.querySelector('.goods-price em, .price em, [class*="price"] em, [class*="price"] strong') ||
                    document.querySelector('.goods-price, [class*="current-price"]');
      var priceText = priceEl ? priceEl.textContent.trim().replace(/[^0-9.]/g, '') : '';
      var price = parseFloat(priceText) || null;

      var imgEl = document.querySelector('.goods-gallery img, .product-img img, .swiper-slide img');
      var imgUrl = imgEl ? (imgEl.src || imgEl.getAttribute('data-src') || '') : '';
      if (imgUrl && imgUrl.startsWith('//')) imgUrl = 'https:' + imgUrl;

      var breadcrumbLinks = document.querySelectorAll('nav a, .breadcrumb a, [class*="breadcrumb"] a');
      var category = '';
      if (breadcrumbLinks.length > 0) {
        category = breadcrumbLinks[breadcrumbLinks.length - 1].textContent.trim();
      }

      var productData = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": productName,
        "description": productName + " \u2014 SAGMOTO / SHACMAN heavy duty truck for export. Factory-direct pricing, worldwide shipping. Contact Fenghan Trading for quotation.",
        "brand": { "@type": "Brand", "name": "SAGMOTO", "alternateName": "Shaanxi Automobile Group" },
        "manufacturer": { "@type": "Organization", "name": "Shaanxi Automobile Group Co., Ltd.", "url": "https://sagmoto-trucks.com/" },
        "seller": { "@type": "Organization", "name": "Shaanxi Fenghan Trading Co., Ltd.", "url": BASE_URL + "/" },
        "url": window.location.href
      };
      if (imgUrl) productData["image"] = imgUrl;
      if (category) productData["category"] = category;

      if (price && price > 0) {
        productData["offers"] = {
          "@type": "Offer",
          "priceCurrency": "USD",
          "price": price,
          "priceValidUntil": "2026-12-31",
          "availability": "https://schema.org/InStock",
          "seller": { "@type": "Organization", "name": "Shaanxi Fenghan Trading Co., Ltd." },
          "shippingDetails": {
            "@type": "OfferShippingDetails",
            "shippingRate": { "@type": "MonetaryAmount", "value": "0", "currency": "USD" },
            "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "WORLDWIDE" }
          }
        };
      }

      addSchema(productData);

      var bcItems = [{ "@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/" }];
      if (category) {
        bcItems.push({ "@type": "ListItem", "position": 2, "name": category, "item": BASE_URL + "/search?category=" + encodeURIComponent(category) });
        bcItems.push({ "@type": "ListItem", "position": 3, "name": productName, "item": window.location.href });
      } else {
        bcItems.push({ "@type": "ListItem", "position": 2, "name": productName, "item": window.location.href });
      }
      addSchema({ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": bcItems });

      console.log('[SEO] Product JSON-LD injected:', productName, price ? ('$' + price) : '(no price)');
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectProductSchema);
    } else {
      setTimeout(injectProductSchema, 800);
    }
  }

  // ─── 5. hreflang annotations (all pages) ──────────────────────────────────
  var canonicalUrl = BASE_URL + path + window.location.search;

  function addHreflang(lang, href) {
    var link = document.createElement('link');
    link.rel = 'alternate';
    link.hreflang = lang;
    link.href = href;
    HEAD.appendChild(link);
  }

  addHreflang('en', canonicalUrl);
  addHreflang('x-default', canonicalUrl);
  if (path === '/' || path === '' || path === '/index.html') {
    addHreflang('fr', 'https://sagmoto-trucks.com/');
    addHreflang('ar', 'https://sagmoto-trucks.com/');
    addHreflang('ru', 'https://sagmoto-trucks.com/');
    addHreflang('es', 'https://sagmoto-trucks.com/');
    addHreflang('zh-Hans', 'https://sagmoto-trucks.com/');
  }

  // ─── 5b. WebPage schema (non-blog, non-product pages) ─────────────────────
  var isProductPage = path.indexOf('/goods/') !== -1 || path.indexOf('/product/') !== -1;
  if (!isBlog && !isProductPage) {
    addSchema({
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": document.title.split('|')[0].trim() || 'SAGMOTO Heavy Duty Trucks',
      "url": window.location.href,
      "description": (function() {
        var d = HEAD.querySelector('meta[name="description"]');
        return d ? d.getAttribute('content') : 'Authorized SAGMOTO/SHACMAN truck exporter. Factory price, worldwide shipping to 50+ countries.';
      })(),
      "publisher": { "@type": "Organization", "name": "Shaanxi Fenghan Trading Co., Ltd." },
      "potentialAction": {
        "@type": "ReadAction",
        "target": window.location.href
      }
    });
  }

  // ─── 6. Fix empty H1 tags (ALL h1s, not just the first) ─────────────────
  function fixEmptyH1() {
    var h1s = document.querySelectorAll('h1');
    if (h1s.length > 0) {
      var fixed = 0;
      Array.prototype.forEach.call(h1s, function(h) {
        if (!h.textContent.trim()) {
          // Empty H1: fill with page title, visually-hidden style so layout is unchanged
          var title = document.title.split('|')[0].trim() || 'SAGMOTO Heavy Duty Trucks';
          h.textContent = title;
          h.style.cssText = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0;';
          h.setAttribute('aria-hidden', 'false');
          fixed++;
          console.log('[SEO] Fixed empty H1 (hidden fill):', title);
        }
      });
      if (fixed > 0) return;
    } else {
      // No H1 at all - create one (visually hidden for design, visible for SEO)
      var newH1 = document.createElement('h1');
      var pageTitle = document.title.split('|')[0].trim() || 'SAGMOTO Heavy Duty Trucks';
      newH1.textContent = pageTitle;
      newH1.style.cssText = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0;';
      newH1.setAttribute('aria-hidden', 'false');
      var body = document.body || document.documentElement;
      body.insertBefore(newH1, body.firstChild);
      console.log('[SEO] Created missing H1:', pageTitle);
    }
  }

  // ─── 7. Lazy-load images at runtime (SaaS platform cannot edit HTML) ────
  function enableLazyLoading() {
    var imgs = document.querySelectorAll('img');
    var lazyCount = 0;
    Array.prototype.forEach.call(imgs, function(img, i) {
      // Skip images already lazyloaded or inline base64 / svg
      if (img.hasAttribute('loading')) return;
      if (!img.src || img.src.indexOf('data:') === 0) return;
      if (img.closest('[data-lazyload="false"], [data-no-lazy], .no-lazy')) return;
      // First 3 images are above the fold - leave them eager (LCP)
      if (i >= 3) {
        img.setAttribute('loading', 'lazy');
        lazyCount++;
      }
    });
    if (lazyCount > 0) console.log('[SEO] Added loading=lazy to ' + lazyCount + ' images');
  }

  // ─── 8. Fix duplicated title keywords (e.g. "SHACMAN SHACMAN") ──────────
  function fixTitleDupes() {
    try {
      var t = document.title;
      if (!t) return;
      var fixed = t.replace(/\b([A-Za-z0-9]{2,})\s+\1\b/gi, '$1');
      if (fixed !== t) {
        document.title = fixed;
        console.log('[SEO] Fixed duplicated title:', fixed);
      }
    } catch (e) { /* best-effort */ }
  }

  // ─── 9. Fill missing Open Graph + Twitter + Canonical tags ───────────────
  function fillMissingOG() {
    try {
      var head = document.head;
      function hasMeta(attr, val) {
        return head.querySelector('meta[' + attr + '="' + val + '"]');
      }
      function setMeta(prop, content) {
        var m = document.createElement('meta');
        m.setAttribute('property', prop);
        m.setAttribute('content', content);
        head.appendChild(m);
        return m;
      }
      function setNameMeta(name, content) {
        var m = document.createElement('meta');
        m.setAttribute('name', name);
        m.setAttribute('content', content);
        head.appendChild(m);
        return m;
      }
      var changed = [];

      // og:description <- meta description or first paragraph
      var ogDesc = hasMeta('property', 'og:description');
      if (!ogDesc) {
        var md = head.querySelector('meta[name="description"]');
        var desc = md && md.getAttribute('content');
        if (!desc) {
          var p = document.querySelector('.view.rich_media_content p, article p, .blog-content p, main p');
          desc = p ? p.textContent.trim().slice(0, 150) : '';
        }
        if (desc) {
          setMeta('og:description', desc);
          changed.push('og:description');
        }
      }

      // og:image <- first substantial content image, fallback to default
      var ogImg = hasMeta('property', 'og:image');
      if (!ogImg) {
        var imgs = document.querySelectorAll('img');
        var picked = '';
        for (var i = 0; i < imgs.length; i++) {
          var src = imgs[i].src || '';
          if (src.indexOf('data:') === 0) continue;
          if (imgs[i].width >= 200 && imgs[i].height >= 150) { picked = src; break; }
        }
        if (!picked && imgs.length) {
          for (var j = 0; j < imgs.length; j++) {
            if (imgs[j].src && imgs[j].src.indexOf('data:') !== 0) { picked = imgs[j].src; break; }
          }
        }
        if (!picked) picked = 'https://www.fenghan-trade.com/template/default/images/logo.png';
        setMeta('og:image', picked);
        changed.push('og:image');
      }

      // og:title <- document title
      var ogTitle = hasMeta('property', 'og:title');
      if (!ogTitle && document.title) {
        setMeta('og:title', document.title);
        changed.push('og:title');
      }

      // og:url <- canonical or location
      var ogUrl = hasMeta('property', 'og:url');
      if (!ogUrl) {
        var canon = head.querySelector('link[rel="canonical"]');
        setMeta('og:url', canon ? canon.getAttribute('href') : location.href);
        changed.push('og:url');
      }

      // og:type <- page type detection
      if (!hasMeta('property', 'og:type')) {
        var ogType = 'website';
        if (path.indexOf('/blog-news/') !== -1 || path.indexOf('/blog/') !== -1) {
          ogType = 'article';
        } else if (path.indexOf('/goods/') !== -1 || path.indexOf('/product/') !== -1) {
          ogType = 'product';
        }
        setMeta('og:type', ogType);
        changed.push('og:type:' + ogType);
      }

      // og:site_name
      if (!hasMeta('property', 'og:site_name')) {
        setMeta('og:site_name', 'SAGMOTO / SHACMAN Truck Export — Fenghan Trading');
        changed.push('og:site_name');
      }

      // og:locale
      if (!hasMeta('property', 'og:locale')) {
        setMeta('og:locale', 'en_US');
        changed.push('og:locale');
      }

      // ── Canonical link (if missing) ──
      if (!head.querySelector('link[rel="canonical"]')) {
        var canonLink = document.createElement('link');
        canonLink.rel = 'canonical';
        // Strip query params for canonical (except blog ID)
        var canonPath = path;
        var canonSearch = '';
        if (path.indexOf('/blog-news/') !== -1) {
          // Keep blog article URLs clean
          canonSearch = window.location.search;
        }
        canonLink.href = BASE_URL + canonPath + canonSearch;
        head.appendChild(canonLink);
        changed.push('canonical');
      }

      // ── Twitter Card tags (if missing) ──
      if (!hasMeta('name', 'twitter:card')) {
        setNameMeta('twitter:card', 'summary_large_image');
        changed.push('twitter:card');
      }
      if (!hasMeta('name', 'twitter:title') && document.title) {
        setNameMeta('twitter:title', document.title.split('|')[0].trim());
        changed.push('twitter:title');
      }
      if (!hasMeta('name', 'twitter:description')) {
        var tDesc = head.querySelector('meta[name="description"]');
        var tDescContent = tDesc ? tDesc.getAttribute('content') : '';
        if (!tDescContent) {
          var tP = document.querySelector('article p, .blog-content p, main p');
          tDescContent = tP ? tP.textContent.trim().slice(0, 150) : 'Authorized SAGMOTO/SHACMAN truck exporter. Factory price, worldwide shipping.';
        }
        setNameMeta('twitter:description', tDescContent);
        changed.push('twitter:description');
      }
      if (!hasMeta('name', 'twitter:image')) {
        var twImg = hasMeta('property', 'og:image');
        var twImgContent = twImg ? twImg.getAttribute('content') : 'https://www.fenghan-trade.com/template/default/images/logo.png';
        setNameMeta('twitter:image', twImgContent);
        changed.push('twitter:image');
      }

      if (changed.length) console.log('[SEO] Filled missing tags: ' + changed.join(', '));
    } catch (e) { /* best-effort */ }
  }

  // ─── 10. Fix German localization bug "Ansicht" -> "View" ──────────────────
  function fixGermanText() {
    var replaced = 0;
    var elements = document.querySelectorAll('a, span, button, div');
    Array.prototype.forEach.call(elements, function(el) {
      // Only replace if the element's direct text is exactly "Ansicht" (no child elements)
      if (el.children.length === 0 && el.textContent.trim() === 'Ansicht') {
        el.textContent = 'View';
        replaced++;
      }
    });
    // Also check for other common German UI strings from 51微店 template
    var germanMap = {
      'Ansicht': 'View',
      'Details ansehen': 'View Details',
      'Mehr': 'More',
      'Zurück': 'Back',
      'Weiter': 'Next'
    };
    Array.prototype.forEach.call(elements, function(el) {
      if (el.children.length === 0) {
        var txt = el.textContent.trim();
        if (germanMap[txt]) {
          el.textContent = germanMap[txt];
          replaced++;
        }
      }
    });
    if (replaced > 0) console.log('[SEO] Fixed ' + replaced + ' German UI text(s) -> English');
  }

  // ─── 11. Inject SAGMOTO model keywords into meta keywords ────────────────
  function injectSagmotoKeywords() {
    var SAGMOTO_KW = [
      'SAGMOTO X3s', 'SAGMOTO E3', 'SAGMOTO E1st', 'SAGMOTO Z3',
      'SAGMOTO X6', 'SAGMOTO X6s', 'SAGMOTO X7', 'SAGMOTO X9',
      'SAGMOTO X9s', 'SAGMOTO E9', 'SAGMOTO E6', 'SAGMOTO X5',
      'SAGMOTO i9', 'SAGMOTO i5',
      'SAGMOTO X1s', 'SAGMOTO X1', 'X1 dump truck', 'X1s dump truck',
      'X1 mining truck', 'X1 8x4 dump truck', 'X1 6x4 dump truck',
      'X1 tractor truck', 'X1s mining truck', 'X1 truck price',
      'X1 heavy duty truck', 'X1 tipper truck', 'X1 dump truck export',
      'SAGMOTO tractor truck', 'SAGMOTO dump truck', 'SAGMOTO cargo truck',
      'SAGMOTO mixer truck', 'SAGMOTO tanker truck', 'SAGMOTO crane truck',
      'SAGMOTO special vehicle', 'SAGMOTO electric truck', 'SAGMOTO off-road truck',
      'SAGMOTO semi truck', 'SAGMOTO prime mover', 'SAGMOTO tipper truck',
      'SAGMOTO sprinkler truck', 'SAGMOTO garbage truck', 'SAGMOTO tow truck',
      'SAGMOTO new energy truck',
      'SAGMOTO truck price', 'SAGMOTO truck specs', 'buy SAGMOTO truck',
      'SAGMOTO truck export', 'SAGMOTO truck dealer', 'SAGMOTO truck supplier',
      'SAGMOTO truck factory price',
      'Cummins engine truck', 'Weichai engine truck', 'Yuchai engine truck',
      'SAGMOTO 6x4', 'SAGMOTO 8x4', 'SAGMOTO 4x2', 'SAGMOTO 4x4',
      'SAGMOTO truck Africa', 'SAGMOTO truck Middle East',
      'SAGMOTO truck Southeast Asia', 'SAGMOTO truck CIS',
      'SAGMOTO truck Central Asia', 'SAGMOTO truck South America',
      'sagmoto-trucks.com', 'LHD RHD truck'
    ];

    var meta = document.querySelector('meta[name="keywords"]');
    if (meta) {
      var existing = (meta.getAttribute('content') || '').toLowerCase();
      var toAdd = SAGMOTO_KW.filter(function(kw) {
        return existing.indexOf(kw.toLowerCase()) === -1;
      });
      if (toAdd.length > 0) {
        var old = meta.getAttribute('content') || '';
        meta.setAttribute('content', old + (old ? ', ' : '') + toAdd.join(', '));
        console.log('[SEO] Added ' + toAdd.length + ' SAGMOTO keywords to meta keywords');
      }
    } else {
      var m = document.createElement('meta');
      m.setAttribute('name', 'keywords');
      m.setAttribute('content', SAGMOTO_KW.join(', '));
      HEAD.appendChild(m);
      console.log('[SEO] Created meta keywords with ' + SAGMOTO_KW.length + ' SAGMOTO keywords');
    }

    // Also add article:tag, article:author, article:section meta for blog pages
    var isBlogPage = path.indexOf('/blog-news/') !== -1 || path.indexOf('/blog/') !== -1;
    if (isBlogPage) {
      SAGMOTO_KW.slice(0, 15).forEach(function(kw) {
        var tag = document.createElement('meta');
        tag.setAttribute('property', 'article:tag');
        tag.setAttribute('content', kw);
        HEAD.appendChild(tag);
      });
      // article:author
      var artAuthor = document.createElement('meta');
      artAuthor.setAttribute('property', 'article:author');
      artAuthor.setAttribute('content', 'Shaanxi Fenghan Trading Co., Ltd.');
      HEAD.appendChild(artAuthor);
      // article:section
      var artSection = document.createElement('meta');
      artSection.setAttribute('property', 'article:section');
      artSection.setAttribute('content', 'Commercial Vehicles');
      HEAD.appendChild(artSection);
      // article:publisher
      var artPub = document.createElement('meta');
      artPub.setAttribute('property', 'article:publisher');
      artPub.setAttribute('content', BASE_URL + '/');
      HEAD.appendChild(artPub);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      fixEmptyH1();
      setTimeout(enableLazyLoading, 800);
      setTimeout(fixTitleDupes, 500);
      setTimeout(fillMissingOG, 1200);
      setTimeout(fixGermanText, 600);
      setTimeout(injectSagmotoKeywords, 300);
    });
  } else {
    setTimeout(fixEmptyH1, 500);
    setTimeout(enableLazyLoading, 1000);
    setTimeout(fixTitleDupes, 500);
    setTimeout(fillMissingOG, 1200);
    setTimeout(fixGermanText, 600);
    setTimeout(injectSagmotoKeywords, 300);
  }

  console.log('[SEO] JSON-LD v4.7 injected (Org+WebSite+WebPage+Blog+Product+FAQ+Breadcrumb+hreflang+H1Fix-all+lazy-load+title-dedupe+OG+Twitter+Canonical+DE-text-fix+SAGMOTO-keywords+X1-keywords+Bing-verify+robots+geo)');
})();
