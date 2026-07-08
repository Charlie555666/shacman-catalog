#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix navigation in all news_Detail/*.html files to match news.html structure.
Also fix CSS paths and footer.
"""
import os, re, glob

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"
NEWS_DETAIL_DIR = os.path.join(BASE_DIR, "news_Detail")

# Read news.html navigation section (from e_container-1 to end of e_container-2)
with open(os.path.join(BASE_DIR, "news.html"), 'r', encoding='utf-8') as f:
    news_html = f.read()

# Extract nav section from news.html: from e_container-1 start to e_container-2 end
nav_match = re.search(r'(<div class="e_container-1">.*?</div>\s*<!-- ===== HEADER / NAVIGATION ===== -->\s*<div class="e_container-2">.*?</div>\s*</div>)', news_html, re.S)
if not nav_match:
    print("ERROR: Could not find nav section in news.html")
    exit(1)

nav_html = nav_match.group(1)

# Fix paths for news_Detail subdirectory (prepend ../ to page links, keep CDN images)
# Handle various link patterns
path_fixes = [
    # Page links - need ../ prefix
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
    (r'href="contact\.html"', 'href="../contact.html"'),
    (r'href="javascript:;"', 'href="javascript:;"'),  # no change needed
    # Images already use full CDN URLs, no need to change
    # CSS paths - these are relative to news.html root, so for news_Detail we need ../
    # But in our generated pages we already used ../css/ - this is correct!
]

for pattern, replacement in path_fixes:
    nav_html = re.sub(pattern, replacement, nav_html)

# Also create a simple footer matching the style
footer_html = '''<footer class="main-footer" style="margin-top: 60px; background: #0a192f; color: white; padding: 40px 20px; text-align: center;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <p style="margin-bottom: 10px;">© 2025 SAGMOTO - Shaanxi Automobile Group Commercial Vehicle Co., Ltd.</p>
        <p style="font-size: 0.85rem; color: #888;">Room 603A, Floor 6, Building B, Chanba Free Trade Center, Xi'an, Shaanxi, China</p>
    </div>
</footer>'''

# Process each news detail file
for detail_file in sorted(glob.glob(os.path.join(NEWS_DETAIL_DIR, "*.html"))):
    with open(detail_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the entire <body> content from <body> to </body>
    # We need to preserve the <head> section and replace body content
    
    # Extract head section
    head_match = re.search(r'(<head>.*?</head>)', content, re.S)
    if not head_match:
        print(f"WARNING: No head found in {detail_file}")
        continue
    
    head_html = head_match.group(1)
    
    # Fix CSS paths in head - ensure ../css/ is used
    head_html = re.sub(r'href="css/', 'href="../css/', head_html)
    head_html = re.sub(r'href="\.\./css/news\.css"', 'href="../css/app-pages.css"', head_html)
    
    # Get the article title and body from existing file
    title_match = re.search(r'<title>(.*?)</title>', content, re.S)
    title = title_match.group(1) if title_match else "News"
    
    # Extract article content (between news-detail-container and back-to-news)
    article_match = re.search(r'<div class="news-detail-container">(.*?)</div>\s*<a href="\.\./news\.html"', content, re.S)
    if article_match:
        article_body = article_match.group(1)
    else:
        # Try alternate pattern
        article_match = re.search(r'<div class="news-detail-container">(.*?)<a href="', content, re.S)
        article_body = article_match.group(1) if article_match else "<p>Article content not available.</p>"
    
    # Extract date if available
    date_match = re.search(r'<div class="date">(.*?)</div>', content, re.S)
    date_str = date_match.group(1) if date_match else ""
    
    # Extract banner title
    banner_title_match = re.search(r'<h1>(.*?)</h1>', content, re.S)
    banner_title = banner_title_match.group(1) if banner_title_match else title
    
    # Build new HTML with correct navigation
    new_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{head_html}
</head>
<body>
{nav_html}

<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('../images/hero/slide3.jpg') center/cover;">
<div class="container">
<div class="breadcrumb">
<a href="../index.html">Home</a> <span>/</span> <a href="../news.html">News</a> <span>/</span> <span>Article</span>
</div>
<h1>{banner_title}</h1>
</div>
</section>

<div class="news-detail-container" style="max-width: 900px; margin: 40px auto; padding: 0 20px;">
{article_body}
</div>
<a href="../news.html" style="display: block; max-width: 900px; margin: 0 auto 40px; padding: 0 20px;">
    <span style="display: inline-block; padding: 12px 28px; background: #c62828; color: white; text-decoration: none; border-radius: 4px;">← Back to News Center</span>
</a>

{footer_html}
<script src="../js/data-loader.js"></script>
</body>
</html>'''
    
    with open(detail_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Fixed: {os.path.basename(detail_file)}")

print("\nAll news detail pages fixed!")
