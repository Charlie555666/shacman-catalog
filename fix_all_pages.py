#!/usr/bin/env python3
"""
Comprehensive fix script for sagmoto-website sub-pages.
Fixes:
1. service.html - Update card links to point to detailed subdirectory pages
2. Main pages - Update SERVICES dropdown to link to actual subdirectory pages
3. Main pages - Vary banner images for visual diversity
4. Main pages - Fix footer to include off-road truck links
5. Fix broken onerror SVG fallbacks in product card images
6. Check and add any missing CSS classes
"""
import os
import re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sagmoto-website")

# ============================================================
# 1. Fix service.html - Update card links to detailed pages
# ============================================================
def fix_service_html():
    filepath = os.path.join(BASE, "service.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Update service card links to point to detailed pages
    replacements = [
        # Find Your Service Provider
        ('<a href="contact.html" class="btn-outline">Find a Provider</a>',
         '<a href="service_list/1674411714944516096.html" class="btn-outline">Find a Provider</a>'),
        # Maintenance Service
        ('<a href="contact.html" class="btn-outline">Schedule Service</a>',
         '<a href="service_list/1674411730417303552.html" class="btn-outline">Schedule Service</a>'),
        # Driving Reminder
        ('<a href="contact.html" class="btn-outline">Learn More</a>',
         '<a href="service_list/1674411748220751872.html" class="btn-outline">Learn More</a>'),
        # Safe Driving
        ('<a href="contact.html" class="btn-outline">Safety Guidelines</a>',
         '<a href="service_list/1674411767427842048.html" class="btn-outline">Safety Guidelines</a>'),
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  Fixed service.html link: {old[:50]}...")
        else:
            print(f"  WARN: Not found in service.html: {old[:50]}...")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("  service.html saved.")

# ============================================================
# 2. Fix SERVICES dropdown in all main pages
# ============================================================
def fix_services_dropdown():
    """Update SERVICES dropdown links from service.html#anchor to service_list/*.html"""
    main_pages = [
        "qyc.html", "zxc.html", "zhc.html", "special.html",
        "pzkyzyc.html", "pzmtc.html", "tzc.html",
        "service.html", "video_list.html",
        "products.html", "about.html", "contact.html", "news.html"
    ]

    old_dropdown = '''<ul class="dropdown-menu">
<li><a href="service.html">Service Policy</a></li>
<li><a href="service.html#find-provider">Find Your Service Provider</a></li>
<li><a href="service.html#maintenance">Maintenance Service</a></li>
<li><a href="service.html#driving-reminder">Driving Reminder</a></li>
<li><a href="service.html#safe-driving">Safe Driving</a></li>
</ul>'''

    new_dropdown = '''<ul class="dropdown-menu">
<li><a href="service.html">Service Policy</a></li>
<li><a href="service_list/1674411714944516096.html">Find Your Service Provider</a></li>
<li><a href="service_list/1674411730417303552.html">Maintenance Service</a></li>
<li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>
<li><a href="service_list/1674411767427842048.html">Safe Driving</a></li>
</ul>'''

    for page in main_pages:
        filepath = os.path.join(BASE, page)
        if not os.path.exists(filepath):
            print(f"  SKIP {page} - not found")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if old_dropdown in content:
            content = content.replace(old_dropdown, new_dropdown)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Fixed SERVICES dropdown in {page}")
        else:
            print(f"  SKIP {page} - dropdown pattern not found")

# ============================================================
# 3. Vary banner images in main pages
# ============================================================
def vary_banner_images():
    """Use different banner images for different pages"""
    banner_map = {
        "qyc.html": "slide1.jpg",      # Tractor - keep slide1
        "zxc.html": "slide4.jpg",      # Dump Truck - construction
        "zhc.html": "slide2.png",      # Cargo Truck - logistics
        "special.html": "slide5.jpg",  # Special Vehicle
        "pzkyzyc.html": "slide6.jpg",  # Off-road Dump
        "pzmtc.html": "slide3.jpg",    # Off-road Tractor
        "tzc.html": "slide4.jpg",      # Off-road Truck
        "service.html": "slide5.jpg",  # Service
        "video_list.html": "slide3.jpg", # Video Center
    }

    for page, slide in banner_map.items():
        filepath = os.path.join(BASE, page)
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace any slide image with the target slide
        content = re.sub(
            r"url\('images/hero/slide\d+\.(jpg|png)'\)",
            f"url('images/hero/{slide}')",
            content
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Banner set to {slide} for {page}")

# ============================================================
# 4. Fix footer in main pages - add off-road truck links
# ============================================================
def fix_footer_applications():
    """Add off-road truck links to footer APPLICATIONS section in main pages"""
    main_pages = [
        "qyc.html", "zxc.html", "zhc.html", "special.html",
        "pzkyzyc.html", "pzmtc.html", "tzc.html",
        "service.html", "video_list.html",
        "products.html", "about.html", "contact.html", "news.html"
    ]

    old_footer = '''<div class="footer-col">
<h3>APPLICATIONS</h3>
<ul>
<li><a href="qyc.html">Tractor</a></li>
<li><a href="zxc.html">Dump Truck</a></li>
<li><a href="zhc.html">Cargo Truck</a></li>
<li><a href="special.html">Special Vehicle</a></li>
</ul>
</div>'''

    new_footer = '''<div class="footer-col">
<h3>APPLICATIONS</h3>
<ul>
<li><a href="qyc.html">Tractor</a></li>
<li><a href="zxc.html">Dump Truck</a></li>
<li><a href="zhc.html">Cargo Truck</a></li>
<li><a href="special.html">Special Vehicle</a></li>
<li><a href="pzkyzyc.html">Off-road Truck</a></li>
</ul>
</div>'''

    for page in main_pages:
        filepath = os.path.join(BASE, page)
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if old_footer in content:
            content = content.replace(old_footer, new_footer)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Fixed footer in {page}")
        else:
            print(f"  SKIP {page} - footer pattern not found (may already be fixed)")

# ============================================================
# 5. Fix broken onerror SVG fallbacks in product card images
# ============================================================
def fix_onerror_fallbacks():
    """Fix broken SVG onerror fallbacks that use nested single quotes"""
    pages = [
        "qyc.html", "zxc.html", "zhc.html", "special.html",
        "pzkyzyc.html", "pzmtc.html", "tzc.html",
    ]

    # The broken pattern uses single quotes inside single quotes
    old_pattern = r"onerror=\"this\.src='data:image/svg\+xml,%3Csvg xmlns='http://www\.w3\.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23e5e5e5' width='400' height='300'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='%23999' font-size='18'%3ESAGMOTO%3C/text%3E%3C/svg%3E'\""

    new_fallback = 'onerror="this.src=\'data:image/svg+xml,%3Csvg%20xmlns%3D%22http://www.w3.org/2000/svg%22%20width%3D%22400%22%20height%3D%22300%22%3E%3Crect%20fill%3D%22%23e5e5e5%22%20width%3D%22400%22%20height%3D%22300%22%2F%3E%3Ctext%20x%3D%22200%22%20y%3D%22150%22%20text-anchor%3D%22middle%22%20fill%3D%22%23999%22%20font-size%3D%2218%22%3ESAGMOTO%3C%2Ftext%3E%3C%2Fsvg%3E\'"'

    for page in pages:
        filepath = os.path.join(BASE, page)
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(old_pattern, new_fallback, content)
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count = content.count("onerror=")
            print(f"  Fixed onerror fallbacks in {page} ({count} occurrences)")
        else:
            print(f"  SKIP {page} - no broken onerror found")

# ============================================================
# 6. Fix NEWS dropdown to link to news_list/1.html
# ============================================================
def fix_news_dropdown():
    """Update NEWS dropdown to link to news_list/1.html for News Center"""
    main_pages = [
        "qyc.html", "zxc.html", "zhc.html", "special.html",
        "pzkyzyc.html", "pzmtc.html", "tzc.html",
        "service.html", "video_list.html",
        "products.html", "about.html", "contact.html", "news.html"
    ]

    old_news = '''<ul class="dropdown-menu">
<li><a href="news.html">News Center</a></li>
<li><a href="video_list.html">Video Center</a></li>
</ul>'''

    new_news = '''<ul class="dropdown-menu">
<li><a href="news_list/1.html">News Center</a></li>
<li><a href="video_list.html">Video Center</a></li>
</ul>'''

    for page in main_pages:
        filepath = os.path.join(BASE, page)
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if old_news in content:
            content = content.replace(old_news, new_news)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Fixed NEWS dropdown in {page}")

# ============================================================
# Run all fixes
# ============================================================
print("=" * 60)
print("1. Fixing service.html card links...")
fix_service_html()

print("\n" + "=" * 60)
print("2. Fixing SERVICES dropdown in main pages...")
fix_services_dropdown()

print("\n" + "=" * 60)
print("3. Varying banner images...")
vary_banner_images()

print("\n" + "=" * 60)
print("4. Fixing footer APPLICATIONS section...")
fix_footer_applications()

print("\n" + "=" * 60)
print("5. Fixing onerror SVG fallbacks...")
fix_onerror_fallbacks()

print("\n" + "=" * 60)
print("6. Fixing NEWS dropdown links...")
fix_news_dropdown()

print("\n" + "=" * 60)
print("All fixes complete!")
