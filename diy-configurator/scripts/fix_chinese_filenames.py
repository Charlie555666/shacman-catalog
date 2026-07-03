"""
Fix Chinese filenames to ASCII slugs for GitHub Pages compatibility.
Problem: GitHub Pages CDN returns 404 for files with Chinese names.
Solution: Rename vehicles_<Chinese>.json → vehicles_<slug>.json,
          add 'file' field to countries.json, update all references.
"""
import json
import os
import shutil
from urllib.parse import quote, unquote

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
HTML_FILE = os.path.join(os.path.dirname(__file__), '..', 'index.html')

# Name-to-English-slug mapping
SLUG_MAP = {
    'N': 'zone-n',
    'S': 'zone-s',
    '东南非六国': 'east-south-africa-6',
    '中亚三国': 'central-asia',
    '乌兹别克': 'uzbekistan',
    '乌拉圭': 'uruguay',
    '亚美尼亚': 'armenia',
    '伊拉克': 'iraq',
    '几内亚': 'guinea',
    '刚果金': 'drc',
    '利比亚': 'libya',
    '加纳': 'ghana',
    '卡塔尔': 'qatar',
    '卢旺达': 'rwanda',
    '印度尼西亚': 'indonesia',
    '厄瓜多尔': 'ecuador',
    '吉布提': 'djibouti',
    '哈萨克': 'kazakhstan',
    '哥伦比亚': 'colombia',
    '喀麦隆': 'cameroon',
    '埃及': 'egypt',
    '墨西哥': 'mexico',
    '多米尼加': 'dominican-republic',
    '安哥拉': 'angola',
    '尼日利亚': 'nigeria',
    '巴基斯坦': 'pakistan',
    '巴布亚新几内亚': 'papua-new-guinea',
    '巴拉圭': 'paraguay',
    '摩洛哥': 'morocco',
    '斐济': 'fiji',
    '新加坡': 'singapore',
    '智利': 'chile',
    '柬埔寨': 'cambodia',
    '格鲁吉亚': 'georgia',
    '毛里塔尼亚': 'mauritania',
    '沙特': 'saudi-arabia',
    '泰国': 'thailand',
    '牙买加': 'jamaica',
    '科威特': 'kuwait',
    '秘鲁': 'peru',
    '突尼斯': 'tunisia',
    '缅甸': 'myanmar',
    '老挝': 'laos',
    '肯尼亚': 'kenya',
    '苏丹': 'sudan',
    '苏里南': 'suriname',
    '菲律宾': 'philippines',
    '蒙古': 'mongolia',
    '西非五国': 'west-africa-5',
    '越南': 'vietnam',
    '阿尔及利亚': 'algeria',
    '阿曼': 'oman',
    '阿根廷': 'argentina',
    '阿联酋': 'uae',
    '香港': 'hong-kong',
    '马来西亚': 'malaysia',
    '马达加斯加': 'madagascar',
}

def main():
    os.chdir(DATA_DIR)
    
    # Step 1: Rename all vehicles_*.json files
    print("=== Step 1: Renaming vehicle data files ===")
    renamed = 0
    for cn_name, slug in SLUG_MAP.items():
        old_name = f'vehicles_{cn_name}.json'
        new_name = f'vehicles_{slug}.json'
        
        # Check both URL-encoded and direct Chinese paths
        old_encoded = f'vehicles_{quote(cn_name)}.json'
        
        if os.path.exists(old_name):
            if os.path.exists(new_name):
                os.remove(new_name)
            shutil.copy2(old_name, new_name)
            os.remove(old_name)
            print(f'  ✅ {cn_name} → {slug} (direct)')
            renamed += 1
        elif os.path.exists(old_encoded):
            if os.path.exists(new_name):
                os.remove(new_name)
            shutil.copy2(old_encoded, new_name)
            os.remove(old_encoded)
            print(f'  ✅ {cn_name} → {slug} (encoded: {old_encoded})')
            renamed += 1
        else:
            print(f'  ❌ {cn_name}: file not found (tried {old_name}, {old_encoded})')
    
    print(f'\nRenamed {renamed} files.')
    
    # Step 2: Update countries.json with 'file' field
    print("\n=== Step 2: Updating countries.json ===")
    countries_path = os.path.join(DATA_DIR, 'countries.json')
    with open(countries_path, 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    for c in countries:
        name = c['name']
        if name in SLUG_MAP:
            c['file'] = f'vehicles_{SLUG_MAP[name]}.json'
        else:
            print(f'  WARNING: {name} has no slug mapping!')
    
    with open(countries_path, 'w', encoding='utf-8') as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)
    
    print(f'Updated {len(countries)} country entries with file field.')
    
    # Step 3: Update index.html to use file field instead of encodeURIComponent
    print("\n=== Step 3: Updating index.html ===")
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Old code:
    # const safeName = encodeURIComponent(name);
    # STATE.countryData = await fetchJSON(DATA_BASE + 'vehicles_' + safeName + '.json');
    
    old_load_code = """const safeName = encodeURIComponent(name);
  try {
    STATE.countryData = await fetchJSON(DATA_BASE + 'vehicles_' + safeName + '.json');"""
    
    new_load_code = """// Use country's file field (ASCII slug) for reliable GitHub Pages serving
  const countryInfo = STATE.countries.find(c => c.name === name);
  const fileName = countryInfo ? countryInfo.file : 'vehicles_' + encodeURIComponent(name) + '.json';
  try {
    STATE.countryData = await fetchJSON(DATA_BASE + fileName);"""
    
    if old_load_code in html:
        html = html.replace(old_load_code, new_load_code)
        print('  ✅ Updated selectCountry() loading code')
    else:
        print('  ⚠️ Old loading code not found, searching for pattern...')
        # Try with different whitespace
        if 'safeName = encodeURIComponent(name)' in html:
            print('  Found encodeURIComponent call, will do manual edit')
            # Find the exact lines and replace
            import re
            html = html.replace(
                'const safeName = encodeURIComponent(name);',
                'const countryInfo = STATE.countries.find(c => c.name === name);\n  const fileName = countryInfo ? countryInfo.file : \'vehicles_\' + encodeURIComponent(name) + \'.json\';'
            )
            html = html.replace(
                "STATE.countryData = await fetchJSON(DATA_BASE + 'vehicles_' + safeName + '.json');",
