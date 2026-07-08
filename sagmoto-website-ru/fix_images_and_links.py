#!/usr/bin/env python3
"""
Fix two issues in SAGMOTO mirror pages:
1. CMS lazy images → direct src (CMS JS won't process lazy attribute)
2. Dead product detail links → redirect to our products.html or fix to correct paths
"""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    "qyc.html", "zxc.html", "zhc.html", "special.html", "tzc.html",
    "about.html", "pzkyzyc.html", "pzmtc.html", "service.html",
    "video_list.html",
    "service_list/1674411714944516096.html",
    "service_list/1674411730417303552.html",
    "service_list/1674411748220751872.html",
    "service_list/1674411767427842048.html",
    "news_list/81163.html",
    "news_list/1.html",
]

# Map CMS truck model names to our product categories
MODEL_TO_CAT = {
    # Heavy Duty
    "E1st": "heavy", "E3": "heavy", "X3s": "heavy", "Z3": "heavy",
    "E9": "heavy",
    # Medium Duty
    "E6": "medium", "X6": "medium", "X5": "medium",
    # Light Duty
    "i9": "light", "X9": "light", "X7": "light",
    "i5": "light",
    # Off-road
    "4X4": "offroad",
}

def fix_images(html):
    """Replace CMS lazy images with direct src."""
    # Pattern: <img src="...s.png" lazy="https://real-url" ...>
    # Convert to: <img src="https://real-url" ...>
    def replace_lazy_img(match):
        tag = match.group(1)
        # More flexible: match lazy="URL" (could be before or after src)
        lazy_match = re.search(r'lazy="(https://[^"]+)"', tag)
        if lazy_match:
            real_url = lazy_match.group(1)
            # Remove lazy attribute
            tag = re.sub(r'\s+lazy="[^"]*"', '', tag)
            # Remove la="la" if present
            tag = re.sub(r'\s+la="la"', '', tag)
            # Replace src with real URL (if src is a placeholder)
            if 'src="mirror/npublic/img/s.png"' in tag:
                tag = tag.replace('src="mirror/npublic/img/s.png"', f'src="{real_url}"')
            elif 'src="' not in tag:
                tag = tag.replace('<img ', f'<img src="{real_url}" ')
            else:
                tag = re.sub(r'src="[^"]*s\.png"', f'src="{real_url}"', tag)
        return '<img ' + tag.lstrip('<img ')

    # Match <img> tags within a single line (conservative)
    count = 0
    new_lines = []
    for line in html.split('\n'):
        if '<img ' in line and ' lazy="' in line:
            new_line = re.sub(r'(<img[^>]+lazy="https://[^"]+"[^>]*>)', replace_lazy_img, line)
            if new_line != line:
                count += 1
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    if count > 0:
        print(f"  Fixed {count} lazy images → direct src")
    return '\n'.join(new_lines)

def fix_links(html, page_name):
    """Fix dead product detail links."""
    fixes = []
    
    def replace_link(match):
        full_url = match.group(1)
        
        # Product detail pages: mirror/prolist_1/392.html, mirror/prolist/7.html
        if re.search(r'mirror/prolist(?:_\d+)?/\d+\.html', full_url):
            return 'href="products.html"'
        
        # Individual truck model pages: mirror/E3.html, mirror/X9.html, etc.
        model_match = re.search(r'mirror/(E1st|E3|E6|E9|X3s|X5|X6|X7|X9|Z3|i5|i9|4X4)(?:_\d*)?\.html', full_url)
        if model_match:
            model = model_match.group(1)
            cat = MODEL_TO_CAT.get(model, "heavy")
            return f'href="products.html?cat={cat}"'
        
        # SEO/license page
        if 'mirror/seoList.html' in full_url:
            return 'href="index.html"'
        
        # Get quote / inquiry page
        if 'mirror/prolist_2.html' in full_url:
            return 'href="contact.html"'
        
        # Fix mirror/ prefix on anchor-only links to same page
        # mirror/qyc.html#anchor → qyc.html#anchor
        anchor_match = re.match(r'mirror/([\w/]+\.html)(#.*)', full_url)
        if anchor_match:
            target_page = anchor_match.group(1)
            anchor = anchor_match.group(2)
            # Remove subdirectory from target
            target_page = target_page.split('/')[-1]
            return f'href="{target_page}{anchor}"'
        
        # Fix mirror/index.html → index.html
        if full_url == 'mirror/index.html':
            return 'href="index.html"'
        
        return match.group(0)
    
    # Match href="mirror/..." links
    pattern = r'href="(mirror/[^"]+)"'
    new_html, fix_count = re.subn(pattern, replace_link, html)
    
    if fix_count > 0:
        print(f"  Fixed {fix_count} dead/broken links")
    
    return new_html

def main():
    total_img_fixes = 0
    total_link_fixes = 0
    
    for page_file in PAGES:
        filepath = os.path.join(BASE_DIR, page_file)
        if not os.path.exists(filepath):
            print(f"SKIP: {page_file} (not found)")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        orig_len = len(html)
        
        # Fix 1: CMS lazy images
        html = fix_images(html)
        
        # Fix 2: Dead product links
        html = fix_links(html, page_file)
        
        if len(html) != orig_len:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"DONE: {page_file}")
        else:
            print(f"OK: {page_file} (no changes needed)")
    
    # Also fix remaining http:// protocol-relative URLs in CSS/JS refs if any
    print("\n=== Summary ===")
    print(f"All {len(PAGES)} pages processed")

if __name__ == '__main__':
    main()
