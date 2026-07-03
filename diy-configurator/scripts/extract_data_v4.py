"""Extract ALL vehicles with comprehensive price detection - v4
Sources: price_raw, options_raw, base_dh, model-to-price map from quotation sheets
"""
import pandas as pd
import json
import re
import os
import urllib.parse

BASE = r"c:\Users\Administrator\WorkBuddy\20260605101515"
OUT = os.path.join(BASE, "shacman-catalog", "diy-configurator", "data")
DESKTOP = r"C:\Users\Administrator\Desktop\陕汽报价"
os.makedirs(OUT, exist_ok=True)

# ── Step 0: Build comprehensive model-price map from ALL quotation XLSX files ──
print("Step 0: Building model-price map from quotation files...")

def is_numeric_price(val):
    if pd.isna(val): return None
    try:
        n = float(str(val).replace(",", "").replace(" ", ""))
        if 3 < n < 300:
            return round(n, 3)
    except:
        pass
    return None

model_price_map = {}

# Scan all price book directories recursively
for root, dirs, files in os.walk(DESKTOP):
    for fname in files:
        if not (fname.endswith('.xlsx') or fname.endswith('.xls')):
            continue
        # Skip known non-price files
        if any(kw in fname for kw in ['发动机换选装', '换装价格表', '轮胎品牌', '排放法规', '认证要求', '出口车型配置', '出口市场专用车']):
            if '价格册' not in root:
                continue
        
        fp = os.path.join(root, fname)
        try:
            xl = pd.ExcelFile(fp)
        except:
            continue
        
        for sn in xl.sheet_names:
            try:
                df = pd.read_excel(fp, sheet_name=sn, header=None)
            except:
                continue
            
            price_col = None
            model_col = None
            header_row = None
            
            for row_idx in range(min(df.shape[0], 30)):
                for col_idx in range(min(df.shape[1], 40)):
                    v = str(df.iloc[row_idx, col_idx]).strip() if pd.notna(df.iloc[row_idx, col_idx]) else ''
                    if v in ['价格', '底盘价格', '价格（万元）', 'Price']:
                        if price_col is None:
                            price_col = col_idx
                            header_row = row_idx
                    if v in ['设计车型号', '车型号', 'Model', '型号']:
                        if model_col is None:
                            model_col = col_idx
                            if header_row is None:
                                header_row = row_idx
            
            if price_col is None or model_col is None:
                continue
            
            for row_idx in range(header_row + 1, df.shape[0]):
                model = str(df.iloc[row_idx, model_col]).strip() if pd.notna(df.iloc[row_idx, model_col]) else ''
                model = re.sub(r'\s+', '', model)
                price = is_numeric_price(df.iloc[row_idx, price_col])
                
                if model and price and re.match(r'^(SX|LZ)\d', model):
                    if model not in model_price_map:
                        model_price_map[model] = {'price': price, 'source': os.path.basename(root)}

print(f"  Model-price map: {len(model_price_map)} models")

# Save map for reference
with open(os.path.join(OUT, "model_price_map.json"), "w", encoding="utf-8") as f:
    json.dump(model_price_map, f, ensure_ascii=False, indent=2)

# ── Step 1: All Vehicles from Knowledge Base ──
print("\nStep 1: Extracting vehicles from knowledge base...")

vdf = pd.read_excel(os.path.join(BASE, "SHACMAN_全球车型配置知识库_Global_Vehicle_Database.xlsx"))
vdf = vdf.rename(columns={
    "区域/Region": "region", "国家/Country": "country", "车型大类/Category": "category",
    "产品线/Product Line": "product_line", "平台/Platform": "platform", "驱动/Drive": "drive",
    "版本/Version": "version", "车型号/Model": "model", "发动机/Engine": "engine",
    "马力/HP": "hp", "排放/Emission": "emission", "变速箱/Gearbox": "gearbox",
    "速比/Axle Ratio": "axle_ratio", "轮胎/Tires": "tires", "油箱/Fuel Tank": "fuel_tank",
    "轴距/Wheelbase": "wheelbase", "ABS": "abs", "鞍座/5th Wheel": "fifth_wheel",
    "其他/Other": "other", "颜色/Color": "color", "价格/Price": "price_raw",
    "基础车型DH": "base_dh", "基础配置/Base Config": "base_config",
    "选装/Option Items": "options_raw", "一国一策配置/Country Config": "country_config"
})

