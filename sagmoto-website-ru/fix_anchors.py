#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining relative paths in news detail pages."""
import os, glob, re

NEWS_DETAIL_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website\news_Detail"

fixes = [
    (r'href="qyc\.html#', 'href="../qyc.html#'),
    (r'href="zxc\.html#', 'href="../zxc.html#'),
    (r'href="zhc\.html#', 'href="../zhc.html#'),
    (r'href="special\.html#', 'href="../special.html#'),
    (r'href="tzc\.html#', 'href="../tzc.html#'),
]

for filepath in glob.glob(os.path.join(NEWS_DETAIL_DIR, "*.html")):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig = content
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)
    
    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed anchors: {os.path.basename(filepath)}")
    else:
        print(f"No anchor fixes: {os.path.basename(filepath)}")

print("Done!")
