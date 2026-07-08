#!/usr/bin/env python3
"""
Build subpages for sagmoto-website from scraped official pages.
Extracts content from sagmoto-scraped/*.html and generates clean pages
using our site's template with latest navigation.
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
SCRAPED_DIR = BASE_DIR.parent.parent / "sagmoto-scraped"
OUTPUT_DIR = BASE_DIR

# ─── Shared Templates ───────────────────────────────────────────────

def get_shared_header(active_page=""):
    """Return the shared HTML head + navigation (matches index.html)."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png">
    <script src="js/data-loader.js"></script>
'''

def get_shared_footer():
    """Return the shared footer HTML."""
    return '''
    <!-- ===== FOOTER ===== -->
    <footer class="e_container-15">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h3><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO" style="height:30px;vertical-align:middle;"> SAGMOTO</h3>
                    <p>Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. Core subsidiary dedicated to commercial vehicle manufacturing and international export.</p>
                    <div class="footer-social">
                        <a href="#" title="Facebook"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
                        <a href="#" title="YouTube"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
                        <a href="#" title="WhatsApp"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982 1.004-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.891 9.884"/></svg></a>
                    </div>
                </div>
                <div class="footer-col">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="products.html">Products</a></li>
                        <li><a href="qyc.html">Applications</a></li>
                        <li><a href="service.html">Services</a></li>
                        <li><a href="news_list/1.html">News</a></li>
                        <li><a href="about.html">About Us</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Products</h3>
                    <ul>
                        <li><a href="products.html?cat=light-duty">Light Duty Truck</a></li>
                        <li><a href="products.html?cat=medium-duty">Medium Duty Truck</a></li>
                        <li><a href="products.html?cat=heavy-duty">Heavy Duty Truck</a></li>
                        <li><a href="products.html?cat=off-road">Off-road Truck</a></li>
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
    <script src="js/main.js"></script>
