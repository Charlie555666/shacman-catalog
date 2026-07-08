import re
import os

# Product name → detail page mapping
# Based on original sagmoto.com links mapped to our custom pages
PRODUCT_LINK_MAP = {
    'E9': 'e9.html',
    'X9': 'x9.html',
    'i9': 'i9.html',
    'X7': 'x7.html',
    'E6': 'e6.html',
    'X6': 'x6.html',
    'i5': 'i5.html',
    'X5': 'x5.html',
    'Z3': 'z3.html',
    'E1st': 'e1st.html',
    'E3': 'e3.html',
    'X3s': 'x3s.html',
    '4x4': 'off-road-4x4.html',
    '4×4': 'off-road-4x4.html',
}

# Pages to fix
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

    # Pattern: match <a href="products.html?cat=..." ...> ... </a> blocks that contain p_menuItemhat
    # We need to find product links in the p_level3Box section
    # Strategy: find each <a> tag with products.html?cat=... inside p_level3Item context,
    # then look for p_menuItemhat or alt/title to determine product name

    # First, let's find all <a href="products.html?cat=... in the content and their surrounding context
    # Use a regex that captures the <a> tag and its content until </a>

    pattern = r'<a href="products\.html\?cat=[^"]*"([^>]*)>(.*?)</a>'

    def replacer(match):
        nonlocal fixes
        attrs = match.group(1)
        inner = match.group(2)

        # Look for product name in inner HTML
        # Try p_menuItemhat first
        name_match = re.search(r'<span class="p_menuItemhat">([^<]+)</span>', inner)
        if not name_match:
            # Try alt or title attribute in img tag
            name_match = re.search(r'<img[^>]*alt="([^"]+)"', inner)
        if not name_match:
            # Try title attribute
            name_match = re.search(r'<img[^>]*title="([^"]+)"', inner)

        if name_match:
            product_name = name_match.group(1).strip()
            # Handle 4x4 variations
            if product_name in ('4X4', '4×4', '4x4'):
                product_name = '4x4'

            if product_name in PRODUCT_LINK_MAP:
                new_href = PRODUCT_LINK_MAP[product_name]
                # Check if this is in p_level3Item context (to avoid replacing nav category links)
                # Heuristic: if inner contains hbright or p_menuItemhat, it's a product link
                if 'hbright' in inner or 'p_menuItemhat' in inner:
                    fixes += 1
                    return f'<a href="{new_href}"{attrs}>{inner}</a>'

        return match.group(0)  # no change

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  FIXED {filename}: {fixes} product links updated")
        return fixes
    else:
        print(f"  OK {filename}: no changes needed")
        return 0


def main():
    total = 0
    for page in PAGES:
        print(f"Processing {page}...")
        total += fix_page(page)
    print(f"\nTotal fixes: {total}")


if __name__ == '__main__':
    main()
