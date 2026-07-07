#!/usr/bin/env python3
"""Fix product card image AND text links in all application pages.
Handles \r\n line endings on Windows.
Fixes both:
  Pattern 1: <a href="products.html" target="_self">\n<img alt="MODEL"...
  Pattern 2: <a href="products.html" target="_self">\n    TEXT\n        </a>
Key: group(3) is the raw text content — use it directly, don't duplicate.
"""

import re, os

FILES = ['qyc.html','zxc.html','zhc.html','special.html','pzkyzyc.html','pzmtc.html','tzc.html']

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
    NL = r'\r?\n'
    count = 0
    
    # Pattern 1: Image links — <a href="products.html" target="_self">\n<img alt="MODEL"...
    p1 = re.compile(
        r'(<a href=")products\.html(" target="_self">' + NL + r'\s*<img src="[^"]+" alt=")([^"]+)(")'
    )
    def fix1(m):
        nonlocal count
        alt = m.group(3)
        page = map_model(alt)
        if page != 'products.html':
            count += 1
            return f'{m.group(1)}{page}{m.group(2)}{alt}{m.group(4)}'
        return m.group(0)
    content = p1.sub(fix1, content)
    
    # Pattern 2: Text links below images — <a href="products.html" target="_self">\n    TEXT\n        </a>
    # group(1)=<a href=", group(2)=" target="_self">\r\n\s*, group(3)=TEXT, group(4)=\s*</a>
    p2 = re.compile(
        r'(<a href=")products\.html(" target="_self">' + NL + r'\s*)([A-Za-z0-9][^\n<]+?)' + NL + r'(\s*</a>)'
    )
    def fix2(m):
        nonlocal count
        raw_text = m.group(3)
        page = map_model(raw_text)
        if page != 'products.html':
            count += 1
            # CRITICAL: use raw_text (m.group(3)) directly — do NOT strip and re-inject
            return f'{m.group(1)}{page}{m.group(2)}{raw_text}{m.group(4)}'
        return m.group(0)
    content = p2.sub(fix2, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ {os.path.basename(filepath)}: {count} links fixed')
    else:
        print(f'  ⏭️  {os.path.basename(filepath)}: no changes')
    return count

total = sum(fix_file(f) for f in FILES if os.path.exists(f))
print(f'\n🏁 Total: {total} product card links fixed')