</body>
</html>'''


# ─── Extract from scraped pages ─────────────────────────────────────

def extract_meta(soup):
    """Extract page title and meta description."""
    title = ""
    desc = ""
    if soup.title:
        title = soup.title.get_text(strip=True)
        # Clean: remove " - SAG Commercial Vehicle Company" suffix
        title = re.sub(r'\s*[-–|]\s*SAG\s+Commercial\s+Vehicle\s+Company.*$', '', title, flags=re.IGNORECASE)
        title = title.strip()
    
    for meta in soup.find_all('meta'):
        name = (meta.get('name') or '').lower()
        if name == 'description':
            desc = meta.get('content', '')
            break
    
    return title, desc


def extract_canonical_url(soup):
    """Extract canonical URL for relative path reference."""
    link = soup.find('link', rel='canonical')
    if link and link.get('href'):
        # Extract path from URL
        href = link['href']
        if 'sagmoto.com' in href:
            return '/' + href.split('sagmoto.com/', 1)[1] if 'sagmoto.com/' in href else href
        return href
    return None


def extract_product_cards(soup):
    """Extract all product cards from a scraped page.
    Returns list of dicts with: section_title, image_url, title, link, alt
    """
    cards = []
    
    # Find all product list sections
    for section in soup.find_all(id=re.compile(r'c_product_list')):
        section_title_el = section.find(class_='e_text-10')
        section_title = section_title_el.get_text(strip=True) if section_title_el else ""
        
        for loop_item in section.find_all(class_='cbox-4'):
            card = {'section': section_title}
            
            img_wrap = loop_item.find(class_='e_image-6')
            if img_wrap:
                img_link = img_wrap.find('a')
                if img_link:
                    card['link'] = img_link.get('href', '')
                img = img_wrap.find('img')
                if img:
                    card['image_url'] = img.get('src', '') or img.get('lazy', '') or img.get('data-src', '')
                    card['alt'] = img.get('alt', '')
                    card['title'] = img.get('title', '') or img.get('alt', '')
            
            title_el = loop_item.find(class_='e_text-7')
            if title_el:
                link_a = title_el.find('a')
                if link_a:
                    card['title'] = link_a.get_text(strip=True)
                    if not card.get('link'):
                        card['link'] = link_a.get('href', '')
            
            if card.get('title'):
                cards.append(card)
    
    return cards


def extract_text_content(soup):
    """Extract text content from service/article pages.
    Returns dict with sections list (title, content_html).
    """
    sections = []
    
    # Find article content sections
    for section in soup.find_all(id=re.compile(r'c_new_list|c_article|c_introduce_detail')):
        # Get all text-heavy elements
        title_els = section.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li'])
        texts = []
        for el in title_els:
            t = el.get_text(strip=True)
            if t and len(t) > 3:
                texts.append(t)
        if texts:
            sections.append({
                'id': section.get('id', ''),
                'html': str(section)
            })
    
    return sections


def extract_breadcrumb(soup):
    """Extract breadcrumb navigation."""
    breadcrumb_el = soup.find(class_='e_breadcrumb') or soup.find(class_='p_breadcrumb')
    if breadcrumb_el:
        items = []
        for a in breadcrumb_el.find_all('a'):
            items.append({'text': a.get_text(strip=True), 'href': a.get('href', '#')})
        for span in breadcrumb_el.find_all('span'):
            t = span.get_text(strip=True)
            if t and t != '/':
                items.append({'text': t, 'href': None})
        return items
    return None


# ─── Page Generators ─────────────────────────────────────────────────

def generate_application_page(page_name, title, meta_desc, product_cards, output_path):
    """Generate an application page (qyc, zxc, zhc, special, pzkyzyc, pzmtc)."""
    
    breadcrumb_text = page_name.replace('.html', '').replace('_', ' ').title()
    if breadcrumb_text == 'Pzkyzyc':
        breadcrumb_text = 'Off-road Dump Truck'
    elif breadcrumb_text == 'Pzmtc':
        breadcrumb_text = 'Off-road Tractor'
    elif breadcrumb_text == 'Qyc':
        breadcrumb_text = 'Tractor'
    elif breadcrumb_text == 'Zxc':
        breadcrumb_text = 'Dump Truck'
    elif breadcrumb_text == 'Zhc':
        breadcrumb_text = 'Cargo Truck'
    elif breadcrumb_text == 'Special':
        breadcrumb_text = 'Special Vehicle'
    
    # Build product cards HTML
    cards_html = ""
    current_section = None
    
    for card in product_cards:
        section = card.get('section', '')
        if section and section != current_section:
            if current_section is not None:
                cards_html += '</div>\n'
            current_section = section
            cards_html += f'''
    <section class="section-bg-gray" id="products">
        <div class="container">
            <h2 class="section-title">{current_section}</h2>
            <div class="product-grid">
'''
        
        img_url = card.get('image_url', '')
        card_title = card.get('title', 'Product')
        link = card.get('link', '#')
        
        cards_html += f'''
                <div class="product-card">
                    <a href="{link}">
                        <div class="product-card-img">
                            <img src="{img_url}" alt="{card_title}" loading="lazy">
                        </div>
                        <div class="product-card-body">
                            <h3>{card_title}</h3>
                        </div>
                    </a>
                </div>'''
    
    if current_section is not None:
        cards_html += '''
            </div>
        </div>
    </section>'''
    
    html = f'''{get_shared_header()}
    <meta name="description" content="{meta_desc or title + ' - SAGMOTO commercial vehicles'}">
    <meta name="keywords" content="SAGMOTO,{page_name.replace('.html','')},commercial vehicles,truck">
    <title>{title} - SAGMOTO</title>
