import re
import os

# Product name → detail page mapping
PRODUCT_LINK_MAP = {
    'E9': 'e9.html',
    'X9': 'x9.html',
    'i9': 'i9.html',
    'I9': 'i9.html',
    'X7': 'x7.html',
    'E6': 'e6.html',
    'X6': 'x6.html',
    'i5': 'i5.html',
    'I5': 'i5.html',
    'X5': 'x5.html',
    'Z3': 'z3.html',
    'E1st': 'e1st.html',
    'E3': 'e3.html',
    'X3s': 'x3s.html',
    '4x4': 'off-road-4x4.html',
    '4×4': 'off-road-4x4.html',
    '4X4': 'off-road-4x4.html',
    'Off-road': 'pzkyzyc.html',
    'Off-road Dump': 'pzkyzyc.html',
    'X3S': 'x3s.html',
}

PAGES = ['qyc.html', 'zxc.html', 'zhc.html', 'special.html', 'pzkyzyc.html', 'pzmtc.html', 'tzc.html']

BASE_DIR = r'C:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website'


def fix_page(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixes = 0

    # Fix 1: <a href="products.html?cat=..." target=""> with <span>NAME</span> inside (body product links)
    # Pattern: <a href="products.html?cat=..." target="">\s*<span>(NAME)</span>\s*</a>
    pattern1 = r'<a href="products\.html\?cat=[^"]*" target="">\s*<span>([^<]+)</span>\s*</a>'

    def replacer1(match):
        nonlocal fixes
        name = match.group(1).strip()
        if name in PRODUCT_LINK_MAP:
            fixes += 1
            return f'<a href="{PRODUCT_LINK_MAP[name]}" target=""><span>{name}</span></a>'
        return match.group(0)

    new_content = re.sub(pattern1, replacer1, content)

    # Fix 2: <a href="products.html?cat=..." ...> with <img alt="NAME" .../> NAME</a> (nav dropdown links)
    # These are our custom nav links: <a href="products.html?cat=light"><img src="..." alt="i9"/> i9</a>
    pattern2 = r'<a href="products\.html\?cat=[^"]*"([^>]*)>\s*<img([^>]*alt="([^"]+)"[^>]*)/>\s*([^<]+)</a>'

    def replacer2(match):
        nonlocal fixes
        attrs = match.group(1)
        img_attrs = match.group(2)
        alt_name = match.group(3).strip()
        text_name = match.group(4).strip()

        # Use text name if it matches a product, otherwise try alt
        name = text_name if text_name in PRODUCT_LINK_MAP else alt_name
        if name in PRODUCT_LINK_MAP:
            fixes += 1
            return f'<a href="{PRODUCT_LINK_MAP[name]}"{attrs}><img{img_attrs}/> {text_name}</a>'
        return match.group(0)

    new_content = re.sub(pattern2, replacer2, new_content)

    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  FIXED {filename}: {fixes} links updated")
        return fixes
    else:
        print(f"  OK {filename}: no changes")
        return 0


def main():
    total = 0
    for page in PAGES:
        print(f"Processing {page}...")
        total += fix_page(page)
    print(f"\nTotal fixes: {total}")


if __name__ == '__main__':
    main()
