#!/usr/bin/env python3
"""
Rebuild all mirror pages as custom pages using the same CSS/JS stack as products.html.
Generates: qyc.html, zxc.html, zhc.html, special.html, pzkyzyc.html, pzmtc.html,
           tzc.html, service.html, video_list.html
"""

import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load products
with open(os.path.join(BASE_DIR, 'data', 'products.json'), 'r', encoding='utf-8') as f:
    products_data = json.load(f)

PRODUCTS = products_data['products']

# ===== Shared HTML Components =====

def top_bar():
    return """<!-- ===== TOP BAR ===== -->
<div class="e_container-1">
<div class="container">
<div class="top-contact">
<a href="tel:+8615319431311">
<svg height="14" viewBox="0 0 24 24" width="14"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z" fill="currentColor"></path></svg>
                +86 15319431311
            </a>
<a href="mailto:sales@fenghan-trade.com">
<svg height="14" viewBox="0 0 24 24" width="14"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="currentColor"></path></svg>
                sales@fenghan-trade.com
            </a>
</div>
<div class="lang-selector">
<a class="active" href="#">EN</a>
<a href="#">\u4e2d\u6587</a>
<a href="#">FR</a>
</div>
</div>
</div>"""


def nav_header():
    return """<!-- ===== HEADER / NAVIGATION ===== -->
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
<a href="products.html">PRODUCTS <svg class="nav-arrow" height="10" viewBox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
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
<a href="javascript:;">APPLICATIONS <svg class="nav-arrow" height="10" viewBox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
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
<a href="service.html">SERVICES <svg class="nav-arrow" height="10" viewBox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu">
<li><a href="service.html">Service Policy</a></li>
<li><a href="service.html#find-provider">Find Your Service Provider</a></li>
<li><a href="service.html#maintenance">Maintenance Service</a></li>
<li><a href="service.html#driving-reminder">Driving Reminder</a></li>
<li><a href="service.html#safe-driving">Safe Driving</a></li>
</ul>
</li>
<li class="has-dropdown">
<a href="news.html">NEWS <svg class="nav-arrow" height="10" viewBox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu">
<li><a href="news.html">News Center</a></li>
<li><a href="video_list.html">Video Center</a></li>
</ul>
</li>
<li class="has-dropdown">
<a href="about.html">ABOUT US <svg class="nav-arrow" height="10" viewBox="0 0 1024 1024" width="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"></path></svg></a>
<ul class="dropdown-menu">
<li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>
<li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>
<li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>
<li><a href="contact.html">Contact Us</a></li>
</ul>
</li>
<li class="nav-search"><a href="#" onclick="event.preventDefault();"><svg height="16" viewBox="0 0 24 24" width="16"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" fill="currentColor"></path></svg></a></li></ul>
</div>
</div>"""


def footer():
    return """<!-- ===== FOOTER ===== -->
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
</footer>"""


def page_head(title, desc, keywords):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css" rel="stylesheet"/>
<link href="css/style.css" rel="stylesheet"/>
<link rel="stylesheet" href="css/app-pages.css">
<link href="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png" rel="icon"/>
<script src="js/data-loader.js"></script>
<meta content="{desc}" name="description"/>
<meta content="{keywords}" name="keywords"/>
<title>{title}</title>"""


def page_banner(breadcrumb, h1, subtitle, bg='images/hero/slide1.jpg'):
    return f"""<!-- ===== PAGE BANNER ===== -->
<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('{bg}') center/cover;">
<div class="container">
<div class="breadcrumb">
<a href="index.html">Home</a> <span>/</span> <span>{breadcrumb}</span>
</div>
<h1>{h1}</h1>
<p>{subtitle}</p>
</div>
</section>"""


def product_card_html(p):
    fallback = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23e5e5e5' width='400' height='300'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='%23999' font-size='18'%3ESAGMOTO%3C/text%3E%3C/svg%3E"
    return f"""<div class="product-card">
<a href="products.html?search={p['name']}" class="product-card-img">
<img src="{p['image']}" alt="{p['name']}" onerror="this.src='{fallback}'">
</a>
<div class="product-card-body">
<h3><a href="products.html?search={p['name']}">{p['name']}</a></h3>
<p class="product-card-specs">{p.get('spec','')}</p>
<p class="product-card-desc">{p.get('description','')[:120]}...</p>
</div>
</div>"""


def product_cards_by_category(cat):
    items = [p for p in PRODUCTS if p['category'] == cat]
    return '\n'.join(product_card_html(p) for p in items)


def product_cards_by_ids(ids):
    items = [p for p in PRODUCTS if p['id'] in ids]
    return '\n'.join(product_card_html(p) for p in items)


def scripts():
    return """<script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
<script src="js/main.js"></script>"""


def full_page(filename, title, desc, keywords, breadcrumb, h1, subtitle, content_html, extra_js=''):
    html = page_head(title, desc, keywords)
    html += f"""
