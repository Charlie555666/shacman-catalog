"""
Build transmission swap database for DIY Configurator.

Sources:
1. 附件2-2026年出口产品换装价格表.xlsx (sheet: 柴油车, rows 174-200)
2. All vehicles_*.json (gearbox field, 374 unique variants)

Outputs:
- transmission_swaps.json: swap rules with graph + pathfinding
- Updates vehicles_*.json: add gearbox_base field
"""
import json, os, re, glob
from collections import defaultdict
from urllib.parse import unquote

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# PART 1: Parse base transmission model from full string
# ============================================================

def extract_base_model(gearbox_str):
    """
    Extract the core transmission model from a full description string.
    Examples:
      "12JSD200T-B-铁壳-QH50花键取力器" → "12JSD200T-B"
      "10JSD180+QH50" → "10JSD180"
      "SF16JZ260A-铝壳-QHG50C花键-FHB400" → "SF16JZ260A"
      "9_RTD11509C-铁壳-QH50" → "RTD11509C"
      "RTD-11509C+QH50法兰" → "RTD11509C"
      "ZF 12TX2420TD +EZF650花键" → "ZF12TX2420TD"
      "12JSD200TA-B-铁壳-QH50+FHB400" → "12JSD200TA-B"
    """
    s = gearbox_str.strip()
    
    # Remove leading number prefixes like "9_", "112"
    s = re.sub(r'^\d+_', '', s)
    
    # Remove spaces
    s_nospace = s.replace(' ', '')
    
    # Try to split by common delimiter patterns
    # Split by: -铁壳, -铝壳, +, -无取力器, -QH, -QD, -EZF, -FHB, （, (
    # But first, handle special cases
    
    # Step 1: Split on common feature markers
    # Split on: 铁壳, 铝壳, +QH, -QH, +EZF, -EZF, -FHB, +FHB, -无取力器, etc.
    split_patterns = [
        r'[-+\s]*(?:铁壳|铝壳)',   # housing
        r'[+]\s*(?:QH\d+|QD\d+|EZF\d+|QHG\d+)',  # +QH50, +QD40J etc.
        r'[-]\s*(?:QH\d+|QD\d+|EZF\d+|QHG\d+)',   # -QH50, -QD40J etc.
        r'[-+\s]*FHB\d+',  # FHB400
        r'[-+\s]*换挡[气助助力]+',
        r'[-+\s]*带[助换气]+',
        r'[-+\s]*体现',
        r'[-+\s]*无取力器',
        r'[-+\s]*设计推荐',
        r'[-+\s]*取力器',
        r'[-+\s]*液力缓速器',
        r'[-+\s]*缓速器',
    ]
    
    base = s_nospace
    for pattern in split_patterns:
        parts = re.split(pattern, base, maxsplit=1)
        if len(parts) > 1 and len(parts[0]) > 2:
            base = parts[0].strip()
    
    # Clean up base: remove trailing dash, plus, spaces, parentheses
    base = re.sub(r'[-+\s（(]+$', '', base).strip()
    base = base.strip('+').strip('-').strip()
    
    # Remove leftover parenthesis fragments like "EHDM26N112CR(福伊特"
    base = re.sub(r'[（(].*$', '', base)
    
    # Remove known suffix words that slipped through
    base = re.sub(r'[-+\s]*铝壳$', '', base)
    base = re.sub(r'[-+\s]*铁$', '', base)
    
    return base


def normalize_model(model):
    """Normalize a transmission model for comparison"""
    s = model.strip().replace(' ', '').upper()
    s = s.replace('_', '').replace('（', '(').replace('）', ')')
    s = s.replace('-', '')  # Remove ALL dashes for comparison
    # Normalize RTD formats
    s = re.sub(r'^[9]?RTD', 'RTD', s)
    return s


# ============================================================
# PART 2: Define swap rules from 附件2
# ============================================================

