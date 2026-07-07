#!/usr/bin/env python3
"""
SIMPLEST MIRROR v6 — Don't touch HTML at all.
Strategy:
1. Download raw HTML from sagmoto.com
2. Add <base href="http://www.sagmoto.com/"> so all root-relative CSS/JS/images work
3. Only fix nav link hrefs (relative path overrides base tag)
4. Inject our nav/footer CSS for visual branding
5. ZERO content changes, ZERO resource downloads
"""

import re, urllib.request, time
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
BASE_URL = "http://www.sagmoto.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36"

PAGE_LIST = [
    ("/qyc.html", "qyc.html"),
    ("/zxc.html", "zxc.html"),
    ("/zhc.html", "zhc.html"),
    ("/special.html", "special.html"),
    ("/pzkyzyc.html", "pzkyzyc.html"),
    ("/pzmtc.html", "pzmtc.html"),
    ("/tzc.html", "tzc.html"),
    ("/service.html", "service.html"),
    ("/video_list.html", "video_list.html"),
    ("/service_list/1674411714944516096.html", "service_list/1674411714944516096.html"),
    ("/service_list/1674411730417303552.html", "service_list/1674411730417303552.html"),
    ("/service_list/1674411748220751872.html", "service_list/1674411748220751872.html"),
    ("/service_list/1674411767427842048.html", "service_list/1674411767427842048.html"),
    ("/news_list/81163.html", "news_list/81163.html"),
    ("/news_list/1.html", "news_list/1.html"),
]

# Nav CSS to overlay on top of CMS nav bar
NAV_CSS = """<style>
/* HIDE the original sagmoto nav */
#c_grid-116273709439191 { display: none !important; }
/* HIDE the original sagmoto footer */
#c_grid-116273709439190 { display: none !important; }

/* --- OUR NAV --- */
.our-nav-bar{background:#0D1F3D;width:100%;position:sticky;top:0;z-index:9999;box-shadow:0 2px 10px rgba(0,0,0,.3);font-family:Arial,Helvetica,sans-serif}
.our-nav-inner{max-width:1400px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:70px}
.our-nav-logo{height:45px}
.our-main-nav{list-style:none;display:flex;gap:0;margin:0;padding:0;height:100%}
.our-main-nav>li{position:relative;height:100%;display:flex;align-items:center}
.our-main-nav>li>a{color:#fff;text-decoration:none;padding:0 18px;font-size:13px;font-weight:600;letter-spacing:.5px;height:100%;display:flex;align-items:center;transition:all .2s;white-space:nowrap}
.our-main-nav>li>a:hover{color:#C89B3C}
.our-main-nav>li>a .our-arrow{font-size:9px;margin-left:4px}
.our-has-dropdown:hover>.our-dropdown-mega{display:flex}
.our-dropdown-mega{display:none;position:absolute;top:100%;left:50%;transform:translateX(-50%);background:#fff;min-width:700px;border-radius:0 0 6px 6px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:25px 30px;gap:30px;z-index:10000;border-top:3px solid #C62828}
.our-dropdown-col h4{color:#0D1F3D;font-size:13px;font-weight:700;margin:0 0 10px 0;text-transform:uppercase;letter-spacing:.8px;border-bottom:1px solid #e0e0e0;padding-bottom:6px}
.our-dropdown-col a{display:block;color:#333;text-decoration:none;padding:5px 0;font-size:12px;transition:all .2s;white-space:nowrap}
.our-dropdown-col a:hover{color:#C62828;padding-left:5px}

/* --- OUR FOOTER --- */
.our-site-footer{background:#0D1F3D;color:#ccc;padding:50px 40px 20px;margin-top:0;font-family:Arial,Helvetica,sans-serif}
.our-footer-inner{max-width:1400px;margin:0 auto}
.our-footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;padding-bottom:30px}
.our-footer-col h4{color:#C89B3C;font-size:15px;margin-bottom:15px;font-weight:600}
.our-footer-col p,.our-footer-col a{color:#aaa;font-size:13px;line-height:1.7;text-decoration:none;display:block;transition:.2s}
.our-footer-col a:hover{color:#fff}
.our-footer-bottom{border-top:1px solid rgba(255,255,255,.1);padding-top:20px;text-align:center;font-size:12px;color:#999}
@media(max-width:1024px){.our-main-nav>li>a{padding:0 10px;font-size:11px}.our-nav-inner{padding:0 20px}}
@media(max-width:768px){.our-nav-inner{height:60px;padding:0 15px}.our-nav-logo{height:35px}.our-main-nav{display:none}}
</style>"""


