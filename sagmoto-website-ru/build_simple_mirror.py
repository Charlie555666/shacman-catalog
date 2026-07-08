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
    # Application pages (content 100% from sagmoto.com)
    ("/qyc.html", "qyc.html"),
    ("/zxc.html", "zxc.html"),
    ("/zhc.html", "zhc.html"),
    ("/special.html", "special.html"),
    ("/pzkyzyc.html", "pzkyzyc.html"),
    ("/pzmtc.html", "pzmtc.html"),
    ("/tzc.html", "tzc.html"),
    # Service pages
    ("/service.html", "service.html"),
    ("/video_list.html", "video_list.html"),
    ("/service_list/1674411714944516096.html", "service_list/1674411714944516096.html"),
    ("/service_list/1674411730417303552.html", "service_list/1674411730417303552.html"),
    ("/service_list/1674411748220751872.html", "service_list/1674411748220751872.html"),
    ("/service_list/1674411767427842048.html", "service_list/1674411767427842048.html"),
    # News pages
    ("/news_list/81163.html", "news_list/81163.html"),
    ("/news_list/1.html", "news_list/1.html"),
    # About page (exists on sagmoto.com)
    ("/about.html", "about.html"),
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
.our-logo-link{display:flex;align-items:center;gap:10px;text-decoration:none}
.our-nav-logo{height:42px}
.our-logo-text{color:#fff;font-size:18px;font-weight:700;letter-spacing:2px}
.our-main-nav{list-style:none;display:flex;gap:0;margin:0;padding:0;height:100%}
.our-main-nav>li{position:relative;height:100%;display:flex;align-items:center}
.our-main-nav>li>a{color:#fff;text-decoration:none;padding:0 16px;font-size:13px;font-weight:600;letter-spacing:.5px;height:100%;display:flex;align-items:center;transition:all .2s;white-space:nowrap}
.our-main-nav>li>a:hover{color:#C89B3C}
.our-main-nav>li>a .our-arrow{font-size:9px;margin-left:4px}
.our-has-dropdown:hover>.our-dropdown-mega,.our-has-dropdown:hover>.our-app-dropdown{display:flex}
.our-dropdown-mega{display:none;position:absolute;top:100%;left:50%;transform:translateX(-50%);background:#fff;min-width:700px;border-radius:0 0 6px 6px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:25px 30px;gap:25px;z-index:10000;border-top:3px solid #C62828;flex-wrap:wrap}
.our-app-dropdown{min-width:900px;padding:25px 30px;gap:20px}
.our-dropdown-mega.our-app-dropdown{min-width:1050px}
.our-dropdown-col{flex:1;min-width:150px}
.our-dropdown-col h4{color:#0D1F3D;font-size:13px;font-weight:700;margin:0 0 10px 0;border-bottom:1px solid #e0e0e0;padding-bottom:6px;white-space:nowrap}
.our-dropdown-col h3{color:#C89B3C;font-size:15px;margin:0 0 15px 0;font-weight:600}
.our-dropdown-col a{display:block;color:#333;text-decoration:none;padding:4px 0;font-size:12px;transition:all .2s;white-space:nowrap}
.our-dropdown-col a:hover{color:#C62828;padding-left:5px}
.our-dropdown-col a img{width:28px;height:28px;object-fit:contain;vertical-align:middle;margin-right:5px;border-radius:3px}

/* --- OUR FOOTER --- */
.our-site-footer{background:#0D1F3D;color:#ccc;padding:50px 40px 20px;margin-top:0;font-family:Arial,Helvetica,sans-serif}
.our-footer-inner{max-width:1400px;margin:0 auto}
.our-footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:40px;padding-bottom:30px}
.our-footer-col h3{color:#C89B3C;font-size:15px;margin-bottom:15px;font-weight:600}
.our-footer-col p,.our-footer-col a{color:#aaa;font-size:13px;line-height:1.7;text-decoration:none;display:block;transition:.2s}
.our-footer-col ul{list-style:none;padding:0;margin:0}
.our-footer-col ul li{margin-bottom:6px}
.our-footer-col a:hover{color:#fff}
.our-footer-col .sub{color:#777;font-size:11px;margin-left:4px}
.our-footer-col img{max-width:120px;margin-bottom:10px}
.our-footer-bottom{border-top:1px solid rgba(255,255,255,.1);padding-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;font-size:12px;color:#999}
.our-footer-bottom a{color:#999;text-decoration:none;margin:0 10px}
.our-footer-bottom a:hover{color:#fff}
@media(max-width:1200px){.our-dropdown-mega.our-app-dropdown{min-width:800px}}
@media(max-width:1024px){.our-main-nav>li>a{padding:0 8px;font-size:11px}.our-nav-inner{padding:0 20px}.our-dropdown-mega{min-width:500px}.our-app-dropdown{min-width:600px}.our-footer-grid{grid-template-columns:1fr 1fr}}
@media(max-width:768px){.our-nav-inner{height:60px;padding:0 15px}.our-nav-logo{height:35px}.our-main-nav{display:none}.our-footer-grid{grid-template-columns:1fr}}
</style>"""


def make_nav_html(idx_prefix):
    """Generate nav HTML matching our site structure."""
    products_prefix = idx_prefix
    return f"""<div class="our-nav-bar">
    <div class="our-nav-inner">
        <a href="{idx_prefix}index.html" class="our-logo-link">
            <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO" class="our-nav-logo">
            <span class="our-logo-text">SAG INTL</span>
        </a>
        <ul class="our-main-nav">
            <li class="our-has-dropdown">
                <a href="{products_prefix}products.html">PRODUCTS <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col">
                        <h4>Light Duty Truck(4.5T≤GCW≤25T)</h4>
                        <a href="{products_prefix}products.html?cat=light"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png" alt="i9"/> i9</a>
                        <a href="{products_prefix}products.html?cat=light"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/175cc731-094c-4946-880b-90aa3a1a867e.png" alt="X9"/> X9</a>
                        <a href="{products_prefix}products.html?cat=light"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0630693e-37e8-43be-98dd-acbdb49c70c9.png" alt="X7"/> X7</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Medium Duty Truck(12T≤GCW≤60T)</h4>
                        <a href="{products_prefix}products.html?cat=medium"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64c3428c-c60f-4579-ac04-e561cbe8c772.png" alt="E6"/> E6</a>
                        <a href="{products_prefix}products.html?cat=medium"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png" alt="X6"/> X6</a>
                        <a href="{products_prefix}products.html?cat=medium"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d2bf1d4c-09c4-426a-895a-bd8f6aba5a63.jpg" alt="X5"/> X5</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Heavy Duty Truck(18T≤GCW≤100T)</h4>
                        <a href="{products_prefix}products.html?cat=heavy"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/84912c76-6629-4d69-ad59-d8da5940fbb4.jpg" alt="E1st"/> E1st</a>
                        <a href="{products_prefix}products.html?cat=heavy"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a32c4261-9dac-4e68-87f7-c037b5a56733.jpg" alt="Z3"/> Z3</a>
                        <a href="{products_prefix}products.html?cat=heavy"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0d2ddb14-41e9-4f6c-b60a-1b53fa89e0f3.png" alt="E3"/> E3</a>
                        <a href="{products_prefix}products.html?cat=heavy"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9aa95967-f314-494d-adbe-05935dee2d6c.png" alt="E9"/> E9</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Off-road Truck</h4>
                        <a href="{products_prefix}products.html?cat=offroad"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg" alt="Off-road"/> Off-road Dump</a>
                        <a href="{products_prefix}products.html?cat=offroad"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg" alt="X3s"/> X3s</a>
                    </div>
                </div>
            </li>
            <li class="our-has-dropdown">
                <a href="{idx_prefix}qyc.html">APPLICATIONS <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega our-app-dropdown">
                    <div class="our-dropdown-col">
                        <h4>Tractor</h4>
                        <a href="{idx_prefix}qyc.html">Port Transport</a>
                        <a href="{idx_prefix}qyc.html">Hazardous Chemicals Transport</a>
                        <a href="{idx_prefix}qyc.html">Coal Transport</a>
                        <a href="{idx_prefix}qyc.html">Sand And Gravel Transport</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Dump Truck</h4>
                        <a href="{idx_prefix}zxc.html">Urban Construction</a>
                        <a href="{idx_prefix}zxc.html">Mining</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Cargo Truck</h4>
                        <a href="{idx_prefix}zhc.html">Express Delivery</a>
                        <a href="{idx_prefix}zhc.html">Intercity Logistics</a>
                        <a href="{idx_prefix}zhc.html">City Distribution</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Special Vehicle</h4>
                        <a href="{idx_prefix}special.html">City Transportation</a>
                        <a href="{idx_prefix}special.html">Smart Sanitation</a>
                        <a href="{idx_prefix}special.html">Dangerous Goods Transportation</a>
                        <a href="{idx_prefix}special.html">Road Work & Rescue</a>
                    </div>
                    <div class="our-dropdown-col">
                        <h4>Off-road Truck</h4>
                        <a href="{idx_prefix}pzkyzyc.html">Off-road Dump Truck</a>
                        <a href="{idx_prefix}pzmtc.html">Off-road Tractor</a>
                    </div>
                </div>
            </li>
            <li class="our-has-dropdown">
                <a href="{idx_prefix}service.html">SERVICES <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col">
                        <h4>Service</h4>
                        <a href="{idx_prefix}service.html">Service Policy</a>
                        <a href="{idx_prefix}service_list/1674411714944516096.html">Find Your Service Provider</a>
                        <a href="{idx_prefix}service_list/1674411730417303552.html">Maintenance Service</a>
                        <a href="{idx_prefix}service_list/1674411748220751872.html">Driving Reminder</a>
                        <a href="{idx_prefix}service_list/1674411767427842048.html">Safe Driving</a>
                    </div>
                </div>
            </li>
            <li class="our-has-dropdown">
                <a href="{idx_prefix}news.html">NEWS <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col">
                        <h4>News</h4>
                        <a href="{idx_prefix}news_list/1.html">News Center</a>
                        <a href="{idx_prefix}video_list.html">Video Center</a>
                    </div>
                </div>
            </li>
            <li class="our-has-dropdown">
                <a href="{idx_prefix}about.html">ABOUT US <span class="our-arrow">&#9662;</span></a>
                <div class="our-dropdown-mega">
                    <div class="our-dropdown-col">
                        <h4>About</h4>
                        <a href="{idx_prefix}about.html">Who We Are</a>
                        <a href="{idx_prefix}about.html">When We Started</a>
                        <a href="{idx_prefix}about.html">Technological Innovation</a>
                        <a href="{idx_prefix}contact.html">Contact Us</a>
                    </div>
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
                <h3>PRODUCTS</h3>
                <ul>
                    <li><a href="{idx_prefix}products.html?cat=light">Light Duty Truck<span class="sub">(4.5T≤GCW≤25T)</span></a></li>
                    <li><a href="{idx_prefix}products.html?cat=medium">Medium Duty Truck<span class="sub">(12T≤GCW≤60T)</span></a></li>
                    <li><a href="{idx_prefix}products.html?cat=heavy">Heavy Duty Truck<span class="sub">(18T≤GCW≤100T)</span></a></li>
                    <li><a href="{idx_prefix}products.html?cat=offroad">Off-road Truck</a></li>
                </ul>
            </div>
            <div class="our-footer-col">
                <h3>APPLICATIONS</h3>
                <ul>
                    <li><a href="{idx_prefix}qyc.html">Tractor</a></li>
                    <li><a href="{idx_prefix}zxc.html">Dump Truck</a></li>
                    <li><a href="{idx_prefix}zhc.html">Cargo Truck</a></li>
                    <li><a href="{idx_prefix}special.html">Special Vehicle</a></li>
                    <li><a href="{idx_prefix}tzc.html">Off-road Truck</a></li>
                    <li><a href="{idx_prefix}new-energy.html">New Energy</a></li>
                </ul>
            </div>
            <div class="our-footer-col">
                <h3>CONTACT US</h3>
                <p><strong>Address:</strong><br>Room 603A, Floor 6, Building B,<br>Chanba Free Trade Center, No.777 Eurasia Avenue,<br>Chanba Ecological District, Xi'an, Shaanxi, China</p>
                <p><strong>Tel:</strong> +86 15319431311<br><strong>E-mail:</strong> sales@fenghan-trade.com</p>
            </div>
            <div class="our-footer-col our-qr-code">
                <h3>FOLLOW US</h3>
                <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO QR Code"/>
                <p>Scan to visit our mobile site</p>
            </div>
        </div>
        <div class="our-footer-bottom">
            <p>&copy; 2026 SAGMOTO | 陕汽集团商用车有限公司 | All Rights Reserved</p>
            <p><a href="{idx_prefix}privacy.html">Privacy Policy</a> | <a href="{idx_prefix}terms.html">Terms of Use</a> | <a href="{idx_prefix}index.html">Sitemap</a></p>
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