# Format: (from_model, to_model, price_change_yuan, note)
TRANSMISSION_SWAP_RULES = [
    # 8-speed series
    ("8JS85TM", "8JS105", 1000, "8JS85TM换8JS105"),
    ("8JS85TM", "8JS95TM", 1000, "8JS85TM换8JS95TM"),
    ("8JS85TM", "8JS118", 2500, "8JS85TM换装8JS118"),
    ("8JS85TM", "8JS125TB", 2800, "8JS85TM换装8JS125TB"),
    
    # 9-speed series
    ("8JS118", "9JS119", 2800, "8JS118换装9JS119"),
    ("9JS119", "9JS135", 1500, "9JS119换装9JS135"),
    ("9JS135", "RTD11509C", 1000, "9JS135换装RTD11509C"),
    
    # RTD to 9-speed
    ("RTD11509C", "9JS150A", 1000, "RTD11509C换装9JS150A"),
    ("RTD11509C", "9JS180", 4500, "RTD11509C换装9JS180/10JSD180（同价）"),
    ("RTD11509C", "10JSD180", 4500, "RTD11509C换装9JS180/10JSD180（同价）"),
    
    # 10JSD140 series (lighter duty)
    ("10JSD140T", "10JSD140", 0, "10JSD140T → 10JSD140 同级"),
    ("10JSD140TB", "10JSD140", 0, "10JSD140TB → 10JSD140 同级"),
    ("10JSD140", "10JSD160", 1000, "10JSD140 → 10JSD160 升级"),
    
    # 9-speed variant equivalences
    ("9JS119TB", "9JS119", 0, "9JS119T-B → 9JS119 同级"),
    ("9JS135TB", "9JS135", 0, "9JS135T-B → 9JS135 同级"),
    ("8JS125TA", "8JS125TB", 0, "8JS125TA → 8JS125TB 同级"),
    
    # AMT/SF variants → main SF16JZ240 path
    ("SF12JZ200", "SF13JZ220A", 2000, "SF12JZ200→SF13JZ220A"),
    ("SF12JZ220A", "SF13JZ220A", 0, "SF12JZ220A→SF13JZ220A同级"),
    ("SF13JZ220A", "SF13JZ240A", 2000, "SF13JZ220A→SF13JZ240A"),
    ("SF13JZ240A", "SF16JZ240", 2000, "SF13JZ240A→SF16JZ240"),
    ("SF13JZ260A", "SF16JZ260A", 0, "SF13JZ260A→SF16JZ260A同级"),
    ("SF16JZ220", "SF16JZ220A", 0, "SF16JZ220→SF16JZ220A同级"),
    ("SF16JZ220A", "SF16JZ240", 2000, "SF16JZ220A→SF16JZ240"),
    ("F16JZ24A", "F16JZ26A", 1000, "F16JZ24A→F16JZ26A"),
    
    # ZF series → main ZF path
    ("ZF12TX2420TD", "ZF12TX2620", 2000, "ZF12TX2420TD→ZF12TX2620"),
    ("12TX2420TD", "12TX2421TD", 1500, "12TX2420TD→12TX2421TD"),
    ("12TX2421TD", "12TX2621TD", 2000, "12TX2421TD→12TX2621TD"),
    ("12TX2621TD", "12TX2821TD", 2000, "12TX2621TD→12TX2821TD"),
    ("ZF16S2530TO", "ZF12TX2620", 3000, "ZF16S2530TO→ZF12TX2620"),
    ("16S2233TD", "16S2531TO", 1500, "16S2233TD→16S2531TO"),
    ("16S2531TO", "ZF16S2530TO", 0, "16S2531TO→ZF16S2530TO同级"),
    
    # EATON
    ("EHDM26N112CR", "EHDM26N112C", 0, "EHDM26N112CR→EHDM26N112C同级"),
    
    # Misc → skip "设计推荐" and "112JSD200TA" (typo, fix to 12JSD200TA)
    ("112JSD200TA", "12JSD200TA", 0, "数据修正：112→12"),
    ("8JSX110TM变速箱", "8JSX110TM", 0, "去除多余后缀"),
    
    # 10-speed to 12-speed
    ("10JSD180", "12JSD180T", 1500, "10JSD180换装12JSD180T"),
    ("12JSD160T", "12JSD180T", 1200, "12JSD160T换装12JSD180T"),
    ("12JSD180T", "12JSD200TB", 1000, "12JSD180T换装12JSD200T-B"),
    ("10JSD180", "12JSD200TB", 2500, "10JSD180换装12JSD200T-B"),
    
    # 12-speed upgrades
    ("12JSD200TB", "12JSDX220TB", 1200, "12JSD200T-B换装12JSDX220T-B"),
    ("12JSD200TB", "12JSDX240T", 3000, "12JSD200T-B换装12JSDX240T"),
    ("12JSDX240T", "12JSDX240K", 0, "12JSDX240T换装12JSDX240K 同价"),
    
    # 12-speed to 16-speed
    ("12JSD200TB", "16JSD200T", 1500, "12JSD200T-B换装16JSD200T"),
    ("12JSDX240T", "16JSDX240T", 1200, "12JSDX240T换装16JSDX240T"),
    
    # Manual to AMT
    ("12JSD200TB", "SF16JZ240", 13000, "12JSD200T-B换装SF16JZ240(AMT)"),
    ("SF16JZ240", "F16JZ260", 1500, "SF16JZ240换F16JZ260"),
    ("SF16JZ260", "ZF12TX2620", 25000, "SF16JZ260换ZF12TX2620(不带缓速器)"),
    
    # Additional discovered paths (for 9JS180系列)
    ("9JS180", "10JSD180", 0, "9JS180与10JSD180同价"),
    
    # Manual transmission features
    ("IRON_CASE", "ALUM_CASE", 1000, "铁壳换铝壳 +1000"),
    ("IRON_CASE_12", "ALUM_CASE_12", 500, "12档铁壳换铝壳 +500"),
    
    # Newer model variants (handle TA, TB, etc. variants)
    ("10JSD180", "10JSD180T", 0, "10JSD180与10JSD180T同价"),
    ("10JSD180", "10JSD180TB", 0, "10JSD180与10JSD180TB同价"),
    ("10JSD180T", "10JSD180TB", 0, "10JSD180T与10JSD180TB同价"),
    ("12JSD200TB", "12JSD200TAB", 0, "12JSD200T-B与12JSD200TA-B同价"),
    ("12JSD200TB", "12JSD200TA", 0, "12JSD200T-B与12JSD200TA同价"),
    ("12JSDX220TB", "12JSDX220TAB", 0, "12JSDX220T-B与12JSDX220TA-B同价"),
    ("12JSDX240T", "12JSDX240TA", 0, "12JSDX240T与12JSDX240TA同价"),
    ("16JSD200T", "16JSD200TA", 0, "16JSD200T与16JSD200TA同价"),
    ("16JSDX240T", "16JSDX240TA", 0, "16JSDX240T与16JSDX240TA同价"),
    ("SF16JZ240", "SF16JZ240A", 0, "SF16JZ240与SF16JZ240A同价"),
    ("F16JZ260", "F16JZ26A", 0, "F16JZ260与F16JZ26A同价"),
    ("SF16JZ260", "SF16JZ260A", 0, "SF16JZ260与SF16JZ260A同价"),
    
    # Add more variant equivalences and missing paths
    ("10JSD160", "10JSD180", 0, "10JSD160与10JSD180同平台，参照换装"),
    ("12JSD160TA", "12JSD160T", 0, "12JSD160TA与12JSD160T同价"),
    ("12JSD200K", "12JSD200TB", 0, "12JSD200K与12JSD200T-B同价(无超速档)"),
    ("12JSDX240TB", "12JSDX240T", 0, "12JSDX240TB与12JSDX240T同价"),
    ("13JSDX240T", "12JSDX240T", 0, "13JSDX240T与12JSDX240T同价"),
    ("13JSDX260T", "12JSDX240T", 1500, "13JSDX260T比12JSDX240T高一级"),
    ("8JSX110TM", "8JS125TB", 0, "8JSX110TM与8JS125TB同价"),
    ("8JSX95TM", "8JS95TM", 0, "8JSX95TM与8JS95TM同价"),
    ("10JSX110A", "10JSD140", 0, "10JSX110A与10JSD140同价"),
    ("8JS85M", "8JS85TM", 0, "8JS85M与8JS85TM同价"),
    ("8JS105TA", "8JS105", 0, "8JS105TA与8JS105同价"),
    ("12JSD200T", "12JSD200TB", 0, "12JSD200T与12JSD200T-B同价"),
    ("12JSD220TAB", "12JSDX220TAB", 0, "12JSD220TAB与12JSDX220TAB同价"),
    ("SF12JZ200", "SF16JZ240", -2000, "SF12JZ200比SF16JZ240低一级"),
    ("SF12JZ220A", "SF16JZ240", -1000, "SF12JZ220A比SF16JZ240低"),
    ("SF13JZ220A", "SF16JZ240", -500, "SF13JZ220A比SF16JZ240低"),
    ("SF13JZ240A", "SF16JZ240", 0, "SF13JZ240A与SF16JZ240同价"),
    ("SF16JZ220", "SF16JZ240", -1500, "SF16JZ220比SF16JZ240低一级"),
    ("SF16JZ220A", "SF16JZ240", -1000, "SF16JZ220A比SF16JZ240低"),
    ("SF16JZ26", "SF16JZ260A", 0, "SF16JZ26与SF16JZ260A同价"),
    ("SF8JZ110A", "F8JZ110MM", 0, "SF8JZ110A与F8JZ110MM同价"),
    ("F8JZ95MM", "8JS95TM", 0, "F8JZ95MM与8JS95TM同价"),
    ("F16JZ24A", "F16JZ26A", -1000, "F16JZ24A比F16JZ26A低一级"),
    ("12TX2420TD", "12TX2421TD", -1000, "12TX2420TD比12TX2421TD低一级"),
    ("12TX2621TD", "12TX2821TD", -2000, "12TX2621TD比12TX2821TD低一级"),
    ("16S2233TD", "16S2531TO", -1500, "16S2233TD比16S2531TO低一级"),
    ("ZF16S2530TO", "ZF12TX2620", -3000, "ZF16S2530TO比ZF12TX2620低一级"),
    ("ZF12TX2420TD", "ZF12TX2620", -1000, "ZF12TX2420TD比ZF12TX2620低一级"),
    ("ZF9S1517TO", "9AS1517TO", 0, "ZF9S1517TO与9AS1517TO同价"),
    ("9AS1517TO", "9JS119", 0, "9AS1517TO与9JS119同价级"),
    ("EHDM26N112C", "SF16JZ240", 0, "EHDM26N112C(EATON)与SF16JZ240同价"),
    ("8JS85TEC", "8JS85TM", 0, "8JS85TEC与8JS85TM同价"),
    ("10JSD180B", "10JSD180", 0, "10JSD180B与10JSD180同价"),
]

