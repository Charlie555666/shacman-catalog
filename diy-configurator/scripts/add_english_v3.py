"""Add comprehensive English translations to accessories.json and engine_swaps.json"""
import json, re, os

DATA = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\diy-configurator\data"

# ── Category English names ──
cat_en = {
    "": "Engine / Chassis Options", "悬架系统": "Suspension System",
    "驾驶室": "Cab", "驾驶室悬置": "Cab Suspension", "空调": "Air Conditioning",
    "转向机": "Steering Gear", "驾驶室相关部件": "Cab Components",
    "鞍座": "Fifth Wheel / Tread Patterns",
    "米其林": "Michelin Tires", "三角": "Triangle Tires",
    "玲珑": "Linglong Tires", "双钱": "Double Coin Tires",
    "中策": "Zhongce Tires", "金宇": "Jinyu Tires", "成山": "Chengshan Tires",
    "轮辋": "Wheel Rims", "油箱": "Fuel Tank", "变速箱": "Transmission",
    "离合器": "Clutch", "取力器": "PTO / Power Take-Off", "车桥": "Axle",
    "底盘其他": "Chassis Misc", "安全类": "Safety Equipment", "驱动": "Drivetrain",
    "寒区推荐配置": "Cold Region Package", "高温地区推荐配置": "Hot Region Package",
    "电器系统": "Electrical System", "其他": "Others", "防护类": "Protection",
    "其他附件": "Other Accessories", "超级版自卸": "Super Dump Package",
}