</head>
<body>
    <!-- ===== TOP BAR ===== -->
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
                <a href="#">中文</a>
                <a href="#">FR</a>
            </div>
        </div>
    </div>

    <!-- ===== HEADER / NAVIGATION ===== -->
    <div class="e_container-2">
        <div class="container">
            <div class="logo-area">
                <a href="index.html">
                    <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO" class="logo-icon">
                    <span class="logo-text">SAG INTL</span>
                </a>
            </div>
            <div class="mobile-toggle">
                <span></span><span></span><span></span>
            </div>
            <ul class="main-nav">
                <li class="has-dropdown">
                    <a href="products.html">PRODUCTS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <div class="dropdown-mega">
                        <div class="mega-inner">
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Light Duty Truck(4.5T≦GCW≦25T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png" alt="i9"> i9</a></li>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/175cc731-094c-4946-880b-90aa3a1a867e.png" alt="X9"> X9</a></li>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0630693e-37e8-43be-98dd-acbdb49c70c9.png" alt="X7"> X7</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Medium Duty Truck(12T≦GCW≦60T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64c3428c-c60f-4579-ac04-e561cbe8c772.png" alt="E6"> E6</a></li>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png" alt="X6"> X6</a></li>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d2bf1d4c-09c4-426a-895a-bd8f6aba5a63.jpg" alt="X5"> X5</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Heavy Duty Truck(18T≦GCW≦100T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/84912c76-6629-4d69-ad59-d8da5940fbb4.jpg" alt="E1st"> E1st</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a32c4261-9dac-4e68-87f7-c037b5a56733.jpg" alt="Z3"> Z3</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0d2ddb14-41e9-4f6c-b60a-1b53fa89e0f3.png" alt="E3"> E3</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9aa95967-f314-494d-adbe-05935dee2d6c.png" alt="E9"> E9</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Off-road Truck</h4>
                                <ul>
                                    <li><a href="products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg" alt="Off-road"> Off-road Dump</a></li>
                                    <li><a href="products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg" alt="X3s"> X3s</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>
                <li class="has-dropdown">
                    <a href="javascript:;">APPLICATIONS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu dropdown-wide">
                        <li class="dropdown-group"><a href="qyc.html" class="dropdown-group-title">Tractor</a>
                            <ul class="dropdown-sub">
                                <li><a href="qyc.html">Port Transport</a></li>
                                <li><a href="qyc.html#c_product_list_152-16902759283320">Hazardous Chemicals Transport</a></li>
                                <li><a href="qyc.html#c_product_list_152-16902759511700">Coal Transport</a></li>
                                <li><a href="qyc.html#c_product_list_152-16902759295540">Sand And Gravel Transport</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="zxc.html" class="dropdown-group-title">Dump Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="zxc.html">Urban Construction</a></li>
                                <li><a href="zxc.html#c_product_list_152-16902759962030">Mining</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="zhc.html" class="dropdown-group-title">Cargo Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="zhc.html">Express Delivery</a></li>
                                <li><a href="zhc.html#c_product_list_152-16902759962030">Intercity Logistics</a></li>
                                <li><a href="zhc.html#c_product_list_152-16915679157520">City Distribution</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="special.html" class="dropdown-group-title">Special Vehicle</a>
                            <ul class="dropdown-sub">
                                <li><a href="special.html">City Transportation</a></li>
                                <li><a href="special.html#c_product_list_152-16889614330850">Smart Sanitation</a></li>
                                <li><a href="special.html#c_product_list_152-16889616447540">Dangerous Goods Transportation</a></li>
                                <li><a href="special.html#c_product_list_152-16902780105800">Road Work &amp; Rescue</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="pzkyzyc.html" class="dropdown-group-title">Off-road Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="pzkyzyc.html">Off-road Dump Truck</a></li>
                                <li><a href="pzmtc.html">Off-road Tractor</a></li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="service.html">SERVICES <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="service.html">Service Policy</a></li>
                        <li><a href="service_list/1674411714944516096.html">Find Your Service Provider</a></li>
                        <li><a href="service_list/1674411730417303552.html">Maintenance Service</a></li>
                        <li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>
                        <li><a href="service_list/1674411767427842048.html">Safe Driving</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="news_list/1.html">NEWS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="news_list/1.html">News Center</a></li>
                        <li><a href="video_list.html">Video Center</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="about.html">ABOUT US <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>
                        <li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>
                        <li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>
                        <li><a href="Contact.html">Contact Us</a></li>
                    </ul>
                </li>
                <li class="nav-search"><a href="#" onclick="event.preventDefault();"><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></a></li>
            </ul>
        </div>
    </div>

    <!-- ===== PAGE BANNER ===== -->
    <section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('images/hero/slide1.jpg') center/cover;">
        <div class="container">
            <div class="breadcrumb">
                <a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>{breadcrumb_text}</span>
            </div>
            <h1>{title}</h1>
            <p>APPLICATIONS</p>
        </div>
    </section>

    <!-- ===== PRODUCT CARDS ===== -->
    {cards_html}
    {get_shared_footer()}'''
    
    return html


def generate_service_page(page_name, title, meta_desc, text_sections, output_path):
    """Generate a service/article page."""
    
    breadcrumb_text = page_name
    if '1674411714944516096' in page_name:
        breadcrumb_text = 'Find Your Service Provider'
    elif '1674411730417303552' in page_name:
        breadcrumb_text = 'Maintenance Service'
    elif '1674411748220751872' in page_name:
        breadcrumb_text = 'Driving Reminder'
    elif '1674411767427842048' in page_name:
        breadcrumb_text = 'Safe Driving'
    elif page_name == 'service.html':
        breadcrumb_text = 'Service Policy'
    
    # Extract clean text from sections
    content_html = ''
    for section in text_sections:
        content_html += f'''
    <div class="service-section">
{section['html']}
    </div>'''
    
    if not content_html:
        content_html = f'''
    <div class="service-section">
        <h2>{title}</h2>
        <p>{meta_desc or "Service information from SAGMOTO."}</p>
    </div>'''
    
    html = f'''{get_shared_header()}
    <meta name="description" content="{meta_desc or title}">
    <meta name="keywords" content="SAGMOTO,service,support,maintenance">
    <title>{title} - SAGMOTO</title>
</head>
<body>
    <!-- ===== TOP BAR ===== -->
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
                <a href="#">中文</a>
                <a href="#">FR</a>
            </div>
        </div>
    </div>

    <!-- ===== HEADER / NAVIGATION ===== -->
    <div class="e_container-2">
        <div class="container">
            <div class="logo-area">
                <a href="index.html">
                    <img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" alt="SAGMOTO" class="logo-icon">
                    <span class="logo-text">SAG INTL</span>
                </a>
            </div>
            <div class="mobile-toggle">
                <span></span><span></span><span></span>
            </div>
            <ul class="main-nav">
                <li class="has-dropdown">
                    <a href="products.html">PRODUCTS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <div class="dropdown-mega">
                        <div class="mega-inner">
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Light Duty Truck(4.5T≦GCW≦25T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png" alt="i9"> i9</a></li>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/175cc731-094c-4946-880b-90aa3a1a867e.png" alt="X9"> X9</a></li>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0630693e-37e8-43be-98dd-acbdb49c70c9.png" alt="X7"> X7</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Medium Duty Truck(12T≦GCW≦60T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64c3428c-c60f-4579-ac04-e561cbe8c772.png" alt="E6"> E6</a></li>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png" alt="X6"> X6</a></li>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d2bf1d4c-09c4-426a-895a-bd8f6aba5a63.jpg" alt="X5"> X5</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Heavy Duty Truck(18T≦GCW≦100T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/84912c76-6629-4d69-ad59-d8da5940fbb4.jpg" alt="E1st"> E1st</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a32c4261-9dac-4e68-87f7-c037b5a56733.jpg" alt="Z3"> Z3</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0d2ddb14-41e9-4f6c-b60a-1b53fa89e0f3.png" alt="E3"> E3</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9aa95967-f314-494d-adbe-05935dee2d6c.png" alt="E9"> E9</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Off-road Truck</h4>
                                <ul>
                                    <li><a href="products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg" alt="Off-road"> Off-road Dump</a></li>
                                    <li><a href="products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg" alt="X3s"> X3s</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>
                <li class="has-dropdown">
                    <a href="javascript:;">APPLICATIONS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu dropdown-wide">
                        <li class="dropdown-group"><a href="qyc.html" class="dropdown-group-title">Tractor</a>
                            <ul class="dropdown-sub">
                                <li><a href="qyc.html">Port Transport</a></li>
                                <li><a href="qyc.html#c_product_list_152-16902759283320">Hazardous Chemicals Transport</a></li>
                                <li><a href="qyc.html#c_product_list_152-16902759511700">Coal Transport</a></li>
                                <li><a href="qyc.html#c_product_list_152-16902759295540">Sand And Gravel Transport</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="zxc.html" class="dropdown-group-title">Dump Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="zxc.html">Urban Construction</a></li>
                                <li><a href="zxc.html#c_product_list_152-16902759962030">Mining</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="zhc.html" class="dropdown-group-title">Cargo Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="zhc.html">Express Delivery</a></li>
                                <li><a href="zhc.html#c_product_list_152-16902759962030">Intercity Logistics</a></li>
                                <li><a href="zhc.html#c_product_list_152-16915679157520">City Distribution</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="special.html" class="dropdown-group-title">Special Vehicle</a>
                            <ul class="dropdown-sub">
                                <li><a href="special.html">City Transportation</a></li>
                                <li><a href="special.html#c_product_list_152-16889614330850">Smart Sanitation</a></li>
                                <li><a href="special.html#c_product_list_152-16889616447540">Dangerous Goods Transportation</a></li>
                                <li><a href="special.html#c_product_list_152-16902780105800">Road Work &amp; Rescue</a></li>
                            </ul>
                        </li>
                        <li class="dropdown-group"><a href="pzkyzyc.html" class="dropdown-group-title">Off-road Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="pzkyzyc.html">Off-road Dump Truck</a></li>
                                <li><a href="pzmtc.html">Off-road Tractor</a></li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="service.html">SERVICES <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="service.html">Service Policy</a></li>
                        <li><a href="service_list/1674411714944516096.html">Find Your Service Provider</a></li>
                        <li><a href="service_list/1674411730417303552.html">Maintenance Service</a></li>
                        <li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>
                        <li><a href="service_list/1674411767427842048.html">Safe Driving</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="news_list/1.html">NEWS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="news_list/1.html">News Center</a></li>
                        <li><a href="video_list.html">Video Center</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="about.html">ABOUT US <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>
                        <li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>
                        <li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>
                        <li><a href="Contact.html">Contact Us</a></li>
                    </ul>
                </li>
                <li class="nav-search"><a href="#" onclick="event.preventDefault();"><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></a></li>
            </ul>
        </div>
    </div>

    <!-- ===== PAGE BANNER ===== -->
    <section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('images/hero/slide1.jpg') center/cover;">
        <div class="container">
            <div class="breadcrumb">
                <a href="index.html">Home</a> <span>/</span> <span>Services</span> <span>/</span> <span>{breadcrumb_text}</span>
            </div>
            <h1>{title}</h1>
            <p>SERVICES</p>
        </div>
    </section>

    <!-- ===== CONTENT ===== -->
    <section class="section-bg-white">
        <div class="container">
            <div class="content-area">
{content_html}
            </div>
        </div>
    </section>
    {get_shared_footer()}'''
    
    return html


# ─── Main ───────────────────────────────────────────────────────────

PAGE_CONFIG = {
    # Application pages
    'qyc.html': 'application',
    'zxc.html': 'application',
    'zhc.html': 'application',
    'special.html': 'application',
    'pzkyzyc.html': 'application',
    'pzmtc.html': 'application',
    # Service pages
    'service.html': 'service',
    'service_list/1674411714944516096.html': 'service',
    'service_list/1674411730417303552.html': 'service',
    'service_list/1674411748220751872.html': 'service',
    'service_list/1674411767427842048.html': 'service',
    # News pages
    'news_list/1.html': 'service',
    'video_list.html': 'service',
}


def main():
    stats = {'application': 0, 'service': 0, 'errors': 0}
    
    for page_name, page_type in PAGE_CONFIG.items():
        scraped_path = SCRAPED_DIR / page_name
        output_path = OUTPUT_DIR / page_name
        
        if not scraped_path.exists():
            print(f"  SKIP: {page_name} (file not found)")
            stats['errors'] += 1
            continue
        
        # Create output directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(scraped_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        title, meta_desc = extract_meta(soup)
        
        print(f"  Processing: {page_name} → Title: {title}")
        
        if page_type == 'application':
            cards = extract_product_cards(soup)
            print(f"    Found {len(cards)} product cards in {len(set(c['section'] for c in cards))} sections")
            
            html = generate_application_page(page_name, title, meta_desc, cards, output_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            stats['application'] += 1
            
        elif page_type == 'service':
            sections = extract_text_content(soup)
            print(f"    Found {len(sections)} content sections")
            
            html = generate_service_page(page_name, title, meta_desc, sections, output_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            stats['service'] += 1
    
    print(f"\nDone! Generated: {stats['application']} application pages, {stats['service']} service/news pages")
    if stats['errors']:
        print(f"  Errors: {stats['errors']}")


if __name__ == '__main__':
    main()
