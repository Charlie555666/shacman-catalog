#!/usr/bin/env python3
"""
Rename vehicle data files from Chinese names to ASCII slugs.
Required because GitHub Pages CDN can't serve files with Chinese filenames.
"""
import json, os, shutil
from urllib.parse import quote

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

SLUG_MAP = {
    'N': 'zone-n', 'S': 'zone-s',
    '东南非六国': 'east-south-africa-6', '中亚三国': 'central-asia',
    '乌兹别克': 'uzbekistan', '乌拉圭': 'uruguay', '亚美尼亚': 'armenia',
    '伊拉克': 'iraq', '几内亚': 'guinea', '刚果金': 'drc', '利比亚': 'libya',
    '加纳': 'ghana', '卡塔尔': 'qatar', '卢旺达': 'rwanda',
    '印度尼西亚': 'indonesia', '厄瓜多尔': 'ecuador', '吉布提': 'djibouti',
    '哈萨克': 'kazakhstan', '哥伦比亚': 'colombia', '喀麦隆': 'cameroon',
    '埃及': 'egypt', '墨西哥': 'mexico', '多米尼加': 'dominican-republic',
    '安哥拉': 'angola', '尼日利亚': 'nigeria', '巴基斯坦': 'pakistan',
    '巴布亚新几内亚': 'papua-new-guinea', '巴拉圭': 'paraguay',
    '摩洛哥': 'morocco', '斐济': 'fiji', '新加坡': 'singapore',
    '智利': 'chile', '柬埔寨': 'cambodia', '格鲁吉亚': 'georgia',
    '毛里塔尼亚': 'mauritania', '沙特': 'saudi-arabia', '泰国': 'thailand',
    '牙买加': 'jamaica', '科威特': 'kuwait', '秘鲁': 'peru',
    '突尼斯': 'tunisia', '缅甸': 'myanmar', '老挝': 'laos', '肯尼亚': 'kenya',
    '苏丹': 'sudan', '苏里南': 'suriname', '菲律宾': 'philippines',
    '蒙古': 'mongolia', '西非五国': 'west-africa-5', '越南': 'vietnam',
    '阿尔及利亚': 'algeria', '阿曼': 'oman', '阿根廷': 'argentina',
    '阿联酋': 'uae', '香港': 'hong-kong', '马来西亚': 'malaysia',
    '马达加斯加': 'madagascar',
}

os.chdir(DATA_DIR)

# Step 1: Rename vehicle data files
print("=== Step 1: Renaming files ===")
renamed = 0
for cn_name, slug in SLUG_MAP.items():
    old_direct = f'vehicles_{cn_name}.json'
    old_encoded = f'vehicles_{quote(cn_name)}.json'
    new_name = f'vehicles_{slug}.json'

    found = None
    if os.path.exists(old_direct):
        found = old_direct
    elif os.path.exists(old_encoded):
        found = old_encoded

    if found:
        if os.path.exists(new_name):
            os.remove(new_name)
        shutil.copy2(found, new_name)
        os.remove(found)
        print(f'  {cn_name} -> {slug}')
        renamed += 1
    else:
        print(f'  MISSING: {cn_name} (tried {old_direct}, {old_encoded})')

print(f'Renamed: {renamed}/{len(SLUG_MAP)}')

# Step 2: Update countries.json
print("\n=== Step 2: Updating countries.json ===")
with open('countries.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)

for c in countries:
    name = c['name']
    if name in SLUG_MAP:
        c['file'] = f'vehicles_{SLUG_MAP[name]}.json'

with open('countries.json', 'w', encoding='utf-8') as f:
    json.dump(countries, f, ensure_ascii=False, indent=2)

print(f'Updated {len(countries)} countries with file field')

# Step 3: Verify
print("\n=== Step 3: Verification ===")
slug_files = [f for f in os.listdir('.') if f.startswith('vehicles_') and f.endswith('.json')]
cn_files = [f for f in os.listdir('.') if any('\u4e00' <= c <= '\u9fff' for c in f)]
print(f'Slug-based files: {len(slug_files)}')
print(f'Chinese-named files remaining: {len(cn_files)}')
if cn_files:
    print(f'  WARNING - Chinese-named files still exist: {cn_files}')
else:
    print('  All Chinese-named files cleaned up!')

# Quick validation
for c in countries:
    fname = c.get('file', '')
    if fname and not os.path.exists(fname):
        print(f'  ERROR: {c["name"]} file {fname} missing!')

print('\nDone!')
