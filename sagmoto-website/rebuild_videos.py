#!/usr/bin/env python3
"""Extract all videos from official sagmoto.com video_list page and rebuild video_list.html"""

import re
import html as html_module
import os

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"
OFFICIAL_VIDEOS = os.path.join(BASE_DIR, ".mirror_raw", "video_list_official.html")

with open(OFFICIAL_VIDEOS, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all videoIBox sections
# Each videoIBox contains:
#   1. A thumbnail image (e_image-11) with alt="title"
#   2. A video cover image (coverImage) 
#   3. A <video> tag with src="...mp4"
#   4. A title in <p class="e_text-8 s_title">

# Find all videoIBox blocks
video_box_pattern = r'<div class="cbox-2 p_loopitem videoIBox"><div class="e_container-6 s_layout">(.*?)</div></div></div>'
# This pattern is too greedy/complex. Let me use a different approach.

# Find all <video> tags with their src
video_src_pattern = r'<video class="video" src="(https://omo-oss-video[^"]+)"'
video_srcs = re.findall(video_src_pattern, content)

# Find all titles in e_text-8 s_title
title_pattern = r'<p class="e_text-8 s_title">\s*(.*?)\s*</p>'
titles = re.findall(title_pattern, content)

# Find all thumbnail images (the ones with alt that matches video titles)
# These are in e_image-11 s_img videoimg divs
thumb_pattern = r'<div class="e_image-11 s_img videoimg">\s*<img src="(https://omo-oss-image[^"]+)" alt="([^"]*)"'
thumbs = re.findall(thumb_pattern, content)

# Find all cover images
cover_pattern = r'<div class="coverImage">\s*<img src="(https://omo-oss-image[^"]+)"'
covers = re.findall(cover_pattern, content)

print(f"Found {len(video_srcs)} video sources")
print(f"Found {len(titles)} titles")
print(f"Found {len(thumbs)} thumbnails")
print(f"Found {len(covers)} cover images")

# Combine: for each video, we need title, thumbnail (or cover), and video URL
videos = []
for i in range(len(video_srcs)):
    title = html_module.unescape(titles[i]).strip() if i < len(titles) else f"Video {i+1}"
    thumb = thumbs[i][0] if i < len(thumbs) and thumbs[i][0] else (covers[i] if i < len(covers) else "")
    video_url = video_srcs[i]
    videos.append({
        'title': title,
        'thumbnail': thumb,
        'cover': covers[i] if i < len(covers) else "",
        'video_url': video_url
    })
    print(f"\n  Video {i+1}: {title}")
    print(f"    Thumbnail: {thumb[:80]}")
    print(f"    Video URL: {video_url[:80]}")

# Now rebuild video_list.html
VIDEO_HTML = os.path.join(BASE_DIR, "video_list.html")
with open(VIDEO_HTML, "r", encoding="utf-8") as f:
    video_html = f.read()

# Check if there's already custom content
if '<!-- OUR VIDEO CONTENT -->' in video_html:
    # Replace existing custom content
    old_pattern = r'<!-- OUR VIDEO CONTENT -->.*?<!-- END OUR VIDEO CONTENT -->'
    
    new_content = '''<!-- OUR VIDEO CONTENT -->
<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url('images/hero/slide3.jpg') center/cover;">
<div class="container">
<div class="breadcrumb">
<a href="index.html">Home</a> <span>/</span> <span>Video Center</span>
</div>
<h1>Video Center</h1>
<p>Watch SAGMOTO Trucks in Action</p>
</div>
</section>
<section class="section-bg-white">
<div class="container">
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:30px;padding:50px 0;">
'''
    
    for v in videos:
        title_esc = v['title'].replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        thumb = v['thumbnail'] if v['thumbnail'] else v['cover']
        new_content += f'''<div class="video-card" style="background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 15px rgba(0,0,0,.1);transition:transform .3s ease,box-shadow .3s ease;">
<div style="position:relative;overflow:hidden;aspect-ratio:16/9;cursor:pointer;" onclick="this.querySelector('video').style.display='block';this.querySelector('img').style.display='none';this.querySelector('video').play();">
<img alt="{title_esc}" src="{thumb}" style="width:100%;height:100%;object-fit:cover;display:block;"/>
<video preload="none" controls style="width:100%;height:100%;object-fit:cover;display:none;background:#000;">
<source src="{v['video_url']}" type="video/mp4"/>
</video>
<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;background:rgba(194,40,40,.9);border-radius:50%;display:flex;align-items:center;justify-content:center;pointer-events:none;transition:opacity .3s;">
<svg width="28" height="28" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#fff"/></svg>
</div>
</div>
<div style="padding:16px 20px;border-top:3px solid #C62828;">
<h3 style="margin:0;font-size:16px;color:#0D1F3D;font-weight:600;letter-spacing:.3px;">{title_esc}</h3>
</div>
</div>
'''
    
    new_content += '''</div>
</div>
</section>
<!-- END OUR VIDEO CONTENT -->'''
    
    video_html = re.sub(old_pattern, new_content, video_html, flags=re.DOTALL)
else:
    # Insert content after the nav bar
    # Find the closing of our-nav-bar div
    nav_bar_pos = video_html.find('class="our-nav-bar"')
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
    
    new_content = '\n<!-- OUR VIDEO CONTENT -->\n'
    new_content += '<section class="page-banner" style="background: linear-gradient(rgba(13,31,61,0.85), rgba(13,31,61,0.85)), url(\'images/hero/slide3.jpg\') center/cover;">\n'
    new_content += '<div class="container"><div class="breadcrumb"><a href="index.html">Home</a> <span>/</span> <span>Video Center</span></div>\n'
    new_content += '<h1>Video Center</h1><p>Watch SAGMOTO Trucks in Action</p></div></section>\n'
    new_content += '<section class="section-bg-white"><div class="container">\n'
    new_content += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:30px;padding:50px 0;">\n'
    
    for v in videos:
        title_esc = v['title'].replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        thumb = v['thumbnail'] if v['thumbnail'] else v['cover']
        new_content += f'''<div class="video-card" style="background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 15px rgba(0,0,0,.1);">
<div style="position:relative;overflow:hidden;aspect-ratio:16/9;cursor:pointer;" onclick="this.querySelector('video').style.display='block';this.querySelector('img').style.display='none';this.querySelector('video').play();">
<img alt="{title_esc}" src="{thumb}" style="width:100%;height:100%;object-fit:cover;display:block;"/>
<video preload="none" controls style="width:100%;height:100%;object-fit:cover;display:none;background:#000;">
<source src="{v['video_url']}" type="video/mp4"/>
</video>
<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;background:rgba(194,40,40,.9);border-radius:50%;display:flex;align-items:center;justify-content:center;pointer-events:none;">
<svg width="28" height="28" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="#fff"/></svg>
</div>
</div>
<div style="padding:16px 20px;border-top:3px solid #C62828;">
<h3 style="margin:0;font-size:16px;color:#0D1F3D;font-weight:600;">{title_esc}</h3>
</div>
</div>
'''
    
    new_content += '</div>\n</div></section>\n'
    new_content += '<!-- END OUR VIDEO CONTENT -->\n'
    
    video_html = video_html[:pos] + '\n' + new_content + video_html[pos:]

with open(VIDEO_HTML, "w", encoding="utf-8") as f:
    f.write(video_html)

print(f"\nUpdated video_list.html with {len(videos)} videos (with playable MP4s)")
