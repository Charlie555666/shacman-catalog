#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Completely rebuild news detail pages with correct full navigation from news.html."""
import os, re

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"
NEWS_DETAIL_DIR = os.path.join(BASE_DIR, "news_Detail")

# Read news.html and extract navigation lines (17 to 153)
with open(os.path.join(BASE_DIR, "news.html"), 'r', encoding='utf-8') as f:
    lines = f.readlines()

# news.html line 17 starts e_container-1, line 153 ends e_container-2 (0-indexed: 16 to 152)
nav_lines = lines[16:153]  # lines 17-153 inclusive
nav_html = ''.join(nav_lines)

# Fix all paths for news_Detail subdirectory
path_fixes = [
    (r'href="index\.html"', 'href="../index.html"'),
    (r'href="products\.html"', 'href="../products.html"'),
    (r'href="products\.html\?cat=', 'href="../products.html?cat='),
    (r'href="qyc\.html"', 'href="../qyc.html"'),
    (r'href="zxc\.html"', 'href="../zxc.html"'),
    (r'href="zhc\.html"', 'href="../zhc.html"'),
    (r'href="special\.html"', 'href="../special.html"'),
    (r'href="tzc\.html"', 'href="../tzc.html"'),
    (r'href="pzkyzyc\.html"', 'href="../pzkyzyc.html"'),
    (r'href="pzmtc\.html"', 'href="../pzmtc.html"'),
    (r'href="service\.html"', 'href="../service.html"'),
    (r'href="service_list/', 'href="../service_list/'),
    (r'href="news_list/1\.html"', 'href="../news_list/1.html"'),
    (r'href="video_list\.html"', 'href="../video_list.html"'),
    (r'href="about\.html"', 'href="../about.html"'),
    (r'href="about\.html#', 'href="../about.html#'),
    (r'href="contact\.html"', 'href="../contact.html"'),
]

for pattern, replacement in path_fixes:
    nav_html = re.sub(pattern, replacement, nav_html)

# Process each detail file
for filename in sorted(os.listdir(NEWS_DETAIL_DIR)):
    if not filename.endswith('.html'):
        continue
    
    filepath = os.path.join(NEWS_DETAIL_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.S)
    title = title_match.group(1) if title_match else "News"
    
    # Extract banner title
    banner_match = re.search(r'<h1>(.*?)</h1>', content, re.S)
    banner_title = banner_match.group(1) if banner_match else title
    
    # Extract article content from between news-detail-container divs
    # Find content between <div class="news-detail-container"> and </div><a href="../news.html" or similar
    article_match = re.search(
        r'<div class="news-detail-container"[^>]*>(.*?)</div>\s*<a href="\.\./news\.html"',
        content, re.S
    )
    if article_match:
        article_body = article_match.group(1)
    else:
        # Fallback: try to find content between container and first </div>
        article_match = re.search(
            r'<div class="news-detail-container"[^>]*>(.*?)</div>\s*<a href="',
            content, re.S
        )
        article_body = article_match.group(1) if article_match else "<p>Article content not available.</p>"
    
    # Build new page
    new_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/app-pages.css">
    <link rel="icon" href="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7c996f42-7545-43cf-b326-fff928aa4f57.png">
    <style>
        .page-banner {{ background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('../images/hero/slide3.jpg') center/cover; padding: 100px 0 40px; color: white; text-align: center; }}
        .page-banner .breadcrumb {{ margin-bottom: 15px; font-size: 0.9rem; }}
        .page-banner .breadcrumb a {{ color: #fff; text-decoration: none; }}
        .page-banner .breadcrumb span {{ color: #ccc; }}
        .page-banner h1 {{ font-size: 2rem; max-width: 900px; margin: 0 auto; line-height: 1.3; }}
        .news-detail-container {{ max-width: 900px; margin: 40px auto; padding: 0 20px; font-size: 1.05rem; line-height: 1.8; color: #333; }}
        .news-detail-container img {{ max-width: 100%; border-radius: 6px; margin: 20px 0; }}
        .news-detail-container p {{ margin-bottom: 1.2em; }}
        .back-to-news {{ display: inline-block; margin: 0 auto 40px; padding: 12px 28px; background: #c62828; color: white; text-decoration: none; border-radius: 4px; transition: background 0.3s; }}
        .back-to-news:hover {{ background: #a02222; }}
        .back-wrap {{ max-width: 900px; margin: 0 auto; padding: 0 20px 40px; }}
    </style>
</head>
<body>
{nav_html}
<section class="page-banner">
<div class="container">
<div class="breadcrumb">
<a href="../index.html">Home</a> <span>/</span> <a href="../news.html">News</a> <span>/</span> <span>Article</span>
</div>
<h1>{banner_title}</h1>
</div>
</section>

<div class="news-detail-container">
{article_body}
</div>
<div class="back-wrap">
    <a href="../news.html" class="back-to-news">← Back to News Center</a>
</div>

<footer class="main-footer" style="background: #0a192f; color: white; padding: 40px 20px; text-align: center;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <p style="margin-bottom: 10px;">© 2025 SAGMOTO - Shaanxi Automobile Group Commercial Vehicle Co., Ltd.</p>
        <p style="font-size: 0.85rem; color: #888;">Room 603A, Floor 6, Building B, Chanba Free Trade Center, Xi'an, Shaanxi, China</p>
    </div>
</footer>
<script src="../js/data-loader.js"></script>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Rebuilt: {filename}")

print("\nAll news detail pages rebuilt with full navigation!")
