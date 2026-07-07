import os
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = "http://www.sagmoto.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

OUTPUT_DIR = Path("C:/Users/Administrator/WorkBuddy/20260605101515/shacman-catalog/sagmoto-website")
MIRROR_DIR = OUTPUT_DIR / "mirror"

PAGES = {
    "qyc": "qyc.html",
    "zxc": "zxc.html",
    "zhc": "zhc.html",
    "special": "special.html",
    "pzkyzyc": "pzkyzyc.html",
    "pzmtc": "pzmtc.html",
    "service": "service.html",
    "tzc": "tzc.html",
    "service_1674411714944516096": "service_list/1674411714944516096.html",
    "service_1674411730417303552": "service_list/1674411730417303552.html",
    "service_1674411748220751872": "service_list/1674411748220751872.html",
    "service_1674411767427842048": "service_list/1674411767427842048.html",
    "news_list_1": "news_list/1.html",
    "news_list_81163": "news_list/81163.html",
    "video_list": "video_list.html",
}

PAGE_LINK_MAP = {
    '/': 'index.html',
    '/index.html': 'index.html',
    '/qyc.html': 'qyc.html',
    '/zxc.html': 'zxc.html',
    '/zhc.html': 'zhc.html',
    '/special.html': 'special.html',
    '/pzkyzyc.html': 'pzkyzyc.html',
    '/pzmtc.html': 'pzmtc.html',
    '/service.html': 'service.html',
    '/tzc.html': 'tzc.html',
    '/video_list.html': 'video_list.html',
    '/news_list/1.html': 'news_list/1.html',
    '/news_list/81163.html': 'news_list/81163.html',
    '/news_list/video_list.html': 'video_list.html',
    '/about.html': 'about.html',
    '/contact.html': 'contact.html',
    '/products.html': 'products.html',
    '/news.html': 'news.html',
}

downloaded_count = 0
failed_count = 0


def download_resource(rel_path):
    """Download a resource from sagmoto.com to mirror/. Strip query params for filename."""
    global downloaded_count, failed_count

    if rel_path == '/' or not rel_path or rel_path.startswith('#'):
        return False

    # Strip query params and anchor for filename
    clean_path = rel_path.split('?')[0].split('#')[0]
    if not clean_path or clean_path == '/':
        return False

    url = f"{BASE_URL}{rel_path}"
    local_path = MIRROR_DIR / clean_path.lstrip('/')
    local_path.parent.mkdir(parents=True, exist_ok=True)

    if local_path.exists() and local_path.stat().st_size > 0:
        return True

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Referer": "http://www.sagmoto.com/",
            "Accept": "*/*"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            if len(content) > 0:
                local_path.write_bytes(content)
                downloaded_count += 1
                print(f"    Downloaded: {clean_path} ({len(content)} bytes)")
                return True
            else:
                failed_count += 1
                print(f"    Empty: {rel_path}")
                return False
    except Exception as e:
        failed_count += 1
        print(f"    Failed: {rel_path} ({e})")
        return False


def process_page(filename):
    page_path = OUTPUT_DIR / filename
    if not page_path.exists():
        print(f"Skip: {filename} not found")
        return

    print(f"Processing: {filename}")

    if '/' in filename:
        depth_prefix = '../'
    else:
        depth_prefix = ''

    html = page_path.read_text(encoding='utf-8')

    # 1. Remove base tag
    html = re.sub(r'<base[^>]*>\s*', '', html, flags=re.IGNORECASE)

    # 2. Fix resource paths (href/src/lazy) - process from END to START
    resource_pattern = re.compile(r'(href|src|lazy)="(/[^"]*)"')
    matches = list(resource_pattern.finditer(html))

    for match in reversed(matches):
        attr = match.group(1)
        path = match.group(2)

        if path.startswith('//'):
            continue
        if path == '/' or not path or path.startswith('#'):
            continue

        clean_path = path.split('?')[0].split('#')[0]
        if not clean_path or clean_path == '/':
            continue

        # Skip page links
        if clean_path.endswith('.html') or '/Detail/' in clean_path or '/prolist/' in clean_path or '/news/' in clean_path:
            continue

        # Download
        download_resource(path)

        # Replace with local path (strip query params)
        local_path = f"{depth_prefix}mirror{clean_path}"
        html = html[:match.start(2)] + local_path + html[match.end(2):]

    # 3. Fix page links (a href) - process from END to START
    page_link_pattern = re.compile(r'href="(/[^"]*)"')
    matches = list(page_link_pattern.finditer(html))

    for match in reversed(matches):
        path = match.group(1)

        if path.startswith('//'):
            continue

        # Check direct mapping
        if path in PAGE_LINK_MAP:
            new_path = f"{depth_prefix}{PAGE_LINK_MAP[path]}"
        elif path.startswith('/service_list/'):
            rest = path.replace('/service_list/', '')
            new_path = f"{depth_prefix}service_list/{rest}"
        elif path.startswith('/news_list/'):
            rest = path.replace('/news_list/', '')
            new_path = f"{depth_prefix}news_list/{rest}"
        elif path.startswith('/news_Detail/'):
            rest = path.replace('/news_Detail/', '')
            new_path = f"{depth_prefix}news_Detail/{rest}"
        elif path.startswith('/video_list/'):
            rest = path.replace('/video_list/', '')
            new_path = f"{depth_prefix}video_list/{rest}"
        elif path == '/':
            new_path = f"{depth_prefix}index.html"
        else:
            continue

        html = html[:match.start(1)] + new_path + html[match.end(1)]

    # 4. Fix misc
    html = html.replace('Contact.html', 'contact.html')
    html = html.replace('"//omo-oss-image', '"https://omo-oss-image')
    html = html.replace('"//dcloud-static01', '"https://dcloud-static01')

    page_path.write_text(html, encoding='utf-8')
    print(f"  Updated: {filename}")


# Process all pages
for key, filename in PAGES.items():
    process_page(filename)

print(f"\nDone! Downloaded: {downloaded_count}, Failed: {failed_count}")