# ── Explicit translation dictionary ──
desc_map = {
    "前后少片簧换前后多片簧两骑马螺栓": "Taper-leaf → Multi-leaf springs (double U-bolts)",
    "德龙H3000换M3000同规格驾驶室": "H3000 → M3000 equivalent cab",
    "X3000/X5000液压主座椅换成空气主座椅": "Hydraulic → Air suspension driver seat",
    "中间储物盒": "Center storage box",
    "保险杠状态变化（玻璃钢、金属保险杠互换）": "Bumper swap: FRP / Metal",
    "悬架系统": "Suspension System",
    "驾驶室": "Cab",
    "空调": "Air Conditioning",
    "普通50鞍座换轻量化90型鞍座": "Standard 50 → Lightweight 90 fifth wheel",
    "普通50型鞍座换普通90型鞍座": "Standard 50 → Standard 90 fifth wheel",
    "普通50鞍座换国产JSK37DV鞍座（铸造鞍座）": "Standard 50 → Domestic JSK37DV cast saddle",
    "普通50鞍座换JOST 50鞍座(不带E标)": "Standard 50 → JOST 50 saddle (no E-mark)",
    "普通50鞍座换JOST 50鞍座(带E标)": "Standard 50 → JOST 50 saddle (E-marked)",
    "普通50鞍座换国产铸造50鞍座(L50)": "Standard 50 → Domestic cast L50 saddle",
    "普通90鞍座换国产铸造90鞍座(L90)": "Standard 90 → Domestic cast L90 saddle",
    "11R22.5、12R22.5真空胎指定块状花纹": "11/12R22.5 tubeless: Block tread",
    "295/80R22.5、315/80R22.5子午胎指定块状花纹": "295/315/80R22.5 radial: Block tread",
    "315/70R22.5指定块状花纹": "315/70R22.5: Block tread",
    "13R22.5指定矿用花纹": "13R22.5: Mining tread",
    "315/80R22.5子午胎指定矿用花纹": "315/80R22.5 radial: Mining tread",
    "12.00R24子午胎指定矿用花纹": "12.00R24 radial: Mining tread",
    "12.00R20子午胎指定矿用/越野花纹": "12.00R20 radial: Mining/Off-road tread",
    "14.00R20子午胎指定越野花纹": "14.00R20 radial: Off-road tread",
    "315/80R22.5、12.00R24真空胎18层级换20层级": "315/80R22.5 & 12.00R24: 18PR → 20PR",
    "12.00R20子午胎18层级换20层级": "12.00R20 radial: 18PR → 20PR",
    "单选加宽桥": "Wide axle option",
    "加一条12.00R20轮胎（含轮辋）": "Add 1x 12.00R20 tire (with rim)",
    "加一条14.00R20轮胎（含轮辋）": "Add 1x 14.00R20 tire (with rim)",
    "11R22.5指定米其林品牌": "11R22.5: Michelin",
    "315/80R22.5指定米其林品牌": "315/80R22.5: Michelin",
    "295/80R22.5指定米其林品牌": "295/80R22.5: Michelin",
    "385/65R22.5指定米其林品牌": "385/65R22.5: Michelin",
    "12R22.5指定三角品牌": "12R22.5: Triangle",
    "12.00R20指定三角品牌": "12.00R20: Triangle",
    "295/80R22.5指定三角品牌": "295/80R22.5: Triangle",
    "315/70R22.5指定三角品牌": "315/70R22.5: Triangle",
    "315/80R22.5指定三角品牌": "315/80R22.5: Triangle",
    "13R22.5指定三角品牌": "13R22.5: Triangle",
    "12.00R24指定三角品牌": "12.00R24: Triangle",
    "14.00R20指定三角品牌": "14.00R20: Triangle",
    "385/65R22.5指定三角品牌": "385/65R22.5: Triangle",
    "12R22.5指定双钱品牌": "12R22.5: Double Coin",
    "12.00R20指定双钱品牌": "12.00R20: Double Coin",
    "315/80R22.5指定双钱品牌": "315/80R22.5: Double Coin",
    "315/70R22.5指定双钱品牌": "315/70R22.5: Double Coin",
    "425/65R22.5指定双钱品牌": "425/65R22.5: Double Coin",
    "385/65R22.5、295/80R22.5指定双钱品牌": "385/65R22.5 & 295/80R22.5: Double Coin",
    "12R22.5指定中策品牌": "12R22.5: Zhongce",
    "12.00R20指定中策品牌": "12.00R20: Zhongce",
    "315/70R22.5指定中策品牌": "315/70R22.5: Zhongce",
    "315/80R22.5指定中策品牌": "315/80R22.5: Zhongce",
    "385/65R22.5指定中策品牌": "385/65R22.5: Zhongce",
    "295/80R22.5指定中策品牌": "295/80R22.5: Zhongce",
    "12.00R20子午胎指定金宇品牌": "12.00R20: Jinyu",
    "315/80R22.5指定金宇品牌": "315/80R22.5: Jinyu",
    "295/80R22.5指定金宇品牌": "295/80R22.5: Jinyu",
    "315/70R22.5指定金宇品牌": "315/70R22.5: Jinyu",
    "385/65R22.5指定金宇品牌": "385/65R22.5: Jinyu",
    "12.00R20指定成山品牌": "12.00R20: Chengshan",
    "315/70R22.5指定成山品牌": "315/70R22.5: Chengshan",
    "315/80R22.5指定成山品牌": "315/80R22.5: Chengshan",
    "385/65R22.5、12.00R24指定成山品牌": "385/65R22.5 & 12.00R24: Chengshan",
    "14.00R20指定成山品牌": "14.00R20: Chengshan",
    "295/80R22.5、315/70R22.5、12R22.5、12.00R20、315/80R22.5、13R22.5、12.00R24指定玲珑品牌": "All sizes: Linglong",
    "230L铝合金油箱换260L铝合金油箱": "230L → 260L aluminum fuel tank",
    "260L铝合金油箱换300铝合金油箱": "260L → 300L aluminum fuel tank",
    "200L铁换300L铝合金油箱": "200L steel → 300L aluminum fuel tank",
    "700L铝合金油箱换双腔油箱": "700L aluminum → Dual-chamber fuel tank",
    "400L铝合金油箱换800L铝合金油箱": "400L → 800L aluminum fuel tank",
    "双腔油箱": "Dual-chamber fuel tank",
    "增加一道世柏燃油粗滤器": "Add Shibai fuel pre-filter",
    "增加一道长效粗滤器": "Add long-life fuel pre-filter",
    "增加一道普通粗滤": "Add standard fuel pre-filter",
    "燃油水寒宝": "Fuel water separator / heater",
    "油箱增加1组进回油口": "Add 1 set fuel inlet/return ports",
    "油箱高配换至低配不减价": "High→Low spec tank: no price reduction",
    "8JS85TM换8JS105": "8JS85TM → 8JS105 transmission",
    "8JS85TM换8JS95TM": "8JS85TM → 8JS95TM transmission",
    "同规格变速器带超速档和不带超速档变速箱同价": "Overdrive / Non-overdrive: same price",
    "SF16JZ240换F16JZ260": "SF16JZ240 → F16JZ260 transmission",
    "SF16JZ260换ZF12TX2620(不带缓速器）": "SF16JZ260 → ZF12TX2620 (no retarder)",
    "4.8T前轴换4.8T加强型前轴": "4.8T → 4.8T Heavy-duty front axle",
    "13吨HD技术双级桥与16吨HD技术双级桥": "13T HD → 16T HD tandem axle",
    "前轴、后桥高配换低配不减钱": "High→Low spec axle: no price reduction",
    "后桥稳定杆": "Rear axle stabilizer bar",
    "轴距加长": "Extended wheelbase",
    "底盘整喷聚脲": "Full chassis polyurea coating",
    "持续式磨损报警": "Continuous wear alert system",
    "全车VOSS接头": "Full vehicle VOSS connectors",
    "自动间隙调整臂": "Automatic slack adjuster",
    "车架后悬长度增加（300mm以上）": "Extended frame rear overhang (>300mm)",
    "FDX-2500换到FDX-3200": "FDX-2500 → FDX-3200",
    "保温驾驶室": "Insulated cab",
    "加强暖风": "Heavy-duty heater",
    "低温管线": "Low-temperature hoses & lines",
    "盲区监控": "Blind spot monitoring",
    "180Ah免维护蓄电池换180Ah低温蓄电池": "180Ah MF → 180Ah low-temp battery",
    "预留行驶记录仪线束及接口": "Pre-wired for trip recorder",
    "ETA断容器": "ETA fuse / circuit breaker",
    "逆变电源接口（300W）": "300W inverter outlet",
    "逆变电源接口（1200W）": "1200W inverter outlet",
    "发动机车下启动装置": "Engine remote start switch",
    "三角警示牌": "Warning triangle",
    "全挂车电气路接口": "Full trailer electrical/pneumatic interface",
    "牵引车增加车架引桥": "Add chassis ramp (tractor)",
    "加大操作平台": "Enlarged working platform",
    "增加一片铝合金操作平台": "Add 1 aluminum working platform",
    "约斯特球销式牵引装置": "JOST ball-type towing hitch",
    "出口车随车工具(经济版)": "Export tool kit (Economy)",
    "出口车随车工具(豪华版)": "Export tool kit (Deluxe)",
    "水箱保护栅": "Radiator protection grille",
    "油底壳保护栅": "Oil pan protection grille",
    "前后灯具保护栅": "Front/rear lamp protection grille",
    "燃油防盗报警": "Fuel anti-theft alarm",
    "系统性燃油防盗": "Systematic fuel anti-theft",
    "整体式后视镜": "Integrated rear-view mirror",
    "同配置载货车用作专用车": "Same-spec cargo truck → special vehicle",
    "车架增加尾梁人字反光贴": "Frame tail beam reflective stickers",
    "金属挡泥板换三段整体式挡泥板": "Metal → 3-piece integrated mudguard",
    "分体式挡泥板换轻量化整体式挡泥板": "Split → Lightweight integrated mudguard",
}

