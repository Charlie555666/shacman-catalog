#!/usr/bin/env python3
"""
sagmoto.com Full Mirror Builder v3 (Raw String Replacement)
- Preserves 100% of original HTML (no BeautifulSoup modification)
- Downloads core CMS CSS/JS to local mirror/
- Replaces nav & footer via regex on raw HTML
- Adds our style.css + app-pages.css links
- Fixes root-relative resource paths to use local mirror or sagmoto.com CDN
"""
import os
import re
import urllib.request
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
SCRAPED_DIR = Path(r"C:\Users\Administrator\WorkBuddy\20260605101515\sagmoto-scraped-v3")
MIRROR_DIR = BASE_DIR / "mirror"

SAGMOTO_BASE = "http://www.sagmoto.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

PAGES = [
    ("qyc.html", "qyc.html", ""),
    ("zxc.html", "zxc.html", ""),
    ("zhc.html", "zhc.html", ""),
    ("special.html", "special.html", ""),
    ("pzkyzyc.html", "pzkyzyc.html", ""),
    ("pzmtc.html", "pzmtc.html", ""),
    ("service.html", "service.html", ""),
    ("tzc.html", "tzc.html", ""),
    ("service_1674411714944516096.html", "service_list/1674411714944516096.html", "../"),
    ("service_1674411730417303552.html", "service_list/1674411730417303552.html", "../"),
    ("service_1674411748220751872.html", "service_list/1674411748220751872.html", "../"),
    ("service_1674411767427842048.html", "service_list/1674411767427842048.html", "../"),
    ("news_list_1.html", "news_list/1.html", "../"),
    ("news_list_81163.html", "news_list/81163.html", "../"),
    ("video_list.html", "video_list.html", ""),
]

# Core files already downloaded in previous run — verify they exist
CORE_FILES = [
    "npublic/libs/css/ceccbootstrap.min.css,global.css",
    "css/site.css",
    "npublic/libs/core/ceccjquery.min.js,require.min.js,lib.min.js,page.min.js",
    "npublic/commonjs/common.min.js",
]


def get_nav(path_prefix=""):
    return f"""<div class="nav-bar">
                <div class="nav-inner">
                    <a href="{path_prefix}index.html" class="logo-link">
                        <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/45799ffa-90f5-4dc5-8fc1-f0dd10445b52.png" alt="SAGMOTO" class="nav-logo">
                    </a>
                    <ul class="main-nav">
                        <li><a href="{path_prefix}index.html">HOME</a></li>
                        <li class="dropdown">
                            <a href="{path_prefix}products.html">PRODUCTS <span class="arrow">&#9662;</span></a>
                            <div class="mega-menu">
                                <div class="mega-col">
                                    <h4>TRACTOR TRUCK</h4>
                                    <a href="{path_prefix}x3000-tractor.html">X3000 Tractor</a>
                                    <a href="{path_prefix}x5000-tractor.html">X5000 Tractor</a>
                                    <a href="{path_prefix}f3000-tractor.html">F3000 Tractor</a>
                                    <a href="{path_prefix}h3000s-tractor.html">H3000S Tractor</a>
                                </div>
                                <div class="mega-col">
                                    <h4>DUMP TRUCK</h4>
                                    <a href="{path_prefix}x3000-dump.html">X3000 Dump</a>
                                    <a href="{path_prefix}x5000-dump.html">X5000 Dump</a>
                                    <a href="{path_prefix}f3000-dump.html">F3000 Dump</a>
                                    <a href="{path_prefix}h3000-dump.html">H3000 Dump</a>
                                </div>
                                <div class="mega-col">
                                    <h4>CARGO TRUCK</h4>
                                    <a href="{path_prefix}l3000-cargo.html">L3000 Cargo</a>
                                    <a href="{path_prefix}h3000-cargo.html">H3000 Cargo</a>
                                </div>
                                <div class="mega-col">
                                    <h4>SPECIAL VEHICLE</h4>
                                    <a href="{path_prefix}special-vehicle.html">Special Vehicles</a>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown">
                            <a href="{path_prefix}qyc.html">APPLICATION <span class="arrow">&#9662;</span></a>
                            <div class="mega-menu">
                                <div class="mega-col">
                                    <a href="{path_prefix}qyc.html">Tractor Truck</a>
                                    <a href="{path_prefix}zxc.html">Dump Truck</a>
                                    <a href="{path_prefix}zhc.html">Cargo Truck</a>
                                    <a href="{path_prefix}special.html">Special Vehicle</a>
                                    <a href="{path_prefix}tzc.html">Off-road Truck</a>
                                    <a href="{path_prefix}pzkyzyc.html">Mining Dump Truck</a>
                                    <a href="{path_prefix}pzmtc.html">Mining Tractor</a>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown">
                            <a href="{path_prefix}service.html">SERVICE <span class="arrow">&#9662;</span></a>
                            <div class="mega-menu">
                                <div class="mega-col">
                                    <a href="{path_prefix}service.html">Service Policy</a>
                                    <a href="{path_prefix}service_list/1674411714944516096.html">Find Service Provider</a>
                                    <a href="{path_prefix}service_list/1674411730417303552.html">Maintenance Service</a>
                                    <a href="{path_prefix}service_list/1674411748220751872.html">Driving Reminder</a>
                                    <a href="{path_prefix}service_list/1674411767427842048.html">Safe Driving</a>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown">
                            <a href="{path_prefix}news_list/81163.html">NEWS <span class="arrow">&#9662;</span></a>
                            <div class="mega-menu">
                                <div class="mega-col">
                                    <a href="{path_prefix}news_list/81163.html">News Center</a>
                                    <a href="{path_prefix}video_list.html">Video Center</a>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown">
                            <a href="{path_prefix}about.html">ABOUT US <span class="arrow">&#9662;</span></a>
                            <div class="mega-menu">
                                <div class="mega-col">
                                    <a href="{path_prefix}about.html">Company Profile</a>
                                    <a href="{path_prefix}contact.html">Contact Us</a>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>"""


