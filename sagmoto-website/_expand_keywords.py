"""
_expand_keywords.py - 2号站(sagmoto-trucks.com) SEO关键词全面扩展
修复：品牌名、中文关键词、模板描述、新闻元数据、产品关键词扩充、sitemap、canonical

Operations:
1. Fix brand name: "SAG Commercial Vehicle Company" -> "SAGMOTO" (14 pages)
2. Remove Chinese keyword "其它" (10 pages)
3. Replace template descriptions with page-specific ones (9 pages)
4. Add description/keywords to 5 news detail pages
5. Expand keywords for product pages (13 pages, target 10-15 each)
6. Fix index.html canonical URL
7. Add keywords to privacy/terms
8. Update sitemap.xml with missing URLs
9. Update dateModified to today
"""

import re
import os
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()

changes_log = []

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def log(msg):
    changes_log.append(msg)
    print(f"  [OK] {msg}")

# =============================================================================
# PHASE 1: Fix brand name + remove "其它" + fix template descriptions
# Pages: about, service, video_list, qyc, zxc, zhc, special, tzc, pzkyzyc, pzmtc, news_list/1, news_list/81163, service_list/*
# =============================================================================

def phase1_fix_legacy_pages():
    """Fix brand name, Chinese keywords, template descriptions in legacy pages"""
    
    # Pages with structure: title, description, keywords, og:title, og:description, og:site_name, twitter:title, twitter:description
    # These all have the "SAG Commercial Vehicle Company" brand + "其它" keyword + template desc
    
    legacy_pages = {
        'about.html': {
            'old_title': 'About Us-SAG Commercial Vehicle Company',
            'new_title': 'About Us - SAGMOTO',
            'old_desc': 'SAG Commercial Vehicle Company About Us Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO is one of the top 10 commercial vehicle brands in China, headquartered in Baoji, Shaanxi. Authorized exporter: Shaanxi Fenghan Trading Co., Ltd. Contact us for factory-direct truck pricing, specifications, and export to Africa, Middle East, Latin America, and Southeast Asia.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,About Us',
            'new_kw': 'SAGMOTO, Shaanxi Automobile, commercial vehicle manufacturer, Chinese truck brand, heavy duty truck, light duty truck, Shaanxi Fenghan Trading, truck exporter China',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'service.html': {
            'old_title': 'Service Policy-SAG Commercial Vehicle Company',
            'new_title': 'Service Policy - SAGMOTO',
            'old_desc': 'SAG Commercial Vehicle Company Service Policy Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO service policy and after-sales support. Warranty coverage, spare parts supply, technical training, and maintenance services for SAGMOTO commercial vehicles exported worldwide. Authorized distributor: Shaanxi Fenghan Trading.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Service Policy',
            'new_kw': 'SAGMOTO service, truck after-sales, commercial vehicle warranty, spare parts supply, truck maintenance, technical support, SAGMOTO dealer, Fenghan Trading',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'video_list.html': {
            'old_title': 'Video Center-SAG Commercial Vehicle Company',
            'new_title': 'Video Center - SAGMOTO',
            'old_desc': 'SAG Commercial Vehicle Company Video Center Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO video center featuring commercial vehicle product showcases, factory tours, off-road testing, customer testimonials, and industry exhibitions. Watch SAGMOTO trucks in action across global markets.',
            'old_kw': 'Light duty truck,Heavy duty truck,其它,Video Center',
            'new_kw': 'SAGMOTO video, truck showcase, commercial vehicle video, factory tour, off-road testing, heavy truck video, SAGMOTO truck review, Chinese truck video',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'qyc.html': {
            'old_title': 'Tractor-SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Tractor Trucks | Heavy-Duty Tractor Head for Export',
            'old_desc': 'SAG Commercial Vehicle Company Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO tractor trucks for long-haul logistics and heavy transport. Featuring E1st, Z3, X3s tractor heads with Cummins/Yuchai engines, 420-580HP. Factory-direct export pricing from Shaanxi Fenghan Trading to Africa, Middle East, Latin America, CIS.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Tractor',
            'new_kw': 'SAGMOTO tractor truck, tractor head, heavy duty tractor, long-haul truck, logistics truck, trailer truck, Cummins tractor, 6x4 tractor, Chinese tractor truck, truck for Africa, truck export, Shaanxi Fenghan Trading',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'zxc.html': {
            'old_title': 'Dump truck-SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Dump Trucks | Construction & Mining Tipper Trucks',
            'old_desc': 'SAG Commercial Vehicle Company Dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO dump trucks (tipper trucks) for construction, mining, and earthmoving. Available in 6x4, 8x4 configurations, 25T-90T payload capacity. Models: X1s, X3s, X6, X9, E3. Factory-direct price from Shaanxi Fenghan Trading.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Dump truck',
            'new_kw': 'SAGMOTO dump truck, tipper truck, construction truck, mining dump truck, 6x4 dump truck, 8x4 dump truck, heavy duty tipper, Chinese dump truck, dump truck price, Africa dump truck, Middle East truck, Shaanxi truck',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'zhc.html': {
            'old_title': 'Cargo truck-SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Cargo Trucks | Light & Heavy-Duty Freight Vehicles',
            'old_desc': 'SAG Commercial Vehicle Company Cargo truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO cargo trucks including van trucks, flatbed trucks, stake trucks, and refrigerated trucks. Covering light, medium, and heavy-duty segments. Models: E3, E6, E9, X5, X6, X7, X9. Factory-direct export from Shaanxi Fenghan Trading.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Cargo truck',
            'new_kw': 'SAGMOTO cargo truck, van truck, flatbed truck, refrigerated truck, stake truck, freight truck, light duty truck, heavy duty cargo, logistics vehicle, Chinese cargo truck, truck exporter, Shaanxi truck',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'special.html': {
            'old_title': 'Special vehicle-SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Special Vehicles | Fire Truck, Garbage Truck & More',
            'old_desc': 'SAG Commercial Vehicle Company Special vehicle Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO special purpose vehicles: fire trucks, garbage compactors, sewage suction trucks, road sweepers, water tankers, and concrete mixers. Built on proven SAGMOTO chassis. Factory-direct export pricing from Shaanxi Fenghan Trading.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Special vehicle',
            'new_kw': 'SAGMOTO special vehicle, fire truck, garbage truck, road sweeper, water tanker, sewage truck, concrete mixer truck, municipal vehicle, sanitation truck, specialty truck, Chinese special vehicle, Shaanxi truck',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'tzc.html': {
            'old_title': 'Off-road truck-SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Off-Road Trucks | 4x4 & All-Wheel Drive Vehicles',
            'old_desc': 'SAG Commercial Vehicle Company Off-road truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO off-road trucks built for extreme terrain: mining, oil fields, desert operations. 4x4 and 6x6 all-wheel drive configurations. Heavy-duty chassis with high ground clearance. Factory-direct export from Shaanxi Fenghan Trading to global markets.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Off-road truck',
            'new_kw': 'SAGMOTO off-road truck, 4x4 truck, all-wheel drive truck, mining truck, oil field truck, desert truck, extreme terrain vehicle, off-road dump truck, military truck chassis, Chinese off-road truck, Shaanxi truck',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'pzkyzyc.html': {
            'old_title': 'Off-road dump truck -SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Off-Road Mining Dump Trucks | Heavy-Duty Tipper',
            'old_desc': 'SAG Commercial Vehicle Company Off-road dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO off-road mining dump trucks for large-scale earthmoving and open-pit mining operations. Heavy-duty construction with reinforced chassis, high-torque powertrain. Available in multiple configurations. Factory-direct export pricing from Shaanxi Fenghan Trading.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Off-road dump truck',
            'new_kw': 'SAGMOTO mining truck, off-road dump truck, articulated dump truck, open-pit mining truck, heavy tipper, construction dump truck, 6x4 off-road, mining vehicle China, Shaanxi mining truck, Africa mining, Latin America mining',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
        'pzmtc.html': {
            'old_title': 'Off-road Tractor-SAG Commercial Vehicle Company',
            'new_title': 'SAGMOTO Off-Road Tractor Trucks | Heavy Haul Transport',
            'old_desc': 'SAG Commercial Vehicle Company Off-road Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY.',
            'new_desc': 'SAGMOTO off-road tractor trucks for heavy-haul and extreme condition transport. Built for oil fields, mining sites, and infrastructure projects. High-power engines with heavy-duty drivetrain. Factory-direct export from Shaanxi Fenghan Trading.',
            'old_kw': '其它,Light duty truck,Heavy duty truck,Off-road Tractor',
            'new_kw': 'SAGMOTO off-road tractor, heavy haul tractor, oil field tractor, mining tractor, extreme condition truck, 6x6 tractor, heavy transport truck, Chinese heavy truck, Africa transport, Middle East oil field',
            'old_site_name': 'SAG Commercial Vehicle Company',
            'new_site_name': 'SAGMOTO',
        },
    }
    
    for filename, vars_data in legacy_pages.items():
        filepath = os.path.join(BASE, filename)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {filename} not found")
            continue
        
        content = read_file(filepath)
        original = content
        
        # Replace brand name globally
        content = content.replace('SAG Commercial Vehicle Company', 'SAGMOTO')
        
        # Fix title
        if vars_data['old_title'] in content:
            content = content.replace(vars_data['old_title'], vars_data['new_title'])
        
        # Fix description
        if vars_data['old_desc'] in content:
            content = content.replace(vars_data['old_desc'], vars_data['new_desc'])
        
        # Fix keywords
        if vars_data['old_kw'] in content:
            content = content.replace(vars_data['old_kw'], vars_data['new_kw'])
        
        if content != original:
            write_file(filepath, content)
            log(f"[Phase1] Fixed {filename}: brand+title+desc+keywords")
        else:
            print(f"  [WARN] {filename}: no changes made (check old_strings)")
    
    # Also fix news_list pages (they have different structure)
    news_list_fixes = {
        'news_list/1.html': {
            'old_title': 'News Centre-SAG Commercial Vehicle Company',
            'new_title': 'News Centre - SAGMOTO',
            'old_desc': 'News SAG Commercial Vehicle Company',
            'new_desc': 'SAGMOTO News Centre - Latest updates on SAGMOTO commercial vehicles, industry events, new product launches, and export market developments.',
            'old_kw': 'News,News Centre',
            'new_kw': 'SAGMOTO news, commercial vehicle news, truck industry, SAGMOTO update, Chinese truck news, export truck news, Fenghan Trading',
        },
        'news_list/81163.html': {
            'old_title': 'News-SAG Commercial Vehicle Company',
            'new_title': 'News - SAGMOTO',
            'old_desc': 'News SAG Commercial Vehicle Company',
            'new_desc': 'SAGMOTO News Centre - Latest updates on SAGMOTO commercial vehicles, industry events, new product launches, and export market developments.',
            'old_kw': 'News,News',
            'new_kw': 'SAGMOTO news, commercial vehicle news, truck industry, SAGMOTO update, Chinese truck news, export truck news, Fenghan Trading',
        },
    }
    
    for filename, vars_data in news_list_fixes.items():
        filepath = os.path.join(BASE, filename)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {filename} not found")
            continue
        content = read_file(filepath)
        content = content.replace(vars_data['old_title'], vars_data['new_title'])
        content = content.replace(vars_data['old_desc'], vars_data['new_desc'])
        content = content.replace(vars_data['old_kw'], vars_data['new_kw'])
        write_file(filepath, content)
        log(f"[Phase1] Fixed {filename}: title+desc+keywords")


# =============================================================================
# PHASE 2: Add description + keywords to 5 news detail pages
# =============================================================================

def phase2_fix_news_details():
    """Add missing description and keywords meta tags to news detail pages"""
    
    news_pages = {
        'news_Detail/18.html': {
            'desc': 'SAGMOTO newly upgraded X3s heavy truck with enhanced powertrain, improved cabin comfort, and advanced safety features. Read about the technological breakthroughs and market strategy for global markets including Africa, Middle East, and Southeast Asia. Shaanxi Fenghan Trading - authorized SAGMOTO exporter.',
            'kw': 'SAGMOTO X3s, X3s heavy truck, SAGMOTO upgrade, heavy truck technology, Chinese heavy truck, Shaanxi truck, SAGMOTO news, Fenghan Trading, truck export, Africa truck market',
            'insert_after': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        },
        'news_Detail/19.html': {
            'desc': 'SAGMOTO Chinese New Year Greeting 2025 - Celebrating the Year of the Snake with global partners and customers. SAGMOTO commercial vehicles continue to serve markets across Africa, Middle East, Latin America, and Asia. Shaanxi Fenghan Trading wishes all partners prosperity in the new year.',
            'kw': 'SAGMOTO New Year 2025, Chinese New Year, Year of the Snake, SAGMOTO global, Chinese truck, commercial vehicle greeting, Fenghan Trading, truck industry news',
            'insert_after': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        },
        'news_Detail/20.html': {
            'desc': 'SAGMOTO specialized trucks debut at the 137th Canton Fair, showcasing the full product lineup including tractors, dump trucks, cargo trucks, and special vehicles. Meet SAGMOTO at China\'s largest trade fair. Authorized exporter: Shaanxi Fenghan Trading Co., Ltd.',
            'kw': 'SAGMOTO Canton Fair, 137th Canton Fair, SAGMOTO special truck, Chinese truck exhibition, SAGMOTO product showcase, truck export China, Fenghan Trading, commercial vehicle trade fair, China import export',
            'insert_after': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        },
        'news_Detail/21.html': {
            'desc': 'SAGMOTO X3s tractor truck debuts in Armenia, Caucasus region. A milestone for SAGMOTO\'s expansion into Central Asian and CIS markets. Learn about the X3s specifications, local partnership, and market outlook. Authorized exporter: Shaanxi Fenghan Trading.',
            'kw': 'SAGMOTO Armenia, SAGMOTO X3s tractor, Caucasus truck market, SAGMOTO CIS, Central Asia truck, Armenian truck market, Chinese truck export, Fenghan Trading, X3s tractor truck',
            'insert_after': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        },
        'news_Detail/22.html': {
            'desc': 'Inside Shaanxi Automobile\'s intelligent heavy truck production factory. Discover the automated assembly lines, robotic welding, and quality control systems behind SAGMOTO commercial vehicles. Advanced manufacturing for reliable truck export. Shaanxi Fenghan Trading - authorized SAGMOTO exporter.',
            'kw': 'Shaanxi Automobile factory, SAGMOTO production, intelligent manufacturing, heavy truck assembly, automated production, Chinese truck factory, SAGMOTO quality, Fenghan Trading, truck manufacturing China, Industry 4.0 truck',
            'insert_after': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        },
    }
    
    for filename, data in news_pages.items():
        filepath = os.path.join(BASE, filename)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {filename} not found")
            continue
        content = read_file(filepath)
        
        # Check if description already exists
        if '<meta name="description"' in content:
            print(f"  [SKIP] {filename}: description already exists")
            continue
        
        # Insert description and keywords after the insert point
        insert_html = f'\n    <meta name="description" content="{data["desc"]}"/>\n    <meta name="keywords" content="{data["kw"]}"/>'
        
        if data['insert_after'] in content:
            content = content.replace(data['insert_after'], data['insert_after'] + insert_html)
            write_file(filepath, content)
            log(f"[Phase2] Added desc+keywords to {filename}")
        else:
            print(f"  [WARN] {filename}: insert_after not found")


# =============================================================================
# PHASE 3: Expand keywords for product pages (13 pages)
# =============================================================================

def phase3_expand_product_keywords():
    """Expand keywords for product pages to 10-15 keywords each"""
    
    product_keywords = {
        'e1st.html': {
            'old_kw': 'E1st, SAGMOTO E1st, commercial truck, heavy-duty',
            'new_kw': 'SAGMOTO E1st, E1st tractor truck, SAGMOTO flagship, Cummins Z14 engine, heavy-duty tractor, long-haul truck, 6x4 tractor, Chinese heavy truck, tractor head, truck for Africa, truck for Middle East, Shaanxi Fenghan Trading, truck exporter China',
        },
        'e3.html': {
            'old_kw': 'E3 Series, SAGMOTO E3, tractor truck, dump truck, van truck, cement mixer, garbage truck, commercial truck, heavy-duty',
            'new_kw': 'SAGMOTO E3, E3 series truck, heavy-duty truck, E3 tractor, E3 dump truck, E3 cement mixer, Yuchai engine truck, Chinese commercial vehicle, construction truck, logistics truck, Africa truck supplier, Middle East truck, Shaanxi Fenghan Trading, truck export',
        },
        'e6.html': {
            'old_kw': 'E6 Series, SAGMOTO E6, van truck, stake truck, refrigerated truck, sprinkler truck, truck-mounted crane, commercial truck, medium-duty',
            'new_kw': 'SAGMOTO E6, E6 medium truck, E6 van truck, E6 refrigerated truck, E6 sprinkler truck, E6 truck-mounted crane, medium-duty truck, Chinese truck medium, cold chain truck, municipal truck, Southeast Asia truck, Africa logistics truck, Shaanxi Fenghan Trading',
        },
        'e9.html': {
            'old_kw': 'E9 Series, SAGMOTO E9, van truck, flatbed truck, garbage truck, commercial truck, heavy-duty',
            'new_kw': 'SAGMOTO E9, E9 heavy truck, E9 van truck, E9 flatbed truck, E9 garbage truck, heavy-duty cargo, Chinese heavy truck, long wheelbase truck, freight truck, Latin America truck, Middle East cargo truck, Shaanxi Fenghan Trading, truck exporter',
        },
        'i5.html': {
            'old_kw': 'i5 Electric, SAGMOTO i5 Electric, commercial truck, new-energy',
            'new_kw': 'SAGMOTO i5 electric, i5 EV truck, electric commercial vehicle, electric logistics truck, zero-emission truck, city delivery EV, Chinese electric truck, new energy commercial vehicle, green logistics, last-mile delivery, urban electric truck, Shaanxi Fenghan Trading, BEV truck',
        },
        'i9.html': {
            'old_kw': 'i9 Series, SAGMOTO i9, electric truck, new energy, light-duty, commercial truck, zero-emission',
            'new_kw': 'SAGMOTO i9 electric, i9 EV light truck, electric cargo truck, zero-emission commercial vehicle, electric van truck, Chinese electric truck 2025, new energy truck, green transport, city logistics EV, Africa EV truck, Shaanxi Fenghan Trading, battery electric vehicle',
        },
        'x3s.html': {
            'old_kw': 'X3s Series, SAGMOTO X3s, dump truck, lorry truck, mixer truck, oil tanker, truck-mounted crane, commercial truck, heavy-duty',
            'new_kw': 'SAGMOTO X3s, X3s dump truck, X3s mixer truck, X3s oil tanker, X3s truck-mounted crane, heavy-duty truck, construction truck, 6x4 truck, 8x4 truck, Chinese heavy truck, Africa construction truck, Middle East dump truck, Shaanxi Fenghan Trading, truck export',
        },
        'x5.html': {
            'old_kw': 'X5 Series, SAGMOTO X5 Series, commercial truck, medium-duty',
            'new_kw': 'SAGMOTO X5, X5 medium truck, X5 cargo truck, X5 van truck, medium-duty truck, 4x2 truck, Chinese medium truck, logistics truck, distribution truck, Africa medium truck, Southeast Asia truck, Shaanxi Fenghan Trading, truck price China',
        },
        'x6.html': {
            'old_kw': 'X6 Series, SAGMOTO X6, concrete mixer, garbage truck, fuel tanker, sprinkler truck, sweeper, truck-mounted crane, commercial truck, medium-duty',
            'new_kw': 'SAGMOTO X6, X6 concrete mixer, X6 garbage truck, X6 fuel tanker, X6 sprinkler truck, X6 road sweeper, X6 truck-mounted crane, medium-duty special truck, Chinese special vehicle, municipal truck, construction truck, Africa special truck, Shaanxi Fenghan Trading',
        },
        'x7.html': {
            'old_kw': 'X7 Series, SAGMOTO X7, dump truck, cargo truck, flatbed truck, van truck, concrete mixer, sprinkler truck, truck-mounted crane, commercial truck, light-duty',
            'new_kw': 'SAGMOTO X7, X7 dump truck, X7 cargo truck, X7 flatbed truck, X7 concrete mixer, X7 van truck, light-duty truck, Chinese light truck, small construction truck, city delivery truck, Africa light truck, Latin America truck, Shaanxi Fenghan Trading, truck exporter',
        },
        'x9.html': {
            'old_kw': 'X9 Series, SAGMOTO X9, 4x4 dump truck, refrigerated truck, garbage truck, fuel tanker, cement mixer, sweeper, tow truck, aerial work platform, truck-mounted crane, commercial truck, light-duty',
            'new_kw': 'SAGMOTO X9, X9 4x4 dump truck, X9 refrigerated truck, X9 garbage truck, X9 fuel tanker, X9 cement mixer, X9 sweeper, X9 tow truck, X9 aerial work platform, light-duty truck, all-purpose truck, Chinese light truck, Africa multi-purpose truck, Shaanxi Fenghan Trading',
        },
        'z3.html': {
            'old_kw': 'Z3 Tractor, SAGMOTO Z3 Tractor, commercial truck, heavy-duty',
            'new_kw': 'SAGMOTO Z3, Z3 conventional tractor, long-nose tractor truck, heavy-duty tractor, Cummins tractor, 6x4 tractor head, long-haul transport, Chinese tractor truck, Africa tractor, Middle East tractor, Latin America truck, Shaanxi Fenghan Trading, truck export price',
        },
        'off-road-4x4.html': {
            'old_kw': 'Off-road 4x4, SAGMOTO off-road, dump truck, 4x4, all-wheel drive, mining truck, commercial truck',
            'new_kw': 'SAGMOTO off-road 4x4, 4x4 dump truck, all-wheel drive truck, mining truck, desert truck, oil field truck, extreme terrain vehicle, off-road construction truck, Chinese 4x4 truck, Africa mining truck, Latin America off-road, Shaanxi Fenghan Trading, heavy-duty 4x4',
        },
        'products.html': {
            'old_kw': 'SAGMOTO products, trucks, light duty truck, heavy duty truck, tractor, dump truck, cargo truck, special vehicle',
            'new_kw': 'SAGMOTO products, SAGMOTO truck lineup, light duty truck, medium duty truck, heavy duty truck, tractor truck, dump truck, cargo truck, special vehicle, new energy truck, electric truck, Chinese truck catalog, Shaanxi Fenghan Trading, truck for Africa, truck export China',
        },
        'new-energy.html': {
            'old_kw': 'new energy, electric truck, EV, zero emission, green logistics, SAGMOTO, battery electric vehicle',
            'new_kw': 'SAGMOTO new energy, SAGMOTO electric truck, EV commercial vehicle, zero emission truck, green logistics, battery electric vehicle, BEV truck, Chinese electric truck, urban electric truck, electric sanitation truck, new energy commercial vehicle, Shaanxi Fenghan Trading, sustainable transport',
        },
    }
    
    for filename, data in product_keywords.items():
        filepath = os.path.join(BASE, filename)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {filename} not found")
            continue
        content = read_file(filepath)
        
        kw_pattern = f'<meta content="{data["old_kw"]}" name="keywords"/>'
        if kw_pattern in content:
            new_kw_tag = f'<meta content="{data["new_kw"]}" name="keywords"/>'
            content = content.replace(kw_pattern, new_kw_tag)
            write_file(filepath, content)
            log(f"[Phase3] Expanded keywords for {filename}: {len(data['old_kw'].split(','))} -> {len(data['new_kw'].split(','))} keywords")
        else:
            # Try alternate format
            kw_pattern2 = f'<meta name="keywords" content="{data["old_kw"]}"/>'
            if kw_pattern2 in content:
                new_kw_tag2 = f'<meta name="keywords" content="{data["new_kw"]}"/>'
                content = content.replace(kw_pattern2, new_kw_tag2)
                write_file(filepath, content)
                log(f"[Phase3] Expanded keywords for {filename} (format2): {len(data['old_kw'].split(','))} -> {len(data['new_kw'].split(','))} keywords")
            else:
                print(f"  [WARN] {filename}: keyword pattern not found. Tried: '{data['old_kw'][:50]}...'")


# =============================================================================
# PHASE 4: Fix index.html canonical URL + add keywords to privacy/terms
# =============================================================================

def phase4_misc_fixes():
    """Canonical URL fix, privacy/terms keywords"""
    
    # 4a: Fix index.html canonical
    index_path = os.path.join(BASE, 'index.html')
    if os.path.exists(index_path):
        content = read_file(index_path)
        old_canonical = '<link rel="canonical" href="https://charlie555666.github.io/shacman-catalog/sagmoto-website/">'
        new_canonical = '<link rel="canonical" href="https://sagmoto-trucks.com/">'
        if old_canonical in content:
            content = content.replace(old_canonical, new_canonical)
            write_file(index_path, content)
            log("[Phase4] Fixed index.html canonical -> sagmoto-trucks.com")
        elif 'charlie555666.github.io' in content:
            # Try regex-based replacement
            content = re.sub(
                r'<link rel="canonical" href="https://charlie555666\.github\.io/shacman-catalog/sagmoto-website/?">',
                '<link rel="canonical" href="https://sagmoto-trucks.com/">',
                content
            )
            write_file(index_path, content)
            log("[Phase4] Fixed index.html canonical (regex)")
        else:
            print("  [WARN] index.html: canonical already fixed or not found")
    
    # 4b: Add keywords to privacy.html
    privacy_path = os.path.join(BASE, 'privacy.html')
    if os.path.exists(privacy_path):
        content = read_file(privacy_path)
        if '<meta name="keywords"' not in content:
            # Insert after description meta
            desc_pattern = '<meta name="description" content="SAGMOTO Privacy Policy'
            if desc_pattern in content:
                kw_tag = '\n    <meta name="keywords" content="SAGMOTO privacy, privacy policy, data protection, personal information, commercial vehicle website, Shaanxi Fenghan Trading"/>'
                content = content.replace(desc_pattern, desc_pattern + kw_tag)
                write_file(privacy_path, content)
                log("[Phase4] Added keywords to privacy.html")
            else:
                print("  [WARN] privacy.html: desc pattern not found")
    
    # 4c: Add keywords to terms.html
    terms_path = os.path.join(BASE, 'terms.html')
    if os.path.exists(terms_path):
        content = read_file(terms_path)
        if '<meta name="keywords"' not in content:
            desc_pattern = '<meta name="description" content="SAGMOTO Terms of Use'
            if desc_pattern in content:
                kw_tag = '\n    <meta name="keywords" content="SAGMOTO terms, terms of use, website terms, legal, commercial vehicle terms, Shaanxi Fenghan Trading"/>'
                content = content.replace(desc_pattern, desc_pattern + kw_tag)
                write_file(terms_path, content)
                log("[Phase4] Added keywords to terms.html")
            else:
                print("  [WARN] terms.html: desc pattern not found")
    
    # 4d: Fix index.html keywords expansion
    if os.path.exists(index_path):
        content = read_file(index_path)
        old_kw = '<meta name="keywords" content="SAGMOTO, Shacman, commercial vehicle, tractor, dump truck, cargo truck, Fenghan Trading, light duty truck, heavy duty truck">'
        new_kw = '<meta name="keywords" content="SAGMOTO, Shacman, Shaanxi Automobile, commercial vehicle, tractor truck, dump truck, cargo truck, special vehicle, new energy truck, heavy duty truck, light duty truck, Chinese truck exporter, Fenghan Trading, truck for Africa, truck for Middle East, truck for Latin America, truck for Southeast Asia">'
        if old_kw in content:
            content = content.replace(old_kw, new_kw)
            write_file(index_path, content)
            log("[Phase4] Expanded keywords for index.html")
        else:
            print("  [WARN] index.html: keyword pattern not found")


# =============================================================================
# PHASE 5: Update sitemap.xml with missing URLs + update dates
# =============================================================================

def phase5_update_sitemap():
    """Add missing URLs to sitemap.xml and update lastmod dates"""
    
    sitemap_path = os.path.join(BASE, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        print("  [SKIP] sitemap.xml not found")
        return
    
    content = read_file(sitemap_path)
    
    # Update lastmod dates for existing entries
    content = re.sub(
        r'<lastmod>2026-07-\d{2}</lastmod>',
        f'<lastmod>{TODAY}</lastmod>',
        content
    )
    
    # Add missing URLs (check if already present)
    missing_urls = [
        ('news.html', '0.7', 'weekly'),
        ('privacy.html', '0.3', 'yearly'),
        ('terms.html', '0.3', 'yearly'),
        ('video_list.html', '0.6', 'monthly'),
        ('off-road-4x4.html', '0.8', 'weekly'),
        ('pzkyzyc.html', '0.7', 'monthly'),
        ('pzmtc.html', '0.7', 'monthly'),
        ('news_Detail/18.html', '0.6', 'monthly'),
        ('news_Detail/19.html', '0.5', 'monthly'),
        ('news_Detail/20.html', '0.6', 'monthly'),
        ('news_Detail/21.html', '0.6', 'monthly'),
        ('news_Detail/22.html', '0.6', 'monthly'),
    ]
    
    # Also add news_list and service_list pages
    extra_urls = [
        ('news_list/1.html', '0.5', 'monthly'),
        ('news_list/81163.html', '0.5', 'monthly'),
    ]
    missing_urls.extend(extra_urls)
    
    # Check and add service_list pages
    service_dir = os.path.join(BASE, 'service_list')
    if os.path.exists(service_dir):
        for f in os.listdir(service_dir):
            if f.endswith('.html'):
                extra_urls.append((f'service_list/{f}', '0.5', 'monthly'))
    
    added = 0
    # Find the closing </urlset> tag
    close_tag = '</urlset>'
    
    new_entries = []
    for loc, priority, changefreq in missing_urls:
        if loc in content:
            continue  # Already in sitemap
        
        entry = f"""
  <url>
    <loc>https://sagmoto-trucks.com/{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        new_entries.append(entry)
        added += 1
    
    if added > 0:
        new_xml = '\n'.join(new_entries)
        content = content.replace(close_tag, new_xml + '\n' + close_tag)
        write_file(sitemap_path, content)
        log(f"[Phase5] Added {added} missing URLs to sitemap.xml, updated all lastmod to {TODAY}")
    else:
        log(f"[Phase5] No missing URLs found, updated all lastmod to {TODAY}")


# =============================================================================
# Phase 6: Fix news.html and contact.html keywords expansion
# =============================================================================

def phase6_expand_misc():
    """Expand keywords for news, contact, and other remaining pages"""
    
    misc_pages = {
        'news.html': {
            'old_kw': 'SAGMOTO news, commercial vehicle news, truck industry, events',
            'new_kw': 'SAGMOTO news, commercial vehicle news, truck industry, Chinese truck news, SAGMOTO events, truck export news, Shaanxi Automobile news, Fenghan Trading, new truck launch, industry trade fair, Canton Fair truck',
        },
        'contact.html': {
            'old_kw': 'SAGMOTO contact, truck sales inquiry, commercial vehicle contact, dealer inquiry',
            'new_kw': 'SAGMOTO contact, truck sales inquiry, commercial vehicle contact, dealer inquiry, truck price inquiry, SAGMOTO dealer, Shaanxi Fenghan Trading contact, Chinese truck supplier, truck exporter contact, buy truck from China, WhatsApp truck',
        },
    }
    
    for filename, data in misc_pages.items():
        filepath = os.path.join(BASE, filename)
        if not os.path.exists(filepath):
            continue
        content = read_file(filepath)
        
        kw_pattern = f'<meta name="keywords" content="{data["old_kw"]}">'
        if kw_pattern in content:
            content = content.replace(kw_pattern, f'<meta name="keywords" content="{data["new_kw"]}">')
            write_file(filepath, content)
            log(f"[Phase6] Expanded keywords for {filename}")
        else:
            # Try alternate format
            kw_pattern2 = f'<meta content="{data["old_kw"]}" name="keywords"/>'
            if kw_pattern2 in content:
                content = content.replace(kw_pattern2, f'<meta content="{data["new_kw"]}" name="keywords"/>')
                write_file(filepath, content)
                log(f"[Phase6] Expanded keywords for {filename} (format2)")
            else:
                print(f"  [WARN] {filename}: keyword pattern not found")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"  SAGMOTO 2号站 SEO关键词全面扩展")
    print(f"  Date: {TODAY}")
    print(f"{'='*60}\n")
    
    print("Phase 1: Fix brand name + remove Chinese keywords + fix template descriptions")
    phase1_fix_legacy_pages()
    
    print("\nPhase 2: Add description + keywords to news detail pages")
    phase2_fix_news_details()
    
    print("\nPhase 3: Expand keywords for product pages")
    phase3_expand_product_keywords()
    
    print("\nPhase 4: Canonical fix + privacy/terms keywords + index expansion")
    phase4_misc_fixes()
    
    print("\nPhase 5: Update sitemap.xml")
    phase5_update_sitemap()
    
    print("\nPhase 6: Expand remaining misc pages")
    phase6_expand_misc()
    
    print(f"\n{'='*60}")
    print(f"  COMPLETED - {len(changes_log)} changes made")
    print(f"{'='*60}\n")
    for c in changes_log:
        print(f"  {c}")