# ── Engine English names ──
engine_en = {
    "WP10.336E53": "WP10 336HP Euro V", "WP10.350E53": "WP10 350HP Euro V",
    "WP10.380E22": "WP10 380HP Euro II", "WP10.380E32": "WP10 380HP Euro III",
    "WP10H.375E50": "WP10H 375HP Euro V", "WP12.375E50": "WP12 375HP Euro V",
    "WP12.400E201": "WP12 400HP Euro II", "WP12.430E201": "WP12 430HP Euro II",
    "WP12.460E201": "WP12 460HP Euro II", "WP12.460E50": "WP12 460HP Euro V",
    "WP12.460N": "WP12 460HP NG", "WP13.480E201": "WP13 480HP Euro II",
    "WP13.500E201": "WP13 500HP Euro II", "WP13.550E201": "WP13 550HP Euro II",
    "WP13.550E501": "WP13 550HP Euro V", "ISM11E5.385": "Cummins ISM 385HP Euro V",
    "ISM11E5.440": "Cummins ISM 440HP Euro V", "ISZ13E5.520": "Cummins ISZ 520HP Euro V",
    "X12E6.490": "Cummins X12 490HP Euro VI",
    "ISDe210 30": "Cummins ISDe 210HP Euro III",
    "ISM11E 385": "Cummins ISM 385HP",
    "ISM11E5 345": "Cummins ISM 345HP Euro V",
    "ISM11E5 385": "Cummins ISM 385HP Euro V",
    "ISM11E5 420": "Cummins ISM 420HP Euro V",
    "ISM11E5 440": "Cummins ISM 440HP Euro V",
    "ISM345 30": "Cummins ISM 345HP Euro III",
    "ISM420 30": "Cummins ISM 420HP Euro III",
    "ISME 420 30": "Cummins ISME 420HP Euro III",
    "ISME345 30": "Cummins ISME 345HP Euro III",
    "ISME385 30": "Cummins ISME 385HP Euro III",
    "ISME420 30": "Cummins ISME 420HP Euro III",
    "ISME420_30": "Cummins ISME 420HP Euro III",
    "ISME5 345": "Cummins ISME 345HP Euro V",
    "M10 400": "Weichai M10 400HP",
    "M10 440": "Weichai M10 440HP",
    "M10 480": "Weichai M10 480HP",
    "M10E3 385": "Weichai M10 385HP Euro III",
    "M10E3 440": "Weichai M10 440HP Euro III",
    "M10E3 450": "Weichai M10 450HP Euro III",
    "M10E5 360": "Weichai M10 360HP Euro V",
    "M10E5 385": "Weichai M10 385HP Euro V",
    "M10E5 460": "Weichai M10 460HP Euro V",
    "M13 560": "Weichai M13 560HP",
    "M13 E3 520": "Weichai M13 520HP Euro III",
    "M13E5 520": "Weichai M13 520HP Euro V",
    "W10.340E22": "Weichai W10 340HP Euro II",
    "W10.380E22": "Weichai W10 380HP Euro II",
    "WP10 340E22": "Weichai WP10 340HP Euro II",
    "WP10 380E22": "Weichai WP10 380HP Euro II",
    "WP10.300E22": "Weichai WP10 300HP Euro II",
    "WP10.340E22": "Weichai WP10 340HP Euro II",
    "WP10.375E50": "Weichai WP10 375HP Euro V",
    "WP12 400E201": "Weichai WP12 400HP Euro II",
    "WP12 430E201": "Weichai WP12 430HP Euro II",
    "WP12.400E50": "Weichai WP12 400HP Euro V",
    "WP12.430E50": "Weichai WP12 430HP Euro V",
    "WP13.550E30": "Weichai WP13 550HP Euro III",
    "WP6.180E32": "Weichai WP6 180HP Euro III",
    "WP6.210": "Weichai WP6 210HP",
    "WP6.210E32": "Weichai WP6 210HP Euro III",
    "WP6.240": "Weichai WP6 240HP",
    "WP6.240E32": "Weichai WP6 240HP Euro III",
    "WP7.240E51": "Weichai WP7 240HP Euro V",
    "WP7.270E51": "Weichai WP7 270HP Euro V",
}