def clean_str(v):
    if pd.isna(v): return ""
    return re.sub(r"\s+", " ", str(v).strip().replace("\n", " "))

def is_price(val):
    if pd.isna(val): return False, None
    try:
        n = float(str(val).replace(",", "").replace(" ", ""))
        return 5 < n < 200, round(n, 3)
    except:
        return False, None

vehicles = []
price_sources = {"price_col": 0, "options_col": 0, "base_dh_col": 0, "model_map": 0, "none": 0}

for _, row in vdf.iterrows():
    p_is_price, p_val = is_price(row["price_raw"])
    o_is_price, o_val = is_price(row["options_raw"])
    dh = row.get("base_dh")
    dh_is_price, dh_val = is_price(dh)
    
    price = None
    options_text = ""
    source = "none"
    
    if p_is_price:
        price = p_val
        options_text = clean_str(row["options_raw"]) if not o_is_price else ""
        source = "price_col"
    elif o_is_price:
        price = o_val
        options_text = ""
        source = "options_col"
    elif dh_is_price:
        price = dh_val
        options_text = clean_str(row["options_raw"])
        source = "base_dh_col"
    else:
        # Try model-price map
        model_raw = clean_str(row["model"])
        model_clean = re.sub(r'\s+', '', model_raw)
        if model_clean in model_price_map:
            price = model_price_map[model_clean]["price"]
            options_text = clean_str(row["options_raw"])
            source = "model_map"
        else:
            price = None
            options_text = clean_str(row["options_raw"])
    
    price_sources[source] = price_sources.get(source, 0) + 1
    
    vehicles.append({
        "region": clean_str(row["region"]),
        "country": clean_str(row["country"]),
        "category": clean_str(row["category"]),
        "platform": clean_str(row["platform"]).split("\n")[0],
        "drive": clean_str(row["drive"]),
        "version": clean_str(row["version"]),
        "model": clean_str(row["model"]),
        "engine": clean_str(row["engine"]).split("\n")[0],
        "hp": str(row["hp"]) if pd.notna(row["hp"]) else "",
        "emission": clean_str(row["emission"]),
        "gearbox": clean_str(row["gearbox"]).split("\n")[0],
        "axle_ratio": clean_str(row["axle_ratio"]),
        "tires": clean_str(row["tires"]),
        "fuel_tank": clean_str(row["fuel_tank"]),
        "wheelbase": clean_str(row["wheelbase"]),
        "abs": clean_str(row["abs"]),
        "fifth_wheel": clean_str(row["fifth_wheel"]),
        "base_config": clean_str(row["base_config"])[:300] if pd.notna(row["base_config"]) else "",
        "options": options_text[:300],
        "price": price,
        "has_price": price is not None,
        "price_source": source
    })

print(f"  Total vehicles: {len(vehicles)}")
print(f"  Price sources:")
for src, cnt in sorted(price_sources.items()):
    print(f"    {src}: {cnt}")
print(f"  With price: {sum(1 for v in vehicles if v['has_price'])}")
print(f"  Without price: {sum(1 for v in vehicles if not v['has_price'])}")

