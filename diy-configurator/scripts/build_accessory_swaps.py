#!/usr/bin/env python3
"""
Build accessory_swaps.json from accessories.json.
Parses swap patterns (A→B) with prices, separates from add-on items.
"""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, 'data')

def translate_config(text):
    """Simple Chinese→English for known config terms."""
    TERMS = {
        '加长平顶': 'Extended Flat Roof',
        '加长高顶': 'Extended High Roof',
        '中长平顶': 'Mid-length Flat Roof',
        '标准驾驶室': 'Standard Cab',
        '半高顶': 'Semi High Roof',
        '高顶': 'High Roof',
        '平顶': 'Flat Roof',
        '液压主座椅': 'Hydraulic Driver Seat',
        '空气主座椅': 'Air Driver Seat',
        '通风加热空气主座椅': 'Ventilated & Heated Air Driver Seat',
        '固定副座椅': 'Fixed Passenger Seat',
        '液压副座椅': 'Hydraulic Passenger Seat',
        '空气副座椅': 'Air Passenger Seat',
        '四点液压悬浮': '4-point Hydraulic Cab Suspension',
        '四点空气悬浮': '4-point Air Cab Suspension',
        '四点液压悬置': '4-point Hydraulic Cab Mount',
        '四点空气悬置': '4-point Air Cab Mount',
        '手动翻转': 'Manual Cab Tilt',
        '电动翻转装置': 'Electric Cab Tilt Device',
        '电动翻转': 'Electric Cab Tilt',
        '热区空调': 'Hot-region A/C',
        '电控自动恒温空调': 'Electronic Auto Climate Control',
        '普通暖风': 'Standard Heater',
        '单制冷空调': 'Cooling-only A/C',
        '手动摇窗机': 'Manual Window Crank',
        '电动摇窗机': 'Power Windows',
        '玻璃钢保险杠': 'FRP Bumper',
        '金属保险杠': 'Metal Bumper',
        '工程保险杠': 'Heavy-duty Bumper',
        '普通空滤器': 'Standard Air Filter',
        '中置空滤器': 'Center-mounted Air Filter',
        '油浴式空滤器': 'Oil-bath Air Filter',
        '双级空滤器': 'Dual-stage Air Filter',
        '沙漠式空滤器': 'Desert-type Air Filter',
        '分体式油浴': 'Split-type Oil-bath Filter',
        '普通排气': 'Standard Exhaust',
        '防火型消声器': 'Fireproof Muffler',
        '防火帽': 'Fire Cap',
        '普通50鞍座': 'Standard 50 Fifth Wheel',
        '普通90鞍座': 'Standard 90 Fifth Wheel',
        '轻量化90型鞍座': 'Lightweight 90 Fifth Wheel',
        '普通50型鞍座': 'Standard 50 Fifth Wheel',
        '普通90型鞍座': 'Standard 90 Fifth Wheel',
        '国产JSK37DV鞍座': 'Domestic JSK37DV Fifth Wheel',
        '国产铸造50鞍座': 'Domestic Cast 50 Fifth Wheel',
        '国产铸造90鞍座': 'Domestic Cast 90 Fifth Wheel',
        '加强型90鞍座': 'Heavy-duty 90 Fifth Wheel',
        '加强型90型鞍座': 'Heavy-duty 90 Fifth Wheel',
        '90型普通双摆鞍座': '90-type Dual-oscillation Fifth Wheel',
        '普通50型鞍座换装约斯特国产化加强50鞍座': 'JOST Domestic Heavy-duty 50 Fifth Wheel',
        '德龙X3000': 'Delong X3000',
        '德龙F3000': 'Delong F3000',
        '德龙H3000': 'Delong H3000',
        '德龙L3000': 'Delong L3000',
        '德龙M3000': 'Delong M3000',
        '德龙X5000': 'Delong X5000',
        '200L铁油箱': '200L Steel Fuel Tank',
        '300L铝合金油箱': '300L Aluminum Fuel Tank',
        '400L铝合金油箱': '400L Aluminum Fuel Tank',
        '500L铝合金油箱': '500L Aluminum Fuel Tank',
        '600L铝合金油箱': '600L Aluminum Fuel Tank',
        '700L铝合金油箱': '700L Aluminum Fuel Tank',
        '800L铝合金油箱': '800L Aluminum Fuel Tank',
        '380L铁': '380L Steel',
        '380L铁油箱': '380L Steel Fuel Tank',
        '400L不锈钢油箱': '400L Stainless Steel Fuel Tank',
        '230L铝合金油箱': '230L Aluminum Fuel Tank',
        '260L铝合金油箱': '260L Aluminum Fuel Tank',
        '200L铁': '200L Steel',
        '300铝合金油箱': '300L Aluminum Fuel Tank',
        '260铝合金油箱': '260L Aluminum Fuel Tank',
        '300L铝合金': '300L Aluminum',
        '400L铝合金': '400L Aluminum',
        '(400L+300L)铝合金油箱': '(400L+300L) Dual Aluminum Tanks',
        '进口转向机': 'Imported Steering Gear',
        '国产转向机': 'Domestic Steering Gear',
        '右置方向盘': 'RHD Steering',
        '前后少片簧': 'Parabolic Leaf Springs (F&R)',
        '前后多片簧': 'Multi-leaf Springs (F&R)',
        '两骑马螺栓': '2 U-bolts',
        '四骑马螺栓': '4 U-bolts',
        '复合式空气悬架': 'Composite Air Suspension',
        '全气囊空气悬架': 'Full Airbag Suspension',
        '顶导流罩': 'Roof Deflector',
        '顶侧导流罩': 'Roof & Side Deflectors',
        '中控锁': 'Central Locking',
        '加宽卧铺': 'Wide Sleeper Berth',
        '第三座椅': 'Third Seat',
        '第三级上车踏板': 'Third Step Board',
        '军用保护前围': 'Military Front Guard',
        '不锈钢前围': 'Stainless Steel Front Guard',
        '中间储物盒': 'Center Storage Box',
        '进口驻车空调': 'Imported Parking A/C',
        '国产驻车空调': 'Domestic Parking A/C',
        '普通粗滤': 'Standard Pre-filter',
        '长效粗滤器': 'Long-life Pre-filter',
        '世柏燃油粗滤器': 'SIBO Fuel Pre-filter',
        '燃油水寒宝': 'Fuel Water Separator Heater',
        '进回油口': 'Fuel Inlet/Return Ports',
        '胎压监测装置': 'TPMS',
        '临时鞍座': 'Temporary Fifth Wheel',
        '块状花纹': 'Block Pattern Tread',
        '矿用花纹': 'Mining Pattern Tread',
        '越野花纹': 'Off-road Pattern Tread',
        '横向花纹': 'Lateral Pattern Tread',
        '米其林': 'Michelin',
        '三角': 'Triangle',
        '双钱': 'Double Coin',
        '玲珑': 'Linglong',
        '中策': 'Zhongce',
        '金宇': 'Jinyu',
        '成山': 'Chengshan',
        '铝合金轮辋': 'Aluminum Alloy Wheel Rims',
        '珀然': 'Poman',
        '美铝': 'Alcoa',
        '大偏置': 'Large Offset',
        'ECAS': 'ECAS',
        'WABCO': 'WABCO',
        '康迪泰克': 'ContiTech',
        '两主片': '2 Main Leaves',
        '四主片': '4 Main Leaves',
        'N驾驶室': 'N-type Cab',
        'J驾驶室': 'J-type Cab',
        'M驾驶室': 'M-type Cab',
        'H驾驶室': 'H-type Cab',
        'G驾驶室': 'G-type Cab',
        '5驾驶室': 'Type 5 Cab',
        '4驾驶室': 'Type 4 Cab',
        '6驾驶室': 'Type 6 Cab',
        'D驾驶室': 'D-type Cab',
        '同规格驾驶室': 'Same-spec Cab',
        '保险杠状态变化': 'Bumper Material Change',
        '玻璃钢、金属保险杠互换': 'FRP ↔ Metal Bumper Swap',
        '金属保险杠、玻璃钢保险杠': 'Metal/FRP Bumper',
        '普通50鞍座换装约斯特国产化加强50鞍座(JSK39DV1-28)': 'JOST Domestic Heavy-duty 50 FW (JSK39DV1-28)',
        'F3000换装右置方向盘': 'F3000: RHD Steering',
        'X3000/X5000车型换装右置方向盘': 'X3000/X5000: RHD Steering',
        'H3000S车型换装右置方向盘': 'H3000S: RHD Steering',
        'H3000车型换装右置方向盘': 'H3000: RHD Steering',
        'L3000车型换装右置方向盘': 'L3000: RHD Steering',
        '偏置矿用自卸换装右置方向盘': 'Offset Mining Dump: RHD Steering',
    }

    result = text
    for cn, en in sorted(TERMS.items(), key=lambda x: -len(x[0])):
        result = result.replace(cn, en)
    return result

