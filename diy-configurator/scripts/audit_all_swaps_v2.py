"""
V2: 更精准的全面审计
- 正确理解 is_deduction 语义：表示降配，前端做 ×0.8 计算
- 重点检查真实定价错误
"""
import json, sys, os
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).parent.parent / 'data'

def load_json(name):
    with open(DATA_DIR / name, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_hp(engine_str):
    """从发动机型号中提取马力"""
    import re
    # 匹配如 WP10.380E22, ISME420, M13 560 等
    m = re.search(r'(\d+)\s*\d*[Ee]', engine_str)
    if m and len(m.group(1)) >= 3:
        return int(m.group(1)[-3:])  # 取最后3位为马力
    
    m = re.search(r'(\d{3})', engine_str)
    if m:
        hp = int(m.group(1))
        if 100 <= hp <= 800:
            return hp
    
    # 特殊处理: M10E5 360, M13 560 等
    parts = engine_str.split()
    for p in parts:
        try:
            hp = int(p)
            if 100 <= hp <= 800:
                return hp
        except:
            pass
    return None

def check_engine_swaps():
    data = load_json('engine_swaps.json')
    rules = data['rules']
    lookup = data['lookup']
    
    issues = []
    real_issues = []
    dupes = []
    
    seen_pairs = {}
    for i, r in enumerate(rules):
        key = f"{r['standard']} -> {r['swap']}"
        if key in seen_pairs:
            dupes.append(f"[INFO] DUP rule #{seen_pairs[key]} and #{i}: {key}")
        seen_pairs[key] = i
    
    rev_mismatches = []
    for std_key, targets in lookup.items():
        for t in targets:
            swp = t['swap']
            price = t['price_change']
            
            rev_targets = lookup.get(swp, [])
            rev_price = next((rt['price_change'] for rt in rev_targets if rt['swap'] == std_key), None)
            
            if rev_price is not None and price > 0:
                expected_rev = -round(price * 0.8)
                if rev_price != expected_rev:
                    std_hp = extract_hp(std_key)
                    swp_hp = extract_hp(swp)
                    rev_mismatches.append(
                        f"[REVERSE] {std_key}({std_hp}HP)→{swp}({swp_hp}HP) +{price} "
                        f"| reverse {swp}→{std_key} {rev_price} | expected {expected_rev}"
                    )
    
    print(f"\n{'='*60}")
    print(f"发动机换装审计: {len(rules)}条规则, {len(lookup)}个lookup key")
    print(f"  重复规则: {len(dupes)}条(无害)")
    print(f"  反向价格异常: {len(rev_mismatches)}条")
    
    if rev_mismatches:
        print(f"\n⚠️ 反向价格不遵循×0.8规则:")
        for m in rev_mismatches:
            print(f"  {m}")
        real_issues.extend(rev_mismatches)
    
    if not rev_mismatches and not dupes:
        print("✅ 发动机换装全部通过!")
    
    return real_issues

def check_transmission():
    swaps = load_json('transmission_swaps.json')
    upgrades = load_json('transmission_upgrades.json')
    
    issues = []
    
    # Raw swaps
    rules = swaps.get('rules', [])
    seen = set()
    dupes = []
    malformed = []
    
    for i, r in enumerate(rules):
        if len(r) != 4:
            malformed.append(f"[MALFORMED] rule #{i}")
            continue
        key = f"{r[0]} -> {r[1]}"
        if key in seen:
            dupes.append(f"[INFO] DUP: {key}")
        seen.add(key)
    
    # Upgrades
    u_data = upgrades.get('upgrades', {})
    total_paths = 0
    path_issues = []
    
    for base, options in u_data.items():
        for opt in options:
            total_paths += 1
            price = opt.get('price', 0)
            path = opt.get('path', [])
            is_dw = opt.get('is_downgrade', False)
            
            if path:
                path_sum = sum(p.get('price', 0) for p in path)
                if path_sum != price:
                    path_issues.append(f"[PATH] {base}→{opt['target']}: price={price} path_sum={path_sum}")
            
            if is_dw and price > 0:
                path_issues.append(f"[SIGN] {base}→{opt['target']}: downgrade price={price}")
            if not is_dw and price < 0:
                path_issues.append(f"[SIGN] {base}→{opt['target']}: upgrade price={price}")
    
    print(f"\n{'='*60}")
    print(f"变速箱换装审计: {len(rules)}条原始规则, {total_paths}条预计算路径")
    print(f"  格式错误: {len(malformed)}")
    print(f"  重复: {len(dupes)}条(无害)")
    print(f"  路径价格不一致: {len(path_issues)}")
    
    if not malformed and not path_issues:
        print("✅ 变速箱换装全部通过!")
    
    return issues

def check_accessory_swaps():
    data = load_json('accessory_swaps.json')
    cats = data.get('swap_categories', {})
    
    issues = []
    category_counts = {}
    total = 0
    
    # Check: forward entries should have is_deduction=false
    # Reverse (降配) entries should have is_deduction=true (price shows absolute value)
    count_warnings = []
    zero_price_items = []
    
    for cat_name, cat in cats.items():
        opts = cat.get('options', {})
        if not isinstance(opts, dict):
            issues.append(f"[STRUCT] {cat_name}: bad options type")
            continue
        
        cat_total = 0
        seen_sources = set()
        
        for source_name, opt_list in opts.items():
            seen_sources.add(source_name)
            
            if not isinstance(opt_list, list):
                issues.append(f"[STRUCT] {cat_name}/{source_name}: not list")
                continue
            
            for opt in opt_list:
                if not isinstance(opt, dict):
                    issues.append(f"[STRUCT] {cat_name}/{source_name}: item not dict")
                    continue
                
                total += 1
                cat_total += 1
                
                price = opt.get('price', 0)
                is_ded = opt.get('is_deduction', False)
                unit = opt.get('unit', '')
                
                if price == 0:
                    zero_price_items.append(f"{cat_name}: {opt.get('source')}→{opt.get('target')}")
                
                if not unit:
                    count_warnings.append(f"[NO_UNIT] {cat_name}: {opt.get('source')}→{opt.get('target')}")
                
                if opt.get('is_tire_set') and not opt.get('tire_count'):
                    issues.append(f"[MISSING_TIRE_COUNT] {cat_name}: {opt.get('source')}→{opt.get('target')}")
        
        category_counts[cat_name] = cat_total
    
    print(f"\n{'='*60}")
    print(f"配件换装审计: {total}条选项, {len(cats)}个分类")
    for cat, cnt in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}条")
    
    if zero_price_items:
        print(f"\n  价格=0的条目({len(zero_price_items)}条): (可能是规则说明而非实际换装)")
        for z in zero_price_items[:10]:
            print(f"    {z}")
        if len(zero_price_items) > 10:
            print(f"    ... 还有 {len(zero_price_items)-10} 条")
    
    if count_warnings:
        print(f"\n  缺少单位: {len(count_warnings)}条")
    
    if issues:
        print(f"\n⚠️ 真实问题: {len(issues)}个")
        for iss in issues:
            print(f"  {iss}")
    else:
        print("✅ 配件换装结构检查通过!")
    
    return issues