# ── Step 2: Country extraction ──
def extract_country_name(raw):
    s = raw
    for kw in [".xlsx", "推荐车型配置表", "车型配置表"]:
        s = s.replace(kw, "")
    s = re.sub(r"\d+年[初中下]?半?[\w]*", "", s)
    s = re.sub(r"^\d+[-.]?\d*", "", s)
    for kw in ["中东区", "非洲区", "非洲一区", "非洲二区", "中南美区", "亚俄区", "亚太区", "东南亚", "CIS"]:
        s = s.replace(kw, "")
    s = s.strip().strip("-. ").strip()
    if not s or len(s) < 2: return raw[:20]
    m = re.match(r"([\u4e00-\u9fa5a-zA-Z\s]+)", s)
    if m: s = m.group(1).strip()
    for kw in ["N1", "  ", "产品线", "车型"]:
        s = s.replace(kw, "")
    return s.strip()

country_vehicles = {}
country_regions = {}
for v in vehicles:
    cn = extract_country_name(v["country"])
    if not cn: cn = v["country"][:15]
    if cn not in country_vehicles:
        country_vehicles[cn] = []
        country_regions[cn] = set()
    country_vehicles[cn].append(v)
    country_regions[cn].add(v["region"])

print(f"\n  Countries: {len(country_vehicles)}")

# Country summary
country_summary = []
for cn, vlist in sorted(country_vehicles.items()):
    platforms = sorted(set(v["platform"] for v in vlist if v["platform"]))
    categories = sorted(set(v["category"].split("/")[0] for v in vlist if v["category"]))
    priced_count = sum(1 for v in vlist if v["has_price"])
    country_summary.append({
        "name": cn,
        "regions": sorted(country_regions[cn]),
        "vehicle_count": len(vlist),
        "priced_count": priced_count,
        "platforms": platforms,
        "categories": categories
    })

with open(os.path.join(OUT, "countries.json"), "w", encoding="utf-8") as f:
    json.dump(country_summary, f, ensure_ascii=False, indent=2)