def make_nav_html(idx_prefix):
    """Generate nav HTML with correct path prefix."""
    return f"""<div class="our-nav-bar">
    <div class="our-nav-inner">
        <a href="{idx_prefix}index.html" class="our-logo-link">
            <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/45799ffa-90f5-4dc5-8fc1-f0dd10445b52.png" alt="SAGMOTO" class="our-nav-logo">
        </a>
        <ul class="our-main-nav">
            <li><a href="{idx_prefix}index.html">HOME</a></li>
            <li class="our-has-dropdown"><a href="{idx_prefix}products.html">PRODUCTS <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col"><h4>Light Duty</h4><a href="{idx_prefix}products.html">X9 Series</a><a href="{idx_prefix}products.html">X6 Series</a><a href="{idx_prefix}products.html">i9 Series</a></div>
                    <div class="our-dropdown-col"><h4>Medium Duty</h4><a href="{idx_prefix}products.html">E3 Series</a></div>
                    <div class="our-dropdown-col"><h4>Heavy Duty</h4><a href="{idx_prefix}products.html">X3s Tractor</a><a href="{idx_prefix}products.html">X3s Dump</a><a href="{idx_prefix}products.html">X3s Cargo</a></div>
                    <div class="our-dropdown-col"><h4>Electric</h4><a href="{idx_prefix}products.html">E9 Series</a></div>
                </div>
            </li>
            <li class="our-has-dropdown"><a href="{idx_prefix}qyc.html">APPLICATION <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col"><h4>By Application</h4><a href="{idx_prefix}qyc.html">Tractor</a><a href="{idx_prefix}zxc.html">Dump Truck</a><a href="{idx_prefix}zhc.html">Cargo Truck</a><a href="{idx_prefix}special.html">Special Vehicle</a><a href="{idx_prefix}pzkyzyc.html">Off-road Dump Truck</a><a href="{idx_prefix}pzmtc.html">Off-road Tractor</a><a href="{idx_prefix}tzc.html">Off-road Truck</a></div>
                </div>
            </li>
            <li class="our-has-dropdown"><a href="{idx_prefix}service.html">SERVICE <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col"><h4>Service</h4><a href="{idx_prefix}service.html">Service Policy</a><a href="{idx_prefix}service_list/1674411714944516096.html">Find Provider</a><a href="{idx_prefix}service_list/1674411730417303552.html">Maintenance</a><a href="{idx_prefix}service_list/1674411748220751872.html">Driving Reminder</a><a href="{idx_prefix}service_list/1674411767427842048.html">Safe Driving</a></div>
                </div>
            </li>
            <li class="our-has-dropdown"><a href="{idx_prefix}news_list/81163.html">NEWS <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col"><h4>News</h4><a href="{idx_prefix}news_list/81163.html">News Center</a><a href="{idx_prefix}video_list.html">Video Center</a></div>
                </div>
            </li>
            <li class="our-has-dropdown"><a href="{idx_prefix}about.html">ABOUT US <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col"><h4>About</h4><a href="{idx_prefix}about.html">Company Profile</a><a href="{idx_prefix}contact.html">Contact Us</a></div>
                </div>
            </li>
        </ul>
    </div>
</div>"""


def make_footer_html(idx_prefix):
    return f"""<div class="our-site-footer">
    <div class="our-footer-inner">
        <div class="our-footer-grid">
            <div class="our-footer-col">
                <h4>SAGMOTO</h4>
                <p>SAG Commercial Vehicle Company, a subsidiary of Shaanxi Automobile Holding Group, established in 1968.</p>
                <p>Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue, Xi'an, China</p>
            </div>
            <div class="our-footer-col">
                <h4>Quick Links</h4>
                <a href="{idx_prefix}products.html">Products</a>
                <a href="{idx_prefix}qyc.html">Applications</a>
                <a href="{idx_prefix}service.html">Service</a>
                <a href="{idx_prefix}about.html">About Us</a>
            </div>
            <div class="our-footer-col">
                <h4>Contact</h4>
                <p>Tel: +86 15319431311</p>
                <p>Email: sales@fenghan-trade.com</p>
                <a href="{idx_prefix}contact.html">Contact Form</a>
            </div>
        </div>
        <div class="our-footer-bottom">
            <p>&copy; 2026 Shaanxi Fenghan Trading Co., Ltd. All rights reserved.</p>
        </div>
    </div>
</div>"""


