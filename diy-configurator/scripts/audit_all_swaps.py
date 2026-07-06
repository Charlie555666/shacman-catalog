"""
全面审计 DIY Configurator 所有换装数据
检查 engine_swaps, transmission_swaps, accessory_swaps 的正确性
"""
import json, sys, os, re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'

def load_json(name):
    with open(DATA_DIR / name, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_engine_swaps():
    """审计发动机换装：检查方向、价格重复/冲突、一致性"""
    data = load_json('engine_swaps.json')
    rules = data['rules']
    lookup = data['lookup']
    
    issues = []
    seen_pairs = {}
    
    # Rule-level checks
    for i, r in enumerate(rules):
        std = r['standard']
        swp = r['swap']
        price = r['price_change']
        key = f"{std} -> {swp}"
        
        # Check duplicate
        if key in seen_pairs:
            issues.append(f"[DUP] Rule #{seen_pairs[key]} and #{i}: duplicate {key}")
        seen_pairs[key] = i
        
        # Check for reverse pair existence
        rev_key = f"{swp} -> {std}"
        # This check will be done later
    
    # Lookup checks
    for std_key, targets in lookup.items():
        for t in targets:
            swp = t['swap']
            price = t['price_change']
            
            # Check that reverse exists
            rev_targets = lookup.get(swp, [])
            rev_found = any(rt['swap'] == std_key for rt in rev_targets)
            if not rev_found:
                issues.append(f"[MISSING_REVERSE] lookup[{swp}] missing reverse to {std_key}")
            
            # Check price consistency: forward + reverse should cancel with ×0.8 rule
            rev_price = next((rt['price_change'] for rt in rev_targets if rt['swap'] == std_key), None)
            if rev_price is not None:
                # Forward: +X, reverse should be -(X*0.8)
                if price > 0:
                    expected_rev = -round(price * 0.8)
                    if rev_price != expected_rev:
                        issues.append(f"[REVERSE_PRICE] {std_key}→{swp}(+{price}) reverse {swp}→{std_key}({rev_price}), expected {expected_rev}")
    
    ok_count = len(rules)
    print(f"\n=== 发动机换装审计 ({ok_count}条规则, {len(lookup)}个lookup key) ===")
    if issues:
        print(f"❌ 发现问题 {len(issues)} 个:")
        for iss in issues:
            print(f"  {iss}")
    else:
        print("✅ 全部通过!")
    return issues

def check_transmission_swaps():
    """审计变速箱换装原始数据"""
    data = load_json('transmission_swaps.json')
    rules = data.get('rules', [])
    
    issues = []
    seen = set()
    
    for i, r in enumerate(rules):
        if len(r) != 4:
            issues.append(f"[MALFORMED] rule #{i}: expected 4 elements, got {len(r)}")
            continue
        
        frm, to, price, note = r
        key = f"{frm} -> {to}"
        
        if key in seen:
            issues.append(f"[DUP] duplicate {key}")
        seen.add(key)
        
        if not isinstance(price, (int, float)):
            issues.append(f"[BAD_PRICE] {key}: price={price}")
    
    print(f"\n=== 变速箱换装审计 ({len(rules)}条规则) ===")
    if issues:
        print(f"❌ 发现问题 {len(issues)} 个:")
        for iss in issues:
            print(f"  {iss}")
    else:
        print("✅ 全部通过!")
    return issues

def check_transmission_upgrades():
    """审计变速箱升级预计算数据"""
    data = load_json('transmission_upgrades.json')
    upgrades = data.get('upgrades', {})
    
    issues = []
    total = 0
    
    for base, options in upgrades.items():
        for opt in options:
            total += 1
            target = opt.get('target')
            price = opt.get('price')
            is_dw = opt.get('is_downgrade', False)
            path = opt.get('path', [])
            
            if not path:
                issues.append(f"[NO_PATH] {base}→{target}: no path")
                continue
            
            # Sum path prices
            path_sum = sum(p.get('price', 0) for p in path)
            if path_sum != price:
                issues.append(f"[PATH_SUM_MISMATCH] {base}→{target}: price={price} but path sum={path_sum}")
            
            # Price direction check
            if is_dw and price > 0:
                issues.append(f"[SIGN_MISMATCH] {base}→{target}: downgrade but price={price}")
            if not is_dw and price < 0:
                issues.append(f"[SIGN_MISMATCH] {base}→{target}: upgrade but price={price}")
    
    print(f"\n=== 变速箱升级预计算审计 ({total}条路径) ===")
    if issues:
        print(f"❌ 发现问题 {len(issues)} 个:")
        for iss in issues[:30]:
            print(f"  {iss}")
        if len(issues) > 30:
            print(f"  ... 还有 {len(issues) - 30} 个问题")
    else:
        print("✅ 全部通过!")
    return issues

def check_accessory_swaps():
    """审计配件换装数据"""
    data = load_json('accessory_swaps.json')
    cats = data.get('swap_categories', {})
    
    issues = []
    total = 0
    category_counts = {}
    
    for cat_name, cat in cats.items():
        opts = cat.get('options', {})
        if not isinstance(opts, dict):
            issues.append(f"[BAD_STRUCT] {cat_name}: options is {type(opts).__name__}")
            continue
        
        cat_total = 0
        seen_pairs = set()
        
        for source_name, opt_list in opts.items():
            if not isinstance(opt_list, list):
                issues.append(f"[BAD_STRUCT] {cat_name}/{source_name}: not a list")
                continue
            
            for opt in opt_list:
                if not isinstance(opt, dict):
                    issues.append(f"[BAD_STRUCT] {cat_name}/{source_name}: item not dict")
                    continue
                    
                total += 1
                cat_total += 1
                src = opt.get('source', '')
                tgt = opt.get('target', '')
                price = opt.get('price', 0)
                is_ded = opt.get('is_deduction', False)
                
                pair_key = f"{src} → {tgt}"
                if pair_key in seen_pairs:
                    issues.append(f"[DUP] {cat_name}: {pair_key}")
                seen_pairs.add(pair_key)
                
                if is_ded and price > 0:
                    issues.append(f"[SIGN] {cat_name}: {pair_key} deduction but price={price}")
                if not is_ded and price < 0:
                    issues.append(f"[SIGN] {cat_name}: {pair_key} non-deduction but price={price}")
                
                unit = opt.get('unit', '')
                if not unit:
                    issues.append(f"[NO_UNIT] {cat_name}: {pair_key} no unit")
                
                if opt.get('is_tire_set'):
                    tc = opt.get('tire_count', {})
                    if not tc:
                        issues.append(f"[NO_TIRE_COUNT] {cat_name}: {pair_key} tire set without tire_count")
        
        category_counts[cat_name] = cat_total
    
    print(f"\n=== 配件换装审计 ({total}条选项, {len(cats)}个分类) ===")
    for cat, cnt in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}条")
    if issues:
        print(f"❌ 发现问题 {len(issues)} 个:")
        for iss in issues:
            print(f"  {iss}")
    else:
        print("✅ 全部通过!")
    return issues

