"""Fix the 8 vehicles with missing prices in DIY Configurator data.
Uses direct price extraction from quotation files and similar-model estimation."""

import json, os, glob
from urllib.parse import unquote

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Manually verified prices from direct file inspection
DIRECT_PRICES = {
    # 乌兹别克 - L3000 cargo trucks
    'SX12588K434': 23.385,   # WP7.240E51, found in col[20] of 载货车-2款 sheet
    'SX12588L564': 24.215,   # WP7.270E51, found in col[20] of 载货车-2款 sheet
    
    # S1/CIS - X5000 dumpers  
    'SX32585V384': 36.059,   # WP12.430E50, found in col[20] of 自卸车-23款 sheet
    'SX325853384': 40.459,   # WP13.550E501, found in col[20] of 自卸车-23款 sheet
}

# Estimated prices from similar models in the same region
# 1. SX3315DT386 - similar to SX3315DT386R (30.286万, 非洲二区), but中亚三国 F3000 8x4 dumper
#    Similar models in中亚三国 area: SX3315DT366 at 30.88万 (陕汽报价)
#    SX3315DT386 has WP10.380E32 vs SX3315DT366 which also has WP10.380E32 or similar
#    SX3315DT386R is 30.286万, SX3315DT386CR is 32.511万
#    SX3315DT386 is similar to DT386R but without the R suffix (different variant)
#    Use SX3315DT386R price as reference: 30.286 - small adjustment ≈ 29.8
#    Actually, for中亚三国 market: F3000 8x4 dumper 加强版 with WP10.380E32
#    Let's use 29.8 as estimate (slightly lower than 非洲 because中亚三国 is a lower-price market)

# 2. SX4255NV324 - F3000 6x4 tractor with WP12.420E32, 中亚三国
#    Similar: SX4255DV324 at 28.897万, SX4255JV324 at 30.76万, SX4255DT384 at 28.536万
#    NV in model code suggests a unique variant. With WP12.420E32 + F3000加强版
#    Use average of similar: ~29.5

# 3. SX41884M501TL - X5000 LNG 4x2 tractor for Vietnam, OFFICIALLY NO PRICE
#    Similar LNG/X5000 tractors: SX4188GV381C at 31.435万 (中东), SX4188GS361C at 31.4万 (中南美)
#    But LNG is different. Vietnam market has different pricing.
#    Other Vietnam 4x2 tractors: SX41884T361 at 28.413万, SX41884T361C at 28.654万 (亚太区)
#    Use 31.0 as estimate (LNG typically costs more, but Vietnam lower market)
#    Actually - this vehicle says "配置不全，无基础车型" - it's a proposal, not a real product yet
#    Use 30.5 as a reasonable estimate

# 4. SX3258MR354 - H3000S 6x4 dumper for Vietnam, WP8.340E51
#    Vietnam self-unloading similar: SX3258MT384C at 29.72万 (亚太区), SX3258MU384R at 32.794万
#    H3000S composite version, 6x4
#    Use 30.5 as estimate

ESTIMATED_PRICES = {
    'SX3315DT386': 29.8,     # ~SX3315DT386R (30.286) adjusted for中亚三国 market
    'SX4255NV324': 29.5,     # ~average of similar F3000 6x4 tractors for中亚三国
    'SX41884M501TL': 30.5,   # Vietnam LNG, estimated from similar 4x2 tractors
    'SX3258MR354': 30.5,     # Vietnam H3000S dumper, estimated from similar models
}

ALL_PRICES = {**DIRECT_PRICES, **ESTIMATED_PRICES}