<body>
{top_bar()}
{nav_header()}
{page_banner(breadcrumb, h1, subtitle)}
{content_html}
{footer()}
{scripts()}
{extra_js}
</body>
</html>"""
    with open(os.path.join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Generated: {filename} ({len(html):,} bytes)")


# ===== Application Page Content Builders =====

def scenario_section(section_id, title, desc, features, img_url, img_alt):
    """Build a scenario/application section with image + features"""
    features_html = '\n'.join(
        f'<li><svg width="20" height="20" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" fill="#C62828"/></svg> {f}</li>'
        for f in features
    )
    return f"""<!-- ===== SCENARIO: {title} ===== -->
<section class="app-scenario" id="{section_id}">
<div class="container">
<div class="scenario-wrapper">
<div class="scenario-image">
<img src="{img_url}" alt="{img_alt}" loading="lazy">
</div>
<div class="scenario-content">
<h2>{title}</h2>
<p class="scenario-desc">{desc}</p>
<ul class="scenario-features">
{features_html}
</ul>
<a href="contact.html" class="btn-primary">Request a Quote</a>
</div>
</div>
</div>
</section>"""


def product_showcase_section(title, subtitle, products_html):
    return f"""<!-- ===== PRODUCT SHOWCASE ===== -->
<section class="section-bg-light">
<div class="container">
<div class="s_title category-title">
<h2>{title}</h2>
<p>{subtitle}</p>
</div>
<div class="product-grid">
{products_html}
</div>
</div>
</section>"""


def cta_section():
    return """<!-- ===== CTA SECTION ===== -->
<section class="cta-banner">
<div class="container">
<h2>Need a Custom Solution?</h2>
<p>Our team of experts will help you find the perfect SAGMOTO truck for your specific application.</p>
<a href="contact.html" class="btn-primary btn-large">Contact Us Today</a>
</div>
</section>"""


# ===== Page Definitions =====

def build_qyc():
    """Tractor Application Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Tractor Truck Applications</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO tractor trucks are engineered for maximum efficiency across diverse transport scenarios. From busy port operations to hazardous chemical logistics, our tractor units deliver reliable power, advanced safety systems, and exceptional fuel economy. With Cummins and Yuchai engine options ranging from 340 to 560 HP, we provide the right configuration for every application.</p>
</div>
</div>
</section>"""

    # Port Transport
    content += scenario_section(
        "port",
        "Port Transport",
        "SAGMOTO tractor trucks excel in port logistics with rapid container handling capabilities. Designed for high-frequency short-haul operations, our tractors feature quick acceleration, robust chassis for heavy container loads, and optimized drivetrains for stop-and-go port cycles. The E1st flagship model with Cummins Z14 560HP engine provides the ultimate power for maximum GVW container transport.",
        [
            "Cummins Z14 560HP engine with Eaton AMT gearbox for seamless shifting",
            "Flat-floor cab design with 2.13m interior height for driver comfort during long shifts",
            "Drag coefficient of 0.45 for optimal fuel efficiency in port cycles",
            "Hande maintenance-free axle reduces downtime and operating costs"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg",
        "SAGMOTO E1st Tractor at Port"
    )

    # Hazchem Transport
    content += scenario_section(
        "hazchem",
        "Hazardous Chemicals Transport",
        "Safety is paramount in hazardous chemical transportation. SAGMOTO tractor trucks are equipped with advanced safety systems including anti-lock braking (ABS), electronic brakeforce distribution (EBD), and stability control. The high-strength cab design complies with European ECE-R29-03 collision standards, providing maximum protection for drivers and cargo. Dual warning systems and fire suppression options ensure compliance with international hazmat regulations.",
        [
            "European ECE-R29-03 compliant high-strength safety cab",
            "Dual warning systems for hazardous material transport compliance",
            "Anti-lock braking system (ABS) and electronic stability control",
            "Optional fire suppression and emergency cutoff systems"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg",
        "SAGMOTO Z3 Tractor for Chemical Transport"
    )

    # Coal Transport
    content += scenario_section(
        "coal",
        "Coal Transport",
        "Built for the demanding conditions of coal mining regions, SAGMOTO tractor trucks deliver high torque output and reinforced chassis for heavy coal loads. The X3s tractor with Cummins ISME 420HP engine provides excellent power-to-weight ratio for regional coal haulage. Enhanced cooling systems and heavy-duty filtration ensure reliable operation in dusty environments.",
        [
            "Cummins ISME 420HP engine with high torque for heavy coal loads",
            "Reinforced chassis and suspension for demanding mine road conditions",
            "Enhanced cooling system for sustained heavy-load operation",
            "Heavy-duty air filtration for dusty mining environments"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/70f1e68f-95be-4336-9449-5dbe2e82e895.png",
        "SAGMOTO X3s Tractor for Coal Transport"
    )

    # Sand & Gravel Transport
    content += scenario_section(
        "sand",
        "Sand And Gravel Transport",
        "SAGMOTO tractors are ideal for construction material logistics with balanced performance and operating economy. The E3 tractor with Yuchai 340-400HP engine offers cost-effective solutions for regional sand and gravel hauling. Wide 850mm berths and optimized cab comfort reduce driver fatigue on long construction material delivery routes.",
        [
            "Yuchai YC6MK 340-400HP engine for cost-effective material transport",
            "850mm wide berth for driver rest during long-haul deliveries",
            "Efficient power chain optimized for mixed-load construction routes",
            "Excellent chassis configuration for stable heavy-material hauling"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4ed9de22-91e5-4290-8c61-65f41329d720.jpg",
        "SAGMOTO E3 Tractor for Construction Materials"
    )

    # Product showcase
    content += product_showcase_section(
        "Recommended Tractor Models",
        "Explore our tractor truck lineup designed for these applications",
        product_cards_by_category('heavy')
    )

    content += "\n" + cta_section()

    full_page('qyc.html',
        'Tractor - SAGMOTO',
        'SAGMOTO tractor trucks for port transport, hazardous chemicals transport, coal transport, and sand & gravel transport. Cummins and Yuchai engines from 340 to 560 HP.',
        'tractor, port transport, hazardous chemicals, coal transport, sand gravel, SAGMOTO, heavy duty truck',
        'Tractor', 'Tractor Applications',
        'Powerful and Reliable Tractor Solutions for Every Transport Need',
        content)


def build_zxc():
    """Dump Truck Application Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Dump Truck Applications</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO dump trucks are built for the toughest jobs. From urban construction sites to large-scale mining operations, our dump trucks deliver exceptional load-bearing capacity, rugged durability, and efficient material handling. With reinforced chassis, powerful hydraulic lifting systems, and engines from 160 to 400 HP, SAGMOTO dump trucks maximize your productivity in any working condition.</p>
