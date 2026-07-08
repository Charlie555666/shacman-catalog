#!/usr/bin/env python3
"""
Full Mirror v5 — 100% sagmoto.com clone using BeautifulSoup for nav/footer swap
+ raw string replacement for resource paths.

Strategy:
1. Download HTML from sagmoto.com
2. Use BS4 to find+extract nav and footer positions in original string
3. Replace them with our nav/footer via string slicing
4. Download ALL CSS/JS/image resources to local mirror/
5. Rewrite resource URLs to local paths
6. Keep ALL original CSS (no custom CSS injection that would conflict)
"""

import os, re, urllib.request, urllib.parse, hashlib, time
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path(__file__).parent
MIRROR_DIR = BASE_DIR / "mirror"
BASE_URL = "http://www.sagmoto.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36"

PAGE_LIST = [
    # (relative_url, output_filename, depth_from_root)
    ("/qyc.html", "qyc.html", 0),
    ("/zxc.html", "zxc.html", 0),
    ("/zhc.html", "zhc.html", 0),
    ("/special.html", "special.html", 0),
    ("/pzkyzyc.html", "pzkyzyc.html", 0),
    ("/pzmtc.html", "pzmtc.html", 0),
    ("/tzc.html", "tzc.html", 0),
    ("/service.html", "service.html", 0),
    ("/video_list.html", "video_list.html", 0),
    ("/service_list/1674411714944516096.html", "service_list/1674411714944516096.html", 1),
    ("/service_list/1674411730417303552.html", "service_list/1674411730417303552.html", 1),
    ("/service_list/1674411748220751872.html", "service_list/1674411748220751872.html", 1),
    ("/service_list/1674411767427842048.html", "service_list/1674411767427842048.html", 1),
    ("/news_list/1.html", "news_list/1.html", 1),
    ("/news_list/81163.html", "news_list/81163.html", 1),
]

# Our nav (from index.html, will be styled by our injected nav CSS)
OUR_NAV = """<div class="nav-bar">
                <div class="nav-inner">
                    <a href="INDEX_PREFIXindex.html" class="logo-link">
                        <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/45799ffa-90f5-4dc5-8fc1-f0dd10445b52.png" alt="SAGMOTO" class="nav-logo">
                    </a>
                    <ul class="main-nav">
                        <li><a href="INDEX_PREFIXindex.html">HOME</a></li>
                        <li class="has-dropdown"><a href="INDEX_PREFIXproducts.html">PRODUCTS <span class="arrow">&#9662;</span></a>
                            <div class="dropdown-mega">
                                <div class="dropdown-col"><h4>Light Duty</h4><a href="INDEX_PREFIXproducts.html">X9 Series</a><a href="INDEX_PREFIXproducts.html">X6 Series</a><a href="INDEX_PREFIXproducts.html">i9 Series</a></div>
                                <div class="dropdown-col"><h4>Medium Duty</h4><a href="INDEX_PREFIXproducts.html">E3 Series</a></div>
                                <div class="dropdown-col"><h4>Heavy Duty</h4><a href="INDEX_PREFIXproducts.html">X3s Tractor</a><a href="INDEX_PREFIXproducts.html">X3s Dump</a><a href="INDEX_PREFIXproducts.html">X3s Cargo</a></div>
                                <div class="dropdown-col"><h4>Electric</h4><a href="INDEX_PREFIXproducts.html">E9 Series</a></div>
                            </div>
                        </li>
                        <li class="has-dropdown"><a href="INDEX_PREFIXqyc.html">APPLICATION <span class="arrow">&#9662;</span></a>
                            <div class="dropdown-mega">
                                <div class="dropdown-col"><h4>By Application</h4><a href="INDEX_PREFIXqyc.html">Tractor</a><a href="INDEX_PREFIXzxc.html">Dump Truck</a><a href="INDEX_PREFIXzhc.html">Cargo Truck</a><a href="INDEX_PREFIXspecial.html">Special Vehicle</a><a href="INDEX_PREFIXpzkyzyc.html">Off-road Dump Truck</a><a href="INDEX_PREFIXpzmtc.html">Off-road Tractor</a><a href="INDEX_PREFIXtzc.html">Off-road Truck</a></div>
                            </div>
                        </li>
                        <li class="has-dropdown"><a href="INDEX_PREFIXservice.html">SERVICE <span class="arrow">&#9662;</span></a>
                            <div class="dropdown-mega">
                                <div class="dropdown-col"><h4>Service</h4><a href="INDEX_PREFIXservice.html">Service Policy</a><a href="INDEX_PREFIXservice_list/1674411714944516096.html">Find Provider</a><a href="INDEX_PREFIXservice_list/1674411730417303552.html">Maintenance</a><a href="INDEX_PREFIXservice_list/1674411748220751872.html">Driving Reminder</a><a href="INDEX_PREFIXservice_list/1674411767427842048.html">Safe Driving</a></div>
                            </div>
                        </li>
                        <li class="has-dropdown"><a href="INDEX_PREFIXnews_list/81163.html">NEWS <span class="arrow">&#9662;</span></a>
                            <div class="dropdown-mega">
                                <div class="dropdown-col"><h4>News</h4><a href="INDEX_PREFIXnews_list/81163.html">News Center</a><a href="INDEX_PREFIXvideo_list.html">Video Center</a></div>
                            </div>
                        </li>
                        <li class="has-dropdown"><a href="INDEX_PREFIXabout.html">ABOUT US <span class="arrow">&#9662;</span></a>
                            <div class="dropdown-mega">
                                <div class="dropdown-col"><h4>About</h4><a href="INDEX_PREFIXabout.html">Company Profile</a><a href="INDEX_PREFIXcontact.html">Contact Us</a></div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>"""

