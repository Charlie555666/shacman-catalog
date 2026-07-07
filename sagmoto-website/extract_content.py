import re, sys, os

pages = ['qyc.html', 'zxc.html', 'zhc.html', 'special.html', 'pzkyzyc.html',
         'pzmtc.html', 'tzc.html', 'service.html', 'video_list.html']

for page in pages:
    if not os.path.exists(page):
        print(f"\n=== {page} NOT FOUND ===")
        continue
    with open(page, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"\n{'='*60}")
    print(f"=== {page} ({len(html)} bytes) ===")
    print(f"{'='*60}")

    # Title
    title = re.findall(r'<title>(.*?)</title>', html)
    print(f"TITLE: {title}")

    # Meta description
    desc = re.findall(r'name=["\']description["\'].*?content=["\'](.*?)["\']', html, re.I)
    print(f"DESC: {desc}")

    # Meta keywords
    kw = re.findall(r'name=["\']keywords["\'].*?content=["\'](.*?)["\']', html, re.I)
    print(f"KEYWORDS: {kw}")

    # Extract all image URLs
    imgs = re.findall(r'src=["\'](https?://[^"\']+\.(?:png|jpg|jpeg|gif|webp))["\']', html, re.I)
    unique_imgs = list(dict.fromkeys(imgs))[:20]
    print(f"IMAGES ({len(unique_imgs)} shown):")
    for img in unique_imgs:
        print(f"  {img}")

    # Extract text content
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.S)
    texts = re.findall(r'>([^<]+)<', clean)
    texts = [t.strip() for t in texts if t.strip() and len(t.strip()) > 2]
    texts = [t for t in texts if not t.startswith('{') and not t.startswith('var ')
             and 'function' not in t and not t.startswith('//') and not t.startswith('SAF')
             and 'require' not in t and 'jquery' not in t.lower()]
    print(f"TEXT CONTENT ({len(texts)} items):")
    for t in texts[:60]:
        print(f"  {t}")
