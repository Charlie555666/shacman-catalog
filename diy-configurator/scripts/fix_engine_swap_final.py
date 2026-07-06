"""修复 engine_swaps.json: WP6.240E32→ISDe210 30 应为 +29000 而非 -29000"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'

with open(DATA_DIR / 'engine_swaps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix 1: WP6.240E32 → ISDe210 30 should be +29000 (Excel row 45 says 2.9万)
# This was incorrectly flipped by the earlier HP-based fix (240HP→210HP looks like downgrade but it's brand upgrade)
for r in data['rules']:
    if r['standard'] == 'WP6.240E32' and r['swap'] == 'ISDe210 30':
        old = r['price_change']
        r['price_change'] = 29000.0
        print(f"Fixed rule: WP6.240E32→ISDe210 30: {old} → 29000.0")

# Rebuild lookup with correct reverse prices
def rebuild_lookup(rules):
    lookup = {}
    # Forward: original entries from rules
    for r in rules:
        std = r['standard']
        swp = r['swap']
        price = r['price_change']
        
        if std not in lookup:
            lookup[std] = []
        entry = {'swap': swp, 'price_change': price}
        if entry not in lookup[std]:
            lookup[std].append(entry)
    
    # Add reverse entries with ×0.8 rule
    for r in rules:
        std = r['standard']
        swp = r['swap']
        price = r['price_change']
        
        if swp not in lookup:
            lookup[swp] = []
        
        # Check if reverse already exists
        exists = any(e['swap'] == std for e in lookup[swp])
        if not exists:
            # ×0.8 deduction: if forward is positive upgrade, reverse is ×0.8 refund
            rev_price = -round(abs(price) * 0.8)
            lookup[swp].append({'swap': std, 'price_change': rev_price})
    
    return lookup

data['lookup'] = rebuild_lookup(data['rules'])

with open(DATA_DIR / 'engine_swaps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nRebuilt engine_swaps.json: {len(data['rules'])} rules, {len(data['lookup'])} lookup keys")

# Verify
for r in data['rules']:
    if r['standard'] == 'WP6.240E32' and r['swap'] == 'ISDe210 30':
        assert r['price_change'] == 29000.0, f"Still wrong: {r['price_change']}"
        print("✅ Verified: WP6.240E32→ISDe210 30 = 29000.0")

# Check auto-generated reverse
rev = next((e for e in data['lookup'].get('ISDe210 30', []) if e['swap'] == 'WP6.240E32'), None)
if rev:
    print(f"✅ Auto-generated reverse: ISDe210 30→WP6.240E32 = {rev['price_change']} (expected: -23200)")
else:
    print("❌ Reverse not found")
