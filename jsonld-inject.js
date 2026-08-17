// JSON-LD Structured Data Injection for fenghan-trade.com
// v4: added empty H1 tag fix + meta description auto-generation
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

  // ─── 6. Fix empty H1 tags ─────────────────────────────────────────────────
  function fixEmptyH1() {
    var h1 = document.querySelector('h1');
    if (h1 && !h1.textContent.trim()) {
      // H1 exists but is empty - fill it based on page context
      var title = document.title.split('|')[0].trim() || 'SHACMAN Heavy Duty Trucks';
      h1.textContent = title;
      h1.setAttribute('aria-label', title);
      console.log('[SEO] Fixed empty H1:', title);
    } else if (!h1) {
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fixEmptyH1);
  } else {
    setTimeout(fixEmptyH1, 500);
  }

  console.log('[SEO] JSON-LD v4 injected (Org+WebSite+Blog+Product+FAQ+Breadcrumb+hreflang+H1Fix)');
})();
