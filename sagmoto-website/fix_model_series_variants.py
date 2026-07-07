import re, os, html

# Variant data for each model series
MODEL_VARIANTS = {
    'e3': {
        'title': 'E3 Series',
        'desc': 'The E3 series offers a comprehensive range of heavy-duty commercial vehicles including tractor trucks, dump trucks, van trucks, cement mixers, and garbage compactor trucks. Built for reliability and cost-effectiveness across diverse applications.',
        'keywords': 'E3 Series, SAGMOTO E3, tractor truck, dump truck, van truck, cement mixer, garbage truck, commercial truck, heavy-duty',
        'variants': [
            {'name': 'E3 Tractor Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d82f0e0f-a783-4e91-950e-5b53e7c5b62b.jpg'},
            {'name': 'E3 Dump Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/641824c6-ae6a-4214-aba1-09cd8cfa49e2.png'},
            {'name': 'E3 Van Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2262cf6f-2bd5-4937-95fd-9afa450d081b.jpg'},
            {'name': 'E3 Cement Mixer Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0a41d6ac-a7e1-4f0e-9003-63fe6abb528a.png'},
            {'name': 'E3 Compactor Garbage Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/bdf3e2e2-21b1-4cb9-a31f-84c9e5ae9313.png'},
        ]
    },
    'e6': {
        'title': 'E6 Series',
        'desc': 'The E6 series delivers versatile medium-duty solutions with van trucks, stake trucks, refrigerated trucks, sprinkler trucks, and truck-mounted cranes. Engineered for efficiency and adaptability in urban and regional logistics.',
        'keywords': 'E6 Series, SAGMOTO E6, van truck, stake truck, refrigerated truck, sprinkler truck, truck-mounted crane, commercial truck, medium-duty',
        'variants': [
            {'name': 'E6 Van Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f85e16e-3943-495e-a10b-f54021855c2f.png'},
            {'name': 'E6 Stake Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/02ff6768-1e5f-49ed-826e-f9acfd009eaa.png'},
            {'name': 'E6 Refrigerated Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/399c3e75-0e13-4c8e-b456-19c7a628d153.png'},
            {'name': 'E6 Sprinkler Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/e5f4f018-4400-4c7c-b8cb-0448bd4c9ef1.png'},
            {'name': 'E6 Truck-mounted Crane', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/401abd66-2e22-484f-8316-28b108572308.jpg'},
        ]
    },
    'e9': {
        'title': 'E9 Series',
        'desc': 'The E9 series represents SAGMOTO\'s premium heavy-duty platform with van trucks, flatbed trucks, and specialized kitchen food waste garbage trucks. Designed for maximum payload and durability in demanding operations.',
        'keywords': 'E9 Series, SAGMOTO E9, van truck, flatbed truck, garbage truck, commercial truck, heavy-duty',
        'variants': [
            {'name': 'E9 Van Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/19ebc623-5f15-41e9-a7ba-cc6d974584ac.png'},
            {'name': 'E9 Flatbed Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/914619e7-474a-4e4e-a11d-b0fc3cecd527.png'},
            {'name': 'E9 Kitchen Food Waste Garbage Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/40585d1d-d507-4989-9a8a-c2185b223a6b.png'},
        ]
    },
    'x3s': {
        'title': 'X3s Series',
        'desc': 'The X3s series provides reliable heavy-duty solutions including dump trucks, lorry trucks, mixer trucks (6x4 and 8x4), oil tankers, and truck-mounted cranes. A proven platform for construction and logistics industries.',
        'keywords': 'X3s Series, SAGMOTO X3s, dump truck, lorry truck, mixer truck, oil tanker, truck-mounted crane, commercial truck, heavy-duty',
        'variants': [
            {'name': 'X3s Dump Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ad8c9fa6-6e55-4d5d-92e1-77960ba555ec.jpg'},
            {'name': 'X3s Lorry Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/e83231d1-3e25-41c6-93ff-0bf15bb13316.png'},
            {'name': 'X3s Mixer Truck 6X4', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4ee9b3c4-a98b-4e54-90c7-89c9dcba1972.png'},
            {'name': 'X3s Mixer Truck 8X4', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3ca8f8b2-cf60-437e-999d-065aeae34090.png'},
            {'name': 'X3s Oil Tanker', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/56c73d45-2060-4cd1-baae-576cf84659d6.png'},
            {'name': 'X3s Truck-mounted Crane', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/88996bcc-1c8b-4b32-ae4c-99716b8f9103.png'},
            {'name': '3 Series Truck-mounted Crane', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4d4f6d4c-5e09-4ec5-baa5-b582daa606ae.jpg'},
        ]
    },
    'x6': {
        'title': 'X6 Series',
        'desc': 'The X6 series offers versatile medium-duty vehicles including concrete mixer trucks, garbage trucks, fuel tankers, sprinkler trucks, sweepers, and truck-mounted cranes. Built for municipal and construction applications.',
        'keywords': 'X6 Series, SAGMOTO X6, concrete mixer, garbage truck, fuel tanker, sprinkler truck, sweeper, truck-mounted crane, commercial truck, medium-duty',
        'variants': [
            {'name': 'X6 Concrete Mixer Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a2e9bffe-b06b-4bff-8566-92551264f616.png'},
            {'name': 'X6 Garbage Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fe165a5a-b4ab-4be6-830a-546fd1bc264d.png'},
            {'name': '6 Series Garbage Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/b7059f2f-8224-45c2-8c0c-e1cb56818806.jpg'},
            {'name': 'X6 Fuel Tanker Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/50232cc9-851e-4f0f-86b4-33b56393e0af.png'},
            {'name': 'X6 Sprinkler Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/696b7074-b190-47e2-a69f-906193cb7bed.png'},
            {'name': '6 Series Sweeper', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a45a8447-4fb2-446e-a911-eaaa126ecffc.jpg'},
            {'name': '6 Series Truck-mounted Crane', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/91479b90-3e33-47eb-b7e4-58bc7e613060.jpg'},
        ]
    },
    'x7': {
        'title': 'X7 Series',
        'desc': 'The X7 series is SAGMOTO\'s versatile light-duty platform featuring dump trucks, cargo trucks, flatbed trucks, van trucks, concrete mixers, sprinkler trucks, and truck-mounted cranes. Ideal for urban construction and logistics.',
        'keywords': 'X7 Series, SAGMOTO X7, dump truck, cargo truck, flatbed truck, van truck, concrete mixer, sprinkler truck, truck-mounted crane, commercial truck, light-duty',
        'variants': [
            {'name': 'X7 Dump Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/892e7233-ff2e-4d46-819e-d7d21fc5d103.jpg'},
            {'name': 'X7 Cargo Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/f238a49d-f9e3-4dcb-b090-78caff542868.png'},
            {'name': 'X7 Flatbed Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/57b40134-f17a-4635-9862-4918881781b5.png'},
            {'name': 'X7 Van Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/73fdd687-d18f-4a96-bd38-6956ea7fa317.png'},
            {'name': 'X7 Concrete Mixer Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2736f8a9-4674-4ae8-bda2-ff995e34c894.png'},
            {'name': 'X7 Sprinkler Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/c3d3dc03-8b45-473d-8eae-1a09e06a8de8.png'},
            {'name': 'X7 Truck-mounted Crane', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/e76174dc-84a9-4f58-b4ee-b0eb7b12d93e.png'},
        ]
    },
    'x9': {
        'title': 'X9 Series',
        'desc': 'The X9 series is SAGMOTO\'s all-purpose light-duty platform with 4x4 dump trucks, refrigerated trucks, garbage trucks, fuel tankers, cement mixers, sweepers, tow trucks, aerial work platforms, and truck-mounted cranes.',
        'keywords': 'X9 Series, SAGMOTO X9, 4x4 dump truck, refrigerated truck, garbage truck, fuel tanker, cement mixer, sweeper, tow truck, aerial work platform, truck-mounted crane, commercial truck, light-duty',
        'variants': [
            {'name': 'X9 4X4 Dump Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3f35ad3a-2ea6-42cb-bb86-2af2c12a16e7.jpg'},
            {'name': 'X9 Refrigerated Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/1135c6a0-02f6-423f-ad62-d237830b8eb3.png'},
            {'name': 'X9 Garbage Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3747b57a-4512-4ca1-ab6a-f66cef7a1d95.png'},
            {'name': '9 Series Garbage Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/aa9b3a8a-b5a2-4e3d-904d-fd31268a36a7.jpg'},
            {'name': 'X9 Fuel Tanker Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/854c60e6-5890-4b39-8eb8-3c34ef50911c.png'},
            {'name': '9 Series Cement Mixer Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/68113b77-4343-4c39-bb99-7ec69618dc51.jpg'},
            {'name': '9 Series Sweeper', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8cd0ebb8-92b2-4dcf-a200-ffbc21fffe71.jpg'},
            {'name': '9 Series Tow Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/eea04d8f-c0d3-44bc-b4bf-9da84c76d707.jpg'},
            {'name': '9 Series Flatbed Tow Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/b9307d53-fd2a-4c1e-a66e-dc6feb87ee49.jpg'},
            {'name': '9 Series Aerial Work Platform', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/cbcfaf9c-300c-4f22-8cee-6c1fade7b88e.jpg'},
            {'name': '9 Series Truck-mounted Crane', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/79bf55f1-1b9a-45e6-b059-2f81ec84a394.jpg'},
        ]
    },
    'i9': {
        'title': 'i9 Series',
        'desc': 'The i9 series represents SAGMOTO\'s commitment to sustainable transportation with electric light-duty trucks. Featuring an integrated electric drive axle and highly integrated structure for zero-emission urban logistics.',
        'keywords': 'i9 Series, SAGMOTO i9, electric truck, new energy, light-duty, commercial truck, zero-emission',
        'variants': [
            {'name': 'i9 Lite', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64a47e38-5f9e-4677-9389-1291e77e33e1.jpg'},
        ]
    },
    'off-road-4x4': {
        'title': 'Off-road 4x4 Series',
        'desc': 'The Off-road 4x4 series is built for extreme terrain and challenging environments. Featuring robust 4x4 all-wheel drive, high ground clearance, and durable construction for mining, construction, and exploration applications.',
        'keywords': 'Off-road 4x4, SAGMOTO off-road, dump truck, 4x4, all-wheel drive, mining truck, commercial truck',
        'variants': [
            {'name': 'Off-road Dump Truck', 'img': 'https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg'},
        ]
    },
}

def generate_variants_html(variants):
    """Generate HTML for the variants section."""
    cards = []
    for v in variants:
        name_escaped = html.escape(v['name'])
        img = v['img']
        fallback = f"data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27200%27 height=%27150%27%3E%3Crect fill=%27%23f5f5f5%27 width=%27200%27 height=%27150%27/%3E%3Ctext x=%27100%27 y=%2775%27 text-anchor=%27middle%27 fill=%27%23999%27 font-size=%2712%27%3E{name_escaped}%3C/text%3E%3C/svg%3E"
        cards.append(f'''    <div class="variant-card">
            <img src="{img}" alt="{name_escaped}" onerror="this.src='{fallback}'">
            <h4>{name_escaped}</h4>
        </div>''')
    
    return '''<!-- ===== MODEL VARIANTS ===== -->
<section class="section-bg-white">
    <div class="container">
        <div class="s_title category-title">
            <h2>Available Variants</h2>
        </div>
        <div class="variants-grid">
''' + '\n'.join(cards) + '''
        </div>
    </div>
</section>
'''

def modify_model_page(model, data):
    """Modify a single model series page."""
    filename = f'{model}.html'
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Modify title
    old_title_pattern = re.search(r'<title>.*?</title>', content)
    if old_title_pattern:
        old_title = old_title_pattern.group(0)
        new_title = f'<title>{data["title"]} - SAGMOTO</title>'
        content = content.replace(old_title, new_title, 1)
    
    # 2. Modify meta description
    old_desc_pattern = re.search(r'<meta content=".*?" name="description"/>', content)
    if old_desc_pattern:
        old_desc = old_desc_pattern.group(0)
        new_desc = f'<meta content="{data["desc"]}" name="description"/>'
        content = content.replace(old_desc, new_desc, 1)
    
    # 3. Modify meta keywords
    old_kw_pattern = re.search(r'<meta content=".*?" name="keywords"/>', content)
    if old_kw_pattern:
        old_kw = old_kw_pattern.group(0)
        new_kw = f'<meta content="{data["keywords"]}" name="keywords"/>'
        content = content.replace(old_kw, new_kw, 1)
    
    # 4. Modify h1 in page banner
    old_h1_pattern = re.search(r'<h1>.*?</h1>', content)
    if old_h1_pattern:
        old_h1 = old_h1_pattern.group(0)
        # Keep any subtitle if present (e.g., <h1>Title<br>Subtitle</h1> or <h1>Title <span>...</span></h1>)
        new_h1 = f'<h1>{data["title"]}</h1>'
        content = content.replace(old_h1, new_h1, 1)
    
    # 5. Modify product-detail-info h2
    # Find pattern like <h2>E3 Tractor</h2> in product-detail-info
    h2_pattern = re.search(r'<div class="product-detail-info">.*?</div>', content, re.DOTALL)
    if h2_pattern:
        info_section = h2_pattern.group(0)
        # Try to replace h2 inside this section
        new_info = re.sub(r'<h2>.*?</h2>', f'<h2>{data["title"]}</h2>', info_section, count=1)
        content = content.replace(info_section, new_info, 1)
    
    # 6. Modify breadcrumb model name (pattern: <span>Model Name</span> at end of breadcrumb)
    # Find the last <span> in breadcrumb that contains the model name
    bc_pattern = re.search(r'<div class="breadcrumb">.*?</div>', content, re.DOTALL)
    if bc_pattern:
        bc_section = bc_pattern.group(0)
        # Replace the last <span>text</span> that doesn't contain a link
        last_span_pattern = re.search(r'<span>([^<]+)</span>\s*</div>', bc_section)
        if last_span_pattern:
            old_span = last_span_pattern.group(0)
            new_span = f'<span>{data["title"]}</span>\n</div>'
            content = content.replace(bc_section, bc_section.replace(old_span, new_span), 1)
    
    # 7. Insert variants section after Technical Specifications and before Applications
    variants_html = generate_variants_html(data['variants'])
    
    # Find the insertion point: after <!-- ===== TECHNICAL SPECIFICATIONS ===== --> section
    # Look for pattern: </section> followed by <!-- ===== APPLICATIONS ===== -->
    insertion_pattern = re.search(r'(</section>\s*)(<!-- ===== APPLICATIONS ===== -->)', content)
    if insertion_pattern:
        content = content.replace(
            insertion_pattern.group(0),
            insertion_pattern.group(1) + variants_html + insertion_pattern.group(2),
            1
        )
    else:
        # Try alternative: find </section> before <!-- ===== CTA ===== --> or before footer
        alt_pattern = re.search(r'(</section>\s*)(<!-- ===== CTA ===== -->)', content)
        if alt_pattern:
            content = content.replace(
                alt_pattern.group(0),
                alt_pattern.group(1) + variants_html + alt_pattern.group(2),
                1
            )
    
    if content == original:
        print(f"  [WARN] {filename} - no changes made")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  [OK] {filename} - modified with {len(data['variants'])} variants")
    return True

if __name__ == '__main__':
    import sys
    
    print("Modifying model series pages to show all variants...")
    modified = 0
    for model, data in MODEL_VARIANTS.items():
        if modify_model_page(model, data):
            modified += 1
    
    print(f"\nDone! Modified {modified} pages.")