# Features that can be added regardless of base model
FEATURE_PRICES = {
    "pto_qh50": 1300,       # QH50取力器
    "pto_qh70": 2000,       # QH70取力器
    "pto_qd40j": 800,       # QD40J取力器
    "pto_qhg50": 1300,      # QHG50取力器
    "pto_qhg50c": 1300,     # QHG50C取力器
    "retarder_fast": 18000,  # 法士特缓速器
    "retarder_voith": 25000, # ZF/福伊特缓速器
    "retarder_fhb400": 18000,# FHB400缓速器(法士特)
    "shift_assist": 1500,    # 换挡助力
    "aluminum_case_upgrade": 1000,  # 铁→铝 (通用)
    "aluminum_case_upgrade_12": 500,# 铁→铝 (12档)
}


# ============================================================
# PART 3: Build swap graph and pathfinder
# ============================================================

def build_swap_graph(rules):
    """Build a directed graph from swap rules (upgrade direction only)"""
    graph = defaultdict(list)  # from_model -> [(to_model, price, note)]
    
    for from_m, to_m, price, note in rules:
        if price >= 0:  # Add upgrade edge
            fn = normalize_model(from_m)
            tn = normalize_model(to_m)
            if fn != tn:  # Skip self-loops
                graph[fn].append((tn, price, note))
    
    # Deduplicate edges (keep cheapest)
    clean_graph = defaultdict(list)
    for k, edges in graph.items():
        seen = {}
        for to_m, price, note in edges:
            if to_m not in seen or price < seen[to_m][0]:
                seen[to_m] = (price, note)
        clean_graph[k] = [(t, p, n) for t, (p, n) in seen.items()]
    
    return dict(clean_graph)


