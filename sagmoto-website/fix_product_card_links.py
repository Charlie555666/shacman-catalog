#!/usr/bin/env python3
"""Fix product card image/text links in all application pages.
Maps vehicle model names (from alt attributes or text) to correct detail pages.
"""

import re
import os

FILES = ['qyc.html', 'zxc.html', 'zhc.html', 'special.html', 'pzkyzyc.html', 'pzmtc.html', 'tzc.html']

# Map model name prefix → detail page
MODEL_MAP = {
    'E9': 'e9.html', 'X9': 'x9.html', 'i9': 'i9.html',
    'E6': 'e6.html', 'X6': 'x6.html',
    'E3': 'e3.html', 'X3': 'x3s.html',
    'X7': 'x7.html',
    'Z3': 'z3.html', 'E1': 'e1st.html',
    'X5': 'x5.html', 'i5': 'i5.html',
    'Off-road': 'off-road-4x4.html',
    '3 Series': 'x3s.html',
    '6 Series': 'x6.html',
    '9 Series': 'x9.html',
}

def map_model(name):
    """Map a vehicle model name to its detail page."""
    name = name.strip()
    # Direct prefix match (longest first to avoid E3 matching before E3)
    for prefix in sorted(MODEL_MAP.keys(), key=len, reverse=True):
        if name.startswith(prefix):
            return MODEL_MAP[prefix]
    return 'products.html'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    replacements = 0
    
    # Pattern 1: Image card links — <a href="products.html" target="_self">\n<img alt="MODEL"...
    # This is the product card image link
    def replace_img_link(m):
        nonlocal replacements
        alt_text = m.group(3)
        model_page = map_model(alt_text)
        if model_page != 'products.html':
            replacements += 1
            return f'{m.group(1)}{model_page}{m.group(2)}{alt_text}{m.group(4)}'
        return m.group(0)
    
    img_pattern = re.compile(
        r'(<a href=")products\.html(" target="_self">\s*\n\s*<img src="[^"]+" alt=")([^"]+)(")'
    )
    content = img_pattern.sub(replace_img_link, content)
    
    # Pattern 2: Text card links — <a href="products.html" target="_self">\n    TEXT\n        </a>
    # These are the text labels below the images
    def replace_text_link(m):
        nonlocal replacements
        text = m.group(2).strip()
        model_page = map_model(text)
        if model_page != 'products.html':
            replacements += 1
            return f'{m.group(1)}{model_page}{m.group(2)}{m.group(3)}'
        return m.group(0)
    
    text_pattern = re.compile(
        r'(<a href=")products\.html(" target="_self">\s*\n\s*)([A-Za-z0-9][^\n<]+?)\s*\n(\s*</a>)'
    )
    content = text_pattern.sub(replace_text_link, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ {os.path.basename(filepath)}: {replacements} links fixed')
    else:
        print(f'  ⏭️  {os.path.basename(filepath)}: no changes needed')
    
    return replacements

def main():
    total = 0
    for f in FILES:
        if os.path.exists(f):
            r = fix_file(f)
            total += r
        else:
            print(f'  ❌ {f}: file not found')
    print(f'\n🏁 Total: {total} product card links fixed across {len(FILES)} files')

if __name__ == '__main__':
    main()
