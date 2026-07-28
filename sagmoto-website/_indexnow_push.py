"""Submit all 38 URLs to IndexNow"""
import json
import urllib.request

KEY = "a53caa61-08c9-4988-868e-c1561233ed50"
SITEMAP_URL = "https://sagmoto-trucks.com/sitemap.xml"

urls = [
    "https://sagmoto-trucks.com/index.html",
    "https://sagmoto-trucks.com/products.html",
    "https://sagmoto-trucks.com/about.html",
    "https://sagmoto-trucks.com/contact.html",
    "https://sagmoto-trucks.com/service.html",
    "https://sagmoto-trucks.com/x1s.html",
    "https://sagmoto-trucks.com/x3s.html",
    "https://sagmoto-trucks.com/e1st.html",
    "https://sagmoto-trucks.com/z3.html",
    "https://sagmoto-trucks.com/e3.html",
    "https://sagmoto-trucks.com/x6.html",
    "https://sagmoto-trucks.com/x7.html",
    "https://sagmoto-trucks.com/x9.html",
    "https://sagmoto-trucks.com/e9.html",
    "https://sagmoto-trucks.com/i9.html",
    "https://sagmoto-trucks.com/x5.html",
    "https://sagmoto-trucks.com/i5.html",
    "https://sagmoto-trucks.com/e6.html",
    "https://sagmoto-trucks.com/qyc.html",
    "https://sagmoto-trucks.com/zxc.html",
    "https://sagmoto-trucks.com/zhc.html",
    "https://sagmoto-trucks.com/special.html",
    "https://sagmoto-trucks.com/tzc.html",
    "https://sagmoto-trucks.com/new-energy.html",
    "https://sagmoto-trucks.com/news.html",
    "https://sagmoto-trucks.com/privacy.html",
    "https://sagmoto-trucks.com/terms.html",
    "https://sagmoto-trucks.com/video_list.html",
    "https://sagmoto-trucks.com/off-road-4x4.html",
    "https://sagmoto-trucks.com/pzkyzyc.html",
    "https://sagmoto-trucks.com/pzmtc.html",
    "https://sagmoto-trucks.com/news_Detail/18.html",
    "https://sagmoto-trucks.com/news_Detail/19.html",
    "https://sagmoto-trucks.com/news_Detail/20.html",
    "https://sagmoto-trucks.com/news_Detail/21.html",
    "https://sagmoto-trucks.com/news_Detail/22.html",
    "https://sagmoto-trucks.com/news_list/1.html",
    "https://sagmoto-trucks.com/news_list/81163.html",
]

# Submit URL list to IndexNow
payload = json.dumps({
    "host": "sagmoto-trucks.com",
    "key": KEY,
    "keyLocation": f"https://sagmoto-trucks.com/{KEY}.txt",
    "urlList": urls
}).encode()

req = urllib.request.Request(
    "https://api.indexnow.org/IndexNow",
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

try:
    resp = urllib.request.urlopen(req)
    print(f"IndexNow URL list: {resp.status} {resp.read().decode()}")
except Exception as e:
    print(f"IndexNow URL list error: {e}")

# Also notify Bing
payload2 = json.dumps({
    "host": "sagmoto-trucks.com",
    "key": KEY,
    "keyLocation": f"https://sagmoto-trucks.com/{KEY}.txt",
    "url": SITEMAP_URL
}).encode()

req2 = urllib.request.Request(
    "https://www.bing.com/indexnow",
    data=payload2,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

try:
    resp2 = urllib.request.urlopen(req2)
    print(f"Bing IndexNow: {resp2.status} {resp2.read().decode()}")
except Exception as e:
    print(f"Bing IndexNow error: {e}")

print(f"\nDone! Submitted {len(urls)} URLs to IndexNow")
