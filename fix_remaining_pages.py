#!/usr/bin/env python3
"""Fix remaining issues across sagmoto-website pages:
1. Fix footer APPLICATIONS links in about, news, index, contact, products
2. Add images to about page content sections
3. Add WhatsApp contact to contact page
4. Create Privacy Policy and Terms of Use pages
5. Fix footer Privacy/Terms/Sitemap links
6. Fix footer off-road links to include tzc.html
"""

import os
import re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sagmoto-website")

# Old footer APPLICATIONS links (pointing to products.html)
OLD_APPS_FOOTER = '''<h3>APPLICATIONS</h3>
<ul>
<li><a href="products.html?cat=heavy-duty">Tractor</a></li>
<li><a href="products.html?cat=off-road">Dump Truck</a></li>
<li><a href="products.html?cat=medium-duty">Cargo Truck</a></li>
<li><a href="products.html?cat=special">Special Vehicle</a></li>
</ul>'''

NEW_APPS_FOOTER = '''<h3>APPLICATIONS</h3>
<ul>
<li><a href="qyc.html">Tractor</a></li>
<li><a href="zxc.html">Dump Truck</a></li>
<li><a href="zhc.html">Cargo Truck</a></li>
<li><a href="special.html">Special Vehicle</a></li>
<li><a href="tzc.html">Off-road Truck</a></li>
</ul>'''

# Subdirectory version (with ../ prefix)
OLD_APPS_FOOTER_SUB = '''<h3>APPLICATIONS</h3>
<ul>
<li><a href="../products.html?cat=heavy-duty">Tractor</a></li>
<li><a href="../products.html?cat=off-road">Dump Truck</a></li>
<li><a href="../products.html?cat=medium-duty">Cargo Truck</a></li>
<li><a href="../products.html?cat=special">Special Vehicle</a></li>
</ul>'''

NEW_APPS_FOOTER_SUB = '''<h3>APPLICATIONS</h3>
<ul>
<li><a href="../qyc.html">Tractor</a></li>
<li><a href="../zxc.html">Dump Truck</a></li>
<li><a href="../zhc.html">Cargo Truck</a></li>
<li><a href="../special.html">Special Vehicle</a></li>
<li><a href="../tzc.html">Off-road Truck</a></li>
</ul>'''

# Footer Privacy/Terms/Sitemap links
OLD_FOOTER_LINKS = '<p><a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a> | <a href="#">Sitemap</a></p>'
NEW_FOOTER_LINKS = '<p><a href="privacy.html">Privacy Policy</a> | <a href="terms.html">Terms of Use</a> | <a href="index.html">Sitemap</a></p>'

# Subdirectory version
OLD_FOOTER_LINKS_SUB = '<p><a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a> | <a href="#">Sitemap</a></p>'
NEW_FOOTER_LINKS_SUB = '<p><a href="../privacy.html">Privacy Policy</a> | <a href="../terms.html">Terms of Use</a> | <a href="../index.html">Sitemap</a></p>'

