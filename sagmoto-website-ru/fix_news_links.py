#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix links in news.html and news_list/1.html to point to local news_Detail pages."""
import os, re

BASE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"

# Mapping from news_Detail IDs to local paths
LINK_MAP = {
    r'href="http://www\.sagmoto\.com/news_Detail/22\.html"[^>]*': 'href="news_Detail/22.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/21\.html"[^>]*': 'href="news_Detail/21.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/20\.html"[^>]*': 'href="news_Detail/20.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/19\.html"[^>]*': 'href="news_Detail/19.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/18\.html"[^>]*': 'href="news_Detail/18.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/17\.html"[^>]*': 'href="news_Detail/17.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/16\.html"[^>]*': 'href="news_Detail/16.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/15\.html"[^>]*': 'href="news_Detail/15.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/14\.html"[^>]*': 'href="news_Detail/14.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/13\.html"[^>]*': 'href="news_Detail/13.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/12\.html"[^>]*': 'href="news_Detail/12.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/11\.html"[^>]*': 'href="news_Detail/11.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/9\.html"[^>]*': 'href="news_Detail/9.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/8\.html"[^>]*': 'href="news_Detail/8.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/6\.html"[^>]*': 'href="news_Detail/6.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/5\.html"[^>]*': 'href="news_Detail/5.html"',
    r'href="http://www\.sagmoto\.com/news_Detail/1096035317589622784\.html"[^>]*': 'href="news_Detail/1096035317589622784.html"',
}

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for pattern, replacement in LINK_MAP.items():
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed links in: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

# Fix news.html
fix_file(os.path.join(BASE_DIR, "news.html"))

# Fix news_list/1.html - but need to handle relative paths (it's in news_list/ subdir)
news_list_path = os.path.join(BASE_DIR, "news_list", "1.html")
if os.path.exists(news_list_path):
    with open(news_list_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    # For news_list/1.html, links need ../news_Detail/ prefix since it's in news_list/ subdir
    for pattern, replacement in LINK_MAP.items():
        local_replacement = replacement.replace('href="news_Detail/', 'href="../news_Detail/')
        content = re.sub(pattern, local_replacement, content)
    
    if content != original:
        with open(news_list_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed links in: {news_list_path}")
    else:
        print(f"No changes needed: {news_list_path}")
else:
    print(f"File not found: {news_list_path}")

print("Done!")
