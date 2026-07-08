import re

# Read index.html
with open(r'c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Mapping: alt text -> target detail page
product_links = {
    'X9 4X4 Dump Truck': 'x9.html',
    'X9 Tow truck': 'x9.html',
    'X7 Flatbed Truck': 'x7.html',
    '9 Series Sweeper': 'x9.html',
    'X6 Dropside Truck': 'x6.html',
    'X6 AWD Cargo truck': 'x6.html',
    'X6 Cement Mixers Truck': 'x6.html',
    'X6 Sprinkler Truck': 'x6.html',
    'E1st Tractor': 'e1st.html',
    'Z3 Tractor Truck': 'z3.html',
    'X3s Trailer Truck': 'x3s.html',
    'E3 Tractor Truck': 'e3.html',
    'X9 Aerial Work Platform Truck': 'x9.html',
    'X7 Concrete Mixer Truck': 'x7.html',
    'X3s Mixer trucks 8X4': 'x3s.html',
    '9 series': 'off-road-4x4.html',
    '7 Series': 'x7.html',
    '6 Series': 'x6.html',
    'Off-road Dump Truck': 'off-road-4x4.html',
    'i9': 'i9.html',
    'i9 lite': 'i9.html',
    'i5 compressor car': 'i5.html',
}

# Find the recommended model section
section_start = content.find('<div class="recommended-model" id="recommended">')
section_end_marker = '<!-- ===== ABOUT / WHY CHOOSE ===== -->'
section_end = content.find(section_end_marker)
if section_end == -1:
    section_end = len(content)

before = content[:section_start]
section = content[section_start:section_end]
after = content[section_end:]

# Regex to match a complete product-grid-item block
# The block starts with <div class="product-grid-item"> and ends with </div></div></div> (closing pg-body, then product-grid-item)
# But we use a more precise approach: capture everything up to the closing </div> of product-grid-item
# We know each block has: pg-img (with <a> and <img>), then pg-body (with <h4>, <p> descs, <a> plus)

pattern = r'(<div class="product-grid-item">\s*<div class="pg-img">\s*)<a href="[^"]+"><img src="([^"]+)" alt="([^"]+)"></a>(\s*</div>\s*<div class="pg-body">\s*)<h4><a href="[^"]+">[^<]+</a></h4>(.*?\s*)<a href="[^"]+" class="pg-plus">\+</a>(\s*</div>\s*</div>)'

def replace_block(match):
    pre_img = match.group(1)
    img_src = match.group(2)
    alt = match.group(3)
    mid = match.group(4)
    body_desc = match.group(5)
    post = match.group(6)
    
    if alt in product_links:
        target = product_links[alt]
        print(f'Fixed: {alt} -> {target}')
        return f'{pre_img}<a href="{target}"><img src="{img_src}" alt="{alt}"></a>{mid}<h4><a href="{target}">{alt}</a></h4>{body_desc}<a href="{target}" class="pg-plus">+</a>{post}'
    else:
        print(f'SKIPPED: {alt} (no mapping)')
        return match.group(0)

new_section = re.sub(pattern, replace_block, section, flags=re.DOTALL)

# Reassemble
content = before + new_section + after

# Write back
with open(r'c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone! All product links in Recommended Model section fixed.')