</div>
</div>
</section>"""

    # Urban Construction
    content += scenario_section(
        "urban",
        "Urban Construction",
        "SAGMOTO dump trucks are engineered for urban construction environments with excellent maneuverability and efficient material handling. The X9 4X4 dump truck features all-wheel drive and leaf-spring suspension for strong bearing capacity, making it ideal for construction sites with challenging terrain. Low maintenance costs and extra-long service intervals minimize downtime on busy construction projects.",
        [
            "4x4 all-wheel drive for challenging construction site terrain",
            "Leaf-spring suspension with main and sub-springs for high load capacity",
            "Extra-long service intervals halving maintenance pit stops",
            "Front and rear dampers for improved comfort and load stability"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3f35ad3a-2ea6-42cb-bb86-2af2c12a16e7.jpg",
        "SAGMOTO X9 4X4 Dump Truck at Construction Site"
    )

    # Mining
    content += scenario_section(
        "mining",
        "Mining Operations",
        "For demanding mining operations, SAGMOTO off-road dump trucks deliver unmatched performance. The 850 wide-chassis structure ensures stable performance on poor road conditions, while the specialized rear suspension for mining increases flattening load from 25.3T to 30.5T. Directionally adjustable exhaust tailpipes prevent dust disruption, maintaining driver visibility in harsh mining environments.",
        [
            "850 wide-chassis structure for stability on poor mining roads",
            "Specialized mining rear suspension: load capacity increased to 30.5T",
            "Adjustable exhaust tailpipe to minimize dust and maintain visibility",
            "Reinforced oil pan protection grill and double-layer frame design"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg",
        "SAGMOTO Off-road Dump Truck in Mining"
    )

    # Product showcase
    content += product_showcase_section(
        "Recommended Dump Truck Models",
        "Explore our dump truck lineup for construction and mining applications",
        product_cards_by_ids(['light-01', 'offroad-01', 'offroad-02', 'offroad-03'])
    )

    content += "\n" + cta_section()

    full_page('zxc.html',
        'Dump Truck - SAGMOTO',
        'SAGMOTO dump trucks for urban construction and mining operations. 4x4 all-wheel drive, reinforced chassis, and engines from 160 to 400 HP.',
        'dump truck, tipper, urban construction, mining, off-road dump, SAGMOTO',
        'Dump Truck', 'Dump Truck Applications',
        'Rugged Dump Trucks for Construction and Mining',
        content)


def build_zhc():
    """Cargo Truck Application Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Cargo Truck Applications</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO cargo trucks provide versatile logistics solutions for express delivery, intercity transport, and city distribution. With Cummins ISD engines, optimized transmission systems, and maintenance-free drive axles, our cargo trucks deliver lower fuel consumption and higher efficiency. From the X6 dropside to the X6 AWD cargo truck, we have the right configuration for every logistics scenario.</p>
