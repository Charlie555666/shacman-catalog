#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract news detail content from official sagmoto.com pages and create local versions.
Also fix index.html and news.html links to point to local detail pages.
"""
import re, os, json

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"
MIRROR_DIR = os.path.join(BASE_DIR, ".mirror_raw")
NEWS_DETAIL_DIR = os.path.join(BASE_DIR, "news_Detail")

os.makedirs(NEWS_DETAIL_DIR, exist_ok=True)

# News items to process (the 4 on homepage + any others we want)
NEWS_ITEMS = [
    {"id": 22, "title": "Intelligent Production of Heavy Trucks at Shaanxi Automobile's Factory", "date": "2025-05-20", "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/594bfd0b-975f-4f11-9637-3747a91cdcef.png"},
    {"id": 21, "title": "Caucasus' New Jewel SAGMOTO X3s Tractor Debuts in Armenia", "date": "2025-04-15", "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg"},
    {"id": 20, "title": "SAGMOTO brand specialized trucks makes an appearance in the 137th Canton Fair", "date": "2025-04-10", "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/1a8052fb-a9f5-4739-abba-33ff76548683.jpg"},
    {"id": 19, "title": "SAGMOTO Chinese New Year Greeting 2025", "date": "2025-01-28", "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/cdf6fe4e-268d-4f08-9994-7e6c7fd20ac8.jpg"},
    {"id": 18, "title": "Charting the Path of Courageous Advancement, SAGMOTO Newly Upgraded X3s Heavy Truck to Realize a New Journey", "date": "2025-01-17", "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fed9afb3-0258-4c67-9c06-e2f9ac4c7503e.jpg"},
]

def extract_content_from_html(filepath):
    """Extract article content from official HTML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None, []
    
    # Try to extract title
    title_match = re.search(r'<h1[^>]*class="[^"]*p_title[^"]*"[^>]*>(.*?)</h1>', html, re.S|re.I)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', html, re.S|re.I)
    title = title_match.group(1).strip() if title_match else "News"
    title = re.sub(r'<[^>]+>', '', title)
    
    # Extract article body - look for the rich text content div
    body_match = re.search(r'<div[^>]*class="[^"]*p_richText[^"]*e_richText[^"]*"[^>]*>(.*?)</div>\s*</div>\s*<div[^>]*class="[^"]*p_wftj[^"]*"', html, re.S|re.I)
    if not body_match:
        # Try alternate pattern
        body_match = re.search(r'<div[^>]*class="[^"]*e_richText[^"]*"[^>]*>(.*?)</div>\s*</div>\s*<div', html, re.S|re.I)
    if not body_match:
        body_match = re.search(r'<div[^>]*class="[^"]*detail-content[^"]*"[^>]*>(.*?)</div>', html, re.S|re.I)
    
    body = body_match.group(1) if body_match else ""
    
    # Clean up body - fix relative URLs, remove lazy attributes, etc.
    # Convert lazy="url" to src="url" for images
    body = re.sub(r'<img[^>]*src="/npublic/img/s\.png"[^>]*lazy="([^"]*)"[^>]*>', r'<img src="\1" alt="">', body)
    body = re.sub(r'<img[^>]*lazy="([^"]*)"[^>]*src="/npublic/img/s\.png"[^>]*>', r'<img src="\1" alt="">', body)
    # Remove empty style attributes
    body = re.sub(r'style=""', '', body)
    # Fix relative links to absolute
    body = body.replace('href="/', 'href="http://www.sagmoto.com/')
    body = body.replace('src="/', 'src="http://www.sagmoto.com/')
    
    # Extract images from the body for hero/header use
    img_urls = re.findall(r'src="(https?://[^"]+)"', body)
    
    return title, body, img_urls

def create_detail_page(item, title, body, img_urls):
    """Create a local news detail HTML page."""
    # Use first image in body as hero, or fallback to item img
    hero_img = img_urls[0] if img_urls else item["img"]
    
    # Get article text preview for meta description
    text_preview = re.sub(r'<[^>]+>', '', body)
    text_preview = text_preview[:200].strip() + "..." if len(text_preview) > 200 else text_preview
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{item["title"]} | SAGMOTO News</title>
    <meta name="description" content="{text_preview}">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/news.css">
    <style>
        .news-detail-banner {{ background: linear-gradient(135deg, #0a192f 0%, #1a365d 100%); padding: 80px 0 40px; text-align: center; color: white; }}
        .news-detail-banner h1 {{ font-size: 2.2rem; max-width: 900px; margin: 0 auto; line-height: 1.3; }}
        .news-detail-banner .date {{ color: #e0e0e0; margin-top: 15px; font-size: 0.95rem; }}
        .news-detail-container {{ max-width: 900px; margin: 40px auto; padding: 0 20px; }}
        .news-hero-img {{ width: 100%; border-radius: 8px; margin-bottom: 30px; }}
        .news-content {{ font-size: 1.05rem; line-height: 1.8; color: #333; }}
        .news-content p {{ margin-bottom: 1.2em; }}
        .news-content img {{ max-width: 100%; border-radius: 6px; margin: 20px 0; }}
        .back-to-news {{ display: inline-block; margin-top: 40px; padding: 12px 28px; background: #c62828; color: white; text-decoration: none; border-radius: 4px; transition: background 0.3s; }}
        .back-to-news:hover {{ background: #a02222; }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="main-nav">
        <div class="nav-container">
            <a href="../index.html" class="logo">
                <img src="../images/logo.png" alt="SAGMOTO" style="height: 50px;">
            </a>
            <ul class="nav-menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../products.html">Products</a></li>
                <li><a href="../news.html" class="active">News</a></li>
                <li><a href="../video_list.html">Video</a></li>
                <li><a href="../about.html">About</a></li>
                <li><a href="../contact.html">Contact</a></li>
            </ul>
        </div>
    </nav>

    <div class="news-detail-banner">
        <h1>{item["title"]}</h1>
        <div class="date">{item["date"]}</div>
    </div>

    <div class="news-detail-container">
        <img src="{hero_img}" alt="{item["title"]}" class="news-hero-img" onerror="this.style.display='none'">
        <div class="news-content">
            {body}
        </div>
        <a href="../news.html" class="back-to-news">← Back to News Center</a>
    </div>

    <!-- Footer -->
    <footer class="main-footer" style="margin-top: 60px;">
        <div class="footer-container" style="max-width: 1200px; margin: 0 auto; padding: 40px 20px; text-align: center; border-top: 1px solid #ddd;">
            <p style="color: #888;">© 2025 SAGMOTO - Shaanxi Automobile Group Commercial Vehicle Co., Ltd.</p>
        </div>
    </footer>
</body>
</html>'''
    
    output_path = os.path.join(NEWS_DETAIL_DIR, f"{item['id']}.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {output_path}")

# Process each news item
for item in NEWS_ITEMS:
    filepath = os.path.join(MIRROR_DIR, f"news_detail_{item['id']}_official.html")
    title, body, img_urls = extract_content_from_html(filepath)
    if body:
        create_detail_page(item, title, body, img_urls)
    else:
        print(f"Warning: No content extracted for {item['id']}")

print("\nDone creating detail pages!")
