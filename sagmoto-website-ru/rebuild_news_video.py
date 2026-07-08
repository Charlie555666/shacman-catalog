#!/usr/bin/env python3
"""Rebuild news.html and video_list.html with real content from official sagmoto.com"""

import re
import html as html_module
import os

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"

# ========== EXTRACT NEWS ==========
OFFICIAL_NEWS = os.path.join(BASE_DIR, ".mirror_raw", "news_list1_official.html")
with open(OFFICIAL_NEWS, "r", encoding="utf-8") as f:
    content = f.read()

# Find all news_Detail IDs
detail_pattern = r'href="/news_Detail/(\d+)\.html"'
matches = list(re.finditer(detail_pattern, content))
seen_ids = []
for m in matches:
    nid = m.group(1)
    if nid not in seen_ids:
        seen_ids.append(nid)

news_items = []
for nid in seen_ids:
    link_pos = content.find(f'/news_Detail/{nid}.html')
    if link_pos < 0:
        continue
    start = max(0, link_pos - 500)
    end = min(len(content), link_pos + 2000)
    block = content[start:end]
    
    # Get lazy image URL
    lazy_match = re.search(r'lazy="(https://omo-oss-image[^"]+)"', block)
    image_url = lazy_match.group(1) if lazy_match else ""
    
    # Get title from alt attribute
    alt_match = re.search(r'alt="([^"]+)"', block)
    title = ""
    if alt_match:
        title = html_module.unescape(alt_match.group(1)).strip()
    
    if image_url and title:
        news_items.append({
            'id': nid,
            'title': title,
            'image': image_url,
        })

print(f"Extracted {len(news_items)} news items")