</div>
</div>
</section>"""

    # Express Delivery
    content += scenario_section(
        "express",
        "Express Delivery",
        "SAGMOTO cargo trucks are optimized for time-critical express delivery operations. The X6 dropside truck features minimum ground clearance of 314mm and approach angle greater than 25 degrees, ensuring accessibility to various delivery locations. The efficient new transmission system combined with maintenance-free drive axles and low-rolling-resistance tires delivers lower fuel consumption for cost-effective express delivery operations.",
        [
            "Efficient new transmission system for lower fuel consumption",
            "Maintenance-free high-efficiency drive axles",
            "Special low-rolling-resistance tires for reduced operating costs",
            "Airbag shock-absorbing main seat for driver comfort on long routes"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png",
        "SAGMOTO X6 Dropside for Express Delivery"
    )

    # Intercity Logistics
    content += scenario_section(
        "intercity",
        "Intercity Logistics",
        "For intercity logistics operations, SAGMOTO cargo trucks deliver the perfect balance of power, efficiency, and comfort. The X6 AWD cargo truck with 4x4 all-wheel drive provides reliable performance across varying road conditions between cities. The widest part of the lower sleeper reaches 85cm, ensuring driver rest quality during long-haul intercity routes.",
        [
            "4x4 all-wheel drive for varying intercity road conditions",
            "85cm wide lower sleeper for comfortable driver rest",
            "Cummins ISD 210HP engine for balanced power and efficiency",
            "Optimized aerodynamics for highway fuel efficiency"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9b7254c2-82fe-49dc-b3de-36d66fc0bdd2.jpg",
        "SAGMOTO X6 AWD Cargo Truck for Intercity Logistics"
    )

    # City Distribution
    content += scenario_section(
        "city-dist",
        "City Distribution",
        "SAGMOTO cargo trucks excel in urban city distribution with compact dimensions and flexible configurations. The modular weight reduction design with aluminum alloy and high-strength profiles enables higher payload capacity. Short wheelbase design with optional shortened axle provides smaller turning radius, ideal for navigating narrow city streets and tight delivery locations.",
        [
            "Modular weight reduction design with aluminum alloy profiles",
            "Short wheelbase with optional shortened axle for tight city streets",
            "Smaller turning radius for urban maneuverability",
            "Flexible configurations for various city distribution needs"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a9351ff3-e79c-44f1-b08f-a7bb8659d32f.png",
        "SAGMOTO X6 for City Distribution"
    )

    # Product showcase
    content += product_showcase_section(
        "Recommended Cargo Truck Models",
        "Explore our cargo truck lineup for logistics and distribution",
        product_cards_by_category('medium')
    )

    content += "\n" + cta_section()

    full_page('zhc.html',
        'Cargo Truck - SAGMOTO',
        'SAGMOTO cargo trucks for express delivery, intercity logistics, and city distribution. Cummins ISD engines, 4x4 AWD, and lightweight design.',
        'cargo truck, logistics, express delivery, intercity, city distribution, SAGMOTO',
        'Cargo Truck', 'Cargo Truck Applications',
        'Efficient Cargo Trucks for Modern Logistics',
        content)


def build_special():
    """Special Vehicle Application Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Special Vehicle Applications</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO special vehicles are purpose-built for specialized applications including city transportation, smart sanitation, dangerous goods transport, and road work & rescue. With high-strength materials, precision engineering, and multi-level safety protection systems, our special vehicles deliver reliable performance in the most demanding specialized operations.</p>
