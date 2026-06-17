// JSON-LD Structured Data Injection for fenghan-trade.com
// Injects Organization + WebSite + Product structured data for SEO/GEO
// v2: added Product Schema on product detail pages + hreflang annotations
(function() {
  'use strict';

  var BASE_URL = 'https://www.fenghan-trade.com';
  var path = window.location.pathname;

  // ─── 0. Google Search Console verification meta ────────────────────────────
  var gscMeta = document.createElement('meta');
  gscMeta.name = 'google-site-verification';
  gscMeta.content = 'ToFV2gZpfLfPuYrf8hPCWdo8VJwGuGxn5jf-UCn9YnQ';
  document.head.appendChild(gscMeta);

  // ─── 1. Organization schema (all pages) ───────────────────────────────────
  var orgScript = document.createElement('script');
  orgScript.type = 'application/ld+json';
  orgScript.textContent = JSON.stringify({
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
  document.head.appendChild(orgScript);

  // ─── 2. WebSite schema (homepage only) ────────────────────────────────────
  if (path === '/' || path === '' || path === '/index.html') {
    var siteScript = document.createElement('script');
    siteScript.type = 'application/ld+json';
    siteScript.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Fenghan Trading \u2014 SHACMAN Heavy Duty Trucks",
      "url": BASE_URL + "/",
      "description": "Your trusted SHACMAN heavy duty truck supplier. Browse SHACMAN tractor trucks, dump trucks, cargo trucks and special vehicles with factory-direct pricing and worldwide shipping.",
      "inLanguage": ["en", "fr", "es", "ru", "zh"],
      "publisher": {
        "@type": "Organization",
        "name": "Shaanxi Fenghan Trading Co., Ltd."
      },
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": BASE_URL + "/search?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    });
    document.head.appendChild(siteScript);
  }

  // ─── 3. Product schema (product detail pages only) ────────────────────────
  if (path.indexOf('/goods/') !== -1 || path.indexOf('/product/') !== -1 ||
      document.querySelector('h1.goods-name, h1[class*="product"], .product-detail h1')) {

    // Wait for DOM to be ready, then extract product data
    function injectProductSchema() {
      // Extract product name from H1
      var nameEl = document.querySelector('h1') ||
                   document.querySelector('.goods-name') ||
                   document.querySelector('[class*="product-name"]');
      var productName = nameEl ? nameEl.textContent.trim() : document.title.split('|')[0].trim();

      // Extract price
      var priceEl = document.querySelector('.goods-price em, .price em, [class*="price"] em, [class*="price"] strong') ||
                    document.querySelector('.goods-price, [class*="current-price"]');
      var priceText = priceEl ? priceEl.textContent.trim().replace(/[^0-9.]/g, '') : '';
      var price = parseFloat(priceText) || null;

      // Extract image
      var imgEl = document.querySelector('.goods-gallery img, .product-img img, .swiper-slide img');
      var imgUrl = imgEl ? (imgEl.src || imgEl.getAttribute('data-src') || '') : '';
      if (imgUrl && imgUrl.startsWith('//')) imgUrl = 'https:' + imgUrl;

      // Extract category from breadcrumb
      var breadcrumbLinks = document.querySelectorAll('nav a, .breadcrumb a, [class*="breadcrumb"] a');
      var category = '';
      if (breadcrumbLinks.length > 0) {
        var lastBc = breadcrumbLinks[breadcrumbLinks.length - 1];
        category = lastBc.textContent.trim();
      }

      // Build Product schema
      var productData = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": productName,
        "description": productName + " \u2014 SHACMAN heavy duty truck for export. Factory-direct pricing, worldwide shipping. Contact Fenghan Trading for quotation.",
        "brand": {
          "@type": "Brand",
          "name": "SHACMAN",
          "alternateName": "Shaanxi Automobile Group"
        },
        "manufacturer": {
          "@type": "Organization",
          "name": "Shaanxi Automobile Group Co., Ltd.",
          "url": "https://www.shacman.com.cn/"
        },
        "seller": {
          "@type": "Organization",
          "name": "Shaanxi Fenghan Trading Co., Ltd.",
          "url": BASE_URL + "/"
        },
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
          "seller": {
            "@type": "Organization",
            "name": "Shaanxi Fenghan Trading Co., Ltd."
          },
          "shippingDetails": {
            "@type": "OfferShippingDetails",
            "shippingRate": {
              "@type": "MonetaryAmount",
              "value": "0",
              "currency": "USD"
            },
            "shippingDestination": {
              "@type": "DefinedRegion",
              "addressCountry": "WORLDWIDE"
            }
          }
        };
      }

      var productScript = document.createElement('script');
      productScript.type = 'application/ld+json';
      productScript.textContent = JSON.stringify(productData);
      document.head.appendChild(productScript);

      // BreadcrumbList schema for product pages
      var bcItems = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"}];
      if (category) {
        bcItems.push({"@type": "ListItem", "position": 2, "name": category, "item": BASE_URL + "/search?category=" + encodeURIComponent(category)});
        bcItems.push({"@type": "ListItem", "position": 3, "name": productName, "item": window.location.href});
      } else {
        bcItems.push({"@type": "ListItem", "position": 2, "name": productName, "item": window.location.href});
      }

      var bcScript = document.createElement('script');
      bcScript.type = 'application/ld+json';
      bcScript.textContent = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": bcItems
      });
      document.head.appendChild(bcScript);

      console.log('[SEO] Product JSON-LD injected:', productName, price ? ('$' + price) : '(no price)');
    }

    // Run after DOM settles
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectProductSchema);
    } else {
      setTimeout(injectProductSchema, 800);
    }
  }

  // ─── 4. hreflang annotations (all pages) ──────────────────────────────────
  // fenghan-trade.com is primarily English with multilingual capability
  // We declare x-default + en canonical
  var canonicalUrl = BASE_URL + path + window.location.search;

  function addHreflang(lang, href) {
    var link = document.createElement('link');
    link.rel = 'alternate';
    link.hreflang = lang;
    link.href = href;
    document.head.appendChild(link);
  }

  // x-default and en point to same URL (English is default)
  addHreflang('en', canonicalUrl);
  addHreflang('x-default', canonicalUrl);
  // Catalog on GitHub Pages covers French, Arabic, Russian, Spanish markets
  if (path === '/' || path === '' || path === '/index.html') {
    addHreflang('fr', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('ar', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('ru', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('es', 'https://charlie555666.github.io/shacman-catalog/index.html');
    addHreflang('zh-Hans', 'https://charlie555666.github.io/shacman-catalog/index.html');
  }

  console.log('[SEO] JSON-LD v2 + hreflang injected');
})();
