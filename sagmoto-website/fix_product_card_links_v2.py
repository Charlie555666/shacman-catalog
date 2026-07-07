#!/usr/bin/env python3
"""Fix product card image/text links in all application pages.
Handles both \n and \r\n line endings.
"""

import re
import os

FILES = ['qyc.html', 'zxc.html', 'zhc.html', 'special.html', 'pzkyzyc.html', 'pzmtc.html', 'tzc.html']

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
    name = name.strip()
    for prefix in sorted(MODEL_MAP.keys(), key=len, reverse=True):
        if name.startswith(prefix):
            return MODEL_MAP[prefix]
    return 'products.html'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    count_img = 0
    count_text = 0
    NL = r'\r?\n'  # Handle both Windows and Unix line endings
    
    # Pattern 1: Image card links
    img_pattern = re.compile(
        r'(<a href=")products\.html(" target="_self">' + NL + r'\s*<img src="[^"]+" alt=")([^"]+)(")'
    )
    def replace_img(m):
        nonlocal count_img
        alt_text = m.group(3)
        model_page = map_model(alt_text)
        if model_page != 'products.html':
            count_img += 1
            return f'{m.group(1)}{model_page}{m.group(2)}{alt_text}{m.group(4)}'
        return m.group(0)
    content = img_pattern.sub(replace_img, content)
    
    # Pattern 2: Text card links (below images)
    text_pattern = re.compile(
        r'(<a href=")products\.html(" target="_self">' + NL + r'\s*)([A-Za-z0-9][^\n<]+?)' + NL + r'(\s*</a>)'
    )
    def replace_text(m):
        nonlocal count_text
        text = m.group(3).strip()
        model_page = map_model(text)
        if model_page != 'products.html':
            count_text += 1
            return f'{m.group(1)}{model_page}{m.group(2)}{text}{m.group(3)}{m.group(4)}'
        return m.group(0)
    content = text_pattern.sub(replace_text, content)
    
    total = count_img + count_text
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ {os.path.basename(filepath)}: {count_img} img + {count_text} text = {total} links fixed')
    else:
        print(f'  ⏭️  {os.path.basename(filepath)}: no changes needed')
    
    return total

def main():
    total = 0
    for f in FILES:
        if os.path.exists(f):
            total += fix_file(f)
        else:
            print(f'  ❌ {f}: file not found')
    print(f'\n🏁 Total: {total} product card links fixed')

if __name__ == '__main__':
    main()
