// JSON-LD Structured Data Injection for fenghan-trade.com
// Injects Organization + WebSite + Product structured data for SEO/GEO
(function() {
  'use strict';

  // Organization schema
  var orgScript = document.createElement('script');
  orgScript.type = 'application/ld+json';
  orgScript.textContent = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Shaanxi Fenghan Trading Co., Ltd.",
    "alternateName": ["Fenghan Trading", "陕西风瀚贸易有限公司"],
    "url": "https://www.fenghan-trade.com/",
    "logo": "https://www.fenghan-trade.com/company_logo.png",
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

  // WebSite schema (only on homepage)
  if (window.location.pathname === '/' || window.location.pathname === '' || window.location.pathname === '/index.html') {
    var siteScript = document.createElement('script');
    siteScript.type = 'application/ld+json';
    siteScript.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Fenghan Trading \u2014 SHACMAN Heavy Duty Trucks",
      "url": "https://www.fenghan-trade.com/",
      "description": "Your trusted SHACMAN heavy duty truck supplier. Browse SHACMAN tractor trucks, dump trucks, cargo trucks and special vehicles with factory-direct pricing and worldwide shipping.",
      "inLanguage": ["en", "fr", "es", "ru", "zh"],
      "publisher": {
        "@type": "Organization",
        "name": "Shaanxi Fenghan Trading Co., Ltd."
      }
    });
    document.head.appendChild(siteScript);
  }

  console.log('[SEO] JSON-LD structured data injected');
})();
