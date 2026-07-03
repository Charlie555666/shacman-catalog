/**
 * whatsapp-inject.js — 51微店 fenghan-trade.com WhatsApp悬浮按钮
 * Injected via 统计代码 as: <script src="whatsapp-inject.js"></script>
 * Version: 2026-07-02
 */
(function() {
    if (window.__fenghanWAInjected) return;
    window.__fenghanWAInjected = 1;

    // Inject CSS
    var style = document.createElement('style');
    style.textContent =
        '.whatsapp-float{position:fixed;bottom:24px;right:24px;z-index:99999;display:flex;align-items:center;gap:8px;text-decoration:none}' +
        '.whatsapp-float .btn-wa{width:56px;height:56px;border-radius:50%;background:#25D366;color:white;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(37,211,102,0.4);cursor:pointer;transition:transform 0.2s}' +
        '.whatsapp-float .btn-wa:hover{transform:scale(1.1)}' +
        '.whatsapp-float .btn-wa svg{width:28px;height:28px;fill:white}' +
        '.whatsapp-float .wa-label{background:white;padding:8px 16px;border-radius:20px;font-size:13px;font-weight:600;color:#075e54;box-shadow:0 2px 8px rgba(0,0,0,0.15);white-space:nowrap}' +
        '@media(max-width:768px){.whatsapp-float .wa-label{display:none}}';
    document.head.appendChild(style);

    // Inject HTML
    var wa = document.createElement('a');
    wa.href = 'https://wa.me/8615319431311?text=Hi%20Fenghan%20Trading,%20I%27m%20interested%20in%20SHACMAN%20trucks';
    wa.className = 'whatsapp-float';
    wa.target = '_blank';
    wa.rel = 'noopener';
    wa.innerHTML =
        '<span class="wa-label">Chat on WhatsApp</span>' +
        '<span class="btn-wa">' +
        '<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>' +
        '</span>';

    // Inject after DOM ready
    function inject() {
        document.body.appendChild(wa);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inject);
    } else {
        inject();
    }
})();