OUR_FOOTER = """<footer class="site-footer">
    <div class="footer-inner">
        <div class="footer-grid">
            <div class="footer-col">
                <h4>SAGMOTO</h4>
                <p>SAG Commercial Vehicle Company, a subsidiary of Shaanxi Automobile Holding Group, established in 1968.</p>
                <p>Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue, Xi'an, China</p>
            </div>
            <div class="footer-col">
                <h4>Quick Links</h4>
                <a href="INDEX_PREFIXproducts.html">Products</a>
                <a href="INDEX_PREFIXqyc.html">Applications</a>
                <a href="INDEX_PREFIXservice.html">Service</a>
                <a href="INDEX_PREFIXabout.html">About Us</a>
            </div>
            <div class="footer-col">
                <h4>Contact</h4>
                <p>Tel: +86 15319431311</p>
                <p>Email: sales@fenghan-trade.com</p>
                <a href="INDEX_PREFIXcontact.html">Contact Form</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Shaanxi Fenghan Trading Co., Ltd. All rights reserved.</p>
        </div>
    </div>
</footer>"""

# Minimal nav CSS that we inject (doesn't conflict with CMS styles)
OUR_NAV_CSS = """<style>
.nav-bar{background:#0D1F3D;width:100%;position:sticky;top:0;z-index:9999;box-shadow:0 2px 10px rgba(0,0,0,.3)}
.nav-inner{max-width:1400px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:70px}
.nav-logo{height:45px}
.main-nav{list-style:none;display:flex;gap:0;margin:0;padding:0;height:100%}
.main-nav>li{position:relative;height:100%;display:flex;align-items:center}
.main-nav>li>a{color:#fff;text-decoration:none;padding:0 18px;font-size:13px;font-weight:600;letter-spacing:.5px;height:100%;display:flex;align-items:center;transition:all .2s;white-space:nowrap}
.main-nav>li>a:hover{color:#C89B3C}
.main-nav>li>a .arrow{font-size:9px;margin-left:4px}
.has-dropdown:hover>.dropdown-mega{display:flex}
.dropdown-mega{display:none;position:absolute;top:100%;left:50%;transform:translateX(-50%);background:#fff;min-width:700px;border-radius:0 0 6px 6px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:25px 30px;gap:30px;z-index:10000;border-top:3px solid #C62828}
.dropdown-col h4{color:#0D1F3D;font-size:13px;font-weight:700;margin:0 0 10px 0;text-transform:uppercase;letter-spacing:.8px;border-bottom:1px solid #e0e0e0;padding-bottom:6px}
.dropdown-col a{display:block;color:#333;text-decoration:none;padding:5px 0;font-size:12px;transition:all .2s;white-space:nowrap}
.dropdown-col a:hover{color:#C62828;padding-left:5px}
.site-footer{background:#0D1F3D;color:#ccc;padding:50px 40px 20px;margin-top:0}
.footer-grid{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;padding-bottom:30px}
.footer-col h4{color:#C89B3C;font-size:15px;margin-bottom:15px;font-weight:600}
.footer-col p,.footer-col a{color:#aaa;font-size:13px;line-height:1.7;text-decoration:none;display:block;transition:.2s}
.footer-col a:hover{color:#fff}
.footer-bottom{max-width:1400px;margin:0 auto;border-top:1px solid rgba(255,255,255,.1);padding-top:20px;text-align:center;font-size:12px;color:#999}
@media(max-width:1024px){.main-nav>li>a{padding:0 10px;font-size:11px}.nav-inner{padding:0 20px}}
@media(max-width:768px){.nav-inner{height:60px;padding:0 15px}.nav-logo{height:35px}.main-nav{display:none}}
</style>"""