def detect_vehicle_source(base_config, category):
    """Detect what a vehicle currently has for a given swap category."""
    if not base_config:
        return None

    detectors = {
        '驾驶室': [
            (r'(加长平顶)', '加长平顶'),
            (r'(加长高顶)', '加长高顶'),
            (r'(中长平顶)', '中长平顶'),
            (r'(半高顶)', '半高顶'),
            (r'(高顶)', '高顶'),
            (r'(标准驾驶室)', '标准驾驶室'),
            (r'(平顶)', '平顶'),
        ],
        '空调': [
            (r'(热区空调)', '热区空调'),
            (r'(电控自动恒温空调)', '电控自动恒温空调'),
            (r'(普通暖风)', '普通暖风'),
        ],
        '驾驶室悬置': [
            (r'(四点液压悬浮)', '四点液压悬浮'),
            (r'(四点空气悬浮)', '四点空气悬浮'),
        ],
    }

    if category in detectors:
        for pattern, label in detectors[category]:
            if re.search(pattern, base_config):
                return label
    return None

# ── Load accessories ──
with open(os.path.join(DATA_DIR, 'accessories.json'), 'r', encoding='utf-8') as f:
    acc_data = json.load(f)

items = acc_data.get('items', [])

# ── Swap/Add-on patterns ──
SWAP_PATTERNS = [
    (r'^(.+?)换装(.+)$', 'swap'),
    (r'^(.+?)换(.+)$', 'swap'),
    (r'^(.+?)指定(.+)$', 'swap'),   # 轮胎品牌指定
]