</div>
</div>
</section>"""

    # City Transportation
    content += scenario_section(
        "city",
        "City Transportation",
        "SAGMOTO special vehicles for city transportation combine efficiency with smart technology. The X9 aerial work platform truck features strong stability, convenient operation, and flexible mobility for urban elevated operations. Multi-level telescopic arms provide large operating range and fast lifting speed, making it ideal for municipal maintenance, signage installation, and urban infrastructure work.",
        [
            "Multi-level telescopic arms with large operating range",
            "Strong stability and convenient operation for urban environments",
            "High-strength materials and precision manufacturing",
            "Multiple safety protection systems in the cab"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg",
        "SAGMOTO X9 Aerial Work Platform Truck"
    )

    # Smart Sanitation
    content += scenario_section(
        "sanitation",
        "Smart Sanitation",
        "SAGMOTO smart sanitation vehicles bring efficiency to urban cleaning operations. The 9 Series Sweeper features high-capacity debris collection and powerful sweeping with dust suppression capabilities. The X6 sprinkler truck offers lightweight chassis design with frame beam suspension and the practical M3000 cab with sedan-like interior for comfortable municipal operations.",
        [
            "High-capacity debris collection system for efficient street cleaning",
            "Powerful sweeping with dust suppression for urban environments",
            "Lightweight chassis design for improved fuel efficiency",
            "Sedan-like interior cab for operator comfort"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8cd0ebb8-92b2-4dcf-a200-ffbc21fffe71.jpg",
        "SAGMOTO 9 Series Sweeper"
    )

    # Dangerous Goods
    content += scenario_section(
        "dangerous-goods",
        "Dangerous Goods Transportation",
        "SAGMOTO special vehicles for dangerous goods transportation are engineered with the highest safety standards. High-strength wear-resistant steel construction and reliable hydraulic systems ensure safe transport of hazardous materials. Reinforced multi-leaf springs and high-strength double-layer chassis handle complex working conditions while maintaining cargo integrity.",
        [
            "High-strength wear-resistant steel construction",
            "Reliable hydraulic system for safe hazardous material handling",
            "Reinforced multi-leaf springs for heavy-duty operations",
            "High-strength double-layer chassis for complex conditions"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2736f8a9-4674-4ae8-bda2-ff995e34c894.png",
        "SAGMOTO X7 Concrete Mixer for Special Applications"
    )

    # Road Work & Rescue
    content += scenario_section(
        "rescue",
        "Road Work & Rescue",
        "SAGMOTO recovery vehicles and road work trucks are designed for rapid response and reliable performance. The X9 tow truck handles gradients over 30%, easily coping with tough working conditions. With maximum gradient capability and robust construction, these vehicles provide dependable service for roadside assistance, construction support, and emergency recovery operations.",
        [
            "Maximum gradient capacity over 30% for tough terrain",
            "Robust construction for demanding recovery operations",
            "Reliable performance in emergency response scenarios",
            "Versatile configuration for various road work applications"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a2e376e5-bc63-4f1c-9379-cbef769fe0eb.jpg",
        "SAGMOTO X9 Tow Truck for Road Work & Rescue"
    )

    # Product showcase
    content += product_showcase_section(
        "Recommended Special Vehicle Models",
        "Explore our special vehicle lineup for specialized applications",
        product_cards_by_category('special')
    )

    content += "\n" + cta_section()

    full_page('special.html',
        'Special Vehicle - SAGMOTO',
        'SAGMOTO special vehicles for city transportation, smart sanitation, dangerous goods transport, and road work & rescue. High-strength materials and multi-level safety systems.',
        'special vehicle, aerial work, sanitation, sweeper, tow truck, dangerous goods, SAGMOTO',
        'Special Vehicle', 'Special Vehicle Applications',
        'Purpose-Built Special Vehicles for Every specialized Need',
        content)


def build_pzkyzyc():
    """Off-road Dump Truck Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Off-road Dump Truck</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO off-road dump trucks are engineered for the most extreme conditions. With 850 wide-chassis structure, specialized mining suspension, and powerful engines from 285 to 400 HP, these trucks deliver unmatched durability and load-bearing capacity in mining, quarrying, and large-scale construction operations. The directionally adjustable exhaust system and reinforced design ensure reliable performance where other trucks cannot operate.</p>
</div>
</div>
</section>"""

    # Key Features Section
    content += """
<!-- ===== KEY FEATURES ===== -->
<section class="section-bg-light">
<div class="container">
<div class="s_title category-title">
<h2>Key Advantages</h2>
<p>Engineered for extreme conditions</p>
</div>
<div class="feature-grid">
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M12 2L4 7v10c0 5.55 3.84 9.74 8 11 4.16-1.26 8-5.45 8-11V7l-8-5z" fill="#0D1F3D"/></svg></div>
<h3>850 Wide Chassis</h3>
<p>Adopting 850 wide-chassis structure for stable performance and adaptability to the most challenging road conditions in mining and construction environments.</p>
</div>
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z" fill="#C62828"/></svg></div>
<h3>30.5T Load Capacity</h3>
<p>Specialized rear suspension for mining operations increases flattening load from 25.3T to 30.5T, maximizing productivity per trip.</p>
</div>
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8z" fill="#C89B3C"/></svg></div>
<h3>Powerful Engines</h3>
<p>Yuchai and Cummins engine options from 285 to 400 HP deliver the high torque and reliable power needed for extreme off-road conditions.</p>
</div>
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#0D1F3D"/></svg></div>
<h3>Smart Dust Control</h3>
<p>Directionally adjustable exhaust tailpipe effectively prevents dust disruption, maintaining driver visibility in dusty mining environments.</p>
</div>
</div>
</div>
</section>"""

    # Off-road Dump Truck detail
    content += scenario_section(
        "offroad-dump",
        "Off-road Dump Truck",
        "The SAGMOTO off-road dump truck is built for the toughest mining and construction environments. With double-layer frame design, reinforced oil pan protection grill, and iron bumper, this truck handles the most punishing conditions. The 9 series offers multiple cab options and can be adapted for fuel tankers, sprinklers, and dump trucks.",
        [
            "Double-layer frame design for maximum structural integrity",
            "Reinforced oil pan protection grill for engine safety",
            "Iron bumper for enhanced front-end protection",
            "Multiple cab options and versatile upper-body configurations"
        ],
        "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg",
        "SAGMOTO Off-road Dump Truck"
    )

    # Product showcase
    content += product_showcase_section(
        "Off-road Truck Models",
        "Explore our complete off-road truck lineup",
        product_cards_by_category('offroad')
    )

    content += "\n" + cta_section()

    full_page('pzkyzyc.html',
        'Off-road Dump Truck - SAGMOTO',
        'SAGMOTO off-road dump trucks with 850 wide-chassis, 30.5T load capacity, and powerful engines for mining and extreme conditions.',
        'off-road dump truck, mining, 850 chassis, heavy duty, SAGMOTO',
        'Off-road Dump Truck', 'Off-road Dump Truck',
        'Built for the Toughest Mining and Construction Environments',
        content)


def build_pzmtc():
    """Off-road Tractor Product List Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Off-road Tractor</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO off-road tractors combine the power of heavy-duty tractors with the rugged capability of off-road trucks. Designed for operations that require both hauling capacity and off-road maneuverability, these vehicles are ideal for mining transport, forestry operations, and remote construction sites where conventional tractors cannot operate.</p>