def fix_vehicle_prices():
    """Fix prices in all vehicle JSON files and regenerate summary."""
    
    fixed_count = 0
    vehicle_files = sorted(glob.glob(os.path.join(DATA_DIR, 'vehicles_*.json')))
    
    # Load model_price_map
    with open(os.path.join(DATA_DIR, 'model_price_map.json'), 'r', encoding='utf-8') as f:
        model_price_map = json.load(f)
    
    for vf in vehicle_files:
        fname = os.path.basename(vf)
        country_encoded = fname.replace('vehicles_', '').replace('.json', '')
        country_name = unquote(country_encoded)
        
        with open(vf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        vehicles = data if isinstance(data, list) else data.get('vehicles', [])
        modified = False
        
        for v in vehicles:
            model = v.get('model', '')
            if model in ALL_PRICES:
                old_price = v.get('price')
                new_price = ALL_PRICES[model]
                v['price'] = new_price
                
                # Determine source
                if model in DIRECT_PRICES:
                    v['price_source'] = 'quotation_file_direct'
                else:
                    v['price_source'] = 'estimated_from_similar'
                
                # Update model_price_map
                model_price_map[model] = {
                    'price': new_price,
                    'source': v.get('source_file', 'unknown')
                }
                
                fixed_count += 1
                modified = True
                print(f'  ✅ [{country_name}] {model} ({v.get("name","")}): {old_price} -> {new_price}万元 [{v["price_source"]}]')
        
        if modified:
            # Re-save the file
            if isinstance(data, list):
                with open(vf, 'w', encoding='utf-8') as f:
                    json.dump(vehicles, f, ensure_ascii=False, indent=2)
            else:
                data['vehicles'] = vehicles
                with open(vf, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Save updated model_price_map
    with open(os.path.join(DATA_DIR, 'model_price_map.json'), 'w', encoding='utf-8') as f:
        json.dump(model_price_map, f, ensure_ascii=False, indent=2)
    
    print(f'\n总计修复: {fixed_count} 辆')
    print(f'model_price_map 更新至: {len(model_price_map)} 条')
    
    return fixed_count

def rebuild_all_vehicles():
    """Rebuild all_vehicles.json from country files."""
    all_vehicles = []
    vehicle_files = sorted(glob.glob(os.path.join(DATA_DIR, 'vehicles_*.json')))
    
    for vf in vehicle_files:
        with open(vf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        vehicles = data if isinstance(data, list) else data.get('vehicles', [])
        all_vehicles.extend(vehicles)
    
    with open(os.path.join(DATA_DIR, 'all_vehicles.json'), 'w', encoding='utf-8') as f:
        json.dump(all_vehicles, f, ensure_ascii=False, indent=2)
    
    print(f'all_vehicles.json 重建完成: {len(all_vehicles)} 辆')

def update_summary():
    """Update summary.json with correct price counts."""
    all_vehicles = []
    price_sources_count = {'quotation_file_direct': 0, 'estimated_from_similar': 0, 'none': 0}
    
    for vf in sorted(glob.glob(os.path.join(DATA_DIR, 'vehicles_*.json'))):
        with open(vf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        vehicles = data if isinstance(data, list) else data.get('vehicles', [])
        all_vehicles.extend(vehicles)
    
    for v in all_vehicles:
        price = v.get('price')
        source = v.get('price_source', 'none')
        if price is not None and price > 0:
            if source == 'estimated_from_similar':
                price_sources_count['estimated_from_similar'] += 1
            else:
                price_sources_count['quotation_file_direct'] += 1
        else:
            price_sources_count['none'] += 1
    
    # Load existing summary
    summary_path = os.path.join(DATA_DIR, 'summary.json')
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary = json.load(f)
    
    summary['total_vehicles'] = len(all_vehicles)
    summary['price_coverage'] = {
        'with_price': price_sources_count['quotation_file_direct'] + price_sources_count['estimated_from_similar'],
        'estimated': price_sources_count['estimated_from_similar'],
        'missing': price_sources_count['none'],
        'coverage_pct': round((price_sources_count['quotation_file_direct'] + price_sources_count['estimated_from_similar']) / len(all_vehicles) * 100, 1)
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f'\n== 最终统计 ==')
    print(f'总车辆: {len(all_vehicles)}')
    print(f'报价文件价格: {price_sources_count["quotation_file_direct"]}')
    print(f'估算价格: {price_sources_count["estimated_from_similar"]}')
    print(f'缺价: {price_sources_count["none"]}')
    print(f'覆盖率: {summary["price_coverage"]["coverage_pct"]}%')

if __name__ == '__main__':
    fix_vehicle_prices()
    rebuild_all_vehicles()
    update_summary()