ADD_PATTERNS = [
    r'^加装', r'^选装', r'^增加', r'^单选', r'^加一条',
    r'^中间储物盒', r'^取消', r'^燃油水寒宝', r'^双腔油箱$',
    r'^油箱高配换至低配不减价',
    r'^X3000/X5000加装', r'^加装胎压',
]

# Categories that are primarily swap-based
SWAP_CATEGORIES = {'驾驶室', '鞍座', '油箱', '空调', '转向机', '驾驶室悬置', '悬架系统'}

# ── Categorize each item ──
swap_items = []
addon_items = []

for item in items:
    desc = item.get('description', '')
    cat = item.get('category', '')
    is_addon = False

    for pat in ADD_PATTERNS:
        if re.match(pat, desc):
            is_addon = True
            break

    if not is_addon:
        found_swap = False
        for pat, stype in SWAP_PATTERNS:
            m = re.match(pat, desc)
            if m:
                item['_source'] = m.group(1).strip()
                item['_target'] = m.group(2).strip()
                item['_swap_type'] = stype
                swap_items.append(item)
                found_swap = True
                break
        if not found_swap:
            addon_items.append(item)
    else:
        addon_items.append(item)

print(f"Swap items: {len(swap_items)}")
print(f"Add-on items: {len(addon_items)}")

# ── Build swap lookup by category ──
swap_by_cat = {}
for item in swap_items:
    cat = item.get('category', 'Other')
    if cat not in swap_by_cat:
        swap_by_cat[cat] = []
    swap_by_cat[cat].append({
        'source': item['_source'],
        'target': item['_target'],
        'price': item.get('price', 0),
        'is_deduction': item.get('is_deduction', False),
        'note': item.get('note', ''),
        'source_en': translate_config(item['_source']),
        'target_en': translate_config(item['_target']),
        'description_cn': item.get('description', ''),
        'description_en': item.get('description_en', ''),
        'note_en': item.get('note_en', ''),
        'unit': item.get('unit', '辆'),
        'is_tire_set': item.get('is_tire_set', False),
        'tire_count': item.get('tire_count', {})
    })

