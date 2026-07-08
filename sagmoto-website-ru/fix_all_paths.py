#!/usr/bin/env python3
"""
Fix all absolute path links in sagmoto-website HTML files.
Also generate missing pages (tzc.html, news_list/81163.html).
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent  # sagmoto-website/
SCRAPED_DIR = BASE_DIR.parent.parent / "sagmoto-scraped"

# Pages to generate (missing ones)
MISSING_PAGES = {
    'tzc.html': ('Applications', 'Off-road Truck'),
    'news_list/81163.html': ('', 'News Center'),
}

def fix_absolute_paths(html_content, file_depth=0):
    """Replace /xxx.html absolute paths with relative paths."""
    prefix = '../' * file_depth
    
    # Fix href="/xxx" -> href="prefix + xxx" (but not href="//" for protocol-relative)
    # Also fix src="/xxx" -> src="prefix + xxx"
    # But DON'T touch href="#" or href="javascript:" or http/https URLs
    
    def replace_href(match):
        attr = match.group(1)  # href or src
        path = match.group(2)
        
        # Skip protocol-relative URLs (//xxx)
        if path.startswith('//'):
            return match.group(0)
        # Skip absolute URLs with protocol
        if re.match(r'https?:', path):
            return match.group(0)
        # Skip # anchors and javascript:
        if path.startswith('#') or path.startswith('javascript'):
            return match.group(0)
        # Skip paths that are already relative (don't start with /)
        if not path.startswith('/'):
            return match.group(0)
        
        # Remove leading slash and add prefix
        new_path = prefix + path[1:]
        return f'{attr}="{new_path}"'
    
    # Match href="..." and src="..." with single or double quotes
    html_content = re.sub(r'(href|src)="(/[^"]*)"', replace_href, html_content)
    # Also handle single quotes
    html_content = re.sub(r"(href|src)='(/[^']*)'", lambda m: replace_href(re.sub(r'"', "'", m.group(0))), html_content)
    
    return html_content


def fix_contact_case(html_content):
    """Fix /Contact.html or Contact.html -> contact.html"""
    html_content = re.sub(r'(?i)Contact\.html', 'contact.html', html_content)
    return html_content


def ensure_app_pages_css(html_content, file_depth=0):
    """Ensure app-pages.css is referenced."""
    prefix = '../' * file_depth
    css_ref = f'css/app-pages.css' if file_depth == 0 else f'{prefix}css/app-pages.css'
    
    if 'app-pages.css' not in html_content:
        # Insert after style.css
        html_content = re.sub(
            r'(<link[^>]*style\.css["\s][^>]*>)',
            f'\\1\n    <link rel="stylesheet" href="{css_ref}">',
            html_content
        )
    return html_content


def generate_missing_page(page_name, category, subtitle):
    """Generate a missing page from scraped HTML."""
    # Map page names to scraped file names
    scraped_map = {
        'tzc.html': 'tzc.html',
        'news_list/81163.html': 'news_list_81163.html',
    }
    
    scraped_file = SCRAPED_DIR / scraped_map.get(page_name, page_name)
    if not scraped_file.exists():
        print(f"  SKIP: {page_name} (scraped file not found at {scraped_file})")
        return False
    
    with open(scraped_file, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    soup = BeautifulSoup(raw, 'html.parser')
    
    # Extract title
    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)
        title = re.sub(r'\s*[-–|]\s*SAG\s+Commercial\s+Vehicle\s+Company.*$', '', title, flags=re.IGNORECASE).strip()
    
    # Extract meta description
    meta_desc = ""
    for meta in soup.find_all('meta'):
        if (meta.get('name') or '').lower() == 'description':
            meta_desc = meta.get('content', '')[:160]
            break
    
    # Extract body content (same logic as build_subpages_v2.py)
    body = soup.find('body')
    if not body:
        body = soup
    
    main = body.find('div', class_='main')
    if not main:
        main = body
    
    content_parts = []
    nav_ended = False
    
    for child in main.children:
        if not hasattr(child, 'get'):
            continue
        
        child_id = child.get('id', '')
        
        if child_id == 'c_grid-116273709439191':
            nav_ended = True
            continue
        
        if child_id == 'c_grid-116273709439190':
            break
        
        if nav_ended:
            content_html = str(child)
            content_html = re.sub(r'<input type="hidden"[^>]*>', '', content_html)
            content_html = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', content_html)
            
            # Fix lazy images
            def fix_lazy_img(match):
                tag = match.group(0)
                lazy_match = re.search(r'lazy="([^"]*)"', tag)
                if lazy_match:
                    real_url = lazy_match.group(1)
                    tag = re.sub(r'src="[^"]*"', f'src="{real_url}"', tag)
                return tag
            content_html = re.sub(r'<img[^>]*>', fix_lazy_img, content_html)
            
            # Fix relative image paths
            content_html = content_html.replace('src="/npublic/', 'src="https://www.sagmoto.com/npublic/')
            
            # Remove CMS link/css tags
            content_html = re.sub(r'<link[^>]*>', '', content_html)
            
            if content_html.strip():
                content_parts.append(content_html)
    
    content = '\n'.join(content_parts)
    
    # Build breadcrumb
    breadcrumb = '<a href="index.html">Home</a>'
    if category:
        breadcrumb += f' <span>/</span> <span>{category}</span>'
    breadcrumb += f' <span>/</span> <span>{subtitle}</span>'
    
    page_title = title or subtitle
    depth = page_name.count('/')
    css_path = '../' * depth + 'css/style.css' if depth > 0 else 'css/style.css'
    app_css_path = '../' * depth + 'css/app-pages.css' if depth > 0 else 'css/app-pages.css'
    js_path = '../' * depth + 'js/main.js' if depth > 0 else 'js/main.js'
    data_loader_path = '../' * depth + 'js/data-loader.js' if depth > 0 else 'js/data-loader.js'
    
    # Read nav from build_subpages_v2.py's get_nav() - we'll inline it
    # Use relative paths based on depth
    nav_html = get_nav_for_depth(depth)
    topbar_html = get_topbar()
    
    output_path = BASE_DIR / page_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css">
    <link rel="stylesheet" href="{css_path}">
    <link rel="stylesheet" href="{app_css_path}">
    <link rel="icon" href="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png">
    <script src="{data_loader_path}"></script>
    <meta name="description" content="{meta_desc or page_title}">
    <meta name="keywords" content="SAGMOTO,{page_name.replace('.html','')},commercial vehicles,truck">
    <title>{page_title} - SAGMOTO</title>
</head>
<body>
    <div class="main">
{topbar_html}
{nav_html}
    <!-- ===== PAGE BANNER ===== -->
    <section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('{'../' * depth}images/hero/slide1.jpg') center/cover;">
        <div class="container">
            <div class="breadcrumb">
                {breadcrumb}
            </div>
            <h1>{page_title}</h1>
            <p>{category}</p>
        </div>
    </section>
    <!-- ===== MAIN CONTENT ===== -->
    <div class="scraped-content">
{content}
    </div>
{get_footer_for_depth(depth)}'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"  OK: {page_name} ({len(full_html):,} bytes)")
    return True


def get_topbar():
    return '''    <!-- ===== TOP BAR ===== -->
    <div class="e_container-1">
        <div class="container">
            <div class="top-contact">
                <a href="tel:+8615319431311">
                    <svg viewBox="0 0 24 24" width="14" height="14"><path fill="currentColor" d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z"/></svg>
                    +86 15319431311
                </a>
                <a href="mailto:sales@fenghan-trade.com">
                    <svg viewBox="0 0 24 24" width="14" height="14"><path fill="currentColor" d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                    sales@fenghan-trade.com
                </a>
            </div>
            <div class="lang-selector">
                <a href="#" class="active">EN</a>
                <a href="#">FR</a>
            </div>
        </div>
    </div>'''


def get_nav_for_depth(depth=0):
    """Return navigation with correct relative paths for given depth."""
    p = '../' * depth  # prefix for sub-directory pages
    
    return f'''    <!-- ===== HEADER / NAVIGATION ===== -->
    <div class="e_container-2">
        <div class="container">
            <div class="logo-area">
                <a href="{p}index.html">
                    <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO" class="logo-icon">
                    <span class="logo-text">SAG INTL</span>
                </a>
            </div>
            <div class="mobile-toggle"><span></span><span></span><span></span></div>
            <ul class="main-nav">
                <li class="has-dropdown">
                    <a href="{p}products.html">PRODUCTS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <div class="dropdown-mega">
                        <div class="mega-inner">
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Light Duty Truck(4.5T&le;GCW&le;25T)</h4>
                                <ul>
                                    <li><a href="{p}products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png" alt="i9"> i9</a></li>
                                    <li><a href="{p}products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/175cc731-094c-4946-880b-90aa3a1a867e.png" alt="X9"> X9</a></li>
                                    <li><a href="{p}products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0630693e-37e8-43be-98dd-acbdb49c70c9.png" alt="X7"> X7</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Medium Duty Truck(12T&le;GCW&le;60T)</h4>
                                <ul>
                                    <li><a href="{p}products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64c3428c-c60f-4579-ac04-e561cbe8c772.png" alt="E6"> E6</a></li>
                                    <li><a href="{p}products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png" alt="X6"> X6</a></li>
                                    <li><a href="{p}products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d2bf1d4c-09c4-426a-895a-bd8f6aba5a63.jpg" alt="X5"> X5</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Heavy Duty Truck(18T&le;GCW&le;100T)</h4>
                                <ul>
                                    <li><a href="{p}products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/84912c76-6629-4d69-ad59-d8da5940fbb4.jpg" alt="E1st"> E1st</a></li>
                                    <li><a href="{p}products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a32c4261-9dac-4e68-87f7-c037b5a56733.jpg" alt="Z3"> Z3</a></li>
                                    <li><a href="{p}products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0d2ddb14-41e9-4f6c-b60a-1b53fa89e0f3.png" alt="E3"> E3</a></li>
                                    <li><a href="{p}products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9aa95967-f314-494d-adbe-05935dee2d6c.png" alt="E9"> E9</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Off-road Truck</h4>
                                <ul>
                                    <li><a href="{p}products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg" alt="Off-road"> Off-road Dump</a></li>
                                    <li><a href="{p}products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg" alt="X3s"> X3s</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>
                <li class="has-dropdown">
                    <a href="javascript:;">APPLICATIONS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu dropdown-wide">
                        <li class="dropdown-group"><a href="{p}qyc.html" class="dropdown-group-title">Tractor</a>
                            <ul class="dropdown-sub">
                                <li><a href="{p}qyc.html">Port Transport</a></li>
                                <li><a href="{p}qyc.html#c_product_list_152-16902759283320">Hazardous Chemicals</a></li>
                                <li><a href="{p}qyc.html#c_product_list_152-16902759511700">Coal Transport</a></li>
                                <li><a href="{p}qyc.html#c_product_list_152-16902759295540">Sand &amp; Gravel</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="{p}zxc.html" class="dropdown-group-title">Dump Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="{p}zxc.html">Urban Construction</a></li>
                                <li><a href="{p}zxc.html#c_product_list_152-16902759962030">Mining</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="{p}zhc.html" class="dropdown-group-title">Cargo Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="{p}zhc.html">Express Delivery</a></li>
                                <li><a href="{p}zhc.html#c_product_list_152-16902759962030">Intercity Logistics</a></li>
                                <li><a href="{p}zhc.html#c_product_list_152-16915679157520">City Distribution</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="{p}special.html" class="dropdown-group-title">Special Vehicle</a>
                            <ul class="dropdown-sub">
                                <li><a href="{p}special.html">City Transportation</a></li>
                                <li><a href="{p}special.html#c_product_list_152-16889614330850">Smart Sanitation</a></li>
                                <li><a href="{p}special.html#c_product_list_152-16889616447540">Dangerous Goods</a></li>
                                <li><a href="{p}special.html#c_product_list_152-16902780105800">Road Work &amp; Rescue</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="{p}tzc.html" class="dropdown-group-title">Off-road Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="{p}pzkyzyc.html">Off-road Dump Truck</a></li>
                                <li><a href="{p}pzmtc.html">Off-road Tractor</a></li>
                            </ul></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="{p}service.html">SERVICES <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="{p}service.html">Service Policy</a></li>
                        <li><a href="{p}service_list/1674411714944516096.html">Find Your Service Provider</a></li>
                        <li><a href="{p}service_list/1674411730417303552.html">Maintenance Service</a></li>
                        <li><a href="{p}service_list/1674411748220751872.html">Driving Reminder</a></li>
                        <li><a href="{p}service_list/1674411767427842048.html">Safe Driving</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="{p}news_list/1.html">NEWS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="{p}news_list/1.html">News Center</a></li>
                        <li><a href="{p}video_list.html">Video Center</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="{p}about.html">ABOUT US <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="{p}about.html#c_category_427-16821721350130">Who We Are</a></li>
                        <li><a href="{p}about.html#c_static_001-1682265886008">When We Started</a></li>
                        <li><a href="{p}about.html#c_static_001-16822977301490">Technological Innovation</a></li>
                        <li><a href="{p}contact.html">Contact Us</a></li>
                    </ul>
                </li>
                <li class="nav-search"><a href="#" onclick="event.preventDefault();"><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></a></li>
            </ul>
        </div>
    </div>'''


def get_footer_for_depth(depth=0):
    p = '../' * depth
    return f'''    <!-- ===== FOOTER ===== -->
    <footer class="e_container-15">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h3><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO" style="height:30px;vertical-align:middle;"> SAGMOTO</h3>
                    <p>Founded in 1968, Shaanxi Automobile Holding Group Company. Core subsidiary dedicated to commercial vehicle manufacturing and international export.</p>
                    <div class="footer-social">
                        <a href="#" title="Facebook"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
                        <a href="#" title="YouTube"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
                        <a href="#" title="WhatsApp"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982 1.004-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.891 9.884"/></svg></a>
                    </div>
                </div>
                <div class="footer-col">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="{p}products.html">Products</a></li>
                        <li><a href="{p}qyc.html">Applications</a></li>
                        <li><a href="{p}service.html">Services</a></li>
                        <li><a href="{p}news_list/1.html">News</a></li>
                        <li><a href="{p}about.html">About Us</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Products</h3>
                    <ul>
                        <li><a href="{p}products.html?cat=light-duty">Light Duty Truck</a></li>
                        <li><a href="{p}products.html?cat=medium-duty">Medium Duty Truck</a></li>
                        <li><a href="{p}products.html?cat=heavy-duty">Heavy Duty Truck</a></li>
                        <li><a href="{p}products.html?cat=off-road">Off-road Truck</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Contact</h3>
                    <ul class="footer-contact">
                        <li><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg> Room 603A, Building B, Chanba Free Trade Center, Xi'an, China</li>
                        <li><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z"/></svg> +86 15319431311</li>
                        <li><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg> sales@fenghan-trade.com</li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>
    <div class="e_container-16">
        <div class="container" style="text-align:center;padding:15px 0;">
            <p style="margin:0;color:#999;font-size:13px;">&copy; 2026 Shaanxi Fenghan Trading Co., Ltd. All Rights Reserved.</p>
        </div>
    </div>
    <script src="{p}js/main.js"></script>
</body>
</html>'''


def fix_all_html_files():
    """Fix absolute paths in ALL HTML files."""
    
    # Step 1: Generate missing pages
    print("=== Step 1: Generate missing pages ===")
    for page_name, (cat, sub) in MISSING_PAGES.items():
        generate_missing_page(page_name, cat, sub)
    
    # Step 2: Fix absolute paths in all HTML files
    print("\n=== Step 2: Fix absolute paths in all HTML files ===")
    
    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip admin directory and node_modules
        if 'admin' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(Path(root) / f)
    
    total_fixed = 0
    for html_file in sorted(html_files):
        rel_path = html_file.relative_to(BASE_DIR)
        depth = len(rel_path.parts) - 1  # 0 for root, 1 for subdirectory
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Fix /Contact.html -> contact.html (case insensitive)
        content = fix_contact_case(content)
        
        # Fix absolute paths
        content = fix_absolute_paths(content, depth)
        
        # Ensure app-pages.css is referenced
        content = ensure_app_pages_css(content, depth)
        
        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            total_fixed += 1
            print(f"  FIXED: {rel_path} (depth={depth})")
        else:
            print(f"  OK: {rel_path} (no changes)")
    
    print(f"\nDone! Fixed {total_fixed}/{len(html_files)} files.")


if __name__ == '__main__':
    fix_all_html_files()
