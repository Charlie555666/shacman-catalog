#!/usr/bin/env python3
"""Fix article 22 image and inject news content into news_list/1.html mirror page"""

import re
import os

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"

# ========== FIX ARTICLE 22 IMAGE IN news.html ==========
NEWS_HTML = os.path.join(BASE_DIR, "news.html")
with open(NEWS_HTML, "r", encoding="utf-8") as f:
    news_html = f.read()

# Article 22 image is currently 260cfe2b (same as article 21) - replace with a factory image
# Use the SAGMOTO factory image from CDN
old_img_22 = 'src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/260cfe2b-40c3-44d9-9381-00bbef2b082c.jpg"/>\n</div>\n<div class="card-body">\n<h3>Intelligent Production'
new_img_22 = 'src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg"/>\n</div>\n<div class="card-body">\n<h3>Intelligent Production'

if old_img_22 in news_html:
    news_html = news_html.replace(old_img_22, new_img_22)
    print("Fixed article 22 image in news.html")
else:
    print("WARNING: Could not find article 22 image pattern to replace")

with open(NEWS_HTML, "w", encoding="utf-8") as f:
    f.write(news_html)

# ========== INJECT NEWS CONTENT INTO news_list/1.html ==========
NEWS_LIST_HTML = os.path.join(BASE_DIR, "news_list", "1.html")
with open(NEWS_LIST_HTML, "r", encoding="utf-8") as f:
    news_list_html = f.read()

# Extract the news grid from news.html
news_grid_match = re.search(r'(<div class="news-grid news-page">.*?</div>\s*</div>\s*</section>)', news_html, re.DOTALL)
if not news_grid_match:
    # Try alternative pattern
    news_grid_match = re.search(r'(<div class="news-grid news-page">.*?</div>)\s*</div>\s*</section>', news_html, re.DOTALL)

if news_grid_match:
    news_grid_html = news_grid_match.group(0)
    # Extract just the inner grid (without the section wrapper)
    inner_match = re.search(r'(<div class="news-grid news-page">.*?</div>)\s*$', news_grid_html.rstrip(), re.DOTALL)
    if inner_match:
        news_grid_inner = inner_match.group(1)
    else:
        news_grid_inner = news_grid_html
    
    # Build the content to inject
    inject_content = '''
<!-- OUR NEWS CONTENT -->
<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('../images/hero/slide3.jpg') center/cover;">
<div class="container" style="max-width:1400px;margin:0 auto;padding:60px 40px;">
<div class="breadcrumb" style="margin-bottom:15px;">
<a href="../index.html" style="color:#C89B3C;text-decoration:none;">Home</a> 
<span style="color:#999;">/</span> 
<span style="color:#fff;">News</span>
</div>
<h1 style="color:#fff;font-size:36px;margin:0 0 10px 0;font-weight:700;">News Center</h1>
<p style="color:#ccc;font-size:16px;margin:0;">Latest News &amp; Updates from SAGMOTO</p>
</div>
</section>
<section style="background:#f5f5f5;padding:50px 0;">
<div style="max-width:1400px;margin:0 auto;padding:0 40px;">
''' + news_grid_inner + '''
</div>
</section>
<!-- END OUR NEWS CONTENT -->
'''
    
    # Check if there's already custom content
    if '<!-- OUR NEWS CONTENT -->' in news_list_html:
        # Replace existing
        old_pattern = r'<!-- OUR NEWS CONTENT -->.*?<!-- END OUR NEWS CONTENT -->'
        news_list_html = re.sub(old_pattern, inject_content.strip(), news_list_html, flags=re.DOTALL)
        print("Replaced existing news content in news_list/1.html")
    else:
        # Find the end of the nav bar (our-nav-bar div)
        nav_bar_pos = news_list_html.find('class="our-nav-bar"')
        if nav_bar_pos >= 0:
            # Find the closing div of our-nav-bar
            depth = 0
            pos = nav_bar_pos
            while pos < len(news_list_html):
                open_div = news_list_html.find('<div', pos)
                close_div = news_list_html.find('</div>', pos)
                if close_div < 0:
                    break
                if open_div >= 0 and open_div < close_div:
                    depth += 1
                    pos = open_div + 4
                else:
                    depth -= 1
                    pos = close_div + 6
                    if depth == 0:
                        break
            
            # Insert news content after the nav bar
            news_list_html = news_list_html[:pos] + '\n' + inject_content + '\n' + news_list_html[pos:]
            print("Injected news content into news_list/1.html after nav bar")
        else:
            print("WARNING: Could not find nav bar in news_list/1.html")
    
    # Also add CSS for news cards if not already present
    news_css = '''
<style>
.news-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:25px;}
.news-card{background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.08);text-decoration:none;color:inherit;transition:transform .3s,box-shadow .3s;display:block;}
.news-card:hover{transform:translateY(-3px);box-shadow:0 5px 20px rgba(0,0,0,.15);}
.news-card .card-img{width:100%;aspect-ratio:16/9;overflow:hidden;}
.news-card .card-img img{width:100%;height:100%;object-fit:cover;transition:transform .3s;}
.news-card:hover .card-img img{transform:scale(1.05);}
.news-card .card-body{padding:15px 20px;}
.news-card .card-body .date{color:#C62828;font-size:12px;font-weight:600;margin-bottom:8px;}
.news-card .card-body h3{font-size:15px;color:#0D1F3D;margin:0;line-height:1.4;font-weight:600;}
@media(max-width:768px){.news-grid{grid-template-columns:1fr;}}
</style>
'''
    
    # Add CSS before the closing </head> if not already there
    if '.news-card' not in news_list_html:
        news_list_html = news_list_html.replace('</style>\n</head>', news_css + '\n</style>\n</head>')
        # If that didn't work, try another pattern
        if '.news-card' not in news_list_html:
            news_list_html = news_list_html.replace('</head>', news_css + '\n</head>')
    
    with open(NEWS_LIST_HTML, "w", encoding="utf-8") as f:
        f.write(news_list_html)
    
    print("Updated news_list/1.html with real news content")
else:
    print("ERROR: Could not extract news grid from news.html")

print("\nDone!")