# ── Detect vehicle source for each swap category ──
vehicle_sources = {}
for vf in os.listdir(DATA_DIR):
    if not vf.startswith('vehicles_') or not vf.endswith('.json'):
        continue
    with open(os.path.join(DATA_DIR, vf), 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    for v in vehicles:
        bc = v.get('base_config', '')
        if not bc:
            continue
        for cat in SWAP_CATEGORIES:
            src = detect_vehicle_source(bc, cat)
            if src:
                if cat not in vehicle_sources:
                    vehicle_sources[cat] = {}
                vehicle_sources[cat][src] = vehicle_sources[cat].get(src, 0) + 1

# ── Build output ──
output = {
    'swap_categories': {},
    'addon_items': [],
    'vehicle_sources': {cat: sorted(sources.items(), key=lambda x: -x[1])
                        for cat, sources in vehicle_sources.items()}
}

# Swap categories
for cat, items in sorted(swap_by_cat.items()):
    by_source = {}
    for item in items:
        src = item['source']
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(item)

    output['swap_categories'][cat] = {
        'label_cn': cat,
        'label_en': translate_config(cat) if translate_config(cat) != cat else '',
        'options': {}
    }

    for src, opts in sorted(by_source.items()):
        opts_sorted = sorted(opts, key=lambda x: x['price'])
        output['swap_categories'][cat]['options'][src] = opts_sorted

    # Generate reverse (downgrade) entries for each forward swap
    # If A→B costs +X, then B→A costs -X×0.8 (downgrade 80% rule)
    for src, opts in sorted(by_source.items()):
        for item in opts:
            target = item['target']
            if target not in output['swap_categories'][cat]['options']:
                output['swap_categories'][cat]['options'][target] = []
            # Check if reverse already exists (avoid duplicates)
            rev_exists = any(r['target'] == item['source'] for r in output['swap_categories'][cat]['options'][target])
            if not rev_exists:
                downgrade_base = round(item['price'] * 0.8)  # positive base, is_deduction=True will negate in frontend
                output['swap_categories'][cat]['options'][target].append({
                    'source': target,
                    'target': item['source'],
                    'price': downgrade_base,
                    'is_deduction': True,  # ★ 标记为扣减项，前端会取负
                    'note': item.get('note', ''),
                    'source_en': item['target_en'],
                    'target_en': item['source_en'],
                    'description_cn': f'{target}换装{item["source"]}',
                    'description_en': f'Swap {item["target_en"]} to {item["source_en"]}',
                    'note_en': item.get('note_en', ''),
                    'unit': '辆',
                    'is_tire_set': False,
                    'tire_count': {}
                })

    # Re-sort sources after adding reverse entries
    for src in output['swap_categories'][cat]['options']:
        output['swap_categories'][cat]['options'][src] = sorted(
            output['swap_categories'][cat]['options'][src], key=lambda x: x['price']
        )

# Add-on items
for item in addon_items:
    output['addon_items'].append({
        'category': item.get('category', 'Other'),
        'description': item.get('description', ''),
        'description_en': item.get('description_en', ''),
        'price': item.get('price', 0),
        'is_deduction': item.get('is_deduction', False),
        'note': item.get('note', ''),
        'note_en': item.get('note_en', ''),
        'unit': item.get('unit', '辆'),
        'is_tire_set': item.get('is_tire_set', False),
        'tire_count': item.get('tire_count', {})
    })

# Write output
with open(os.path.join(DATA_DIR, 'accessory_swaps.json'), 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Stats
total_sources = sum(len(v['options']) for v in output['swap_categories'].values())
print(f"\nSwap categories: {len(output['swap_categories'])}")
print(f"Total source groups: {total_sources}")
print(f"Add-on items: {len(output['addon_items'])}")
for cat in sorted(output['swap_categories'].keys()):
    sc = output['swap_categories'][cat]
    n = len(sc['options'])
    total_targets = sum(len(opts) for opts in sc['options'].values())
    print(f"  {cat}: {n} source groups → {total_targets} targets")
