#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix double head tags in news detail pages."""
import os, glob

NEWS_DETAIL_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website\news_Detail"

for filepath in glob.glob(os.path.join(NEWS_DETAIL_DIR, "*.html")):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix double head tags: <head> followed by <head>
    content = content.replace('<head>\n<head>', '<head>')
    # Fix double closing head tags: </head>\n</head>
    content = content.replace('</head>\n</head>', '</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {os.path.basename(filepath)}")

print("Done!")