def get_footer(path_prefix=""):
    return f"""<footer class="site-footer">
        <div class="footer-inner">
            <div class="footer-col">
                <h4>SAGMOTO</h4>
                <p>Professional commercial vehicle manufacturer, providing reliable truck solutions for global markets.</p>
            </div>
            <div class="footer-col">
                <h4>Quick Links</h4>
                <a href="{path_prefix}products.html">Products</a>
                <a href="{path_prefix}qyc.html">Applications</a>
                <a href="{path_prefix}service.html">Service</a>
                <a href="{path_prefix}about.html">About Us</a>
            </div>
            <div class="footer-col">
                <h4>Contact</h4>
                <p>Room 603A, Floor 6, Building B, Chanba Free Trade Center</p>
                <p>No.777 Eurasia Avenue, Chanba Ecological District</p>
                <p>Xi'an, Shaanxi, China</p>
                <p>+86 15319431311</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Shaanxi Fenghan Trading Co., Ltd. All Rights Reserved.</p>
        </div>
    </footer>"""


def preprocess_news_81163():
    """Remove leader photo from news_list_81163 using raw string replacement."""
    path = SCRAPED_DIR / "news_list_81163.html"
    if not path.exists():
        return False
    
    content = path.read_text(encoding='utf-8')
    # Find and remove the specific news item with leader photo
    # Pattern: <div class="cbox-XX p_loopItem">...Charting the Path...Courageous Advancement...</div>
    pattern = r'<div class="cbox-\d+ p_loopItem">.*?Charting the Path of Courageous Advancement.*?</div>\s*</div>\s*</div>\s*</div>'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content != content:
        path.write_text(new_content, encoding='utf-8')
        print("  [preprocess] Removed leader photo from news_list_81163.html")
        return True
    else:
        # Try broader match
        pattern2 = r'<div class="cbox-\d+ p_loopItem">.*?Courageous Advancement.*?</div>\s*</div>\s*</div>'
        new_content = re.sub(pattern2, '', content, flags=re.DOTALL)
        if new_content != content:
            path.write_text(new_content, encoding='utf-8')
            print("  [preprocess] Removed leader photo (broad match) from news_list_81163.html")
            return True
    
    print("  [preprocess] Leader photo NOT FOUND in news_list_81163.html")
    return False


