#!/usr/bin/env python3
"""Fix dead links in custom pages."""
import os, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mapping: dead page → target
LINK_MAP = {
    'href="e1st.html"': 'href="products.html?cat=heavy"',
    'href="e3.html"': 'href="products.html?cat=heavy"',
    'href="e6.html"': 'href="products.html?cat=medium"',
    'href="e9.html"': 'href="products.html?cat=heavy"',
    'href="i5.html"': 'href="products.html?cat=light"',
    'href="i9.html"': 'href="products.html?cat=light"',
    'href="x3s.html"': 'href="products.html?cat=heavy"',
    'href="x5.html"': 'href="products.html?cat=medium"',
    'href="x6.html"': 'href="products.html?cat=medium"',
    'href="x7.html"': 'href="products.html?cat=light"',
    'href="x9.html"': 'href="products.html?cat=light"',
    'href="z3.html"': 'href="products.html?cat=heavy"',
    'href="off-road-4x4.html"': 'href="products.html?cat=offroad"',
    # Also fix any links that point to mirror/ pages from custom pages
}

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    orig = html
    for old, new in LINK_MAP.items():
        html = html.replace(old, new)
    if html != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        fixes = sum(1 for old in LINK_MAP if old in orig)
        print(f"FIXED {os.path.basename(filepath)}: {fixes} dead links")
    else:
        print(f"OK: {os.path.basename(filepath)}")

CUSTOM_PAGES = [
    'index.html',
    'products.html',
    'contact.html',
    'news.html',
    'new-energy.html',
    'privacy.html',
    'terms.html',
]

for page in CUSTOM_PAGES:
    filepath = os.path.join(BASE_DIR, page)
    if os.path.exists(filepath):
        fix_file(filepath)
    else:
        print(f"SKIP: {page}")

print("\nAll custom pages checked.")