</div>
</div>
</section>"""

    # Key Features
    content += """
<!-- ===== KEY FEATURES ===== -->
<section class="section-bg-light">
<div class="container">
<div class="s_title category-title">
<h2>Off-road Tractor Advantages</h2>
<p>Power meets versatility in challenging terrains</p>
</div>
<div class="feature-grid">
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M12 2L4 7v10c0 5.55 3.84 9.74 8 11 4.16-1.26 8-5.45 8-11V7l-8-5z" fill="#0D1F3D"/></svg></div>
<h3>All-Terrain Capability</h3>
<p>4x4 and 6x6 configurations with high ground clearance for operation on unpaved roads, mining tracks, and forestry paths.</p>
</div>
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z" fill="#C62828"/></svg></div>
<h3>High Torque Engines</h3>
<p>Cummins and Yuchai engines delivering up to 400 HP with high low-end torque for heavy-load hauling on challenging terrain.</p>
</div>
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8z" fill="#C89B3C"/></svg></div>
<h3>Reinforced Drivetrain</h3>
<p>Heavy-duty transmission, reinforced axles, and protected drivetrain components for reliable operation in extreme conditions.</p>
</div>
<div class="feature-card">
<div class="feature-icon"><svg width="48" height="48" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#0D1F3D"/></svg></div>
<h3>Versatile Configurations</h3>
<p>Multiple cab options and customizable upper-body configurations for fuel tankers, water bowsers, and specialized transport.</p>
</div>
</div>
</div>
</section>"""

    # Product showcase
    content += product_showcase_section(
        "Off-road Tractor Models",
        "Explore our off-road tractor and heavy-duty truck lineup",
        product_cards_by_category('offroad')
    )

    content += "\n" + cta_section()

    full_page('pzmtc.html',
        'Off-road Tractor - SAGMOTO',
        'SAGMOTO off-road tractors with 4x4/6x6 configurations, Cummins and Yuchai engines up to 400 HP for mining, forestry, and remote operations.',
        'off-road tractor, 4x4, mining tractor, heavy duty, SAGMOTO',
        'Off-road Tractor', 'Off-road Tractor',
        'Powerful Off-road Tractors for the Most Demanding Terrains',
        content)


def build_tzc():
    """Off-road Truck Product List Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Off-road Truck</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO off-road trucks are designed for operations where conventional trucks cannot go. With powerful engines, reinforced chassis, and all-terrain capability, our off-road truck series includes the 9 Series, 7 Series, and 6 Series, each engineered for specific off-road applications from mining to forestry to remote construction sites.</p>
</div>
</div>
</section>"""

    # Series showcase
    content += """
<!-- ===== SERIES SHOWCASE ===== -->
<section class="section-bg-light">
<div class="container">
<div class="s_title category-title">
<h2>Our Off-road Truck Series</h2>
<p>Three series engineered for different off-road challenges</p>
</div>
<div class="series-grid">"""

    # 9 Series
    content += """
<div class="series-card">
<div class="series-img">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8065c0e4-5d81-4f00-97c1-6026bc4ef78c.jpg" alt="9 Series Off-road Truck" loading="lazy">
</div>
<div class="series-body">
<h3>9 Series</h3>
<p class="series-spec">Durability & High Performance | Extreme Conditions</p>
<p>Engineered for maximum durability, high performance, and high load-bearing capacity. Multiple cab options available with convenient adaptation for fuel tankers, sprinklers, and dump trucks.</p>
<ul class="series-features">
<li>Yuchai / Cummins engine options up to 400 HP</li>
<li>High load-bearing capacity for extreme conditions</li>
<li>Versatile upper-body adaptation capability</li>
</ul>
</div>
</div>"""

    # 7 Series
    content += """
<div class="series-card">
<div class="series-img">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0c12b07d-79ed-4ed7-90af-72345564bbe7.jpg" alt="7 Series Off-road Truck" loading="lazy">
</div>
<div class="series-body">
<h3>7 Series</h3>
<p class="series-spec">Powerful Engine | Excellent Maneuverability</p>
<p>Built with a powerful engine and excellent maneuverability for challenging off-road environments. Reinforced oil pan protection grill and double-layer frame design ensure durability.</p>
<ul class="series-features">
<li>Yuchai engine with 340 HP output</li>
<li>Reinforced oil pan protection grill</li>
<li>Double-layer frame design for structural integrity</li>
</ul>
</div>
</div>"""

    # 6 Series
    content += """