# Save per-country vehicle files
for cn, vlist in country_vehicles.items():
    safe_name = urllib.parse.quote(cn)
    fpath = os.path.join(OUT, f"vehicles_{safe_name}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(vlist, f, ensure_ascii=False, indent=2)

with open(os.path.join(OUT, "all_vehicles.json"), "w", encoding="utf-8") as f:
    json.dump(vehicles, f, ensure_ascii=False)

print(f"  Saved {len(country_vehicles)} country vehicle files")

# ── Step 3: Engine Swaps ──
print("\nStep 3: Extracting engine swaps...")

edf = pd.read_excel(os.path.join(DESKTOP, "V1-发动机换选装价格（2）.xlsx"), sheet_name="Sheet1")
engine_swaps = []
for _, row in edf.iterrows():
    if pd.isna(row.get("标配")) or pd.isna(row.get("换选装")):
        continue
    std = clean_str(row["标配"])
    swap = clean_str(row["换选装"])
    price = None
    try:
        p = float(str(row.get("加价（W）")).replace(",", ""))
        if pd.notna(row.get("加价（W）")): price = p * 10000
    except: pass
    if price is None: continue
    note = clean_str(row.get("Unnamed: 7", "")) if "Unnamed: 7" in row else ""
    engine_swaps.append({
        "standard": std, "swap": swap, "price_change": price, "note": note
    })

reverse_map = {}
for es in engine_swaps:
    key = f"{es['standard']}->{es['swap']}"
    rev_key = f"{es['swap']}->{es['standard']}"
    if es["price_change"] > 0:
        reverse_map[rev_key] = round(-es["price_change"] * 0.8)
    else:
        reverse_map[rev_key] = round(es["price_change"] / 0.8) if es["price_change"] != 0 else 0

engine_lookup = {}
for es in engine_swaps:
    std = es["standard"]
    if std not in engine_lookup: engine_lookup[std] = []
    engine_lookup[std].append({"swap": es["swap"], "price_change": es["price_change"]})

for rev_key, rev_price in reverse_map.items():
    std, sw = rev_key.split("->", 1)
    if std not in engine_lookup: engine_lookup[std] = []
    existing = [e for e in engine_lookup[std] if e["swap"] == sw]
    if not existing:
        engine_lookup[std].append({"swap": sw, "price_change": rev_price})

with open(os.path.join(OUT, "engine_swaps.json"), "w", encoding="utf-8") as f:
    json.dump({"rules": engine_swaps, "lookup": engine_lookup}, f, ensure_ascii=False, indent=2)
print(f"  Engine swaps: {len(engine_swaps)} rules, {len(engine_lookup)} engines")

# ── Step 4: Accessories ──
print("\nStep 4: Extracting accessories...")

adf = pd.read_excel(os.path.join(DESKTOP, "附件2-2026年出口产品换装价格表.xlsx"), sheet_name="柴油车", header=None)
accessories = []
current_category = ""
for i in range(1, len(adf)):
    row = adf.iloc[i]
    seq = row.iloc[0]
    try:
        is_num = not pd.isna(seq) and re.match(r"^\d+(\.0)?$", str(seq).strip())
    except:
        is_num = False
    
    if is_num:
        if pd.notna(row.iloc[1]):
            current_category = clean_str(row.iloc[1])
        desc = clean_str(row.iloc[2])
        unit = clean_str(row.iloc[3]) if pd.notna(row.iloc[3]) else "辆"
        price_str = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
        note = clean_str(row.iloc[5]) if pd.notna(row.iloc[5]) else ""
        if not desc: continue
        
        p = 0
        pneg = False
        try:
            price_str_clean = re.sub(r"[^-\d]", "", price_str)
            if price_str_clean:
                if price_str_clean.startswith("-"):
                    p = int(price_str_clean)
                    pneg = True
                else:
                    p = int(price_str_clean)
        except:
            p = 0
        
        accessories.append({
            "category": current_category,
            "description": desc,
            "unit": unit,
            "price": abs(p),
            "is_deduction": pneg,
            "note": note
        })

acc_by_cat = {}
for a in accessories:
    cat = a["category"]
    if cat not in acc_by_cat: acc_by_cat[cat] = []
    acc_by_cat[cat].append(a)

with open(os.path.join(OUT, "accessories.json"), "w", encoding="utf-8") as f:
    json.dump({"items": accessories, "by_category": acc_by_cat}, f, ensure_ascii=False, indent=2)
print(f"  Accessories: {len(accessories)} items in {len(acc_by_cat)} categories")

# ── Step 5: Summary ──
summary = {
    "total_vehicles": len(vehicles),
    "total_countries": len(country_vehicles),
    "total_engine_swaps": len(engine_swaps),
    "total_accessories": len(accessories),
    "price_sources": price_sources,
    "model_price_map_size": len(model_price_map),
    "all_engines": sorted(set(v["engine"] for v in vehicles if v["engine"]))[:50],
    "all_platforms": sorted(set(v["platform"] for v in vehicles if v["platform"])),
    "all_categories": sorted(set(v["category"].split("/")[0] for v in vehicles if v["category"]))
}
with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"SHACMAN DIY Configurator Data Summary v4")
print(f"{'='*60}")
print(f"Model-price map: {len(model_price_map)} models")
print(f"Countries:       {len(country_vehicles)}")
print(f"Vehicles:        {len(vehicles)} ({sum(1 for v in vehicles if v['has_price'])} priced, {sum(1 for v in vehicles if not v['has_price'])} missing)")
print(f"  price_col:     {price_sources['price_col']}")
print(f"  options_col:   {price_sources['options_col']}")
print(f"  base_dh_col:   {price_sources['base_dh_col']}")
print(f"  model_map:     {price_sources['model_map']}")
print(f"  none:          {price_sources['none']}")
print(f"Engines:         {len(engine_swaps)} swap rules")
print(f"Options:         {len(accessories)} items")
print(f"Data saved to:   {OUT}")