def fix_resource_paths(content, path_prefix=""):
    """Fix root-relative resource paths: /xxx.css -> mirror/xxx.css (local) or sagmoto.com/xxx.css (CDN fallback)."""
    
    def fix_path(match):
        full_match = match.group(0)
        attr = match.group(1)  # href or src
        url = match.group(2)   # the URL value
        
        # Skip absolute URLs and data URIs
        if url.startswith('http') or url.startswith('//') or url.startswith('data:'):
            return full_match
        
        # Check for local mirror copy
        clean = url.split('?')[0].lstrip('/')
        local = MIRROR_DIR / clean
        if local.exists():
            return full_match.replace(url, "mirror/" + clean)
        
        # Fallback: absolute URL to sagmoto.com
        if url.startswith('/'):
            return full_match.replace(url, SAGMOTO_BASE + url)
        
        return full_match
    
    # Fix link href for CSS files
    content = re.sub(
        r'(href)="(/[^"]*\.css[^"]*)"',
        fix_path,
        content
    )
    
    # Fix script src for JS files (including combo paths)
    content = re.sub(
        r'(src)="(/npublic/[^"]+)"',
        fix_path,
        content
    )
    content = re.sub(
        r'(src)="(/upload/[^"]*\.js[^"]*)"',
        fix_path,
        content
    )
    content = re.sub(
        r'(src)="(/npublic/commonjs/[^"]+)"',
        fix_path,
        content
    )
    
    # Fix favicon
    content = re.sub(
        r'(href)="(/favicon\.ico[^"]*)"',
        fix_path,
        content
    )
    
    # Fix internal page links: /qyc.html -> qyc.html (relative)
    def fix_page_link(match):
        full = match.group(0)
        url = match.group(2)
        if url.startswith('/') and not url.startswith('//'):
            page = url.lstrip('/')
            return full.replace(url, path_prefix + page)
        return full
    
    content = re.sub(r'(href)="(/\w[^"]*\.html[^"]*)"', fix_page_link, content)
    
    return content


def build_page(src_file, output_file, path_prefix):
    """Build one page using raw string replacement."""
    html_path = SCRAPED_DIR / src_file
    if not html_path.exists():
        print(f"  SKIP: {src_file} not found")
        return False
    
    content = html_path.read_text(encoding='utf-8')
    original_size = len(content)
    
    # === Step 1: Remove top c_static bar ===
    # Find first <div class="...c_static..."> block
    content = re.sub(
        r'<div[^>]*class="[^"]*c_static[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>',
        '',
        content,
        count=1,
        flags=re.DOTALL
    )
    
    # === Step 2: Replace nav ===
    # Find <div id="c_grid-116273709439191"> ... </div></div></div> (the nav block)
    nav_pattern = r'<div[^>]*id="[^"]*116273709439191[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>'
    nav_count = len(re.findall(nav_pattern, content, re.DOTALL))
    content = re.sub(nav_pattern, get_nav(path_prefix), content, count=1, flags=re.DOTALL)
    
    # === Step 3: Replace footer ===
    # Find <div id="c_grid-116273709439190"> ... </div></div></div> (the footer block)
    footer_pattern = r'<div[^>]*id="[^"]*116273709439190[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>'
    footer_count = len(re.findall(footer_pattern, content, re.DOTALL))
    content = re.sub(footer_pattern, get_footer(path_prefix), content, count=1, flags=re.DOTALL)
    
    # === Step 4: Add our CSS after <title> tag ===
    css_insert = f'\n    <link rel="stylesheet" href="{path_prefix}css/style.css">\n    <link rel="stylesheet" href="{path_prefix}css/app-pages.css">'
    content = re.sub(r'(<title>[^<]*</title>)', r'\1' + css_insert, content, count=1)
    
    # === Step 5: Fix resource paths ===
    content = fix_resource_paths(content, path_prefix)
    
    # === Step 6: Write output ===
    out_path = BASE_DIR / output_file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')
    
    new_size = len(content)
    size_kb = new_size / 1024
    retention = new_size / original_size * 100 if original_size > 0 else 0
    
    # Status
    status = []
    if nav_count == 0:
        status.append("NAV-MISSING")
    if footer_count == 0:
        status.append("FOOTER-MISSING")
    status_str = " " + ", ".join(status) if status else ""
    
    print(f"  OK: {output_file} ({size_kb:.0f} KB, {retention:.0f}% kept){status_str}")
    return True


def main():
    print("=" * 60)
    print("sagmoto.com Full Mirror Builder v3 (Raw String)")
    print("=" * 60)
    
    # Verify core files exist
    missing = []
    for f in CORE_FILES:
        if not (MIRROR_DIR / f).exists():
            missing.append(f)
    if missing:
        print(f"\n[WARNING] Missing core files: {missing}")
        print("Run download step first or previous build_mirror.py")
    
    # Step 1: Preprocess
    print("\n[1/2] Preprocessing...")
    preprocess_news_81163()
    
    # Step 2: Build pages
    print(f"\n[2/2] Building {len(PAGES)} pages...")
    success = 0
    for src_file, out_file, path_prefix in PAGES:
        if build_page(src_file, out_file, path_prefix):
            success += 1
    
    print(f"\n{'=' * 60}")
    print(f"Done! Built {success}/{len(PAGES)} pages.")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