<div class="series-card">
<div class="series-img">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/c98399ce-d138-4d6d-b27c-bfddda9aa601.jpg" alt="6 Series Off-road Truck" loading="lazy">
</div>
<div class="series-body">
<h3>6 Series</h3>
<p class="series-spec">Strong Power | Efficient Transportation</p>
<p>Combining strong power with efficient transportation capability. Reinforced design with iron bumper and customized upper-body options for specialized off-road applications.</p>
<ul class="series-features">
<li>Cummins ISD engine with 285 HP</li>
<li>Reinforced design with iron bumper</li>
<li>Customized upper-body options available</li>
</ul>
</div>
</div>"""

    content += """
</div>
</div>
</section>"""

    # Product showcase
    content += product_showcase_section(
        "All Off-road Models",
        "Complete off-road truck lineup",
        product_cards_by_category('offroad')
    )

    content += "\n" + cta_section()

    full_page('tzc.html',
        'Off-road Truck - SAGMOTO',
        'SAGMOTO off-road trucks: 9 Series, 7 Series, and 6 Series with Cummins and Yuchai engines for mining, forestry, and remote construction.',
        'off-road truck, 9 series, 7 series, 6 series, mining, SAGMOTO',
        'Off-road Truck', 'Off-road Truck',
        'Conquer Any Terrain with SAGMOTO Off-road Trucks',
        content)


def build_service():
    """Service Policy Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Service Policy</h2>
<div class="app-intro-line"></div>
<p>SAGMOTO is committed to providing comprehensive service and support for all our commercial vehicles. Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. Our global service network ensures that wherever your SAGMOTO truck operates, professional support is always within reach.</p>
</div>
</div>
</section>"""

    # Service sections
    content += """
<!-- ===== SERVICE SECTIONS ===== -->
<section class="section-bg-light">
<div class="container">
<div class="service-grid">"""

    # Find Provider
    content += """
<div class="service-card" id="find-provider">
<div class="service-icon"><svg width="56" height="56" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z" fill="#C62828"/></svg></div>
<h3>Find Your Service Provider</h3>
<p>SAGMOTO has established a comprehensive global service network with authorized service providers in over 50 countries. Our service centers are staffed with trained technicians who understand your vehicle inside and out. Use our service locator to find the nearest authorized service provider for maintenance, repairs, and genuine parts.</p>
<a href="contact.html" class="btn-outline">Find a Provider</a>
</div>"""

    # Maintenance
    content += """
<div class="service-card" id="maintenance">
<div class="service-icon"><svg width="56" height="56" viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z" fill="#0D1F3D"/></svg></div>
<h3>Maintenance Service</h3>
<p>Regular maintenance is key to maximizing the lifespan and performance of your SAGMOTO truck. Our maintenance service program includes scheduled inspections, engine tuning, transmission service, brake system checks, and chassis lubrication. With extra-long service intervals and maintenance-free components, SAGMOTO trucks minimize downtime and reduce total cost of ownership.</p>
<a href="contact.html" class="btn-outline">Schedule Service</a>
</div>"""

    # Driving Reminder
    content += """
<div class="service-card" id="driving-reminder">
<div class="service-icon"><svg width="56" height="56" viewBox="0 0 24 24"><path d="M11 17h2v-6h-2v6zm1-15C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zM11 9h2V7h-2v2z" fill="#C89B3C"/></svg></div>
<h3>Driving Reminder</h3>
<p>Safety on the road starts with proper driving habits. SAGMOTO driving reminders cover pre-trip inspections, load securing, speed management, and route planning. Our trucks are equipped with dual warning systems to ensure driving safety. Always check tire pressure, brake function, and fluid levels before departure. Maintain safe following distances and adjust speed for road and weather conditions.</p>
<a href="contact.html" class="btn-outline">Learn More</a>
</div>"""

    # Safe Driving
    content += """
<div class="service-card" id="safe-driving">
<div class="service-icon"><svg width="56" height="56" viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z" fill="#C62828"/></svg></div>
<h3>Safe Driving</h3>
<p>SAGMOTO prioritizes driver safety with advanced safety systems including ABS, EBD, and stability control. Our cabs meet European ECE-R29-03 collision standards for maximum protection. We provide comprehensive safe driving guidelines covering hazardous conditions, emergency procedures, and best practices for long-haul operations. The width of berths reaches 850mm with 800mm between upper and lower berths for comfortable, safe rest.</p>
<a href="contact.html" class="btn-outline">Safety Guidelines</a>
</div>"""

    content += """
</div>
</div>
</section>"""

    # Contact CTA
    content += """
