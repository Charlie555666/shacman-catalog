#!/usr/bin/env python3
"""Extract news items from official sagmoto.com HTML and generate replacement HTML for news.html"""

import re
import html

OFFICIAL_HTML = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website\.mirror_raw\news_list1_official.html"

with open(OFFICIAL_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# Find all news_Detail links with their surrounding context
# Pattern: find blocks containing news_Detail links, titles, and lazy images
# The official HTML structure has: <a href="/news_Detail/XX.html">...<img ... lazy="URL" />...<title text>...

# Strategy: find each news_Detail link, then search nearby for the image (lazy attr) and title text
# The news items are in a repeating structure

# Extract all news_Detail IDs (unique, preserving order)
detail_pattern = r'href="/news_Detail/(\d+)\.html"'
matches = list(re.finditer(detail_pattern, content))
seen_ids = []
for m in matches:
    nid = m.group(1)
    if nid not in seen_ids:
        seen_ids.append(nid)

print(f"Found {len(seen_ids)} unique news IDs: {seen_ids}")

# For each news ID, find the block and extract title + image
news_items = []
for nid in seen_ids:
    # Find first occurrence of this news_Detail link
    link_pos = content.find(f'/news_Detail/{nid}.html')
    if link_pos < 0:
        continue
    
    # Search in a window around this link (500 chars before, 2000 after)
    start = max(0, link_pos - 500)
    end = min(len(content), link_pos + 2000)
    block = content[start:end]
    
    # Find lazy image URL (the real image)
    lazy_match = re.search(r'lazy="(https://omo-oss-image[^"]+)"', block)
    image_url = lazy_match.group(1) if lazy_match else ""
    
    # Find the title - look for <p class="p_text"> or text inside the link
    # Official structure: title is in a <p> or <span> near the link
    # Try multiple patterns
    title = ""
    
    # Pattern 1: Look for title in alt attribute of the image
    alt_match = re.search(r'alt="([^"]+)"', block)
    if alt_match and alt_match.group(1) not in ["", "PRODUCTS", "SAG MOTO"]:
        title = alt_match.group(1)
    
    # Pattern 2: Look for p_text or similar title class
    if not title:
        title_match = re.search(r'class="p_text[^"]*"[^>]*>([^<]+)<', block)
        if title_match:
            title = title_match.group(1).strip()
    
    # Pattern 3: Look for news title in a heading or paragraph after the image
    if not title:
        title_match = re.search(r'<p[^>]*>\s*([^<]{10,})\s*</p>', block)
        if title_match:
            t = title_match.group(1).strip()
            if t and not t.startswith('http') and len(t) > 15:
                title = t
    
    # Pattern 4: Look for text content after the image area
    if not title:
        # Find text between > and < that looks like a title (longer text)
        texts = re.findall(r'>\s*([A-Z][^<>]{15,})\s*<', block)
        for t in texts:
            t = t.strip()
            if t and not t.startswith('http') and 'svg' not in t and 'path' not in t:
                title = t
                break
    
    # Clean up title
    title = html.unescape(title).strip()
    
    if image_url or title:
        news_items.append({
            'id': nid,
            'title': title,
            'image': image_url,
            'link': f'/news_Detail/{nid}.html'
        })
        print(f"  [{nid}] title={title[:60]}... image={'YES' if image_url else 'NO'}")

# Also search for the news item with long ID (1096035317589622784)
# This might be the "National Machinery Industry Quality Award" article
long_id = '1096035317589622784'
if long_id in seen_ids:
    link_pos = content.find(f'/news_Detail/{long_id}.html')
    start = max(0, link_pos - 500)
    end = min(len(content), link_pos + 2000)
    block = content[start:end]
    
    lazy_match = re.search(r'lazy="(https://omo-oss-image[^"]+)"', block)
    image_url = lazy_match.group(1) if lazy_match else ""
    
    # Try to find title
    alt_match = re.search(r'alt="([^"]+)"', block)
    title = alt_match.group(1) if alt_match else ""
    
    if not title:
        texts = re.findall(r'>\s*([A-Z][^<>]{15,})\s*<', block)
        for t in texts:
            t = t.strip()
            if t and not t.startswith('http') and 'svg' not in t:
                title = t
                break
    
    print(f"\n  [{long_id}] title={title[:60]}... image={'YES' if image_url else 'NO'}")

print(f"\n=== Total news items extracted: {len(news_items)} ===")
for item in news_items:
    print(f"  ID={item['id']}: {item['title'][:70]}")
    print(f"    Image: {item['image'][:80]}..." if item['image'] else "    Image: NONE")