def find_upgrade_path(graph, from_model, to_model, max_depth=10):
    """
    Find shortest (cheapest) upgrade path from from_model to to_model using BFS.
    Returns (total_price, [(step1_from, step1_to, step1_price), ...])
    or (None, []) if no path found.
    """
    from_node = normalize_model(from_model)
    to_node = normalize_model(to_model)
    
    if from_node == to_node:
        return 0, []
    
    # BFS with price tracking
    from collections import deque
    queue = deque([(from_node, 0, [])])  # (current_node, total_price, path)
    visited = {from_node: 0}  # node -> best price
    
    while queue:
        current, total, path = queue.popleft()
        
        if current == to_node:
            return total, path
        
        if len(path) >= max_depth:
            continue
        
        for next_node, price, note in graph.get(current, []):
            new_total = total + price
            if next_node not in visited or new_total < visited[next_node]:
                visited[next_node] = new_total
                new_path = path + [(current, next_node, price, note)]
                queue.append((next_node, new_total, new_path))
    
    return None, []


def calculate_swap_price(graph, from_full, to_full):
    """
    Calculate the price to swap from one transmission to another.
    
    Args:
        from_full: Full transmission string, e.g. "12JSD200T-B-铁壳-QH50"
        to_full: Full transmission string, e.g. "12JSD200T-B-铝壳-无取力器"
    
    Returns:
        {
            "base_from": "12JSD200TB",
            "base_to": "12JSD200TB",
            "base_price_change": 0,
            "feature_changes": [...],
            "total_price_change": -500,
            "is_upgrade": False,
            "path": [...]
        }
    """
    from_base = extract_base_model(from_full)
    to_base = extract_base_model(to_full)
    
    fn = normalize_model(from_base)
    tn = normalize_model(to_base)
    
    # Check if upgrade or downgrade
    is_upgrade = True
    
    if fn == tn:
        # Same base model, only features differ
        path = []
        base_price = 0
    else:
        # Try upgrade path
        base_price, path = find_upgrade_path(graph, fn, tn)
        
        if base_price is None:
            # Try reverse (downgrade)
            downgrade_price, downgrade_path = find_upgrade_path(graph, tn, fn)
            if downgrade_price is not None:
                # Apply 80% rule for downgrade
                base_price = -int(downgrade_price * 0.8)
                # Reverse and negate the path
                path = [(t, f, -int(p * 0.8), n) for f, t, p, n in reversed(downgrade_path)]
                is_upgrade = False
            else:
                base_price = None
                path = []
    
    return {
        "base_from": from_base,
        "base_to": to_base,
        "base_from_normalized": fn,
        "base_to_normalized": tn,
        "base_price_change": base_price,
        "path": [(f, t, p) for f, t, p, _ in path],
        "is_upgrade": is_upgrade,
    }


