// JSON-LD Structured Data Injection for fenghan-trade.com
// v4.12: Auto-FAQ by SAGMOTO model (X3s/E3/Z3/E1st/X6/X7/E9/i9 etc.) + LHD/RHD (2026-09-07)
// v4.12: Auto-FAQ by SAGMOTO model URL slug (X3s/E3/Z3/E1st/X6/X7/E9/i9) (2026-09-07)
// v4.11: Organization升级三品牌领先出口商定位 (description/slogan/knowsAbout) (2026-09-04)
// v4.10: Inline底部互链条 (GitHub Pages边缘节点无法及时刷新独立js, 直接inline确保1号站生效) (2026-09-04)
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

  // SAGMOTO model-specific FAQ database (v4.12: auto-FAQ by URL model slug)
  // Key: model slug (lowercase). Each has 3-4 buyer questions.
  var SAGMOTO_MODEL_FAQ = {
    'x3s': [
      ['What is the engine and power of SAGMOTO X3s?',
       'SAGMOTO X3s is powered by Cummins ISME 420HP inline-6 turbo-diesel with 12JSD200T manual transmission (12 forward + 2 reverse gears). Torque 2,100 Nm at 1,100-1,400 rpm. Max GCW 90T. Best for heavy bulk haulage and Africa/Middle East regional transport.'],
      ['What is the FOB price for SAGMOTO X3s?',
       'FOB price for SAGMOTO X3s 6x4 tractor ranges USD 38,000 - 58,000 depending on configuration (cab, axle, emission). CIF West Africa adds USD 2,800-3,500. Bulk orders 10+ units qualify for 3-7% discount tier.'],
      ['X3s vs E3 flagship: which should I choose?',
       'X3s uses Cummins ISME 420HP with manual transmission - proven workhorse for Africa/Middle East, ideal for heavy bulk 40T+ GCW, mining, regional haulage. E3 uses Yuchai YC6MK 400HP - more fuel efficient in tropical conditions. For premium express logistics consider E1st.'],
      ['What warranty does SAGMOTO X3s come with?',
       'Complete vehicle warranty 24 months or 150,000 km. Powertrain (engine + transmission + axle) 36 months or 300,000 km. Genuine Cummins parts available through 50+ authorized service centers across Africa, Middle East and CIS.']
    ],
    'e3': [
      ['What is the engine of SAGMOTO E3?',
       'SAGMOTO E3 is powered by Yuchai YC6MK 400HP inline-6 turbo-diesel with 12JSD200T manual transmission. Torque 1,920 Nm. Designed for tropical climates and African duty cycles with reinforced cooling package.'],
      ['How does E3 differ from X3s?',
       'E3 uses Yuchai engine (made in China) - lower acquisition cost (USD 4,000-6,000 less than X3s), excellent parts availability in Africa and Southeast Asia, well-suited for fleet operators prioritizing TCO. X3s uses Cummins for brand recognition and resale value.'],
      ['What is the SAGMOTO E3 FOB price?',
       'FOB SAGMOTO E3 6x4 tractor: USD 35,000 - 52,000. E3 is positioned as the value flagship for fleet buyers in emerging markets. CIF East Africa (Mombasa/Dar es Salaam) typically USD 2,400-2,900 additional.'],
      ['Does E3 support RHD and Euro V emissions?',
       'Yes. E3 supports LHD (standard) and RHD (4-6 weeks lead time, USD 1,200-1,800 adder for Indonesia, Kenya, Tanzania). Available in Euro II/III for standard Africa/CIS markets and Euro V for Kenya, Nigeria new rules, GCC markets.']
    ],
    'e3max': [
      ['What is SAGMOTO E3 MAX?',
       'E3 MAX is the upgraded E3 with Yuchai YC6MK 430HP engine, reinforced rear axle and 1,500 Nm torque. Designed for medium-haul logistics in tropical markets with 65T GCW.'],
      ['E3 MAX price and warranty?',
       'FOB E3 MAX 6x4 tractor: USD 42,000 - 58,000. Same 24-month vehicle warranty + 36-month powertrain warranty as X3s flagship.'],
      ['E3 MAX vs E3 vs X3s flagship?',
       'E3 MAX sits between E3 (value) and X3s (premium). It offers 30HP more than E3 and 8% better fuel economy than X3s in regional haulage duty. Best choice for mixed-load logistics operators.']
    ],
    'z3': [
      ['What is the engine and power of SAGMOTO Z3?',
       'SAGMOTO Z3 is the premium dump truck and tractor flagship, powered by Cummins M13 520HP with 12JSD240TA manual transmission. Max torque 2,400 Nm. Max GCW 80T. Designed for heavy bulk mining and 100+ ton dump operations.'],
      ['What is SAGMOTO Z3 dump truck FOB price?',
       'FOB SAGMOTO Z3 6x4 dump truck: USD 45,000 - 68,000. Z3 8x4 dump truck with reinforced frame: USD 55,000 - 85,000. CIF options available to major African and Middle Eastern ports.'],
      ['Z3 vs X3s: which is right for mining?',
       'Z3 has higher power (520HP vs 420HP), stronger frame and reinforced dump body options - ideal for 70T+ mining operations. X3s 6x4 is more versatile for mixed regional haulage. For 100T+ heavy mining dump operations, specify Z3.'],
      ['What dump body options are available for Z3?',
       'Z3 6x4 dump supports 18-25 cubic meter U-shape and square-shape bodies in HARDOX 450/500 wear steel. Z3 8x4 dump supports 25-35 cubic meter bodies. Rock bodies (3mm HARDOX), coal bodies (4mm standard steel), and tipper configurations available.']
    ],
    'e1st': [
      ['What is the engine and power of SAGMOTO E1st flagship?',
       'SAGMOTO E1st is the new-generation flagship with Cummins Z14 560HP inline-6 turbo-diesel and Eaton 12-speed AMT (automated manual). Max torque 2,650 Nm. Max GCW 100T. Cab is high-roof flat-floor with 2.13m internal height.'],
      ['E1st FOB price and lead time?',
       'FOB SAGMOTO E1st 6x4: USD 52,000 - 78,000. Custom-configured units 30-45 days production; stock units 15-20 days. Sea transit West Africa 35-40 days, Middle East 18-22 days, South America 38-45 days.'],
      ['How does E1st compare to Volvo FH and Mercedes Actros?',
       'E1st delivers comparable engine output (560HP) and equivalent AMT technology at 40-55% lower acquisition cost than European premium brands. Buyers in CIS, Africa and Southeast Asia report 80-85% of premium-brand TCO over 5 years.'],
      ['Does E1st meet EU GSR (General Safety Regulation)?',
       'Yes. E1st Euro VI variant includes AEBS (Advanced Emergency Braking), LDWS (Lane Departure Warning), blind spot detection, ISA and driver drowsiness monitoring - all required for EU type approval from July 2024.']
    ],
    'x6': [
      ['What is the SAGMOTO X6 medium truck used for?',
       'SAGMOTO X6 is a medium-duty truck (4x2/4x4, 8-15T GVW) powered by Cummins ISD 210HP engine with Fastgear 6DS transmission. Best for urban distribution, construction, agricultural transport, and municipal services across Africa, Middle East and Southeast Asia.'],
      ['What is SAGMOTO X6 FOB price?',
       'FOB SAGMOTO X6 4x2 medium truck: USD 22,000 - 32,000. X6 4x4 off-road variant: USD 28,000 - 42,000. Popular cab-chassis configuration for local body builders.'],
      ['X6 body configurations available?',
       'X6 supports dry cargo box, curtain-side, refrigerated box, tipper/dump, concrete mixer (6-8 m3 drum), water tanker, compactor, and specialized bodies (crane, aerial, recovery). Local Asian and African body builders familiar with X6 chassis mounting points.'],
      ['Does X6 support right-hand drive?',
       'Yes. X6 RHD is factory-direct with 4-6 weeks lead time, USD 1,200-1,500 adder. Common RHD markets: Indonesia, Malaysia, Kenya, Tanzania, Hong Kong, Singapore.']
    ],
    'x6s': [
      ['What is SAGMOTO X6s?',
       'X6s is the upgraded X6 medium-duty truck with Cummins ISD 240HP (vs 210HP), 9-speed Fastgear transmission, and reinforced chassis. Designed for heavier payload and mountainous terrain operation.'],
      ['X6s FOB price?',
       'FOB SAGMOTO X6s 4x2: USD 25,000 - 36,000. Premium medium-duty positioning for African, Middle East and CIS markets.'],
      ['X6s vs X6 vs X7?',
       'X6s sits between X6 (210HP, standard) and X7 (light 140HP, 4x2). Choose X6s for medium-duty premium positioning with stronger drivetrain.']
    ],
    'x7': [
      ['What is SAGMOTO X7 light truck used for?',
       'SAGMOTO X7 is a light-duty truck (4x2, 4.5-12T GVW) powered by Yuchai YC4E 140-160HP engine with 6DS transmission. Best for urban last-mile delivery, light municipal services, and small business logistics.'],
      ['What is SAGMOTO X7 FOB price?',
       'FOB SAGMOTO X7 4x2 light truck: USD 14,000 - 22,000. Cab-chassis configuration popular for local body building (cargo box, refrigerated, tipper).'],
      ['X7 vs X5 light duty?',
       'X7 is the modern light-duty flagship with Yuchai YC4E 140-160HP. X5 is the entry-level with smaller engine (YC4D 120HP) for ultra-cost-sensitive markets. X7 preferred for African and Middle East fleet operators.']
    ],
    'x7s': [
      ['What is SAGMOTO X7s?',
       'X7s is the upgraded X7 with Yuchai YC4E 160HP and 9-speed transmission, designed for medium-haul logistics with 12T GVW capability.'],
      ['X7s FOB price?',
       'FOB SAGMOTO X7s: USD 18,000 - 26,000. Positioned between X7 and X9 in the Sagmoto light/medium lineup.']
    ],
    'e9': [
      ['What is SAGMOTO E9 medium heavy truck?',
       'SAGMOTO E9 is a medium-heavy truck (18-25T GVW) powered by Yuchai YC6MK 350-380HP engine with 9JS119 manual transmission. Designed for regional haulage and construction site logistics.'],
      ['E9 FOB price?',
       'FOB SAGMOTO E9 6x4: USD 32,000 - 48,000. E9 is positioned as the bridge between medium-duty (X6) and heavy-duty (X3s) flagships.']
    ],
    'i9': [
      ['What is SAGMOTO i9?',
       'SAGMOTO i9 is the cab-chassis configuration optimized for specialized body building (refrigerated trucks, tankers, garbage compactors, fire trucks). Yuchai YC6MK 350HP with 9JS119 transmission.'],
      ['i9 vs X9 comparison?',
       'X9 is the standard sleeper-cab tractor for long-distance. i9 is the cab-chassis for special body upfits. Same drivetrain, different body strategy.']
    ],
    'x9': [
      ['What is SAGMOTO X9 used for?',
       'SAGMOTO X9 is a heavy-duty tractor (6x4) with Yuchai YC4E/D 140-160HP or higher powerplant for medium-heavy regional haulage. Common in Southeast Asia and Latin America.'],
      ['X9 vs X3s flagship?',
       'X9 is the medium-heavy configuration (16-25T GVW) for regional logistics. X3s is the heavy flagship (40T+ GCW). Different duty cycles - choose by load profile.']
    ],
    'x5': [
      ['What is SAGMOTO X5 light duty truck?',
       'SAGMOTO X5 is the entry-level light-duty truck (4x2, 4.5-8T GVW) with Yuchai YC4D 120HP engine and 6DS manual transmission. Optimized for cost-sensitive markets and basic logistics.'],
      ['X5 FOB price?',
       'FOB SAGMOTO X5: USD 11,000 - 17,000. The most affordable Sagmoto model. Popular in CIS, Southeast Asia and African small business operators.']
    ],
    'i5': [
      ['What is SAGMOTO i5?',
       'SAGMOTO i5 is the cab-chassis version of X5 for specialized body builders - refrigerated trucks, light tankers, and small dump applications. Yuchai YC4D 120HP drivetrain.'],
      ['i5 vs X5?',
       'i5 is the cab-chassis (no body), X5 comes with factory cargo box. Same drivetrain, different body strategy. Choose i5 for local body building.']
    ]
  };


  // ─── 1. Organization schema (all pages) ───────────────────────────────────
  addSchema({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Shaanxi Fenghan Trading Co., Ltd.",
    "alternateName": ["Fenghan Trading", "陕西风瀚贸易有限公司"],
    "url": BASE_URL + "/",
    "logo": BASE_URL + "/company_logo.png",
    "description": "Leading authorized exporter of SAGMOTO (SHACMAN) heavy duty trucks and Dongfeng new energy trucks from Xi'an, China. Tractor trucks, dump trucks, cargo trucks, and special vehicles exported to 50+ countries across Africa, Middle East, CIS, Southeast Asia, and Latin America. Models: X3s, E3, E1st, Z3, X6, X9, i9.",
    "slogan": "Your Best Truck Export Partner from China",
    "knowsAbout": [
      "SAGMOTO trucks",
      "SHACMAN trucks",
      "Dongfeng electric trucks",
      "heavy duty tractor trucks",
      "dump trucks",
      "cargo trucks",
      "Cummins engines",
      "Weichai engines",
      "Yuchai engines",
      "China truck export",
      "FOB CIF truck shipping"
    ],
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

      // FAQPage auto-detect (v4.12): visible Q&A blocks + model-based FAQ from URL slug
      try {
        var mainEntity = [];

        // (a) Visible Q&A blocks
        var faqBlocks = document.querySelectorAll('.faq-item, .faq, .q-and-a, [class*="faq"]');
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

        // (b) Model-based FAQ from URL slug (fallback / supplement)
        if (mainEntity.length < 2) {
          var urlLower = path.toLowerCase();
          // Try model slugs in order (longest first to avoid e3 matching in e3max)
          var modelSlugs = Object.keys(SAGMOTO_MODEL_FAQ).sort(function(a, b) { return b.length - a.length; });
          for (var i = 0; i < modelSlugs.length; i++) {
            var slug = modelSlugs[i];
            // Match slug with word boundary to avoid x6 matching x60/x600
            var slugRe = new RegExp('(^|[\\-])' + slug + '([\\-]|[0-9]|$)', 'i');
            if (slugRe.test(urlLower)) {
              var faqs = SAGMOTO_MODEL_FAQ[slug];
              faqs.forEach(function(pair) {
                mainEntity.push({
                  "@type": "Question",
                  "name": pair[0],
                  "acceptedAnswer": { "@type": "Answer", "text": pair[1] }
                });
              });
              break;
            }
          }
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

  // ─── 99. Inline crosslink (底部互链) ─────────────────────────────────────
  // 由于GitHub Pages对独立js文件缓存较强,直接inline底部条代码,避免拉不到新版
  if (window.__fenghanCrossLink) { /* already loaded */ }
  else {
    window.__fenghanCrossLink = 1;
    var xStyle = document.createElement('style');
    xStyle.textContent =
      '.fenghan-crosslink-bar{position:fixed;bottom:0;left:0;right:0;z-index:99990;' +
      'background:linear-gradient(90deg,#0D1F3D,#1a3a6e);color:#fff;text-align:center;' +
      'padding:10px 16px;font-size:13px;display:flex;align-items:center;justify-content:center;' +
      'gap:8px;flex-wrap:wrap;box-shadow:0 -2px 12px rgba(0,0,0,0.3);line-height:1.5}' +
      '.fenghan-crosslink-bar strong{color:#C89B3C;font-weight:600}' +
      '.fenghan-crosslink-bar a{color:#C89B3C;text-decoration:none;font-weight:600;' +
      'border-bottom:1px dashed #C89B3C;transition:color 0.2s;padding:0 4px}' +
      '.fenghan-crosslink-bar a:hover{color:#fff;border-bottom-color:#fff}' +
      '.fenghan-crosslink-divider{color:#666;font-size:14px}' +
      '.fenghan-crosslink-close{color:#999;cursor:pointer;font-size:18px;line-height:1;' +
      'padding:0 4px;margin-left:8px;transition:color 0.2s}' +
      '.fenghan-crosslink-close:hover{color:#fff}';
    document.head.appendChild(xStyle);

    var xBar = document.createElement('div');
    xBar.className = 'fenghan-crosslink-bar';
    xBar.innerHTML =
      '🚛 <strong>Our Brand Network</strong> — ' +
      '<a href="https://sagmoto-trucks.com/" target="_blank" rel="noopener">SAGMOTO (sagmoto-trucks.com)</a>' +
      '<span class="fenghan-crosslink-divider">·</span>' +
      '⚡ <a href="https://dongfengevtrucks.com/" target="_blank" rel="noopener">Dongfeng EV (dongfengevtrucks.com)</a>' +
      '<span class="fenghan-crosslink-close" title="关闭">✕</span>';

    xBar.querySelector('.fenghan-crosslink-close').addEventListener('click', function() {
      xBar.style.display = 'none';
    });

    function xInsert() {
      if (document.body) {
        document.body.appendChild(xBar);
        var wa = document.querySelector('.whatsapp-float');
        if (wa) wa.style.bottom = '56px';
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', xInsert);
    } else {
      xInsert();
    }
  }
})();