def check_accessories():
    """审计基础配件列表"""
    data = load_json('accessories.json')
    items = data.get('items', [])
    
    issues = []
    prices = []
    
    for i, item in enumerate(items):
        desc = item.get('description', '')
        price = item.get('price')
        unit = item.get('unit', '')
        
        if price is None:
            issues.append(f"[NO_PRICE] #{i}: {desc}")
        elif not isinstance(price, (int, float)) or price <= 0:
            issues.append(f"[BAD_PRICE] #{i}: {desc} price={price}")
        else:
            prices.append(price)
        
        if not desc:
            issues.append(f"[NO_DESC] #{i}")
        if not unit:
            issues.append(f"[NO_UNIT] #{i}: {desc}")
    
    print(f"\n=== 基础配件审计 ({len(items)}条配件) ===")
    if prices:
        print(f"  价格范围: ¥{min(prices):,} ~ ¥{max(prices):,}, 均价: ¥{sum(prices)/len(prices):,.0f}")
    if issues:
        print(f"❌ 发现问题 {len(issues)} 个:")
        for iss in issues:
            print(f"  {iss}")
    else:
        print("✅ 全部通过!")
    return issues

def check_engine_price_consistency():
    """检查 engine_swaps.json 中 lookup 和 rules 的一致性"""
    data = load_json('engine_swaps.json')
    rules = data['rules']
    lookup = data['lookup']
    
    issues = []
    
    # Build rule map
    rule_map = {}
    for r in rules:
        key = (r['standard'], r['swap'])
        rule_map[key] = r['price_change']
    
    # Check lookup matches rules
    for std_key, targets in lookup.items():
        for t in targets:
            key = (std_key, t['swap'])
            if key in rule_map:
                if rule_map[key] != t['price_change']:
                    issues.append(f"[LOOKUP_MISMATCH] {key}: rule={rule_map[key]} lookup={t['price_change']}")
    
    # Check rules are all in lookup
    for key, price in rule_map.items():
        std, swp = key
        if std not in lookup:
            issues.append(f"[RULE_NOT_IN_LOOKUP] {key}: {std} not in lookup")
        else:
            found = any(t['swap'] == swp for t in lookup[std])
            if not found:
                issues.append(f"[RULE_NOT_IN_LOOKUP] {key}: not found in lookup[{std}]")
    
    print(f"\n=== 发动机 rules/lookup 一致性 ===")
    if issues:
        print(f"❌ 发现问题 {len(issues)} 个:")
        for iss in issues:
            print(f"  {iss}")
    else:
        print("✅ 全部通过!")
    return issues

if __name__ == '__main__':
    all_issues = []
    all_issues.extend(check_engine_swaps())
    all_issues.extend(check_engine_price_consistency())
    all_issues.extend(check_transmission_swaps())
    all_issues.extend(check_transmission_upgrades())
    all_issues.extend(check_accessory_swaps())
    all_issues.extend(check_accessories())
    
    print(f"\n{'='*60}")
    print(f"审计汇总: 共 {len(all_issues)} 个问题")
    if not all_issues:
        print("🎉 所有检查通过!")
    else:
        print(f"⚠️ 需要处理 {len(all_issues)} 个问题")
    
    sys.exit(0 if not all_issues else 1)