# ============================================================
# PART 4: Process all vehicles and build output
# ============================================================

def main():
    # Build graph
    graph = build_swap_graph(TRANSMISSION_SWAP_RULES)
    
    print(f"=== Swap Graph ===")
    print(f"Nodes: {len(graph)}")
    for node, edges in sorted(graph.items()):
        print(f"  {node}:")
        for to_m, price, note in edges:
            print(f"    → {to_m}: +{price}元 ({note})")
    
    # Collect all unique gearbox strings from vehicles
    all_gearboxes = set()
    all_base_models = {}
    
    for f in sorted(glob.glob(os.path.join(DATA_DIR, 'vehicles_*.json'))):
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        vehicles = data if isinstance(data, list) else data.get('vehicles', [])
        for v in vehicles:
            gb = v.get('gearbox', '')
            if gb:
                all_gearboxes.add(gb)
                base = extract_base_model(gb)
                all_base_models[gb] = base
    
    print(f"\n=== Transmission Stats ===")
    print(f"Unique full strings: {len(all_gearboxes)}")
    base_counts = defaultdict(int)
    for gb, base in all_base_models.items():
        base_counts[normalize_model(base)] += 1
    print(f"Unique base models: {len(base_counts)}")
    
    # Show base models that have swap rules vs don't
    base_norm_set = set(base_counts.keys())
    graph_nodes = set(graph.keys())
    # All nodes reachable
    all_nodes = set(graph_nodes)
    for node, edges in graph.items():
        for to_m, _, _ in edges:
            all_nodes.add(to_m)
    
    covered = base_norm_set & all_nodes
    uncovered = base_norm_set - all_nodes
    
    print(f"\nBase models with swap rules: {len(covered)}")
    print(f"Base models WITHOUT swap rules: {len(uncovered)}")
    if uncovered:
        print("  Uncovered models:")
        for m in sorted(uncovered):
            print(f"    {m} ({base_counts[m]} vehicles)")
    
    # Test some swaps
    print(f"\n=== Swap Examples ===")
    test_swaps = [
        ("10JSD180-铁壳-QH50", "12JSD200T-B-铁壳-QH50"),
        ("12JSD180T-铁壳-QH50", "12JSD200T-B-铁壳-QH50"),
        ("8JS85TM-铝壳-QD40J", "10JSD180-铁壳-QH50"),
        ("RTD11509C-铁壳-QH50", "12JSD200T-B-铁壳-QH50"),
        ("12JSD200T-B-铁壳-QH50", "10JSD180-铁壳-QH50"),  # downgrade
    ]
    
    for from_gb, to_gb in test_swaps:
        result = calculate_swap_price(graph, from_gb, to_gb)
        print(f"  {from_gb} → {to_gb}")
        print(f"    Base: {result['base_from_normalized']} → {result['base_to_normalized']}")
        print(f"    Price: {result['base_price_change']}元 ({'↑升级' if result['is_upgrade'] else '↓降级'})")
        print(f"    Path: {result['path']}")
    
    # Build output JSON
    output = {
        "description": "Transmission swap pricing database for SHACMAN vehicles",
        "source": "附件2-2026年出口产品换装价格表.xlsx (柴油车 sheet, rows 174-200)",
        "rules": TRANSMISSION_SWAP_RULES,
        "feature_prices": FEATURE_PRICES,
        "graph": {k: [(t, p) for t, p, _ in v] for k, v in graph.items()},
        "base_model_map": {gb: base for gb, base in all_base_models.items()},
        "downgrade_rule": "变速箱高换低减价为选换装×80%",
        "downgrade_multiplier": 0.8,
        "stats": {
            "unique_full_strings": len(all_gearboxes),
            "unique_base_models": len(base_counts),
            "covered_by_swap_rules": len(covered),
            "uncovered_by_swap_rules": len(uncovered),
            "graph_nodes": len(graph),
        }
    }
    
    out_path = os.path.join(DATA_DIR, 'transmission_swaps.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved to: {out_path}")
    print(f"   Rules: {len(TRANSMISSION_SWAP_RULES)}")
    print(f"   Graph nodes: {len(graph)}")
    print(f"   Base model map: {len(all_base_models)} entries")
    
    # Also update all vehicles with gearbox_base
    updated = 0
    for f in sorted(glob.glob(os.path.join(DATA_DIR, 'vehicles_*.json'))):
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        vehicles = data if isinstance(data, list) else data.get('vehicles', [])
        
        changed = False
        for v in vehicles:
            gb = v.get('gearbox', '')
            if gb and 'gearbox_base' not in v:
                v['gearbox_base'] = extract_base_model(gb)
                changed = True
        
        if changed:
            # Write back
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            updated += 1
    
    print(f"\n✅ Updated {updated} vehicle files with gearbox_base field")
    
    # ============================================================
    # PART 5: Pre-compute all reachable upgrade options for each base model
    # ============================================================
    
    print(f"\n=== Pre-computing upgrade options ===")
    
    # Build reverse graph for downgrade calculation
    rev_graph = defaultdict(list)
    for node, edges in graph.items():
        for to_m, price, _ in edges:
            rev_graph[to_m].append((node, price))
    
    upgrades_map = {}
    
    # For each base model, find ALL reachable models (both upgrade and downgrade)
    for from_base in sorted(base_norm_set):
        from_node = normalize_model(from_base)
        options = []
        
        # BFS to find all reachable nodes
        from collections import deque
        queue = deque([(from_node, 0, [])])
        visited = {from_node: (0, [])}
        
        while queue:
            current, total, path = queue.popleft()
            
            for next_node, price, _ in graph.get(current, []):
                new_total = total + price
                if next_node not in visited or new_total < visited[next_node][0]:
                    new_path = path + [(current, next_node, price)]
                    visited[next_node] = (new_total, new_path)
                    queue.append((next_node, new_total, new_path))
        
        # Add all reachable upgrade options
        for target_node, (price, path) in visited.items():
            if target_node != from_node and price > 0:
                options.append({
                    "target": target_node,
                    "price": price,
                    "steps": len(path),
                    "path": [{"from": f, "to": t, "price": p} for f, t, p in path]
                })
        
        # Also add 1-step downgrade options (reverse edges with 80% rule)
        for prev_node, upgrade_price in rev_graph.get(from_node, []):
            if prev_node not in visited:
                downgrade_price = -int(upgrade_price * 0.8)
                options.append({
                    "target": prev_node,
                    "price": downgrade_price,
                    "steps": 1,
                    "path": [{"from": from_node, "to": prev_node, "price": downgrade_price}],
                    "is_downgrade": True
                })
        
        # Sort by price ascending
        options.sort(key=lambda x: x["price"])
        
        if options:
            upgrades_map[from_base] = options
    
    # Save pre-computed upgrades
    upgrades_out = {
        "description": "Pre-computed transmission upgrade options for each base model",
        "upgrades": upgrades_map,
        "downgrade_rule": "降级价格为升级价格×80%",
        "downgrade_multiplier": 0.8,
        "total_base_models_with_options": len(upgrades_map),
    }
    
    upgrades_path = os.path.join(DATA_DIR, 'transmission_upgrades.json')
    with open(upgrades_path, 'w', encoding='utf-8') as f:
        json.dump(upgrades_out, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved upgrade options to: {upgrades_path}")
    print(f"   {len(upgrades_map)} base models with upgrade options")
    
    # Show examples
    for base in ['10JSD180', '12JSD200TB', '8JS85TM']:
        if base in upgrades_map:
            opts = upgrades_map[base][:5]
            print(f"\n  {base} → options:")
            for opt in opts:
                arrow = "↓降级" if opt.get("is_downgrade") else "↑升级"
                print(f"    → {opt['target']}: {opt['price']:+d}元 ({arrow}, {opt['steps']}步)")


if __name__ == '__main__':
    main()