def translate_desc(desc):
    if desc in desc_map:
        return desc_map[desc]
    # Pattern: "指定XX品牌" = "Specify XX brand"  (for tire brand items)
    m = re.search(r'指定(.+?)品牌', desc)
    if m: return f"Specify {m.group(1)} brand"
    # Pattern: "换装/换" = swap/upgrade
    if "换装" in desc:
        parts = desc.split("换装", 1)
        return f"Upgrade to {parts[1]}" if parts[1].strip() else f"Replace {parts[0]}"
    if "换成" in desc:
        parts = desc.split("换成", 1)
        return f"→ {parts[1]}"
    # Pattern: "加装" = add
    if "加装" in desc:
        return f"Add {desc.replace('加装', '').strip()}"
    if "加一条" in desc:
        return f"Add 1 extra tire: {desc.replace('加一条', '').replace('（含轮辋）', ' (with rim)').strip()}"
    # Pattern: "选装" = optional
    if "选装" in desc:
        return f"Optional: {desc.replace('选装', '').strip()}"
    return ""

# ── 1. Process accessories ──
acc = json.load(open(os.path.join(DATA, "accessories.json"), "r", encoding="utf-8"))
for item in acc["items"]:
    cat = item["category"]
    # Category EN
    if cat in cat_en:
        item["category_en"] = cat_en[cat]
    # Description EN
    if not item.get("description_en"):
        item["description_en"] = translate_desc(item["description"])
    # Note EN
    note = item.get("note", "")
    if note and not item.get("note_en"):
        if "降配" in note: item["note_en"] = "Downgrade"
        elif "升级" in note or "升配" in note: item["note_en"] = "Upgrade"
        elif "差价" in note: item["note_en"] = "Price diff"

with open(os.path.join(DATA, "accessories.json"), "w", encoding="utf-8") as f:
    json.dump(acc, f, ensure_ascii=False, indent=2)

en_count = sum(1 for item in acc["items"] if item.get("description_en"))
still_missing = sum(1 for item in acc["items"] if not item.get("description_en"))
print(f"Accessories: {en_count}/{len(acc['items'])} with English ({still_missing} missing)")

# ── 2. Process engine swaps ──
es = json.load(open(os.path.join(DATA, "engine_swaps.json"), "r", encoding="utf-8"))
for rule in es["rules"]:
    if not rule.get("standard_en"):
        rule["standard_en"] = engine_en.get(rule["standard"], "")
    if not rule.get("swap_en"):
        rule["swap_en"] = engine_en.get(rule["swap"], "")

with open(os.path.join(DATA, "engine_swaps.json"), "w", encoding="utf-8") as f:
    json.dump(es, f, ensure_ascii=False, indent=2)

rule_en = sum(1 for r in es["rules"] if r.get("standard_en"))
print(f"Engine swaps: {rule_en}/{len(es['rules'])} with English")

# Print remaining missing
if still_missing > 0:
    print(f"\nStill missing English ({still_missing}):")
    for item in acc["items"]:
        if not item.get("description_en"):
            print(f"  [{item['category']}] {item['description'][:70]}")

print("\nDone!")