<!-- ===== CONTACT CTA ===== -->
<section class="section-bg-white">
<div class="container">
<div class="service-contact">
<h2>Sales Service Hotline</h2>
<p>For service inquiries, parts orders, and technical support:</p>
<div class="contact-info">
<a href="tel:+8615319431311" class="contact-phone">
<svg width="24" height="24" viewBox="0 0 24 24"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z" fill="currentColor"/></svg>
+86 15319431311
</a>
<a href="mailto:sales@fenghan-trade.com" class="contact-email">
<svg width="24" height="24" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="currentColor"/></svg>
sales@fenghan-trade.com
</a>
</div>
</div>
</div>
</section>"""

    full_page('service.html',
        'Service Policy - SAGMOTO',
        'SAGMOTO service policy: find service providers, maintenance service, driving reminders, and safe driving guidelines. Global service network in 50+ countries.',
        'service, maintenance, repair, safe driving, service provider, SAGMOTO',
        'Services', 'Service Policy',
        'Comprehensive Service and Support for Your SAGMOTO Fleet',
        content)


def build_video_list():
    """Video Center Page"""
    content = """
<!-- ===== INTRO ===== -->
<section class="section-bg-white">
<div class="container">
<div class="app-intro">
<h2>Video Center</h2>
<div class="app-intro-line"></div>
<p>Explore SAGMOTO commercial vehicles in action. Watch product showcases, application demonstrations, and technology highlights. See how our trucks perform across diverse industries and challenging environments.</p>
</div>
</div>
</section>"""

    # Video grid
    content += """
<!-- ===== VIDEO GRID ===== -->
<section class="section-bg-light">
<div class="container">
<div class="video-grid">
<div class="video-card">
<div class="video-thumbnail">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg" alt="E1st Tractor Showcase" loading="lazy">
<div class="play-button"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="white"/></svg></div>
</div>
<div class="video-info">
<h3>E1st Flagship Tractor</h3>
<p>Cummins Z14 560HP flagship tractor truck showcase with Eaton AMT gearbox and intelligent cab design.</p>
</div>
</div>
<div class="video-card">
<div class="video-thumbnail">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg" alt="Z3 Tractor Technology" loading="lazy">
<div class="play-button"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="white"/></svg></div>
</div>
<div class="video-info">
<h3>Z3 Tractor Technology</h3>
<p>Next-generation powertrain and intelligent electronic systems with European safety standard cab design.</p>
</div>
</div>
<div class="video-card">
<div class="video-thumbnail">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3f35ad3a-2ea6-42cb-bb86-2af2c12a16e7.jpg" alt="X9 4X4 Dump Truck" loading="lazy">
<div class="play-button"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="white"/></svg></div>
</div>
<div class="video-info">
<h3>X9 4X4 Dump Truck</h3>
<p>All-wheel drive dump truck with leaf-spring suspension for strong bearing capacity in construction applications.</p>
</div>
</div>
<div class="video-card">
<div class="video-thumbnail">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png" alt="X6 Cargo Truck" loading="lazy">
<div class="play-button"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="white"/></svg></div>
</div>
<div class="video-info">
<h3>X6 Cargo Truck</h3>
<p>Efficient new transmission system with maintenance-free drive axles and low-rolling-resistance tires.</p>
</div>
</div>
<div class="video-card">
<div class="video-thumbnail">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg" alt="Off-road Dump Truck" loading="lazy">
<div class="play-button"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="white"/></svg></div>
</div>
<div class="video-info">
<h3>Off-road Dump Truck</h3>
<p>850 wide-chassis with 30.5T load capacity for mining operations in extreme conditions.</p>
</div>
</div>
<div class="video-card">
<div class="video-thumbnail">
<img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a161feeb-72a6-456a-8368-32970c2d9df0.jpg" alt="i9 Electric Truck" loading="lazy">
<div class="play-button"><svg width="64" height="64" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="white"/></svg></div>
</div>
<div class="video-info">
<h3>i9 Electric Truck</h3>
<p>Integrated electric drive axle with 430km range and 120KW fast charging technology for new energy logistics.</p>
</div>
</div>
</div>
</div>
</section>"""

    content += "\n" + cta_section()

    full_page('video_list.html',
        'Video Center - SAGMOTO',
        'Watch SAGMOTO commercial vehicle videos: tractor trucks, dump trucks, cargo trucks, off-road trucks, and new energy vehicles in action.',
        'video, SAGMOTO, truck video, product showcase, commercial vehicle',
        'Video Center', 'Video Center',
        'Watch SAGMOTO Trucks in Action',
        content)


# ===== Main =====
if __name__ == '__main__':
    print("Building SAGMOTO custom sub-pages...")
    print()

    build_qyc()
    build_zxc()
    build_zhc()
    build_special()
    build_pzkyzyc()
    build_pzmtc()
    build_tzc()
    build_service()
    build_video_list()

    print()
    print("All pages generated successfully!")