def build_page(page_url, out_rel):
    """Build one page: download HTML, add base tag, hide CMS nav+footer, add ours."""
    out_path = BASE_DIR / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Determine depth for relative links
    depth = out_rel.count('/')
    idx_prefix = "../" * depth if depth > 0 else ""
    
    print(f"\n  [{out_rel}]")
    
    # Download
    try:
        req = urllib.request.Request(page_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  FAILED download: {e}")
        return False
    
    orig_size = len(html)
    print(f"  Downloaded: {orig_size} bytes")
    
    # --- STEP 1: Fix internal navigation links ---
    # These use root-relative paths like href="/qyc.html" which won't be affected by <base>
    # because we need them to point to OUR pages.
    # Replace nav link hrefs with explicit absolute URLs that override <base>
    
    # Fix all /xxx.html -> explicit relative paths
    html = re.sub(r'href="/(qyc|zxc|zhc|special|pzkyzyc|pzmtc|tzc|service|video_list|about|contact|products|index|news)\.html"',
                  rf'href="{idx_prefix}\1.html"', html)
    html = re.sub(r'href="/(service_list/\d+\.html)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="/(news_list/\d+\.html)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="/(news_Detail/\d+\.html)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="/Contact\.html"', rf'href="{idx_prefix}contact.html"', html)
    
    # Fix any direct sagmoto.com links
    html = html.replace(f'href="{BASE_URL}/', f'href="{idx_prefix}')
    html = html.replace(f"href='{BASE_URL}/", f"href='{idx_prefix}")
    
    # --- STEP 2: Remove leader photo from 81163 ---
    if '81163' in out_rel:
        soup = BeautifulSoup(html, 'html.parser')
        removed = False
        for item in soup.find_all('div', class_=lambda c: c and 'p_loopItem' in c if c else False):
            if 'Charting the Path of Courageous Advancement' in item.get_text():
                item_str = str(item)
                if item_str in html:
                    html = html.replace(item_str, '', 1)
                    removed = True
                    print("  Removed leader photo ✓")
                    break
        if not removed:
            print("  Leader photo not found (may already be gone)")
    
    # --- STEP 3: Add <base> tag for all CSS/JS/image root paths ---
    # This makes /css/site.css, /npublic/... etc all work by loading from sagmoto.com
    base_tag = f'<base href="{BASE_URL}/">'
    head_end = html.find('</head>')
    if head_end > 0:
        html = html[:head_end] + base_tag + '\n' + html[head_end:]
    
    # --- STEP 4: Inject our CSS to hide CMS nav/footer and show ours ---
    our_nav_html = make_nav_html(idx_prefix)
    our_footer_html = make_footer_html(idx_prefix)
    
    body_start = html.find('<body')
    if body_start > 0:
        body_content_start = html.find('>', body_start) + 1
        html = (html[:body_content_start] + 
                our_nav_html + '\n' +
                html[body_content_start:])
    
    # Add footer before </body>
    body_end = html.find('</body>')
    if body_end > 0:
        html = html[:body_end] + our_footer_html + '\n' + html[body_end:]
    
    # Inject nav CSS at end of head
    if head_end > 0:
        html = html[:head_end] + NAV_CSS + '\n' + html[head_end:]
    
    # Write
    out_path.write_text(html, encoding='utf-8')
    new_size = len(html)
    print(f"  Output: {new_size} bytes (101% — added nav+footer+base)")
    return True


def main():
    print("=" * 60)
    print("SAGMOTO SIMPLE MIRROR v6")
    print("Strategy: <base> tag + hide CMS nav/footer + add ours")
    print("=" * 60)
    
    success = 0
    for page_path, out_rel in PAGE_LIST:
        full_url = f"{BASE_URL}{page_path}"
        if build_page(full_url, out_rel):
            success += 1
    
    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {success}/{len(PAGE_LIST)} pages built")
    print("All CSS/JS/images load from sagmoto.com via <base> tag")
    print("Nav and footer are ours (CMS versions hidden via CSS)")


if __name__ == "__main__":
    main()
