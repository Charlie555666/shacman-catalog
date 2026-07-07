#!/usr/bin/env python3
"""
Rebuild all sagmoto-website sub-pages as custom pages.
Uses the same CSS/JS/nav/footer as about.html and products.html.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== HEADER TEMPLATE (from about.html) =====
HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css" rel="stylesheet"/>
<link href="css/style.css" rel="stylesheet"/>
<link rel="stylesheet" href="css/app-pages.css">
<link href="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" rel="icon"/>
<script src="js/data-loader.js"></script>
{meta}
<title>{title}</title>
</head>
<body>
<!-- ===== TOP BAR ===== -->
<div class="e_container-1">
<div class="container">
<div class="top-contact">
<a href="tel:+8615319431311">
<svg height="14" viewbox="0 0 24 24" width="14"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z" fill="currentColor"></path></svg>
                    +86 15319431311
                </a>
<a href="mailto:sales@fenghan-trade.com">
<svg height="14" viewbox="0 0 24 24" width="14"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="currentColor"></path></svg>
                    sales@fenghan-trade.com
                </a>
</div>
<div class="lang-selector">
<a class="active" href="#">EN</a>
<a href="#">\u4e2d\u6587</a>
<a href="#">FR</a>
</div>
</div>
</div>
<!-- ===== HEADER / NAVIGATION ===== -->
<div class="e_container-2">
<div class="container">
<div class="logo-area">
<a href="index.html">
<img alt="SAGMOTO" class="logo-icon" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png"/>
<span class="logo-text">SAG INTL</span>
</a>
</div>
<div class="mobile-toggle">
<span></span>
<span></span>
<span></span>
</div>
<ul class="main-nav"><li class="has-dropdown">
<a href="products.html">PRODUCTS <svg class="nav-arrow" height="10" viewbox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<div class="dropdown-mega">
<div class="mega-inner">
<div class="mega-col">
<h4 class="mega-cat-title">Light Duty Truck(4.5T\u2264GCW\u226425T)</h4>
<ul>
<li><a href="products.html?cat=light-duty"><img alt="i9" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png"/> i9</a></li>
<li><a href="products.html?cat=light-duty"><img alt="X9" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/175cc731-094c-4946-880b-90aa3a1a867e.png"/> X9</a></li>
<li><a href="products.html?cat=light-duty"><img alt="X7" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0630693e-37e8-43be-98dd-acbdb49c70c9.png"/> X7</a></li>
</ul>
</div>
<div class="mega-col">
<h4 class="mega-cat-title">Medium Duty Truck(12T\u2264GCW\u226460T)</h4>
<ul>
<li><a href="products.html?cat=medium-duty"><img alt="E6" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64c3428c-c60f-4579-ac04-e561cbe8c772.png"/> E6</a></li>
<li><a href="products.html?cat=medium-duty"><img alt="X6" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png"/> X6</a></li>
<li><a href="products.html?cat=medium-duty"><img alt="X5" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d2bf1d4c-09c4-426a-895a-bd8f6aba5a63.jpg"/> X5</a></li>
</ul>
</div>
<div class="mega-col">
<h4 class="mega-cat-title">Heavy Duty Truck(18T\u2264GCW\u2264100T)</h4>
<ul>
<li><a href="products.html?cat=heavy-duty"><img alt="E1st" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/84912c76-6629-4d69-ad59-d8da5940fbb4.jpg"/> E1st</a></li>
<li><a href="products.html?cat=heavy-duty"><img alt="Z3" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a32c4261-9dac-4e68-87f7-c037b5a56733.jpg"/> Z3</a></li>
<li><a href="products.html?cat=heavy-duty"><img alt="E3" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0d2ddb14-41e9-4f6c-b60a-1b53fa89e0f3.png"/> E3</a></li>
<li><a href="products.html?cat=heavy-duty"><img alt="E9" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9aa95967-f314-494d-adbe-05935dee2d6c.png"/> E9</a></li>
</ul>
</div>
<div class="mega-col">
<h4 class="mega-cat-title">Off-road Truck</h4>
<ul>
<li><a href="products.html?cat=off-road"><img alt="Off-road" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg"/> Off-road Dump</a></li>
<li><a href="products.html?cat=off-road"><img alt="X3s" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg"/> X3s</a></li>
</ul>
</div>
</div>
</div>
</li>
<li class="has-dropdown">
<a href="javascript:;">APPLICATIONS <svg class="nav-arrow" height="10" viewbox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu dropdown-wide">
<li class="dropdown-group"><a class="dropdown-group-title" href="qyc.html">Tractor</a>
<ul class="dropdown-sub">
<li><a href="qyc.html">Port Transport</a></li>
<li><a href="qyc.html#hazchem">Hazardous Chemicals Transport</a></li>
<li><a href="qyc.html#coal">Coal Transport</a></li>
<li><a href="qyc.html#sand">Sand And Gravel Transport</a></li>
</ul></li>
<li class="dropdown-group"><a class="dropdown-group-title" href="zxc.html">Dump Truck</a>
<ul class="dropdown-sub">
<li><a href="zxc.html">Urban Construction</a></li>
<li><a href="zxc.html#mining">Mining</a></li>
</ul></li>
<li class="dropdown-group"><a class="dropdown-group-title" href="zhc.html">Cargo Truck</a>
<ul class="dropdown-sub">
<li><a href="zhc.html">Express Delivery</a></li>
<li><a href="zhc.html#intercity">Intercity Logistics</a></li>
<li><a href="zhc.html#city-dist">City Distribution</a></li>
</ul></li>
<li class="dropdown-group"><a class="dropdown-group-title" href="special.html">Special Vehicle</a>
<ul class="dropdown-sub">
<li><a href="special.html">City Transportation</a></li>
<li><a href="special.html#sanitation">Smart Sanitation</a></li>
<li><a href="special.html#dangerous-goods">Dangerous Goods Transportation</a></li>
<li><a href="special.html#rescue">Road Work &amp; Rescue</a></li>
</ul></li>
<li class="dropdown-group"><a class="dropdown-group-title" href="pzkyzyc.html">Off-road Truck</a>
<ul class="dropdown-sub">
<li><a href="pzkyzyc.html">Off-road Dump Truck</a></li>
<li><a href="pzmtc.html">Off-road Tractor</a></li>
</ul></li>
</ul>
</li>
<li class="has-dropdown">
<a href="service.html">SERVICES <svg class="nav-arrow" height="10" viewbox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu">
<li><a href="service.html">Service Policy</a></li>
<li><a href="service_list/1674411714944516096.html">Find Your Service Provider</a></li>
<li><a href="service_list/1674411730417303552.html">Maintenance Service</a></li>
<li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>
<li><a href="service_list/1674411767427842048.html">Safe Driving</a></li>
</ul>
</li>
<li class="has-dropdown">
<a href="news_list/1.html">NEWS <svg class="nav-arrow" height="10" viewbox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu">
<li><a href="news_list/1.html">News Center</a></li>
<li><a href="video_list.html">Video Center</a></li>
</ul>
</li>
<li class="has-dropdown">
<a href="about.html">ABOUT US <svg class="nav-arrow" height="10" viewbox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu">
<li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>
<li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>
<li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>
<li><a href="contact.html">Contact Us</a></li>
</ul>
</li>
<li class="nav-search"><a href="#" onclick="event.preventDefault();"><svg height="16" viewbox="0 0 24 24" width="16"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" fill="currentColor"></path></svg></a></li></ul>
</div>
</div>
'''

# ===== FOOTER TEMPLATE (from about.html) =====
FOOTER = '''
<!-- ===== FOOTER ===== -->
<footer class="e_container-30">
<div class="container">
<div class="footer-grid">
<div class="footer-col">
<h3>PRODUCTS</h3>
<ul>
<li><a href="products.html?cat=light-duty">Light Duty Truck<span class="sub">(4.5T\u2264GCW\u226425T)</span></a></li>
<li><a href="products.html?cat=medium-duty">Medium Duty Truck<span class="sub">(12T\u2264GCW\u226460T)</span></a></li>
<li><a href="products.html?cat=heavy-duty">Heavy Duty Truck<span class="sub">(18T\u2264GCW\u2264100T)</span></a></li>
<li><a href="products.html?cat=heavy-duty">E1st</a></li>
<li><a href="products.html?cat=off-road">Off-road Truck</a></li>
<li><a href="products.html?cat=off-road">Off-road Dump Truck</a></li>
</ul>
</div>
<div class="footer-col">
<h3>APPLICATIONS</h3>
<ul>
<li><a href="qyc.html">Tractor</a></li>
<li><a href="zxc.html">Dump Truck</a></li>
<li><a href="zhc.html">Cargo Truck</a></li>
<li><a href="special.html">Special Vehicle</a></li>
<li><a href="pzkyzyc.html">Off-road Truck</a></li>
</ul>
</div>
<div class="footer-col">
<h3>CONTACT US</h3>
<p>
<strong>Address:</strong><br/>
                        Room 603A, Floor 6, Building B,<br/>
                        Chanba Free Trade Center, No.777 Eurasia Avenue,<br/>
                        Chanba Ecological District, Xi'an, Shaanxi, China
                    </p>
<p>
<strong>Tel:</strong> +86 15319431311<br/>
<strong>E-mail:</strong> sales@fenghan-trade.com
                    </p>
</div>
<div class="footer-col qr-code">
<h3>FOLLOW US</h3>
<img alt="SAGMOTO QR Code" src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png"/>
<p>Scan to visit our mobile site</p>
</div>
</div>
<div class="footer-bottom">
<p>\u00a9 2026 SAGMOTO | \u9655\u6c7d\u96c6\u56e2\u5546\u7528\u8f66\u6709\u9650\u516c\u53f8 | All Rights Reserved</p>
<p><a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a> | <a href="#">Sitemap</a></p>
</div>
</div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
<script src="js/main.js"></script>
</body>
</html>
'''

# ===== HELPER =====
def make_page(meta, title, body_content, subdir_prefix=""):
    """Build a complete HTML page."""
    # Adjust paths for subdirectory pages
    header = HEADER
    footer = FOOTER
    if subdir_prefix:
        header = header.replace('href="css/', f'href="{subdir_prefix}css/')
        header = header.replace('src="js/', f'src="{subdir_prefix}js/')
        header = header.replace('href="https://cdn', f'href="{subdir_prefix}https://cdn')  # CDN stays same actually
        header = header.replace('href="index.html"', f'href="{subdir_prefix}index.html"')
        header = header.replace('href="products.html', f'href="{subdir_prefix}products.html')
        header = header.replace('href="qyc.html', f'href="{subdir_prefix}qyc.html')
        header = header.replace('href="zxc.html', f'href="{subdir_prefix}zxc.html')
        header = header.replace('href="zhc.html', f'href="{subdir_prefix}zhc.html')
        header = header.replace('href="special.html', f'href="{subdir_prefix}special.html')
        header = header.replace('href="pzkyzyc.html', f'href="{subdir_prefix}pzkyzyc.html')
        header = header.replace('href="pzmtc.html', f'href="{subdir_prefix}pzmtc.html')
        header = header.replace('href="tzc.html', f'href="{subdir_prefix}tzc.html')
        header = header.replace('href="service.html', f'href="{subdir_prefix}service.html')
        header = header.replace('href="about.html', f'href="{subdir_prefix}about.html')
        header = header.replace('href="contact.html', f'href="{subdir_prefix}contact.html')
        header = header.replace('href="news_list/', f'href="{subdir_prefix}news_list/')
        header = header.replace('href="video_list.html', f'href="{subdir_prefix}video_list.html')
        header = header.replace('href="service_list/', f'href="{subdir_prefix}service_list/')
        header = header.replace('href="javascript:;', 'href="javascript:;')

        footer = footer.replace('href="products.html', f'href="{subdir_prefix}products.html')
        footer = footer.replace('href="qyc.html', f'href="{subdir_prefix}qyc.html')
        footer = footer.replace('href="zxc.html', f'href="{subdir_prefix}zxc.html')
        footer = footer.replace('href="zhc.html', f'href="{subdir_prefix}zhc.html')
        footer = footer.replace('href="special.html', f'href="{subdir_prefix}special.html')
        footer = footer.replace('href="pzkyzyc.html', f'href="{subdir_prefix}pzkyzyc.html')
        footer = footer.replace('src="js/', f'src="{subdir_prefix}js/')

        # Fix CDN links back (they shouldn't have prefix)
        header = header.replace(f'{subdir_prefix}https://cdn', 'https://cdn')
        # Fix image URLs (they shouldn't have prefix)
        header = header.replace(f'{subdir_prefix}https://omo-oss', 'https://omo-oss')

    full = header + body_content + footer
    return full

def page_banner(breadcrumb, h1, subtitle, bg_image='images/hero/slide1.jpg'):
    return f'''<!-- ===== PAGE BANNER ===== -->
<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('{bg_image}') center/cover;">
<div class="container">
<div class="breadcrumb">
{breadcrumb}
</div>
<h1>{h1}</h1>
<p>{subtitle}</p>
</div>
</section>
'''

def product_card(name, spec, desc, image, link="products.html"):
    return f'''<div class="product-card">
<a href="{link}"><img src="{image}" alt="{name}"/></a>
<h3>{name}</h3>
<p class="spec">{spec}</p>
<p class="desc">{desc}</p>
<a href="{link}" class="btn-learn">Learn More &rsaquo;</a>
</div>'''

def application_section(section_id, title, desc, products):
    cards = "\n".join(product_card(p['name'], p['spec'], p['desc'], p['image'], p.get('link', 'products.html')) for p in products)
    return f'''<!-- ===== {title} ===== -->
<section class="section-bg-white" id="{section_id}">
<div class="container">
<div class="s_title">
<h2>{title}</h2>
<p>{desc}</p>
</div>
<div class="product-grid">
{cards}
</div>
</div>
</section>'''

# ===== PAGE: qyc.html (Tractor Application) =====
def build_qyc():
    meta = '<meta content="SAGMOTO Tractor Trucks for Port Transport, Hazardous Chemicals Transport, Coal Transport, and Sand & Gravel Transport. Heavy-duty tractor trucks 18T-100T GCW." name="description"/>\n<meta content="tractor truck, port transport, hazardous chemicals, coal transport, sand gravel, heavy duty tractor" name="keywords"/>'
    title = "Tractor Application - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Tractor</span>',
        "Tractor Applications",
        "HEAVY-DUTY TRACTOR SOLUTIONS"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Tractor Truck Applications</h2>
<p>SAGMOTO tractor trucks are engineered for diverse transportation scenarios, delivering reliability, efficiency, and safety across port operations, hazardous material handling, bulk cargo, and construction material logistics.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Power &amp; Efficiency</h3>
<p>Powered by Cummins and Yuchai engines ranging from 340HP to 560HP, matched with Eaton AMT gearboxes and Hande maintenance-free axles for optimal fuel economy and power delivery.</p>
</div>
<div class="about-feature">
<h3>Safety First</h3>
<p>Cab strength meets the latest European ECE R29-03 collision standards. Dual warning systems, advanced braking, and intelligent driver assistance ensure maximum safety.</p>
</div>
<div class="about-feature">
<h3>Versatile Configurations</h3>
<p>Available in 4x2, 6x4, and 6x2 configurations with wheelbase options from 3200mm to 4500mm, adaptable to various trailer types and operating conditions.</p>
</div>
</div>
</div>
</section>
'''

    # Port Transport
    body += application_section('port', 'Port Transport',
        'Efficient container handling and short-haul operations at ports and terminals. Optimized for frequent start-stop cycles and tight maneuvering.',
        [
            {'name': 'E3 Tractor Truck', 'spec': 'Yuchai 340-400HP | 4x2', 'desc': 'Efficient power chain for port operations with excellent maneuverability and low fuel consumption.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4ed9de22-91e5-4290-8c61-65f41329d720.jpg'},
            {'name': 'Z3 Tractor Truck', 'spec': 'Cummins M13 520HP | 6x4', 'desc': 'Premium cab with flat-floor design for enhanced driver comfort during long shifts.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg'},
        ])

    # Hazardous Chemicals Transport
    body += application_section('hazchem', 'Hazardous Chemicals Transport',
        'Specialized configurations for safe transportation of hazardous materials with enhanced safety systems and anti-static protection.',
        [
            {'name': 'E1st Tractor', 'spec': 'Cummins Z14 560HP | 6x4', 'desc': 'Flagship model with intelligent safety systems and maximum power for heavy chemical tanker transport.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg'},
            {'name': 'E3 Tractor Truck', 'spec': 'Yuchai 340-400HP | 4x2', 'desc': 'Reliable and cost-effective solution for regional chemical distribution with dual warning systems.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4ed9de22-91e5-4290-8c61-65f41329d720.jpg'},
        ])

    # Coal Transport
    body += application_section('coal', 'Coal Transport',
        'Rugged and durable tractors designed for the demanding conditions of coal mining regions with excellent climbing ability and heat resistance.',
        [
            {'name': 'Z3 Tractor Truck', 'spec': 'Cummins M13 520HP | 6x4', 'desc': 'High-strength cab and powerful engine ideal for heavy coal transport in challenging terrain.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg'},
            {'name': 'X3s Trailer Truck', 'spec': 'Cummins ISME 420HP | 6x4', 'desc': 'Versatile tractor with excellent power-to-weight ratio for regional coal logistics.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/70f1e68f-95be-4336-9449-5dbe2e82e895.png'},
        ])

    # Sand & Gravel Transport
    body += application_section('sand', 'Sand And Gravel Transport',
        'Built for construction material logistics with reinforced chassis and high-load capacity for aggregate and bulk material hauling.',
        [
            {'name': 'E3 Tractor Truck', 'spec': 'Yuchai 340-400HP | 4x2', 'desc': 'Cost-effective solution for construction material transport with excellent chassis configuration.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4ed9de22-91e5-4290-8c61-65f41329d720.jpg'},
            {'name': 'E1st Tractor', 'spec': 'Cummins Z14 560HP | 6x4', 'desc': 'Maximum power and advanced aerodynamics for high-tonnage aggregate transport.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg'},
        ])

    # CTA
    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need a Tractor Solution?</h2>
<p>Contact our team for customized tractor truck configurations tailored to your specific application.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: zxc.html (Dump Truck Application) =====
def build_zxc():
    meta = '<meta content="SAGMOTO Dump Trucks for Urban Construction and Mining applications. Rugged, high-capacity dump trucks for construction sites and mining operations." name="description"/>\n<meta content="dump truck, urban construction, mining, construction truck, mining truck, heavy duty dump" name="keywords"/>'
    title = "Dump Truck Application - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Dump Truck</span>',
        "Dump Truck Applications",
        "RUGGED & RELIABLE DUMP SOLUTIONS"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Dump Truck Applications</h2>
<p>SAGMOTO dump trucks are built tough for the most demanding construction and mining environments. With reinforced chassis, high-strength steel bodies, and powerful engines, they deliver unmatched performance and durability.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Reinforced Structure</h3>
<p>High-strength steel frame and wear-resistant body design ensure long service life even under the most challenging loading conditions.</p>
</div>
<div class="about-feature">
<h3>High Load Capacity</h3>
<p>Available in 6x4 and 8x4 configurations with payload capacities from 15T to 40T, meeting diverse construction and mining requirements.</p>
</div>
<div class="about-feature">
<h3>All-Condition Capability</h3>
<p>Advanced suspension systems and optional all-wheel drive enable operation on rough terrain, steep grades, and soft ground conditions.</p>
</div>
</div>
</div>
</section>
'''

    body += application_section('urban', 'Urban Construction',
        'Designed for city construction sites with excellent maneuverability, low noise operation, and efficient material handling for urban infrastructure projects.',
        [
            {'name': 'X9 4X4 Dump Truck', 'spec': '4x4 AWD | 4.5T-25T GCW', 'desc': 'All-wheel drive dump truck with strong bearing capacity and low maintenance cost for urban construction.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3f35ad3a-2ea6-42cb-bb86-2af2c12a16e7.jpg'},
            {'name': 'X6 Dropside Truck', 'spec': '12T-60T GCW | Cummins ISD', 'desc': 'Versatile dropside with low fuel consumption and airbag seats for comfortable urban operation.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png'},
        ])

    body += application_section('mining', 'Mining',
        'Heavy-duty dump trucks engineered for the extreme conditions of mining operations with reinforced suspensions and high-temperature resistance.',
        [
            {'name': 'Off-road Dump Truck', 'spec': '850 Wide Chassis | 30.5T Load', 'desc': 'Specialized rear suspension for mining with directional exhaust to minimize dust. Adaptable to poor road conditions.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg'},
            {'name': '9 Series Off-road', 'spec': 'Yuchai/Cummins 400HP | Mining', 'desc': 'Multiple cab options with high load-bearing capacity. Adaptable to fuel tankers, sprinklers, and dump trucks.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8065c0e4-5d81-4f00-97c1-6026bc4ef78c.jpg'},
        ])

    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need a Dump Truck Solution?</h2>
<p>Contact our team for customized dump truck configurations for your construction or mining project.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: zhc.html (Cargo Truck Application) =====
def build_zhc():
    meta = '<meta content="SAGMOTO Cargo Trucks for Express Delivery, Intercity Logistics, and City Distribution. Versatile cargo trucks 4.5T-60T GCW." name="description"/>\n<meta content="cargo truck, express delivery, intercity logistics, city distribution, freight truck, logistics" name="keywords"/>'
    title = "Cargo Truck Application - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Cargo Truck</span>',
        "Cargo Truck Applications",
        "EFFICIENT LOGISTICS SOLUTIONS"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Cargo Truck Applications</h2>
<p>From last-mile city distribution to long-haul intercity freight, SAGMOTO cargo trucks deliver the versatility, efficiency, and reliability that modern logistics demands. With multiple wheelbase and body options, we configure the perfect truck for your specific logistics needs.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Fuel Efficiency</h3>
<p>Advanced powertrain optimization and low-rolling-resistance tires deliver up to 15% better fuel economy compared to conventional designs.</p>
</div>
<div class="about-feature">
<h3>Driver Comfort</h3>
<p>Airbag shock-absorbing seats, spacious sleeper berths up to 850mm wide, and sedan-like interiors reduce driver fatigue on long routes.</p>
</div>
<div class="about-feature">
<h3>Flexible Configurations</h3>
<p>Available as flatbed, dropside, box van, and refrigerated bodies with wheelbase options from 3300mm to 6500mm for any cargo requirement.</p>
</div>
</div>
</div>
</section>
'''

    body += application_section('express', 'Express Delivery',
        'Time-critical delivery solutions with optimized powertrains for high-speed long-distance transport and rapid turnaround.',
        [
            {'name': 'X6 Dropside Truck', 'spec': '12T-60T GCW | Cummins ISD 210HP', 'desc': 'Efficient transmission + maintenance-free axles + low-rolling-resistance tires for lower fuel consumption.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png'},
            {'name': 'X7 Flatbed Truck', 'spec': '4.5T-25T GCW | Yuchai 160HP', 'desc': 'Semi-floating cab with airbag seat and pointer+LCD dashboard for comfortable and efficient delivery operations.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/57b40134-f17a-4635-9862-4918881781b5.png'},
        ])

    body += application_section('intercity', 'Intercity Logistics',
        'Medium to heavy-duty configurations for intercity freight with emphasis on reliability, fuel economy, and driver comfort.',
        [
            {'name': 'X6 AWD Cargo Truck', 'spec': '4x4 AWD | 12T-60T GCW', 'desc': 'All-wheel drive cargo truck for intercity routes with varying road conditions and weather.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9b7254c2-82fe-49dc-b3de-36d66fc0bdd2.jpg'},
            {'name': 'X6 Dropside Truck', 'spec': '12T-60T GCW | Airbag Seat', 'desc': 'Sleeper berth 85cm wide for rest during long-haul intercity routes. Optimized for freight efficiency.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png'},
        ])

    body += application_section('city-dist', 'City Distribution',
        'Compact and maneuverable trucks for urban delivery with tight turning radius and low emissions for city center access.',
        [
            {'name': 'X7 Flatbed Truck', 'spec': '4.5T-25T GCW | Yuchai 160HP', 'desc': 'Compact dimensions with fully wrapped airline seats for efficient city distribution and last-mile delivery.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/57b40134-f17a-4635-9862-4918881781b5.png'},
            {'name': 'X6 Sprinkler Truck', 'spec': '12T-60T GCW | Municipal', 'desc': 'Lightweight chassis design with M3000 cab and sedan-like interior for municipal and city services.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/69a018d4-9ea8-4478-911c-d37afa898d10.png'},
        ])

    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need a Cargo Truck Solution?</h2>
<p>Contact our team for customized cargo truck configurations for your logistics operations.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: special.html (Special Vehicle Application) =====
def build_special():
    meta = '<meta content="SAGMOTO Special Vehicles for City Transportation, Smart Sanitation, Dangerous Goods, and Road Work & Rescue. Specialized commercial vehicles." name="description"/>\n<meta content="special vehicle, city transportation, smart sanitation, dangerous goods, road rescue, aerial work platform, sweeper, concrete mixer" name="keywords"/>'
    title = "Special Vehicle Application - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Special Vehicle</span>',
        "Special Vehicle Applications",
        "SPECIALIZED SOLUTIONS FOR EVERY MISSION"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Special Vehicle Applications</h2>
<p>SAGMOTO special vehicles are purpose-built for specific operational requirements, from municipal services to emergency response. Each vehicle is engineered with specialized equipment and safety systems to excel in its designated role.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Purpose-Built Design</h3>
<p>Each special vehicle is configured with mission-specific equipment including telescopic arms, high-pressure systems, mixer drums, and recovery winches.</p>
</div>
<div class="about-feature">
<h3>Safety &amp; Compliance</h3>
<p>Multiple safety protection systems, high-strength materials, and precision engineering ensure safe operation in hazardous environments.</p>
</div>
<div class="about-feature">
<h3>Versatile Platforms</h3>
<p>Built on proven SAGMOTO chassis platforms from light-duty X7 to heavy-duty X3s, adaptable to diverse upper-body configurations.</p>
</div>
</div>
</div>
</section>
'''

    body += application_section('city-transport', 'City Transportation',
        'Efficient urban transport solutions including aerial work platforms and municipal service vehicles for city infrastructure maintenance.',
        [
            {'name': 'X9 Aerial Work Platform', 'spec': 'Telescopic Arms | Yuchai YC4D 140HP', 'desc': 'Strong stability, convenient operation, and flexible mobility. Multi-level telescopic arms with large operating range.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg'},
            {'name': 'X9 Tow Truck', 'spec': 'Recovery Vehicle | Yuchai YC4E 160HP', 'desc': 'Maximum gradient over 30% for tough recovery operations. Heavy-duty winch system for reliable vehicle recovery.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a2e376e5-bc63-4f1c-9379-cbef769fe0eb.jpg'},
        ])

    body += application_section('sanitation', 'Smart Sanitation',
        'Advanced sanitation vehicles with efficient sweeping, sprinkling, and dust suppression systems for modern urban maintenance.',
        [
            {'name': '9 Series Sweeper', 'spec': 'Municipal | 4.5T-25T GCW | Yuchai 140HP', 'desc': 'Efficient street sweeper with high-capacity debris collection and powerful dust suppression for urban road maintenance.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8cd0ebb8-92b2-4dcf-a200-ffbc21fffe71.jpg'},
            {'name': 'X6 Sprinkler Truck', 'spec': '12T-60T GCW | Cummins ISD 210HP', 'desc': 'Lightweight chassis with M3000 cab. Water sprinkling system for road cleaning and dust suppression.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/69a018d4-9ea8-4478-911c-d37afa898d10.png'},
        ])

    body += application_section('dangerous-goods', 'Dangerous Goods Transportation',
        'Specialized vehicles for safe transport of hazardous materials with enhanced safety systems and leak prevention.',
        [
            {'name': 'X9 Tow Truck', 'spec': 'Recovery | Heavy-Duty Winch | 160HP', 'desc': 'Heavy-duty recovery vehicle suitable for emergency response in hazardous material incidents.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a2e376e5-bc63-4f1c-9379-cbef769fe0eb.jpg'},
            {'name': 'X7 Concrete Mixer', 'spec': 'High-Strength Steel | Yuchai 160HP', 'desc': 'Reliable hydraulic system with reinforced multi-leaf springs for demanding mixing operations.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2736f8a9-4674-4ae8-bda2-ff995e34c894.png'},
        ])

    body += application_section('rescue', 'Road Work & Rescue',
        'Emergency response and road maintenance vehicles equipped for rapid deployment and recovery operations.',
        [
            {'name': 'X9 Aerial Work Platform', 'spec': 'Telescopic Arms | 140HP', 'desc': 'Ideal for elevated road work, infrastructure maintenance, and emergency rescue operations at height.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg'},
            {'name': 'X9 Tow Truck', 'spec': 'Recovery | 160HP | 30% Grade', 'desc': 'Rapid response recovery vehicle with heavy-duty winch for roadside assistance and accident recovery.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a2e376e5-bc63-4f1c-9379-cbef769fe0eb.jpg'},
        ])

    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need a Special Vehicle Solution?</h2>
<p>Contact our team for customized special vehicle configurations tailored to your operational requirements.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: pzkyzyc.html (Off-road Dump Truck) =====
def build_pzkyzyc():
    meta = '<meta content="SAGMOTO Off-road Dump Trucks - Rugged mining and construction dump trucks with wide chassis, reinforced suspension, and high load capacity for extreme conditions." name="description"/>\n<meta content="off-road dump truck, mining dump truck, construction dump, wide chassis, heavy duty off-road" name="keywords"/>'
    title = "Off-road Dump Truck - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Off-road Dump Truck</span>',
        "Off-road Dump Truck",
        "BUILT FOR EXTREME CONDITIONS"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Off-road Dump Truck Series</h2>
<p>When the going gets tough, SAGMOTO off-road dump trucks deliver. Engineered with 850mm wide-chassis structures, specialized mining suspensions, and directional exhaust systems, these trucks are built to perform in the most challenging off-road environments.</p>
</div>
</div>
</section>

<!-- ===== FEATURES ===== -->
<section class="section-bg-light">
<div class="container">
<div class="about-features">
<div class="about-feature">
<h3>Wide Chassis Structure</h3>
<p>850mm wide-chassis design provides exceptional stability and performance on poor road conditions, reducing the risk of rollover on uneven terrain.</p>
</div>
<div class="about-feature">
<h3>Mining-Grade Suspension</h3>
<p>Specialized rear suspension for mining operations increases flattening load capacity from 25.3T to 30.5T, maximizing payload per trip.</p>
</div>
<div class="about-feature">
<h3>Directional Exhaust</h3>
<p>Adjustable exhaust tailpipe directs emissions away from the ground, preventing dust clouds that impair driver visibility in dry conditions.</p>
</div>
<div class="about-feature">
<h3>Multi-Purpose Adaptability</h3>
<p>Convenient adaptation to fuel tankers, sprinklers, and various dump body configurations for diverse operational needs.</p>
</div>
</div>
</div>
</section>
'''

    body += application_section('products', 'Off-road Dump Truck Products',
        'Complete lineup of off-road dump trucks for mining, construction, and heavy-duty material handling.',
        [
            {'name': 'Off-road Dump Truck', 'spec': '850 Wide Chassis | 30.5T Load | 400HP', 'desc': 'Adopting 850 wide-chassis structure, stable performance and adaptable to poor road conditions. Specialized rear suspension for mining.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg'},
            {'name': '9 Series Off-road', 'spec': 'Yuchai/Cummins 400HP | Mining', 'desc': 'Durability, high performance, and high load-bearing capacity. Multiple cab options. Adaptable to fuel tankers, sprinklers, dump trucks.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8065c0e4-5d81-4f00-97c1-6026bc4ef78c.jpg'},
            {'name': '7 Series Off-road', 'spec': 'Yuchai 340HP | Mining', 'desc': 'Powerful engine, excellent maneuverability. Reinforced oil pan protection grill and double-layer frame design.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0c12b07d-79ed-4ed7-90af-72345564bbe7.jpg'},
            {'name': '6 Series Off-road', 'spec': 'Cummins ISD 285HP | Efficient', 'desc': 'Strong power and efficient transportation. Reinforced design with iron bumper and customized upper-body options.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/c98399ce-d138-4d6d-b27c-bfddda9aa601.jpg'},
        ])

    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need an Off-road Dump Truck?</h2>
<p>Contact our team for customized off-road dump truck configurations for your mining or construction project.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: pzmtc.html (Off-road Tractor) =====
def build_pzmtc():
    meta = '<meta content="SAGMOTO Off-road Tractor Trucks - Powerful tractors for off-road trailer operations in mining, construction, and remote area logistics." name="description"/>\n<meta content="off-road tractor, mining tractor, off-road trailer truck, heavy duty tractor, construction tractor" name="keywords"/>'
    title = "Off-road Tractor - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Off-road Tractor</span>',
        "Off-road Tractor",
        "POWER AND PRECISION IN TOUGH TERRAIN"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Off-road Tractor Truck Series</h2>
<p>SAGMOTO off-road tractor trucks combine raw power with intelligent engineering to deliver unmatched performance in remote area logistics, mining operations, and construction site trailer transport. Built on reinforced chassis with all-condition capability.</p>
</div>
</div>
</section>

<!-- ===== FEATURES ===== -->
<section class="section-bg-light">
<div class="container">
<div class="about-features">
<div class="about-feature">
<h3>High-Torque Engines</h3>
<p>Yuchai and Cummins engines delivering 285HP to 560HP with high low-end torque for excellent climbing and pulling performance on rough terrain.</p>
</div>
<div class="about-feature">
<h3>Reinforced Drivetrain</h3>
<p>Double-layer frame design, reinforced oil pan protection, and heavy-duty axles ensure reliability in the most demanding off-road conditions.</p>
</div>
<div class="about-feature">
<h3>All-Condition Traction</h3>
<p>Optional all-wheel drive configurations with differential locks and aggressive tread tires for maximum traction on soft, wet, or uneven surfaces.</p>
</div>
</div>
</div>
</section>
'''

    body += application_section('products', 'Off-road Tractor Products',
        'Complete lineup of off-road tractor trucks for mining, construction, and remote logistics.',
        [
            {'name': 'X3s Trailer Truck', 'spec': 'Cummins ISME 420HP | 18T-100T GCW', 'desc': 'Versatile heavy-duty tractor with excellent power-to-weight ratio. Cab meets ECER29-03 collision standard.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/70f1e68f-95be-4336-9449-5dbe2e82e895.png'},
            {'name': '6 Series Off-road', 'spec': 'Cummins ISD 285HP | Strong Power', 'desc': 'Strong power and efficient transportation with reinforced design, iron bumper, and customized upper-body options.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/c98399ce-d138-4d6d-b27c-bfddda9aa601.jpg'},
            {'name': '7 Series Off-road', 'spec': 'Yuchai 340HP | Mining Grade', 'desc': 'Powerful engine with excellent maneuverability. Reinforced oil pan protection grill and double-layer frame design.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0c12b07d-79ed-4ed7-90af-72345564bbe7.jpg'},
        ])

    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need an Off-road Tractor?</h2>
<p>Contact our team for customized off-road tractor configurations for your operations.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: tzc.html (Off-road Truck - general) =====
def build_tzc():
    meta = '<meta content="SAGMOTO Off-road Trucks - Complete lineup of off-road trucks for mining, construction, and extreme conditions. 6, 7, and 9 Series available." name="description"/>\n<meta content="off-road truck, mining truck, construction truck, extreme conditions, off-road vehicle, heavy duty" name="keywords"/>'
    title = "Off-road Truck - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Applications</span> <span>/</span> <span>Off-road Truck</span>',
        "Off-road Truck",
        "ENGINEERED FOR THE EXTREME"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Off-road Truck Series</h2>
<p>The SAGMOTO off-road truck lineup covers the 6 Series, 7 Series, and 9 Series, offering a comprehensive range of solutions for mining, construction, and specialized off-road operations. Each series is engineered with reinforced structures, powerful engines, and adaptable configurations.</p>
</div>
</div>
</section>

<!-- ===== SERIES COMPARISON ===== -->
<section class="section-bg-light">
<div class="container">
<div class="about-features">
<div class="about-feature">
<h3>6 Series</h3>
<p>Strong power and efficient transportation. Reinforced design with iron bumper and customized upper-body options. Ideal for medium-duty off-road applications.</p>
</div>
<div class="about-feature">
<h3>7 Series</h3>
<p>Powerful engine with excellent maneuverability. Reinforced oil pan protection grill and double-layer frame design for demanding mining conditions.</p>
</div>
<div class="about-feature">
<h3>9 Series</h3>
<p>Durability, high performance, and high load-bearing capacity. Multiple cab options. Adaptable to fuel tankers, sprinklers, and dump trucks.</p>
</div>
</div>
</div>
</section>
'''

    body += application_section('products', 'Off-road Truck Products',
        'Complete off-road truck lineup with various configurations and power ratings.',
        [
            {'name': '9 Series Off-road', 'spec': 'Yuchai/Cummins 400HP | Mining', 'desc': 'Durability, high performance, and high load-bearing capacity. Multiple cab options for diverse applications.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8065c0e4-5d81-4f00-97c1-6026bc4ef78c.jpg'},
            {'name': '7 Series Off-road', 'spec': 'Yuchai 340HP | Mining Grade', 'desc': 'Powerful engine, excellent maneuverability. Reinforced oil pan protection grill and double-layer frame design.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0c12b07d-79ed-4ed7-90af-72345564bbe7.jpg'},
            {'name': '6 Series Off-road', 'spec': 'Cummins ISD 285HP | Efficient', 'desc': 'Strong power and efficient transportation. Reinforced design with iron bumper and customized upper-body.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/c98399ce-d138-4d6d-b27c-bfddda9aa601.jpg'},
            {'name': 'Off-road Dump Truck', 'spec': '850 Wide Chassis | 30.5T Load', 'desc': 'Specialized rear suspension for mining. Directional exhaust to minimize dust. Adaptable to poor road conditions.', 'image': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg'},
        ])

    body += '''<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need an Off-road Truck?</h2>
<p>Contact our team for customized off-road truck configurations for your mining or construction operations.</p>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: service.html =====
def build_service():
    meta = '<meta content="SAGMOTO Service Policy - Comprehensive service network, maintenance programs, driving safety guidelines, and customer support for commercial vehicle owners." name="description"/>\n<meta content="service policy, maintenance, service network, driving safety, customer support, truck service" name="keywords"/>'
    title = "Service Policy - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>Services</span>',
        "Service & Support",
        "COMMITTED TO YOUR SUCCESS"
    )

    body += '''<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Our Service Commitment</h2>
<p>At SAGMOTO, we understand that vehicle uptime is critical to your business. Our comprehensive service network spans 50+ countries, providing expert maintenance, genuine parts, and technical support wherever your operations take you.</p>
</div>
</div>
</section>

<!-- ===== SERVICE ITEMS ===== -->
<section class="section-bg-light">
<div class="container">
<div class="service-grid">
<a href="service_list/1674411714944516096.html" class="service-item">
<div class="service-icon">
<svg viewBox="0 0 24 24" width="40" height="40"><path fill="#0D1F3D" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>
</div>
<h3>Find Your Service Provider</h3>
<p>Locate authorized SAGMOTO service centers and distributors in your region. Our global network ensures support is never far away.</p>
<span class="btn-learn">Learn More &rsaquo;</span>
</a>
<a href="service_list/1674411730417303552.html" class="service-item">
<div class="service-icon">
<svg viewBox="0 0 24 24" width="40" height="40"><path fill="#0D1F3D" d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg>
</div>
<h3>Maintenance Service</h3>
<p>Scheduled maintenance programs, genuine parts, and expert technical service to keep your fleet running at peak performance.</p>
<span class="btn-learn">Learn More &rsaquo;</span>
</a>
<a href="service_list/1674411748220751872.html" class="service-item">
<div class="service-icon">
<svg viewBox="0 0 24 24" width="40" height="40"><path fill="#0D1F3D" d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>
</div>
<h3>Driving Reminder</h3>
<p>Essential driving tips and reminders for safe and efficient operation of SAGMOTO commercial vehicles in various conditions.</p>
<span class="btn-learn">Learn More &rsaquo;</span>
</a>
<a href="service_list/1674411767427842048.html" class="service-item">
<div class="service-icon">
<svg viewBox="0 0 24 24" width="40" height="40"><path fill="#0D1F3D" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
</div>
<h3>Safe Driving</h3>
<p>Comprehensive safety guidelines, defensive driving techniques, and emergency procedures for commercial vehicle operators.</p>
<span class="btn-learn">Learn More &rsaquo;</span>
</a>
</div>
</div>
</section>

<!-- ===== WARRANTY ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Warranty &amp; Support</h2>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Standard Warranty</h3>
<p>Comprehensive warranty coverage on all new SAGMOTO vehicles, including engine, transmission, and axle components. Extended warranty options available.</p>
</div>
<div class="about-feature">
<h3>Genuine Parts</h3>
<p>Authentic SAGMOTO replacement parts available through our global distribution network, ensuring optimal performance and longevity.</p>
</div>
<div class="about-feature">
<h3>Technical Training</h3>
<p>Professional training programs for service technicians and fleet operators, covering maintenance, diagnostics, and repair procedures.</p>
</div>
<div class="about-feature">
<h3>24/7 Support</h3>
<p>Round-the-clock technical support hotline and online assistance for urgent operational issues and troubleshooting.</p>
</div>
</div>
</div>
</section>

<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need Service Support?</h2>
<p>Contact our service team for maintenance scheduling, parts ordering, or technical assistance.</p>
<a href="contact.html" class="btn-primary">Contact Service Team</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== PAGE: video_list.html =====
def build_video_list():
    meta = '<meta content="SAGMOTO Video Center - Watch product showcases, vehicle demonstrations, and company videos. See our commercial vehicles in action." name="description"/>\n<meta content="video center, product video, truck video, commercial vehicle video, SAGMOTO video" name="keywords"/>'
    title = "Video Center - SAGMOTO"

    body = page_banner(
        '<a href="index.html">Home</a> <span>/</span> <span>News</span> <span>/</span> <span>Video Center</span>',
        "Video Center",
        "SEE SAGMOTO IN ACTION"
    )

    body += '''<!-- ===== VIDEOS ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Product Videos</h2>
<p>Explore our video library to see SAGMOTO commercial vehicles in real-world operations.</p>
</div>
<div class="video-grid">
<div class="video-card">
<div class="video-thumb" style="background: linear-gradient(rgba(13,31,61,0.7), rgba(13,31,61,0.7)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg') center/cover;">
<div class="play-btn">&#9658;</div>
</div>
<h3>E1st Flagship Tractor</h3>
<p>Cummins Z14 560HP flagship tractor truck showcase - power, comfort, and innovation.</p>
</div>
<div class="video-card">
<div class="video-thumb" style="background: linear-gradient(rgba(13,31,61,0.7), rgba(13,31,61,0.7)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg') center/cover;">
<div class="play-btn">&#9658;</div>
</div>
<h3>Z3 Tractor Truck</h3>
<p>Next-generation tractor with intelligent electronic systems and European safety standards.</p>
</div>
<div class="video-card">
<div class="video-thumb" style="background: linear-gradient(rgba(13,31,61,0.7), rgba(13,31,61,0.7)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg') center/cover;">
<div class="play-btn">&#9658;</div>
</div>
<h3>Off-road Dump Truck</h3>
<p>See the 850 wide-chassis off-road dump truck in action at a mining site.</p>
</div>
<div class="video-card">
<div class="video-thumb" style="background: linear-gradient(rgba(13,31,61,0.7), rgba(13,31,61,0.7)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3f35ad3a-2ea6-42cb-bb86-2af2c12a16e7.jpg') center/cover;">
<div class="play-btn">&#9658;</div>
</div>
<h3>X9 4x4 Dump Truck</h3>
<p>All-wheel drive dump truck demonstrating off-road capability and bearing capacity.</p>
</div>
<div class="video-card">
<div class="video-thumb" style="background: linear-gradient(rgba(13,31,61,0.7), rgba(13,31,61,0.7)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg') center/cover;">
<div class="play-btn">&#9658;</div>
</div>
<h3>X9 Aerial Work Platform</h3>
<p>Telescopic arm aerial work platform demonstrating operation range and lifting speed.</p>
</div>
<div class="video-card">
<div class="video-thumb" style="background: linear-gradient(rgba(13,31,61,0.7), rgba(13,31,61,0.7)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a161feeb-72a6-456a-8368-32970c2d9df0.jpg') center/cover;">
<div class="play-btn">&#9658;</div>
</div>
<h3>i9 Electric Truck</h3>
<p>Integrated electric drive axle with 430km range and 120KW fast charging technology.</p>
</div>
</div>
</div>
</section>

<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Want to See More?</h2>
<p>Subscribe to our YouTube channel for the latest product videos and demonstrations.</p>
<a href="contact.html" class="btn-primary">Contact Us</a>
</div>
</div>
</section>
'''

    return make_page(meta, title, body)

# ===== SERVICE LIST PAGES =====
def build_service_page(filename, title, meta_desc, body_title, body_content):
    meta = f'<meta content="{meta_desc}" name="description"/>'
    full_title = f"{title} - SAGMOTO"

    body = page_banner(
        f'<a href="../index.html">Home</a> <span>/</span> <a href="../service.html">Services</a> <span>/</span> <span>{body_title}</span>',
        body_title,
        "SAGMOTO SERVICE & SUPPORT"
    )
    body += body_content
    body += '''
<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Need More Information?</h2>
<p>Our service team is ready to assist you with any questions or support needs.</p>
<a href="../contact.html" class="btn-primary">Contact Service Team</a>
</div>
</div>
</section>
'''
    return make_page(meta, full_title, body, subdir_prefix="../")

def build_service_find_provider():
    return build_service_page(
        "find_provider", "Find Your Service Provider",
        "Find authorized SAGMOTO service centers and distributors worldwide. Global service network covering 50+ countries.",
        "Find Your Service Provider",
        '''<!-- ===== CONTENT ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Global Service Network</h2>
<p>SAGMOTO has established a comprehensive international service network spanning Africa, Southeast Asia, the Middle East, Central Asia, South America, and more. Our authorized distributors and service centers provide localized support wherever you operate.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Africa</h3>
<p>Service centers across North Africa, West Africa, East Africa, and Southern Africa providing parts, maintenance, and technical support.</p>
</div>
<div class="about-feature">
<h3>Southeast Asia</h3>
<p>Authorized distributors in Vietnam, Philippines, Indonesia, Thailand, and other ASEAN countries with full-service capabilities.</p>
</div>
<div class="about-feature">
<h3>Middle East &amp; Central Asia</h3>
<p>Service partners in Saudi Arabia, UAE, Kazakhstan, Uzbekistan, and throughout the region for rapid response.</p>
</div>
<div class="about-feature">
<h3>South America</h3>
<p>Growing network of distributors and service providers across South American markets with Spanish and Portuguese support.</p>
</div>
</div>
</div>
</section>
<section class="section-bg-light">
<div class="container">
<div class="s_title">
<h2>How to Find Service</h2>
</div>
<div class="about-features">
<div class="about-feature">
<h3>1. Contact Us</h3>
<p>Reach out to our service coordination team at +86 15319431311 or sales@fenghan-trade.com with your location and vehicle model.</p>
</div>
<div class="about-feature">
<h3>2. Get Matched</h3>
<p>We will connect you with the nearest authorized service provider in your region for immediate assistance.</p>
</div>
<div class="about-feature">
<h3>3. Receive Service</h3>
<p>Visit the service center or schedule an on-site visit for maintenance, repairs, or parts replacement.</p>
</div>
</div>
</div>
</section>'''
    )

def build_service_maintenance():
    return build_service_page(
        "maintenance", "Maintenance Service",
        "SAGMOTO maintenance service programs, scheduled maintenance, genuine parts, and expert technical support for commercial vehicles.",
        "Maintenance Service",
        '''<!-- ===== CONTENT ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Maintenance Programs</h2>
<p>Regular maintenance is the key to maximizing vehicle uptime, fuel efficiency, and service life. SAGMOTO offers comprehensive maintenance programs tailored to your fleet size and operational profile.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Scheduled Maintenance</h3>
<p>Planned service intervals based on mileage, operating hours, or time periods. Includes oil changes, filter replacements, brake inspections, and system diagnostics.</p>
</div>
<div class="about-feature">
<h3>Genuine Parts</h3>
<p>Authentic SAGMOTO replacement parts manufactured to exact specifications, ensuring optimal fit, performance, and warranty compliance.</p>
</div>
<div class="about-feature">
<h3>Diagnostic Services</h3>
<p>Advanced electronic diagnostics using SAGMOTO proprietary tools to identify issues quickly and accurately, minimizing downtime.</p>
</div>
<div class="about-feature">
<h3>Emergency Repair</h3>
<p>Rapid response repair services for unexpected breakdowns. Mobile service units available in select regions for on-site repairs.</p>
</div>
</div>
</div>
</section>
<section class="section-bg-light">
<div class="container">
<div class="s_title">
<h2>Maintenance Intervals</h2>
</div>
<div class="cert-grid">
<div class="cert-item">
<h3>First Service</h3>
<p>1,000 - 5,000 km or 1 month: Initial inspection, bolt torque check, fluid levels</p>
</div>
<div class="cert-item">
<h3>Regular Service</h3>
<p>Every 10,000 - 20,000 km: Oil change, filters, brake system, electrical check</p>
</div>
<div class="cert-item">
<h3>Major Service</h3>
<p>Every 50,000 - 80,000 km: Comprehensive overhaul, valve adjustment, injector service</p>
</div>
<div class="cert-item">
<h3>Seasonal Service</h3>
<p>Pre-winter and pre-summer: Coolant, battery, tires, climate system inspection</p>
</div>
</div>
</div>
</section>'''
    )

def build_service_driving_reminder():
    return build_service_page(
        "driving_reminder", "Driving Reminder",
        "Essential driving tips and reminders for safe and efficient operation of SAGMOTO commercial vehicles.",
        "Driving Reminder",
        '''<!-- ===== CONTENT ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Essential Driving Reminders</h2>
<p>Safe and efficient operation of your SAGMOTO commercial vehicle starts with proper driving habits. Follow these essential reminders to maximize performance, fuel efficiency, and safety.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Pre-Trip Inspection</h3>
<p>Always conduct a thorough pre-trip inspection: check tire pressure and condition, fluid levels, lights, brakes, mirrors, and safety equipment before departure.</p>
</div>
<div class="about-feature">
<h3>Optimal RPM Range</h3>
<p>Operate the engine in its optimal RPM range (typically 1,200-1,800 RPM for diesel engines) to maximize fuel efficiency and reduce engine wear.</p>
</div>
<div class="about-feature">
<h3>Load Distribution</h3>
<p>Ensure proper load distribution and securement. Overloading or uneven loading affects vehicle stability, braking performance, and tire wear.</p>
</div>
<div class="about-feature">
<h3>Speed Management</h3>
<p>Observe speed limits and adjust for road, weather, and load conditions. Reducing speed by 10 km/h can improve fuel economy by 5-10%.</p>
</div>
</div>
</div>
</section>
<section class="section-bg-light">
<div class="container">
<div class="s_title">
<h2>Fuel-Saving Tips</h2>
</div>
<div class="cert-grid">
<div class="cert-item">
<h3>Smooth Acceleration</h3>
<p>Avoid aggressive acceleration and braking. Smooth driving can reduce fuel consumption by up to 15%.</p>
</div>
<div class="cert-item">
<h3>Tire Pressure</h3>
<p>Maintain correct tire pressure. Under-inflated tires increase fuel consumption and tire wear.</p>
</div>
<div class="cert-item">
<h3>Idle Reduction</h3>
<p>Minimize idling. Turn off the engine during extended stops to save fuel and reduce emissions.</p>
</div>
<div class="cert-item">
<h3>Route Planning</h3>
<p>Plan routes to avoid congestion, steep grades, and poor road conditions. Use GPS for real-time traffic updates.</p>
</div>
</div>
</div>
</section>'''
    )

def build_service_safe_driving():
    return build_service_page(
        "safe_driving", "Safe Driving",
        "Comprehensive safety guidelines, defensive driving techniques, and emergency procedures for commercial vehicle operators.",
        "Safe Driving",
        '''<!-- ===== CONTENT ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Safety First</h2>
<p>Safety is SAGMOTO's top priority. Our vehicles are equipped with advanced safety features, but safe driving practices remain the most important factor in preventing accidents. Follow these guidelines to protect yourself, your cargo, and others on the road.</p>
</div>
<div class="about-features">
<div class="about-feature">
<h3>Defensive Driving</h3>
<p>Always anticipate potential hazards. Maintain a safe following distance (at least 3 seconds in good conditions, more in adverse weather). Scan the road ahead and check mirrors every 5-8 seconds.</p>
</div>
<div class="about-feature">
<h3>Adverse Weather</h3>
<p>Reduce speed by 25-30% in rain, 50% in snow or ice. Use low gears on descents. Never use cruise control on slippery surfaces. Pull over safely if visibility is severely limited.</p>
</div>
<div class="about-feature">
<h3>Braking Safety</h3>
<p>Maintain proper brake system maintenance. Use engine braking on long descents to prevent brake fade. Keep a much greater following distance when carrying heavy loads or driving on wet roads.</p>
</div>
<div class="about-feature">
<h3>Emergency Procedures</h3>
<p>In case of emergency: activate hazard lights, move to a safe location, set up warning triangles, contact emergency services, and notify your dispatcher. Keep an emergency kit in the vehicle.</p>
</div>
</div>
</div>
</section>
<section class="section-bg-light">
<div class="container">
<div class="s_title">
<h2>Vehicle Safety Features</h2>
</div>
<div class="cert-grid">
<div class="cert-item">
<h3>ECE R29-03 Cab</h3>
<p>Cab strength meets the latest European collision safety standards for maximum driver protection.</p>
</div>
<div class="cert-item">
<h3>Dual Warning System</h3>
<p>Advanced warning systems monitor vehicle status and alert the driver to potential issues.</p>
</div>
<div class="cert-item">
<h3>ABS &amp; EBS</h3>
<p>Anti-lock braking and electronic braking systems ensure optimal braking performance in all conditions.</p>
</div>
<div class="cert-item">
<h3>Blind Spot Reduction</h3>
<p>Main rear view mirror + supplemental blind mirror to reduce the driver's visual blind spot.</p>
</div>
</div>
</div>
</section>'''
    )

# ===== NEWS LIST PAGES =====
def build_news_center():
    meta = '<meta content="SAGMOTO News Center - Latest company news, product launches, industry insights, and event updates from Shaanxi Fenghan Trading." name="description"/>\n<meta content="news, SAGMOTO news, commercial vehicle news, truck industry, company news, product launch" name="keywords"/>'
    title = "News Center - SAGMOTO"

    body = page_banner(
        '<a href="../index.html">Home</a> <span>/</span> <span>News Center</span>',
        "News Center",
        "LATEST UPDATES & INSIGHTS"
    )
    body += '''<!-- ===== NEWS LIST ===== -->
<section class="section-bg-white">
<div class="container">
<div class="s_title">
<h2>Latest News</h2>
<p>Stay updated with the latest developments from SAGMOTO and the commercial vehicle industry.</p>
</div>
<div class="news-grid">
<a href="81163.html" class="news-card">
<div class="news-thumb" style="background: linear-gradient(rgba(13,31,61,0.6), rgba(13,31,61,0.6)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg') center/cover;">
<span class="news-date">2026-07-01</span>
</div>
<div class="news-content">
<h3>SAGMOTO E1st Flagship Tractor Now Available for Export</h3>
<p>The E1st represents the pinnacle of SAGMOTO engineering with Cummins Z14 560HP engine, Eaton AMT gearbox, and intelligent cab design...</p>
<span class="btn-learn">Read More &rsaquo;</span>
</div>
</a>
<div class="news-card">
<div class="news-thumb" style="background: linear-gradient(rgba(13,31,61,0.6), rgba(13,31,61,0.6)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a161feeb-72a6-456a-8368-32970c2d9df0.jpg') center/cover;">
<span class="news-date">2026-06-26</span>
</div>
<div class="news-content">
<h3>i9 Electric Truck: Leading the New Energy Transition</h3>
<p>SAGMOTO's i9 series electric light truck offers 430km range with 120KW fast charging. Integrated electric drive axle technology reduces energy consumption by 15%...</p>
<span class="btn-learn">Read More &rsaquo;</span>
</div>
</a>
<div class="news-card">
<div class="news-thumb" style="background: linear-gradient(rgba(13,31,61,0.6), rgba(13,31,61,0.6)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg') center/cover;">
<span class="news-date">2026-06-20</span>
</div>
<div class="news-content">
<h3>Off-road Dump Truck Excels in Mining Operations</h3>
<p>The 850 wide-chassis off-road dump truck demonstrates exceptional performance in African mining sites, with 30.5T load capacity and specialized mining suspension...</p>
<span class="btn-learn">Read More &rsaquo;</span>
</div>
</a>
<div class="news-card">
<div class="news-thumb" style="background: linear-gradient(rgba(13,31,61,0.6), rgba(13,31,61,0.6)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg') center/cover;">
<span class="news-date">2026-06-15</span>
</div>
<div class="news-content">
<h3>Z3 Tractor Truck Receives European Safety Certification</h3>
<p>The Z3 series tractor truck with Cummins M13 520HP engine has received ECE R29-03 cab collision certification, meeting the latest European safety standards...</p>
<span class="btn-learn">Read More &rsaquo;</span>
</div>
</a>
<div class="news-card">
<div class="news-thumb" style="background: linear-gradient(rgba(13,31,61,0.6), rgba(13,31,61,0.6)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png') center/cover;">
<span class="news-date">2026-06-10</span>
</div>
<div class="news-content">
<h3>X6 Series: The Versatile Medium-Duty Solution</h3>
<p>The X6 series offers flexible configurations for cargo, mixer, and sprinkler applications with Cummins ISD power and airbag comfort seating...</p>
<span class="btn-learn">Read More &rsaquo;</span>
</div>
</a>
<div class="news-card">
<div class="news-thumb" style="background: linear-gradient(rgba(13,31,61,0.6), rgba(13,31,61,0.6)), url('https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg') center/cover;">
<span class="news-date">2026-06-05</span>
</div>
<div class="news-content">
<h3>Special Vehicle Solutions for Urban Services</h3>
<p>SAGMOTO's special vehicle lineup includes aerial work platforms, sweepers, and concrete mixers, providing comprehensive solutions for municipal services...</p>
<span class="btn-learn">Read More &rsaquo;</span>
</div>
</a>
</div>
</div>
</section>
'''
    return make_page(meta, title, body, subdir_prefix="../")

def build_news_detail():
    meta = '<meta content="SAGMOTO E1st Flagship Tractor Now Available for Export - Cummins Z14 560HP engine, Eaton AMT gearbox, and intelligent cab design." name="description"/>'
    title = "E1st Flagship Tractor - News - SAGMOTO"

    body = page_banner(
        '<a href="../index.html">Home</a> <span>/</span> <a href="1.html">News Center</a> <span>/</span> <span>E1st Flagship Tractor</span>',
        "E1st Flagship Tractor Now Available for Export",
        "JULY 1, 2026"
    )
    body += '''<!-- ===== ARTICLE ===== -->
<section class="section-bg-white">
<div class="container">
<div class="article-content">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg" alt="E1st Tractor" style="width:100%;border-radius:8px;margin-bottom:30px;"/>

<p>Shaanxi Fenghan Trading Co., Ltd is proud to announce that the SAGMOTO E1st flagship tractor truck is now available for international export orders. As the premium model in the SAGMOTO heavy-duty lineup, the E1st represents the pinnacle of commercial vehicle engineering.</p>

<h2>Powertrain Excellence</h2>
<p>The E1st is powered by the Cummins Z14 engine, delivering a maximum output of <strong>560 horsepower</strong>. Paired with an Eaton AMT gearbox and Hande maintenance-free axle, this integrated exclusive power chain design ensures optimal performance, reliability, and fuel efficiency.</p>

<h2>Intelligent Cab Design</h2>
<p>The cab adopts an intelligent seat design concept with a flat floor design and an internal height of <strong>2.13 meters</strong>, providing ample space for drivers and passengers. The brand-new cab modeling incorporates CFD (Computational Fluid Dynamics) optimization technology, achieving a whole-vehicle drag coefficient of just <strong>0.45</strong> and fuel consumption of 26.97L per 100km.</p>

<h2>Key Specifications</h2>
<ul>
<li><strong>Engine:</strong> Cummins Z14EVIE 560HP</li>
<li><strong>Transmission:</strong> Eaton AMT</li>
<li><strong>Axle:</strong> Hande maintenance-free</li>
<li><strong>GCW Range:</strong> 18T - 100T</li>
<li><strong>Cab Height:</strong> 2.13m internal</li>
<li><strong>Drag Coefficient:</strong> 0.45</li>
<li><strong>Fuel Consumption:</strong> 26.97L/100km</li>
</ul>

<h2>Safety Features</h2>
<p>The E1st's high-strength cab design complies with the latest European safety standards, providing strong protection for driver and passengers. Advanced driver assistance systems and dual warning systems ensure maximum safety in all operating conditions.</p>

<h2>Availability</h2>
<p>The E1st is now available for export orders through Shaanxi Fenghan Trading Co., Ltd. Contact our sales team at <strong>+86 15319431311</strong> or <strong>sales@fenghan-trade.com</strong> for pricing, configuration options, and delivery information.</p>

<div class="article-footer" style="margin-top:40px;padding:20px;background:#f5f5f5;border-radius:8px;">
<p style="margin:0;"><strong>About SAGMOTO:</strong> SAGMOTO is the commercial vehicle brand of Shaanxi Automobile Holding Group, founded in 1968. With 32,000 employees and total assets of 34.8 billion CNY, SAGMOTO delivers comprehensive commercial vehicle solutions to 50+ countries worldwide.</p>
</div>
</div>
</div>
</section>

<!-- ===== CTA ===== -->
<section class="section-bg-light">
<div class="container">
<div class="cta-box">
<h2>Interested in the E1st?</h2>
<p>Contact our team for detailed specifications, pricing, and export arrangements.</p>
<a href="../contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</section>
'''
    return make_page(meta, title, body, subdir_prefix="../")

# ===== MAIN =====
def main():
    pages = {
        'qyc.html': build_qyc(),
        'zxc.html': build_zxc(),
        'zhc.html': build_zhc(),
        'special.html': build_special(),
        'pzkyzyc.html': build_pzkyzyc(),
        'pzmtc.html': build_pzmtc(),
        'tzc.html': build_tzc(),
        'service.html': build_service(),
        'video_list.html': build_video_list(),
    }

    service_pages = {
        'service_list/1674411714944516096.html': build_service_find_provider(),
        'service_list/1674411730417303552.html': build_service_maintenance(),
        'service_list/1674411748220751872.html': build_service_driving_reminder(),
        'service_list/1674411767427842048.html': build_service_safe_driving(),
    }

    news_pages = {
        'news_list/1.html': build_news_center(),
        'news_list/81163.html': build_news_detail(),
    }

    all_pages = {**pages, **service_pages, **news_pages}

    for filename, content in all_pages.items():
        filepath = os.path.join(BASE_DIR, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        size = len(content)
        print(f"  [OK] {filename} ({size:,} bytes)")

    print(f"\nTotal: {len(all_pages)} pages rebuilt")

if __name__ == '__main__':
    main()
