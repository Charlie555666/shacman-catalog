import requests
import os
import re
import time

output_dir = r"c:/Users/Administrator/WorkBuddy/20260605101515/shacman-catalog/sagmoto-website/images/sagmoto-original"
os.makedirs(output_dir, exist_ok=True)

# Read URLs from file
url_file = r"c:/Users/Administrator/WorkBuddy/20260605101515/sagmoto_all_images.txt"
with open(url_file, 'r', encoding='utf-8') as f:
    raw_urls = f.readlines()

# Clean URLs
urls = []
for u in raw_urls:
    u = u.strip()
    u = u.replace('&quot;', '')
    u = u.replace('"); width: 1903px;', '')
    if not u:
        continue
    urls.append(u)

# Deduplicate
urls = list(set(urls))

print(f"Found {len(urls)} unique image URLs to download")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Referer': 'http://www.sagmoto.com/',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

success = 0
failed = 0
for i, url in enumerate(urls):
    try:
        # Extract filename from URL
        parts = url.split('/')
        filename = parts[-1].split('?')[0]
        # Remove _1920xaf.jpg suffix for hero images (get full size)
        if '_1920xaf' in filename:
            filename = filename.replace('_1920xaf', '')
        if '_560xaf' in filename:
            filename = filename.replace('_560xaf', '')
        filepath = os.path.join(output_dir, filename)
        
        if os.path.exists(filepath):
            print(f"[{i+1}/{len(urls)}] Already exists: {filename}")
            success += 1
            continue
            
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"[{i+1}/{len(urls)}] OK {r.status_code}: {filename} ({len(r.content)} bytes)")
            success += 1
        else:
            print(f"[{i+1}/{len(urls)}] FAIL {r.status_code}: {url}")
            failed += 1
    except Exception as e:
        print(f"[{i+1}/{len(urls)}] ERROR: {url} - {e}")
        failed += 1
    time.sleep(0.2)

print(f"\nDone! Success: {success}, Failed: {failed}")
print(f"Images saved to: {output_dir}")