# Generate news cards HTML
# Links point to official sagmoto.com news detail pages
news_cards_html = '<div class="news-grid news-page">\n'
for item in news_items:
    title_escaped = item['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    # Truncate title for display if too long
    display_title = title_escaped
    if len(display_title) > 90:
        display_title = display_title[:87] + '...'
    
    news_cards_html += f'''<a class="news-card" href="http://www.sagmoto.com/news_Detail/{item['id']}.html" target="_blank">
<div class="card-img">
<img alt="{title_escaped}" src="{item['image']}"/>
</div>
<div class="card-body">
<h3>{display_title}</h3>
</div>
</a>
'''
news_cards_html += '</div>'

# ========== REPLACE IN news.html ==========
NEWS_HTML = os.path.join(BASE_DIR, "news.html")
with open(NEWS_HTML, "r", encoding="utf-8") as f:
    news_html = f.read()

# Replace the old news-grid section (from <div class="news-grid news-page"> to its closing </div>)
# The section is between: <div class="news-grid news-page"> ... </div> (before </div></section>)
old_pattern = r'<div class="news-grid news-page">.*?</div>\s*</div>\s*</section>'
new_section = news_cards_html + '\n</div>\n</section>'

news_html_new = re.sub(old_pattern, new_section, news_html, flags=re.DOTALL)

# Also update the page title and meta
news_html_new = news_html_new.replace(
    'Latest Updates &amp; Industry Insights',
    'Latest News &amp; Updates from SAGMOTO'
)

with open(NEWS_HTML, "w", encoding="utf-8") as f:
    f.write(news_html_new)

print(f"Updated news.html with {len(news_items)} real news articles")

# ========== EXTRACT VIDEOS ==========
OFFICIAL_VIDEOS = os.path.join(BASE_DIR, ".mirror_raw", "video_list_official.html")
if os.path.exists(OFFICIAL_VIDEOS):
    with open(OFFICIAL_VIDEOS, "r", encoding="utf-8") as f:
        video_content = f.read()
    
    # Find video items - look for lazy images and titles
    # Official video page has 4 videos with titles and thumbnail images
    video_pattern = r'lazy="(https://omo-oss-image[^"]+)"[^>]*alt="([^"]+)"'
    video_matches = re.findall(video_pattern, video_content)
    
    videos = []
    seen_titles = set()
    for img_url, title in video_matches:
        title = html_module.unescape(title).strip()
        if title and title not in seen_titles and 'SAG' not in title[:3] or title.startswith('SAGMOTO') or title.startswith('Off-road') or title.startswith('X3s'):
            if title not in seen_titles:
                videos.append({'title': title, 'image': img_url})
                seen_titles.add(title)
    
    # If the above didn't work well, try a different approach
    if len(videos) < 4:
        # Find all lazy images
        all_lazy = re.findall(r'lazy="(https://omo-oss-image[^"]+)"', video_content)
        all_alts = re.findall(r'alt="([^"]+)"', video_content)
        
        # Filter out logo/favicon
        filtered_lazy = [u for u in all_lazy if '7c996f42' not in u and '45799ffa' not in u]
        filtered_alts = [a for a in all_alts if a and a not in ['SAG MOTO', 'PRODUCTS', 'SAG Commercial Vehicle Company', '']]
        
        videos = []
        seen_imgs = set()
        for i, img_url in enumerate(filtered_lazy):
            if img_url not in seen_imgs:
                title = filtered_alts[i] if i < len(filtered_alts) else f"Video {i+1}"
                videos.append({'title': title, 'image': img_url})
                seen_imgs.add(img_url)
    
    print(f"\nExtracted {len(videos)} videos:")
    for v in videos:
        print(f"  {v['title']}: {v['image'][:60]}...")
    
    # Generate video section HTML for video_list.html
    # We need to find the video content section in video_list.html and replace it
    VIDEO_HTML = os.path.join(BASE_DIR, "video_list.html")
    with open(VIDEO_HTML, "r", encoding="utf-8") as f:
        video_html = f.read()
    
    # The video_list.html is a mirror page with original sagmoto content hidden
    # We need to inject our video content into the visible section
    # Look for where we can inject content - after the nav bar, before the original content
    
    # Check if there's already a custom video section
    if '<!-- OUR VIDEO CONTENT -->' in video_html:
        # Replace existing custom content
        old_video_pattern = r'<!-- OUR VIDEO CONTENT -->.*?<!-- END OUR VIDEO CONTENT -->'
        new_video_content = '<!-- OUR VIDEO CONTENT -->\n'
        new_video_content += '<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url(\'images/hero/slide3.jpg\') center/cover;">\n'
        new_video_content += '<div class="container"><div class="breadcrumb"><a href="index.html">Home</a> <span>/</span> <span>Video Center</span></div>\n'
        new_video_content += '<h1>Video Center</h1><p>Watch SAGMOTO Trucks in Action</p></div></section>\n'
        new_video_content += '<section class="section-bg-white"><div class="container">\n'
        new_video_content += '<div class="video-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:30px;padding:40px 0;">\n'
        for v in videos:
            title_esc = v['title'].replace('&', '&amp;').replace('"', '&quot;')
            new_video_content += f'''<div class="video-card" style="background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.1);transition:transform .3s;">
<div style="position:relative;overflow:hidden;aspect-ratio:16/9;">
<img alt="{title_esc}" src="{v['image']}" style="width:100%;height:100%;object-fit:cover;"/>
<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:60px;height:60px;background:rgba(194,40,40,.85);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;">
<svg width="24" height="24" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#fff"/></svg>
</div>
</div>
<div style="padding:15px 20px;">
<h3 style="margin:0;font-size:16px;color:#0D1F3D;font-weight:600;">{title_esc}</h3>
</div>
</div>
'''
        new_video_content += '</div>\n</div></section>\n'
        new_video_content += '<!-- END OUR VIDEO CONTENT -->'
        
        video_html = re.sub(old_video_pattern, new_video_content, video_html, flags=re.DOTALL)
    else:
        # Insert our video content right after the nav bar closing </div>
        # Find the end of our-nav-bar
        nav_end = video_html.find('</div>\n    </div>\n    </div>')
        if nav_end < 0:
            nav_end = video_html.find('</div>', video_html.find('our-nav-bar'))
        
        # Find the position after the nav
        nav_close = video_html.find('</div>', video_html.find('class="our-nav-bar"'))
        # Find the second closing div (the inner div)
        nav_close2 = video_html.find('</div>', nav_close + 6)
        
        insert_pos = video_html.find('</div>', nav_close2 + 6)
        
        new_video_content = '\n<!-- OUR VIDEO CONTENT -->\n'
        new_video_content += '<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url(\'images/hero/slide3.jpg\') center/cover;">\n'
        new_video_content += '<div class="container"><div class="breadcrumb"><a href="index.html">Home</a> <span>/</span> <span>Video Center</span></div>\n'
        new_video_content += '<h1>Video Center</h1><p>Watch SAGMOTO Trucks in Action</p></div></section>\n'
        new_video_content += '<section class="section-bg-white"><div class="container">\n'
        new_video_content += '<div class="video-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:30px;padding:40px 0;">\n'
        for v in videos:
            title_esc = v['title'].replace('&', '&amp;').replace('"', '&quot;')
            new_video_content += f'''<div class="video-card" style="background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.1);transition:transform .3s;">
<div style="position:relative;overflow:hidden;aspect-ratio:16/9;">
<img alt="{title_esc}" src="{v['image']}" style="width:100%;height:100%;object-fit:cover;"/>
<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:60px;height:60px;background:rgba(194,40,40,.85);border-radius:50%;display:flex;align-items:center;justify-content:center;">
<svg width="24" height="24" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#fff"/></svg>
</div>
</div>
<div style="padding:15px 20px;">
<h3 style="margin:0;font-size:16px;color:#0D1F3D;font-weight:600;">{title_esc}</h3>
</div>
</div>
'''
        new_video_content += '</div>\n</div></section>\n'
        new_video_content += '<!-- END OUR VIDEO CONTENT -->\n'
        
        # Insert after the nav bar
        # Find the closing of our-nav-bar div
        nav_bar_pos = video_html.find('class="our-nav-bar"')
        # Find matching closing divs
        depth = 0
        pos = nav_bar_pos
        while pos < len(video_html):
            open_div = video_html.find('<div', pos)
            close_div = video_html.find('</div>', pos)
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
        
        video_html = video_html[:pos] + '\n' + new_video_content + video_html[pos:]
    
    with open(VIDEO_HTML, "w", encoding="utf-8") as f:
        f.write(video_html)
    
    print(f"Updated video_list.html with {len(videos)} videos")
else:
    print("WARNING: Official video page not found, skipping video_list.html update")

print("\nDone! Both pages updated.")