def download_url(url, save_path, retries=3):
    save_path = Path(save_path)
    if save_path.exists() and save_path.stat().st_size > 200:  # >200 bytes = valid
        return True
    save_path.parent.mkdir(parents=True, exist_ok=True)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                save_path.write_bytes(resp.read())
                return True
        except Exception as e:
            if i == retries - 1:
                print(f"  FAIL: {url} -> {e}")
                return False
            time.sleep(0.5)
    return False


def css_url_to_local_path(css_url):
    """Convert a CSS url(...) reference to local mirror path."""
    if css_url.startswith('data:'):
        return None
    parsed = urllib.parse.urlparse(css_url)
    path = parsed.path.lstrip('/')
    if not path:
        return None
    return MIRROR_DIR / path


def build_page(page_url, out_rel, depth):
    """Main build function for one page."""
    out_path = BASE_DIR / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    idx_prefix = "../" * depth if depth > 0 else ""
    
    print(f"\n  [{out_rel}] Downloading {page_url}...")
    try:
        req = urllib.request.Request(page_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw_html = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  FAILED: {e}")
        return False
    
    orig_bytes = len(raw_html)
    print(f"  HTML: {orig_bytes} bytes")
    
    # --- PHASE 1: Find nav and footer positions using BS4 ---
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Find the CMS nav container (c_grid-116273709439191)
    nav_div = soup.find('div', id='c_grid-116273709439191')
    footer_div = soup.find('div', id='c_grid-116273709439190')
    
    nav_str = str(nav_div) if nav_div else None
    footer_str = str(footer_div) if footer_div else None
    
    if not nav_div:
        print("  WARNING: Nav container not found!")
    if not footer_div:
        print("  WARNING: Footer container not found!")
    
    # --- PHASE 2: String-based replacement of nav and footer ---
    html = raw_html
    
    # Custom nav with proper index prefix
    our_nav = OUR_NAV.replace("INDEX_PREFIX", idx_prefix)
    our_footer = OUR_FOOTER.replace("INDEX_PREFIX", idx_prefix)
    
    if nav_str and nav_str in html:
        html = html.replace(nav_str, our_nav, 1)
        print("  Nav: replaced ✓")
    elif nav_div:
        # Try finding by the div's opening tag
        start_tag = f'<div id="c_grid-116273709439191"'
        pos = html.find(start_tag)
        if pos >= 0:
            # Find closing tag by counting div depth
            depth_count = 1
            i = pos + len(start_tag)
            while i < len(html) and depth_count > 0:
                next_open = html.find('<div', i)
                next_close = html.find('</div>', i)
                if next_close < 0:
                    break
                if next_open >= 0 and next_open < next_close:
                    depth_count += 1
                    i = next_open + 4
                else:
                    depth_count -= 1
                    if depth_count == 0:
                        end_pos = next_close + 6
                        html = html[:pos] + our_nav + html[end_pos:]
                        print("  Nav: replaced via depth-count ✓")
                        break
                    i = next_close + 6
        else:
            print("  Nav: NOT FOUND in raw HTML!")
    
    if footer_str and footer_str in html:
        html = html.replace(footer_str, our_footer, 1)
        print("  Footer: replaced ✓")
    elif footer_div:
        start_tag = f'<div id="c_grid-116273709439190"'
        pos = html.find(start_tag)
        if pos >= 0:
            depth_count = 1
            i = pos + len(start_tag)
            while i < len(html) and depth_count > 0:
                next_open = html.find('<div', i)
                next_close = html.find('</div>', i)
                if next_close < 0:
                    break
                if next_open >= 0 and next_open < next_close:
                    depth_count += 1
                    i = next_open + 4
                else:
                    depth_count -= 1
                    if depth_count == 0:
                        end_pos = next_close + 6
                        html = html[:pos] + our_footer + html[end_pos:]
                        print("  Footer: replaced via depth-count ✓")
                        break
                    i = next_close + 6
    
    # --- PHASE 3: Extract and download all external resources ---
    resources = set()
    
    # CSS links
    for m in re.finditer(r'(?:href|src)="(https?://[^"]*\.(?:css|js|png|jpg|jpeg|gif|svg|woff2?|ttf|ico)[^"]*)"', html, re.IGNORECASE):
        url = m.group(1)
        if 'sagmoto.com' in url or 'thefastimg.com' in url or 'faststatics.com' in url:
            resources.add(url)
    
    # Lazy images
    for m in re.finditer(r'lazy="(https?://[^"]*)"', html):
        url = m.group(1)
        if 'sagmoto.com' in url or 'thefastimg.com' in url:
            resources.add(url)
    
    # Download resources in parallel, build URL->local_path map
    print(f"  Resources: {len(resources)} found, downloading...")
    url_map = {}
    download_count = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for url in resources:
            parsed = urllib.parse.urlparse(url)
            path = parsed.path.lstrip('/')
            
            # Handle query string in filename
            if parsed.query:
                qhash = hashlib.md5(parsed.query.encode()).hexdigest()[:6]
                base, ext = os.path.splitext(path)
                path = f"{base}_{qhash}{ext}"
            
            local_path = MIRROR_DIR / path
            # Relative path from page to mirror/
            rel_path = f"{idx_prefix}mirror/{path}"
            url_map[url] = rel_path
            
            futures[executor.submit(download_url, url, local_path)] = url
        
        for future in as_completed(futures):
            if future.result():
                download_count += 1
    
    print(f"  Downloaded: {download_count}/{len(resources)}")
    
    # --- PHASE 4: Rewrite all resource URLs to local paths ---
    for orig_url, local_path in url_map.items():
        html = html.replace(orig_url, local_path)
    
    # --- PHASE 5: Fix remaining issues ---
    # Fix /xxx.html absolute paths
    html = re.sub(r'href="/([a-z_]+\.html)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="/(service_list/[^"]+)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="/(news_list/[^"]+)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="/(news_Detail/[^"]+)"', rf'href="{idx_prefix}\1"', html)
    html = re.sub(r'href="http://www\.sagmoto\.com/', f'href="{idx_prefix}', html)
    
    # Contact.html -> contact.html
    html = html.replace('Contact.html', 'contact.html')
    html = html.replace('/Contact.html', f'{idx_prefix}contact.html')
    
    # Remove leader photo from 81163 news page
    if '81163' in out_rel:
        # Find and remove the "Charting the Path" item via BeautifulSoup
        soup2 = BeautifulSoup(html, 'html.parser')
        for item in soup2.find_all('div', class_=lambda c: c and 'p_loopItem' in c if c else False):
            text = item.get_text()
            if 'Charting the Path of Courageous Advancement' in text:
                item_str = str(item)
                if item_str in html:
                    html = html.replace(item_str, '', 1)
                    print("  Removed leader photo news item ✓")
                break
    
    # --- PHASE 6: Inject our nav CSS + style.css for nav/footer ---
    # Insert after <head> or after first <title>
    head_end = html.find('</head>')
    if head_end > 0:
        # Add style.css for nav/footer styling
        style_css_link = f'<link rel="stylesheet" href="{idx_prefix}css/style.css">'
        html = html[:head_end] + style_css_link + '\n' + OUR_NAV_CSS + '\n' + html[head_end:]
    
    # --- Write output ---
    out_path.write_text(html, encoding='utf-8')
    new_bytes = len(html)
    print(f"  Output: {new_bytes} bytes ({new_bytes*100//max(orig_bytes,1)}%)")
    return True


def download_global_resources():
    """Download resources shared across all pages."""
    print("\nDownloading global CMS resources...")
    global_urls = [
        # Bootstrap + global CSS (combo)
        "http://www.sagmoto.com/npublic/libs/css/ceccbootstrap.min.css,global.css?instance=new2023032811535752050&viewType=p&v=1775725714000&siteType=oper",
        # Site CSS
        "http://www.sagmoto.com/css/site.css?instance=new2023032811535752050&viewType=p&v=1775725714000&siteType=oper",
        # Core JS (combo)
        "http://www.sagmoto.com/npublic/libs/core/ceccjquery.min.js,require.min.js,lib.min.js,page.min.js?instance=new2023032811535752050&viewType=p&v=1775725714000&siteType=oper",
        # Common JS
        "http://www.sagmoto.com/npublic/commonjs/common.min.js?instance=new2023032811535752050&viewType=p&v=1775725714000&siteType=oper",
    ]
    
    count = 0
    for url in global_urls:
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.lstrip('/')
        if parsed.query:
            qhash = hashlib.md5(parsed.query.encode()).hexdigest()[:6]
            base, ext = os.path.splitext(path)
            path = f"{base}_{qhash}{ext}"
        local = MIRROR_DIR / path
        if download_url(url, local):
            count += 1
            print(f"  OK: {local}")
    print(f"  Downloaded {count}/{len(global_urls)} global resources")


def main():
    print("=" * 60)
    print("SAGMOTO FULL MIRROR v5")
    print("Strategy: BS4 nav/footer find + raw string replace")
    print("=" * 60)
    
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    
    # First, download global CSS/JS
    download_global_resources()
    
    # Build all pages
    success = 0
    for page_url_path, out_rel, depth in PAGE_LIST:
        full_url = f"{BASE_URL}{page_url_path}"
        if build_page(full_url, out_rel, depth):
            success += 1
    
    # Download favicon
    download_url(
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png",
        MIRROR_DIR / "favicon.png"
    )
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {success}/{len(PAGE_LIST)} pages built")
    
    # Stats
    files = list(MIRROR_DIR.rglob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    print(f"Mirror: {len([f for f in files if f.is_file()])} files, {total_size/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
