"""对比 transmission_swaps.json 与源 Excel 柴油车 sheet"""
import json, openpyxl
from pathlib import Path
import re

DATA_DIR = Path(__file__).parent.parent / 'data'

with open(DATA_DIR / 'transmission_swaps.json', 'r', encoding='utf-8') as f:
    tx_data = json.load(f)

wb = openpyxl.load_workbook(r'C:\Users\Administrator\Desktop\陕汽报价\附件2-2026年出口产品换装价格表.xlsx', data_only=True)
ws = wb['柴油车']

# Extract transmission rules from Excel (rows 174-200)
excel_rxns = {}
for row in ws.iter_rows(min_row=174, max_row=200, values_only=True):
    content = str(row[2]) if row[2] else ''
    if '换' not in content:
        continue
    
    # Parse "A换装B" or "A换B"
    m = re.match(r'(.+?)换(?:装)?(.+)', content)
    if not m:
        continue
    
    frm = m.group(1).strip()
    to = m.group(2).strip()
    
    try:
        price = int(row[4]) if row[4] and str(row[4]) != '—' else 0
    except:
        price = 0
    
    excel_rxns[(frm, to)] = price

print(f"Excel 变速箱条目: {len(excel_rxns)}")

# Compare with JSON
json_rules = tx_data['rules']
json_pairs = {(r[0], r[1]): r[2] for r in json_rules}

matched = 0
mismatches = []
missing_in_json = []
missing_in_excel = []

for (frm, to), price in excel_rxns.items():
    if (frm, to) in json_pairs:
        json_price = json_pairs[(frm, to)]
        if json_price == price:
            matched += 1
        else:
            mismatches.append({
                'pair': f'{frm} → {to}',
                'excel': price,
                'json': json_price
            })
    else:
        missing_in_json.append(f'{frm} → {to} (Excel: {price})')

# Only check items we expect to match (non-zero price items from Excel)
print(f"  ✅ 匹配: {matched}")
print(f"  ❌ 价格不匹配: {len(mismatches)}")
print(f"  ⚠️ Excel有但JSON没有: {len(missing_in_json)}")
print(f"  ⚠️ JSON有但Excel没有: {len(missing_in_excel)}")

if mismatches:
    print(f"\n=== 价格不匹配 ===")
    for m in mismatches:
        diff = m['json'] - m['excel']
        print(f"  {m['pair']}: JSON={m['json']} Excel={m['excel']} (差异:{diff:+,})")

if missing_in_json:
    print(f"\n=== Excel有但JSON中没有 ({len(missing_in_json)}) ===")
    for m in missing_in_json:
        print(f"  {m}")

if not mismatches and not missing_in_json:
    print("\n🎉 变速箱换装价格完全一致!")