def fix_file(filepath, fixes, subdir=False):
    """Apply fixes to a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new, desc in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f"  [OK] {desc}")
        else:
            print(f"  [SKIP] {desc} - pattern not found")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ===== 1. Fix footer APPLICATIONS links in original pages =====
print("=== Fixing footer APPLICATIONS links ===")
original_pages = ['about.html', 'news.html', 'index.html', 'contact.html', 'products.html']
for page in original_pages:
    filepath = os.path.join(BASE, page)
    if os.path.exists(filepath):
        print(f"Processing {page}...")
        fix_file(filepath, [
            (OLD_APPS_FOOTER, NEW_APPS_FOOTER, "APPLICATIONS footer links"),
            (OLD_FOOTER_LINKS, NEW_FOOTER_LINKS, "Privacy/Terms/Sitemap links"),
        ])

# ===== 2. Fix footer links in subdirectory pages =====
print("\n=== Fixing footer links in subdirectory pages ===")
subdir_pages = [
    'service_list/1674411714944516096.html',
    'service_list/1674411730417303552.html',
    'service_list/1674411748220751872.html',
    'service_list/1674411767427842048.html',
    'news_list/1.html',
    'news_list/81163.html',
]
for page in subdir_pages:
    filepath = os.path.join(BASE, page)
    if os.path.exists(filepath):
        print(f"Processing {page}...")
        fix_file(filepath, [
            (OLD_FOOTER_LINKS_SUB, NEW_FOOTER_LINKS_SUB, "Privacy/Terms/Sitemap links"),
        ])

# ===== 3. Add images to about page =====
print("\n=== Adding images to about page ===")
about_path = os.path.join(BASE, 'about.html')
with open(about_path, 'r', encoding='utf-8') as f:
    about_content = f.read()

# Add image to "Who We Are" section
old_who = '''<div class="about-intro">
<p>Shaanxi Fenghan Trading Co., Ltd is an authorized Shacman/SAGMOTO brand exporter, headquartered in Xi'an, Shaanxi Province. We specialize in providing vehicle pricing, configuration, and market support services for commercial vehicle customers across 7 major global regions and over 50 countries.</p>
<p>As a trusted partner of Shaanxi Automobile Holding Group, we have been dedicating to expanding the international presence of Shacman and SAGMOTO brands. Our portfolio covers <strong>tractors, dump trucks, cargo trucks, and special vehicles</strong>, serving markets across Africa, Southeast Asia, the Middle East, Central Asia, South America, and beyond — delivering reliable, cost-effective commercial vehicle solutions worldwide.</p>
</div>'''

new_who = '''<div class="about-intro">
<p>Shaanxi Fenghan Trading Co., Ltd is an authorized Shacman/SAGMOTO brand exporter, headquartered in Xi'an, Shaanxi Province. We specialize in providing vehicle pricing, configuration, and market support services for commercial vehicle customers across 7 major global regions and over 50 countries.</p>
<p>As a trusted partner of Shaanxi Automobile Holding Group, we have been dedicating to expanding the international presence of Shacman and SAGMOTO brands. Our portfolio covers <strong>tractors, dump trucks, cargo trucks, and special vehicles</strong>, serving markets across Africa, Southeast Asia, the Middle East, Central Asia, South America, and beyond — delivering reliable, cost-effective commercial vehicle solutions worldwide.</p>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:40px;">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/cc0e711f-1ba9-4c75-b3e5-a1b1e7b13f63.jpg" alt="SAGMOTO Heavy Duty Tractor" style="width:100%;height:200px;object-fit:cover;border-radius:8px;"/>
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3d9e1f41-7c2e-4da5-b7e5-5eb18f95fbc1.jpg" alt="SAGMOTO Dump Truck" style="width:100%;height:200px;object-fit:cover;border-radius:8px;"/>
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a161feeb-72a6-456a-8368-32970c2d9df0.jpg" alt="SAGMOTO Electric Truck" style="width:100%;height:200px;object-fit:cover;border-radius:8px;"/>
</div>'''

if old_who in about_content:
    about_content = about_content.replace(old_who, new_who)
    print("  [OK] Added images to Who We Are section")
else:
    print("  [SKIP] Who We Are section not found")

# Add icons to certification items
old_cert = '''<div class="cert-grid">
<div class="cert-item">
<h3>ECE R29-03</h3>
<p>Cab strength meets the latest European collision safety standards</p>
</div>
<div class="cert-item">
<h3>Euro II - Euro VI</h3>
<p>Full range of emission standards to meet diverse market requirements</p>
</div>
<div class="cert-item">
<h3>ISO 9001</h3>
<p>Quality management system certification for manufacturing excellence</p>
</div>
<div class="cert-item">
<h3>CCC / E-Mark</h3>
<p>Vehicle certification for both domestic and international markets</p>
</div>
</div>'''

new_cert = '''<div class="cert-grid">
<div class="cert-item">
<div class="cert-icon" style="font-size:36px;color:#C62828;">&#9888;</div>
<h3>ECE R29-03</h3>
<p>Cab strength meets the latest European collision safety standards</p>
</div>
<div class="cert-item">
<div class="cert-icon" style="font-size:36px;color:#0D1F3D;">&#9881;</div>
<h3>Euro II - Euro VI</h3>
<p>Full range of emission standards to meet diverse market requirements</p>
</div>
<div class="cert-item">
<div class="cert-icon" style="font-size:36px;color:#C89B3C;">&#10003;</div>
<h3>ISO 9001</h3>
<p>Quality management system certification for manufacturing excellence</p>
</div>
<div class="cert-item">
<div class="cert-icon" style="font-size:36px;color:#0D1F3D;">&#9741;</div>
<h3>CCC / E-Mark</h3>
<p>Vehicle certification for both domestic and international markets</p>
</div>
</div>'''

if old_cert in about_content:
    about_content = about_content.replace(old_cert, new_cert)
    print("  [OK] Added icons to certification section")
else:
    print("  [SKIP] Certification section not found")

with open(about_path, 'w', encoding='utf-8') as f:
    f.write(about_content)

# ===== 4. Add WhatsApp button to contact page =====
print("\n=== Adding WhatsApp to contact page ===")
contact_path = os.path.join(BASE, 'contact.html')
with open(contact_path, 'r', encoding='utf-8') as f:
    contact_content = f.read()

old_contact_details = '''<div class="contact-info-block">
<h3>Contact Details</h3>
<p>
<strong>Tel:</strong> +86 15319431311<br/>
<strong>E-mail:</strong> sales@fenghan-trade.com<br/>
<strong>Working Hours:</strong> Mon-Fri, 8:30 AM - 5:30 PM (GMT+8)
                        </p>
</div>'''

new_contact_details = '''<div class="contact-info-block">
<h3>Contact Details</h3>
<p>
<strong>Tel:</strong> <a href="tel:+8615319431311" style="color:inherit;">+86 15319431311</a><br/>
<strong>E-mail:</strong> <a href="mailto:sales@fenghan-trade.com" style="color:inherit;">sales@fenghan-trade.com</a><br/>
<strong>WhatsApp:</strong> <a href="https://wa.me/8615319431311" target="_blank" style="color:#25D366;font-weight:bold;">+86 15319431311</a><br/>
<strong>Working Hours:</strong> Mon-Fri, 8:30 AM - 5:30 PM (GMT+8)
                        </p>
</div>'''

if old_contact_details in contact_content:
    contact_content = contact_content.replace(old_contact_details, new_contact_details)
    print("  [OK] Added WhatsApp contact")
else:
    print("  [SKIP] Contact details section not found")

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(contact_content)

# ===== 5. Create Privacy Policy page =====
print("\n=== Creating Privacy Policy page ===")
privacy_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta content="SAGMOTO Privacy Policy - How we collect, use, and protect your personal information." name="description"/>
<title>Privacy Policy - SAGMOTO</title>
<link rel="stylesheet" href="css/style.css"/>
<link rel="stylesheet" href="css/app-pages.css"/>
</head>
<body>
<header class="e_container-2">
<div class="container">
<div class="logo">
<a href="index.html"><img alt="SAGMOTO" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" style="height:50px;"/></a>
</div>
<nav class="main-nav">
<ul class="nav-list">
<li class="has-dropdown">
<a href="products.html">PRODUCTS</a>
<ul class="dropdown-menu">
<li><a href="products.html?cat=light-duty">Light Duty Truck</a></li>
<li><a href="products.html?cat=medium-duty">Medium Duty Truck</a></li>
<li><a href="products.html?cat=heavy-duty">Heavy Duty Truck</a></li>
<li><a href="products.html?cat=off-road">Off-road Truck</a></li>
<li><a href="products.html?cat=special">Special Vehicle</a></li>
<li><a href="products.html?cat=newenergy">New Energy</a></li>
</ul>
</li>
<li class="has-dropdown">
<a href="javascript:;">APPLICATIONS</a>
<ul class="dropdown-menu">
<li><a href="qyc.html">Tractor Application</a></li>
<li><a href="zxc.html">Dump Truck Application</a></li>
<li><a href="zhc.html">Cargo Truck Application</a></li>
<li><a href="special.html">Special Vehicle Application</a></li>
</ul>
</li>
<li class="has-dropdown">
<a href="tzc.html">OFF-ROAD</a>
<ul class="dropdown-menu">
<li><a href="pzkyzyc.html">Off-road Dump Truck</a></li>
<li><a href="pzmtc.html">Off-road Tractor</a></li>
<li><a href="tzc.html">Off-road Truck Series</a></li>
</ul>
</li>
<li><a href="service.html">SERVICES</a></li>
<li><a href="video_list.html">VIDEO CENTER</a></li>
<li><a href="news_list/1.html">NEWS</a></li>
<li><a href="about.html">ABOUT US</a></li>
<li><a href="contact.html">CONTACT US</a></li>
</ul>
</nav>
</div>
</header>
<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('images/hero/slide6.jpg') center/cover;">
<div class="container">
<div class="breadcrumb">
<a href="index.html">Home</a> <span>/</span> <span>Privacy Policy</span>
</div>
<h1>Privacy Policy</h1>
<p>Last Updated: July 2026</p>
</div>
</section>
<section class="section-bg-white">
<div class="container">
<div class="article-content" style="max-width:800px;margin:0 auto;">
<h2>1. Information We Collect</h2>
<p>When you contact us through our website, forms, email, or phone, we may collect the following information:</p>
<ul style="padding-left:20px;line-height:1.8;">
<li>Your name and company/organization name</li>
<li>Email address and phone/WhatsApp number</li>
<li>Country and region of interest</li>
<li>Product inquiry details and specifications</li>
<li>Communications and correspondence</li>
</ul>

<h2>2. How We Use Your Information</h2>
<p>We use the collected information to:</p>
<ul style="padding-left:20px;line-height:1.8;">
<li>Respond to your inquiries and provide product information</li>
<li>Process orders and provide quotations</li>
<li>Provide after-sales support and maintenance services</li>
<li>Send you relevant product updates and newsletters (with your consent)</li>
<li>Improve our products, services, and website</li>
</ul>

<h2>3. Information Sharing</h2>
<p>We do not sell, trade, or rent your personal information to third parties. We may share your information with:</p>
<ul style="padding-left:20px;line-height:1.8;">
<li>Authorized SAGMOTO distributors and service providers in your region (for service delivery)</li>
<li>Shipping and logistics partners (for order fulfillment)</li>
<li>Legal authorities when required by applicable laws</li>
</ul>

<h2>4. Data Security</h2>
<p>We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. These measures include encrypted data transmission, secure servers, and restricted access protocols.</p>

<h2>5. Cookies</h2>
<p>Our website may use cookies to enhance your browsing experience. Cookies are small text files stored on your device. You can configure your browser to refuse cookies, but some features of the website may not function properly.</p>

<h2>6. Your Rights</h2>
<p>You have the right to:</p>
<ul style="padding-left:20px;line-height:1.8;">
<li>Request access to your personal data</li>
<li>Request correction of inaccurate data</li>
<li>Request deletion of your personal data</li>
<li>Opt out of marketing communications at any time</li>
</ul>

<h2>7. Contact Us</h2>
<p>If you have any questions about this Privacy Policy, please contact us at:</p>
<p>
<strong>Email:</strong> sales@fenghan-trade.com<br/>
<strong>Phone:</strong> +86 15319431311<br/>
<strong>Address:</strong> Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue, Chanba Ecological District, Xi'an, Shaanxi, China
</p>
</div>
</div>
</section>
<footer class="e_container-30">
<div class="container">
<div class="footer-grid">
<div class="footer-col">
<h3>PRODUCTS</h3>
<ul>
<li><a href="products.html?cat=light-duty">Light Duty Truck<span class="sub">(4.5T&#8804;GCW&#8804;25T)</span></a></li>
<li><a href="products.html?cat=medium-duty">Medium Duty Truck<span class="sub">(12T&#8804;GCW&#8804;60T)</span></a></li>
<li><a href="products.html?cat=heavy-duty">Heavy Duty Truck<span class="sub">(18T&#8804;GCW&#8804;100T)</span></a></li>
<li><a href="products.html?cat=off-road">Off-road Truck</a></li>
</ul>
</div>
<div class="footer-col">
<h3>APPLICATIONS</h3>
<ul>
<li><a href="qyc.html">Tractor</a></li>
<li><a href="zxc.html">Dump Truck</a></li>
<li><a href="zhc.html">Cargo Truck</a></li>
<li><a href="special.html">Special Vehicle</a></li>
<li><a href="tzc.html">Off-road Truck</a></li>
</ul>
</div>
<div class="footer-col">
<h3>CONTACT US</h3>
<p><strong>Tel:</strong> +86 15319431311<br/><strong>E-mail:</strong> sales@fenghan-trade.com</p>
</div>
</div>
<div class="footer-bottom">
<p>&copy; 2026 SAGMOTO | All Rights Reserved</p>
<p><a href="privacy.html">Privacy Policy</a> | <a href="terms.html">Terms of Use</a> | <a href="index.html">Sitemap</a></p>
</div>
</div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
<script src="js/main.js"></script>
</body>
</html>'''

with open(os.path.join(BASE, 'privacy.html'), 'w', encoding='utf-8') as f:
    f.write(privacy_html)
print("  [OK] Created privacy.html")

# ===== 6. Create Terms of Use page =====
print("\n=== Creating Terms of Use page ===")
terms_html = privacy_html.replace(
    '<title>Privacy Policy - SAGMOTO</title>',
    '<title>Terms of Use - SAGMOTO</title>'
).replace(
    'SAGMOTO Privacy Policy - How we collect, use, and protect your personal information.',
    'SAGMOTO Terms of Use - Terms and conditions for using our website and services.'
).replace(
    '<span>Privacy Policy</span>',
    '<span>Terms of Use</span>'
).replace(
    '<h1>Privacy Policy</h1>',
    '<h1>Terms of Use</h1>'
).replace(
    '<p>Last Updated: July 2026</p>',
    '<p>Last Updated: July 2026</p>'
)

# Replace the article content
terms_article = '''<div class="article-content" style="max-width:800px;margin:0 auto;">
<h2>1. Acceptance of Terms</h2>
<p>By accessing and using the SAGMOTO website (sagmoto.com), you accept and agree to be bound by these Terms of Use. If you do not agree with any part of these terms, please do not use our website.</p>

<h2>2. Use of Website</h2>
<p>You may use this website for lawful purposes only. You agree not to:</p>
<ul style="padding-left:20px;line-height:1.8;">
<li>Use the website in any way that violates applicable laws or regulations</li>
<li>Attempt to gain unauthorized access to any part of the website</li>
<li>Reproduce, duplicate, or sell any content without prior written permission</li>
<li>Use automated scripts to extract data from the website</li>
<li>Post or transmit any content that is defamatory, offensive, or infringes intellectual property rights</li>
</ul>

<h2>3. Intellectual Property</h2>
<p>All content on this website, including text, graphics, logos, images, and software, is the property of SAGMOTO or its content suppliers and is protected by international copyright laws. Product names, model numbers, and specifications are trademarks of SAGMOTO.</p>

<h2>4. Product Information</h2>
<p>While we strive to provide accurate and up-to-date product information, specifications, and pricing, we do not warrant that all information is error-free. Product availability, specifications, and prices may change without notice. Please contact us for the most current information.</p>

<h2>5. Export Compliance</h2>
<p>SAGMOTO vehicles and related products are subject to export control laws and regulations. Buyers are responsible for compliance with all applicable import and export laws in their respective countries.</p>

<h2>6. Limitation of Liability</h2>
<p>SAGMOTO shall not be liable for any direct, indirect, incidental, consequential, or punitive damages arising from the use of, or inability to use, this website or its content. The website is provided "as is" without warranties of any kind.</p>

<h2>7. Third-Party Links</h2>
<p>This website may contain links to third-party websites. We are not responsible for the content, privacy policies, or practices of any third-party websites. Accessing these links is at your own risk.</p>

<h2>8. Changes to Terms</h2>
<p>We reserve the right to modify these Terms of Use at any time. Changes will be effective immediately upon posting on this website. Continued use of the website after changes constitutes acceptance of the updated terms.</p>

<h2>9. Contact Us</h2>
<p>If you have any questions about these Terms of Use, please contact us at:</p>
<p>
<strong>Email:</strong> sales@fenghan-trade.com<br/>
<strong>Phone:</strong> +86 15319431311<br/>
<strong>Address:</strong> Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue, Chanba Ecological District, Xi'an, Shaanxi, China
</p>
</div>'''

# Replace the privacy article content with terms article
old_article_start = '<div class="article-content" style="max-width:800px;margin:0 auto;">'
old_article_end = '</div>\n</div>\n</section>'
idx_start = terms_html.find(old_article_start)
idx_end = terms_html.find(old_article_end, idx_start)
if idx_start != -1 and idx_end != -1:
    terms_html = terms_html[:idx_start] + terms_article + terms_html[idx_end + len(old_article_end):]
    # Re-add the closing tags
    terms_html = terms_html.replace(terms_article, terms_article + '\n</div>\n</section>')

with open(os.path.join(BASE, 'terms.html'), 'w', encoding='utf-8') as f:
    f.write(terms_html)
print("  [OK] Created terms.html")

# ===== 7. Fix footer APPLICATIONS links in subdirectory pages too =====
print("\n=== Fixing footer APPLICATIONS links in subdirectory pages ===")
for page in subdir_pages:
    filepath = os.path.join(BASE, page)
    if os.path.exists(filepath):
        print(f"Processing {page}...")
        fix_file(filepath, [
            (OLD_APPS_FOOTER_SUB, NEW_APPS_FOOTER_SUB, "APPLICATIONS footer links"),
        ])

# ===== 8. Fix footer APPLICATIONS in the 9 main custom pages (already done by fix_all_pages.py, but verify) =====
print("\n=== Verifying main custom pages ===")
main_pages = ['qyc.html', 'zxc.html', 'zhc.html', 'special.html', 'pzkyzyc.html', 'pzmtc.html', 'tzc.html', 'service.html', 'video_list.html']
for page in main_pages:
    filepath = os.path.join(BASE, page)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if OLD_APPS_FOOTER in content:
            print(f"  [FIX] {page} - still has old APPLICATIONS links")
            content = content.replace(OLD_APPS_FOOTER, NEW_APPS_FOOTER)
            content = content.replace(OLD_FOOTER_LINKS, NEW_FOOTER_LINKS)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        elif OLD_FOOTER_LINKS in content:
            print(f"  [FIX] {page} - still has old Privacy/Terms links")
            content = content.replace(OLD_FOOTER_LINKS, NEW_FOOTER_LINKS)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"  [OK] {page} - already correct")

print("\n=== All fixes complete! ===")
