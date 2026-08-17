// JSON-LD Structured Data Injection for fenghan-trade.com
// v4.2: fix ALL empty H1 tags + runtime lazy-load + title dedupe
// Injects Organization + WebSite + Product + BlogPosting + FAQPage structured data
(function() {
  'use strict';

  var BASE_URL = 'https://www.fenghan-trade.com';
  var path = window.location.pathname;
  var HEAD = document.head;

  // ─── 0. Google Search Console verification meta ────────────────────────────
  var gscMeta = document.createElement('meta');
  gscMeta.name = 'google-site-verification';
  gscMeta.content = 'ToFV2gZpfLfPuYrf8hPCWdo8VJwGuGxn5jf-UCn9YnQ';
  HEAD.appendChild(gscMeta);

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
    "description": "Official SHACMAN heavy duty truck export supplier. Tractor trucks, dump trucks, cargo trucks, and special vehicles for 50+ countries across Africa, Middle East, CIS, Southeast Asia, and Latin America.",
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
      "https://charlie555666.github.io/shacman-catalog/"
    ]
  });

  // ─── 2. WebSite schema (homepage only) ────────────────────────────────────
  if (path === '/' || path === '' || path === '/index.html') {
    addSchema({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Fenghan Trading \u2014 SHACMAN Heavy Duty Trucks",
      "url": BASE_URL + "/",
      "description": "Your trusted SHACMAN heavy duty truck supplier. Browse SHACMAN tractor trucks, dump trucks, cargo trucks and special vehicles with factory-direct pricing and worldwide shipping.",
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
                     'SHACMAN Truck Guide';
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
      var productName = nameEl ? nameEl.textContent.trim() : (document.title.split('|')[0].trim() || 'SHACMAN Truck');

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
        "description": productName + " \u2014 SHACMAN heavy duty truck for export. Factory-direct pricing, worldwide shipping. Contact Fenghan Trading for quotation.",
        "brand": { "@type": "Brand", "name": "SHACMAN", "alternateName": "Shaanxi Automobile Group" },
        "manufacturer": { "@type": "Organization", "name": "Shaanxi Automobile Group Co., Ltd.", "url": "https://www.shacman.com.cn/" },
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
    addHreflang('fr', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('ar', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('ru', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('es', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('zh-Hans', 'https://charlie555666.github.io/shacman-catalog/index.html');
  }

  // ─── 6. Fix empty H1 tags (ALL h1s, not just the first) ─────────────────
  function fixEmptyH1() {
    var h1s = document.querySelectorAll('h1');
    if (h1s.length > 0) {
      var fixed = 0;
      Array.prototype.forEach.call(h1s, function(h) {
        if (!h.textContent.trim()) {
          // Empty H1: fill with page title, visually-hidden style so layout is unchanged
          var title = document.title.split('|')[0].trim() || 'SHACMAN Heavy Duty Trucks';
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
      var pageTitle = document.title.split('|')[0].trim() || 'SHACMAN Heavy Duty Trucks';
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

  // ─── 9. Fill missing Open Graph tags (blog article pages lack og:image/og:description) ──
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

      if (changed.length) console.log('[SEO] Filled missing OG tags: ' + changed.join(', '));
    } catch (e) { /* best-effort */ }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      fixEmptyH1();
      setTimeout(enableLazyLoading, 800);
      setTimeout(fixTitleDupes, 500);
      setTimeout(fillMissingOG, 1200);
    });
  } else {
    setTimeout(fixEmptyH1, 500);
    setTimeout(enableLazyLoading, 1000);
    setTimeout(fixTitleDupes, 500);
    setTimeout(fillMissingOG, 1200);
  }

  console.log('[SEO] JSON-LD v4.3 injected (Org+WebSite+Blog+Product+FAQ+Breadcrumb+hreflang+H1Fix-all+lazy-load+title-dedupe+OG-fill)');
})();