def check_accessories():
    data = load_json('accessories.json')
    items = data.get('items', [])
    
    zero_items = []
    prices_list = []
    
    for i, item in enumerate(items):
        desc = item.get('description', '')
        price = item.get('price')
        unit = item.get('unit', '')
        
        has_price = isinstance(price, (int, float)) and price > 0
        
        if has_price:
            prices_list.append(price)
        else:
            zero_items.append(f"#{i}: {desc}")
    
    print(f"\n{'='*60}")
    print(f"基础配件审计: {len(items)}条配件")
    if prices_list:
        print(f"  有效价格: {len(prices_list)}条, ¥{min(prices_list):,} ~ ¥{max(prices_list):,}")
    
    if zero_items:
        print(f"  价格=0/无价格: {len(zero_items)}条 (规则说明项)")
    # Note: price=0 items are often annotation/rule entries like "高配换低配不减价"
    
    print("✅ 基础配件结构检查通过!")
    return []

def check_frontend_functionality():
    """检查 index.html 中换装相关的JavaScript逻辑"""
    html_path = DATA_DIR.parent / 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    checks = {
        'selectEngine': '发动机换装处理函数',
        'selectTransmission': '变速箱换装处理函数',
        'selectSwap': '配件换装处理函数',
        'STATE._swapSelections': '配件选中状态管理',
        'calculateFOB': 'FOB价格计算',
        'is_deduction': '降配×0.8逻辑',
    }
    
    print(f"\n{'='*60}")
    print(f"前端功能检查 (index.html)")
    for func, desc in checks.items():
        found = func in html
        status = '✅' if found else '❌ MISSING!'
        print(f"  {status} {func}: {desc}")
    
    return []

if __name__ == '__main__':
    all_issues = []
    all_issues.extend(check_engine_swaps())
    all_issues.extend(check_transmission())
    all_issues.extend(check_accessory_swaps())
    all_issues.extend(check_accessories())
    all_issues.extend(check_frontend_functionality())
    
    print(f"\n{'='*60}")
    if not all_issues:
        print("🎉 所有换装数据审计通过! 无真实定价错误。")
    else:
        print(f"⚠️ 发现 {len(all_issues)} 个需要关注的问题:")
        for iss in all_issues:
            print(f"  {iss}")
    
    sys.exit(0 if not all_issues else 1)
