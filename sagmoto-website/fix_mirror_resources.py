#!/usr/bin/env python3
"""
FIX MIRROR RESOURCES v2 — Remove base tag, download CSS/JS locally, rewrite paths.
Handles: query params in URLs, combined CSS/JS URLs, Windows filename restrictions.
"""
import re, os, sys, urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

BASE_DIR = Path(__file__).parent
MIRROR_DIR = BASE_DIR / "mirror"
SOURCE_DOMAIN = "http://www.sagmoto.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36"

# All mirror pages to fix
PAGES = [
    "qyc.html", "zxc.html", "zhc.html", "special.html", "tzc.html",
    "pzkyzyc.html", "pzmtc.html", "service.html", "video_list.html",
    "about.html",
    "service_list/1674411714944516096.html",
    "service_list/1674411730417303552.html",
    "service_list/1674411748220751872.html",
    "service_list/1674411767427842048.html",
    "news_list/81163.html",
    "news_list/1.html",
]

def strip_query(url):
    """Remove query string from URL for local file storage."""
    parsed = urlparse(url)
    return urlunparse(parsed._replace(query=""))

def download_url(url, out_path):
    """Download a URL to a local file."""
    out_file = MIRROR_DIR / out_path.lstrip("/")
    if out_file.exists():
        print(f"  (cached) {url}")
        return True
    out_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            out_file.write_bytes(data)
            print(f"  OK: {url} → {out_path} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"  FAIL: {url} — {e}")
        return False

def download_and_combine(urls, out_path):
    """Download multiple URLs and concatenate them into one file."""
    out_file = MIRROR_DIR / out_path.lstrip("/")
    if out_file.exists():
        print(f"  (cached combined) {out_path}")
        return True
    out_file.parent.mkdir(parents=True, exist_ok=True)
    combined = b""
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as resp:
                combined += resp.read()
                combined += b"\n"
        except Exception as e:
            print(f"  FAIL (part): {url} — {e}")
    if combined:
        out_file.write_bytes(combined)
        print(f"  OK combined: {len(urls)} files → {out_path} ({len(combined)} bytes)")
        return True
    return False

def download_all_resources():
    """Download all common and page-specific CSS/JS resources."""
    print("=" * 60)
    print("DOWNLOADING RESOURCES")
    print("=" * 60)
    
    base = SOURCE_DOMAIN
    
    # 1. Common CSS files (individual)
    print("\n--- Common CSS ---")
    download_url(f"{base}/npublic/libs/css/ceccbootstrap.min.css", "npublic/libs/css/ceccbootstrap.min.css")
    download_url(f"{base}/npublic/libs/css/global.css", "npublic/libs/css/global.css")
    download_url(f"{base}/css/site.css", "css/site.css")
    
    # Combined CSS (ceccbootstrap + global as one file to match the HTML href)
    print("\n--- Combined CSS ---")
    download_and_combine(
        [f"{base}/npublic/libs/css/ceccbootstrap.min.css", f"{base}/npublic/libs/css/global.css"],
        "npublic/libs/css/ceccbootstrap.min.css,global.css"
    )
    download_and_combine(
        [f"{base}/npublic/libs/css/ceccbootstrap.min.css", f"{base}/npublic/libs/css/global.css"],
        "npublic/libs/css/ceccbootstrap.min.css,global.css"
    )
    
    # 2. Common JS files (individual)
    print("\n--- Common JS ---")
    download_url(f"{base}/npublic/libs/core/ceccjquery.min.js", "npublic/libs/core/ceccjquery.min.js")
    download_url(f"{base}/npublic/libs/core/require.min.js", "npublic/libs/core/require.min.js")
    download_url(f"{base}/npublic/libs/core/lib.min.js", "npublic/libs/core/lib.min.js")
    download_url(f"{base}/npublic/libs/core/page.min.js", "npublic/libs/core/page.min.js")
    download_url(f"{base}/npublic/commonjs/common.min.js", "npublic/commonjs/common.min.js")
    
    # Combined JS (ceccjquery + require + lib + page)
    print("\n--- Combined JS ---")
    download_and_combine(
        [f"{base}/npublic/libs/core/ceccjquery.min.js",
         f"{base}/npublic/libs/core/require.min.js",
         f"{base}/npublic/libs/core/lib.min.js",
         f"{base}/npublic/libs/core/page.min.js"],
        "npublic/libs/core/ceccjquery.min.js,require.min.js,lib.min.js,page.min.js"
    )
    
    # 3. Page-specific CSS files
    print("\n--- Page-specific CSS ---")
    page_css = {
        "qyc": "qyc_e6047607e228939828a96213f4db2170.min.css",
        "zxc": "zxc_ae74f2d8fbf754f07077c47db87cf16f.min.css",
        "zhc": "zhc_8996a25cb69afbdca28ce6db8cbece62.min.css",
        "special": "special_08ac5b2d30d14f8af9819daf62b2ef8a.min.css",
        "tzc": "tzc_74a0a70e6776531ef2020849dffabc0c.min.css",
        "pzkyzyc": "pzkyzyc_183d232c2f47f2f54f193088ba16b23a.min.css",
        "pzmtc": "pzmtc_31beba3f9fbf9055b7b68dc3d1814a1d.min.css",
        "about": "about_95afd55df18c607efb6df5ae58e9a9f3.min.css",
        "service": "service_ca2723a0aaf92a71c9020a7392725214.min.css",
        "video_list": "video_list_fe49061df8ead2ed833b3acd0c265b9c.min.css",
        "service_list": "service_list_987dfa4eb05ff03ebb6df1e737bf84f4.min.css",
        "news_list": "news_list_d80547c763508d4d908e2ed45148bad2.min.css",
    }
    for name, file in page_css.items():
        url = f"{base}/css/{file}"
        download_url(url, f"css/{file}")
    
    # 4. Upload CSS/JS files
    print("\n--- Upload resources ---")
    upload_files = [
        "css/23c692dbe91e45d1b512ac8b31d08e49.css",
        "css/25560ae2e11a445392da2de68e0cbc00.css",
        "js/3f6e9653db5343719ee71a81b92221b0.js",
        "js/c69a65b94b9d48fe90291c18e82934b0.js",
        "js/f443dc4c19004859b92c4f7a94153c20.js",
    ]
    for f in upload_files:
        download_url(f"{base}/upload/{f}", f"upload/{f}")

def fix_page_paths(html):
    """Rewrite paths in HTML to use local mirror/."""
    
    # Remove <base> tag
    html = re.sub(r'<base\s+[^>]*>', '', html)
    
    # Fix protocol-relative CDN URLs to HTTPS (safe, won't double-replace)
    html = re.sub(
        r'(?<=["\'=\s])(//(?:omo-oss-image\d*\.thefastimg\.com|dcloud-static01\.faststatics\.com))',
        r'https:\1',
        html
    )
    
    # Fix root-relative paths in [href/src/data-*]="..." to "mirror/..."
    # But skip: http://, https://, //, data:, #, javascript:, mailto:, tel:
    def replace_path(m):
        attr = m.group(1)
        path = m.group(2)
        # Strip query params from HTML reference too
        base_path = path.split("?")[0]
        return f'{attr}="mirror/{base_path}"'
    
    html = re.sub(
        r'(href|src|data-original|lazy-src|data-lazy)\s*=\s*"/((?!(?:https?:|//|data:|#|javascript:|mailto:|tel:))[^"]*)"',
        replace_path,
        html
    )
    
    # Fix Contact.html → contact.html
    html = html.replace('href="Contact.html"', 'href="contact.html"')
    
    # Fix favicon
    html = html.replace('href="/favicon.ico"', 'href="mirror/favicon.ico"')
    
    # Safety: recursively fix any https:https:... patterns (belt-and-suspenders)
    while 'https:https:' in html:
        html = html.replace('https:https:', 'https:')
    
    return html

def fix_all_pages():
    """Fix all mirror pages."""
    print("\n" + "=" * 60)
    print("FIXING PAGES")
    print("=" * 60)
    
    for page in PAGES:
        html_file = BASE_DIR / page
        if not html_file.exists():
            print(f"  SKIP: {page} (not found)")
            continue
        
        html = html_file.read_text(encoding="utf-8")
        new_html = fix_page_paths(html)
        html_file.write_text(new_html, encoding="utf-8")
        
        base_removed = '<base' not in new_html
        has_mirror = 'mirror/' in new_html
        print(f"  OK: {page} ({len(html)}→{len(new_html)}B, base={'REMOVED' if base_removed else 'STILL THERE!'}, mirror={'YES' if has_mirror else 'NO'})")

def verify():
    """Verify the fix."""
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    
    sample = BASE_DIR / "qyc.html"
    if sample.exists():
        content = sample.read_text(encoding="utf-8")
        has_base = '<base' in content
        mirror_count = content.count('mirror/')
        http_count = content.count('http://www.sagmoto.com')
        print(f"  qyc.html: base={'YES (BAD!)' if has_base else 'NO (GOOD)'}, mirror/ refs={mirror_count}, http://sagmoto={http_count}")
        
        # Check for remaining root-relative paths
        root_rels = re.findall(r'(?:href|src)="/(?!(?:https?:|//|mirror/))([^"]*)"', content)
        if root_rels:
            print(f"  WARNING: {len(root_rels)} remaining root-relative paths:")
            for r in root_rels[:10]:
                print(f"    /{r}")
        else:
            print("  All root-relative paths converted!")

def main():
    download_all_resources()
    fix_all_pages()
    verify()
    
    print("\n" + "=" * 60)
    print("DONE: Base tags removed, all resources localized to mirror/")
    print("Ready to commit and push to GitHub Pages")
    print("=" * 60)

if __name__ == "__main__":
    main()
