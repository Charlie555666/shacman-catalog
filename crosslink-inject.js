/**
 * crosslink-inject.js — 51微店 fenghan-trade.com → 双向互链条
 * 指向 sagmoto-trucks.com (SAGMOTO品牌站) 和 dongfengevtrucks.com (东风新能源站)
 * Version: 2026-09-04 (v2.0: 加入4号站双向互链)
 */
(function() {
    if (window.__fenghanCrossLink) return;
    window.__fenghanCrossLink = 1;

    var style = document.createElement('style');
    style.textContent =
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
    document.head.appendChild(style);

    var bar = document.createElement('div');
    bar.className = 'fenghan-crosslink-bar';
    bar.innerHTML =
        '🚛 <strong>Our Brand Network</strong> — ' +
        '<a href="https://sagmoto-trucks.com/" target="_blank" rel="noopener">SAGMOTO (sagmoto-trucks.com)</a>' +
        '<span class="fenghan-crosslink-divider">·</span>' +
        '⚡ <a href="https://dongfengevtrucks.com/" target="_blank" rel="noopener">Dongfeng EV (dongfengevtrucks.com)</a>' +
        '<span class="fenghan-crosslink-close" title="关闭">✕</span>';

    bar.querySelector('.fenghan-crosslink-close').addEventListener('click', function() {
        bar.style.display = 'none';
    });

    // Wait for body to be ready
    function insert() {
        if (document.body) {
            document.body.appendChild(bar);
            // Adjust WhatsApp float and other bottom elements
            var wa = document.querySelector('.whatsapp-float');
            if (wa) wa.style.bottom = '56px';
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', insert);
    } else {
        insert();
    }
})();
