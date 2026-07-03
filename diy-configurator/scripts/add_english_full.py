#!/usr/bin/env python3
"""
Complete English translation for all 329 accessories + engine swaps.
Replaces the partial (prefix-only) translations with full, proper English.
"""

import json
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, 'data')

# ── Comprehensive Chinese→English term dictionary ──
TERMS = {
    # Vehicle brands & platforms
    '德龙': 'Delong',
    '陕汽': 'Shacman',
    '德龙X3000': 'Delong X3000',
    '德龙X5000': 'Delong X5000',
    '德龙X6000': 'Delong X6000',
    '德龙F3000': 'Delong F3000',
    '德龙H3000': 'Delong H3000',
    '德龙H3000S': 'Delong H3000S',
    '德龙M3000': 'Delong M3000',
    '德龙L3000': 'Delong L3000',

    # Actions
    '加装': 'Add',
    '换装': 'Upgrade to',
    '选装': 'Optional',
    '取消': 'Cancel/Remove',
    '增加': 'Add',
    '减少': 'Reduce',

    # Engine & brake parts
    '康明斯Jacob制动': 'Cummins Jacobs Engine Brake',
    '康明斯': 'Cummins',
    '潍柴': 'Weichai',
    'ISM': 'ISM',
    'Jacob制动': 'Jacobs Brake',
    '发动机制动': 'Engine Brake',

    # Exhaust & intake
    '防火型消声器': 'Fireproof Muffler',
    '防火帽': 'Fire Cap',
    '消声器': 'Muffler',
    '上排气': 'Upward Exhaust',
    '右排气': 'Right-side Exhaust',
    '右上排气': 'Right-upward Exhaust',
    '右下排气': 'Right-downward Exhaust',

    # Air filters
    '普通空滤': 'Standard Air Filter',
    '中置空滤器': 'Center-mounted Air Filter',
    '油浴式空滤器': 'Oil-bath Air Filter',
    '分体式油浴': 'Split-type Oil-bath Air Filter',
    '双级空滤器': 'Dual-stage Air Filter',
    '沙漠式空滤器': 'Desert-type Air Filter',
    '空滤': 'Air Filter',
    '空滤器': 'Air Filter',

    # Suspension
    '复合式空气悬架': 'Composite Air Suspension',
    '全气囊空气悬架': 'Full Airbag Suspension',
    '空气悬架': 'Air Suspension',
    '四点液压悬置': '4-point Hydraulic Cab Suspension',
    '四点空气悬置': '4-point Air Cab Suspension',
    '液压悬置': 'Hydraulic Cab Suspension',
    '空气悬置': 'Air Cab Suspension',
    '少片簧': 'Parabolic Leaf Spring',
    '多片簧': 'Multi-leaf Spring',
    '两主片两骑马螺栓': '2 Main Leaves + 2 U-bolts',
    '四主片四骑马螺栓': '4 Main Leaves + 4 U-bolts',
    '骑马螺栓': 'U-bolts',
    'WABCO': 'WABCO',
    'ECAS': 'ECAS',
    '康迪泰克': 'Continental',

    # Cab types
    '加长高顶': 'Extended High-roof',
    '加长平顶': 'Extended Flat-roof',
    '半高顶': 'Semi High-roof',
    '平顶': 'Flat-roof',
    '高顶': 'High-roof',
    '标准驾驶室': 'Standard Cab',
    '加长半高顶驾驶室': 'Extended Semi High-roof Cab',
    '驾驶室': 'Cab',
    '顶导流罩': 'Roof Deflector',
    '顶侧导流罩': 'Roof & Side Deflectors',
    '导流罩': 'Deflector',

    # Cab features
    '手动翻转': 'Manual Tilt',
    '电动翻转装置': 'Electric Cab Tilt Device',
    '电动翻转': 'Electric Tilt',
    '进口驻车空调': 'Imported Parking A/C',
    '国产驻车空调': 'Domestic Parking A/C',
    '驻车空调': 'Parking A/C',
    '普通暖风': 'Standard Heater',
    '电控自动恒温空调': 'Electronic Automatic Climate Control',
    '热区空调': 'Hot-region A/C',
    '单制冷空调': 'Cooling-only A/C',
    '恒温空调': 'Climate Control',

    # Steering
    '转向机': 'Steering Gear',
    '进口转向机': 'Imported Steering Gear',
    '国产转向机': 'Domestic Steering Gear',
    '右置方向盘': 'Right-hand Drive Steering',
    '方向盘': 'Steering Wheel',
    '右舵': 'RHD',

    # Seats
    '第三座椅': 'Third Seat',
    '液压主座椅': 'Hydraulic Driver Seat',
    '空气主座椅': 'Air Driver Seat',
    '通风加热空气主座椅': 'Ventilated & Heated Air Driver Seat',
    '主座椅': 'Driver Seat',
    '固定副座椅': 'Fixed Passenger Seat',
    '液压副座椅': 'Hydraulic Passenger Seat',
    '空气副座椅': 'Air Passenger Seat',
    '副座椅': 'Passenger Seat',

    # Door & locks
    '中控锁': 'Central Locking',
    '手动摇窗机': 'Manual Window Crank',
    '电动摇窗机': 'Power Windows',
    '摇窗机': 'Window Mechanism',

    # Cab interior
    '加宽卧铺': 'Wide Sleeper Berth',
    '卧铺': 'Sleeper Berth',
    '中间储物盒': 'Center Storage Box',
    '储物盒': 'Storage Box',
    '卧铺挡帘': 'Berth Curtain',
    '环形窗帘': 'Ring Curtain',

    # Bumpers
    '保险杠': 'Bumper',
    '玻璃钢保险杠': 'FRP Bumper',
    '金属保险杠': 'Metal Bumper',
    '工程保险杠': 'Heavy-duty Bumper',
    '玻璃钢': 'FRP',

    # Steps & guards
    '第三级上车踏板': 'Third Step Board',
    '上车踏板': 'Step Board',
    '军用保护前围': 'Military Front Guard',
    '不锈钢前围': 'Stainless Steel Front Guard',
    '保护前围': 'Front Guard',
    '门下护板': 'Door Lower Guard',
    '防飞溅翼子板': 'Anti-splash Fender',
    '挡泥皮': 'Mud Flap',
    '挡泥板': 'Mudguard',
    '金属挡泥板': 'Metal Mudguard',
    '三段整体式挡泥板': '3-piece Integrated Mudguard',
    '分体式挡泥板': 'Split-type Mudguard',
    '轻量化三段式整体式挡泥板': 'Lightweight 3-piece Integrated Mudguard',
    '轻量化整体式挡泥板': 'Lightweight Integrated Mudguard',

    # Fifth wheel
    '鞍座': 'Fifth Wheel',
    '普通50鞍座': 'Standard 50 Fifth Wheel',
    '普通50型鞍座': 'Standard 50-type Fifth Wheel',
    '普通90鞍座': 'Standard 90 Fifth Wheel',
    '普通90型鞍座': 'Standard 90-type Fifth Wheel',
    '轻量化90型鞍座': 'Lightweight 90-type Fifth Wheel',
    '国产JSK37DV鞍座': 'Domestic JSK37DV Fifth Wheel',
    '国产铸造50鞍座': 'Domestic Cast 50 Fifth Wheel',
    '国产铸造90鞍座': 'Domestic Cast 90 Fifth Wheel',
    'JOST': 'JOST',
    '约斯特': 'JOST',
    '铸造鞍座': 'Cast Fifth Wheel',
    '低位50鞍座': 'Low-profile 50 Fifth Wheel',
    '加强型90鞍座': 'Heavy-duty 90 Fifth Wheel',
    '加强型90型鞍座': 'Heavy-duty 90-type Fifth Wheel',
    '双摆鞍座': 'Dual-oscillation Fifth Wheel',
    '临时鞍座': 'Temporary Fifth Wheel',
    '牵引座': 'Towing Hitch',
    '后牵引座': 'Rear Towing Hitch',

    # Tires
    '子午胎': 'Radial Tire',
    '真空胎': 'Tubeless Tire',
    '斜交轮胎': 'Bias Tire',
    '沙漠轮胎': 'Desert Tire',
    '轮胎': 'Tire',
    '备胎': 'Spare Tire',
    '备胎架': 'Spare Tire Carrier',
    '简易备胎架': 'Simple Spare Tire Carrier',
    '块状花纹': 'Block Pattern Tread',
    '矿用花纹': 'Mining Pattern Tread',
    '越野花纹': 'Off-road Pattern Tread',
    '横向花纹': 'Cross-ply Pattern Tread',
    '层级': 'Ply Rating',

    # Tire brands
    '米其林品牌': 'Michelin Brand',
    '米其林': 'Michelin',
    '三角品牌': 'Triangle Brand',
    '三角': 'Triangle',
    '玲珑品牌': 'Linglong Brand',
    '玲珑': 'Linglong',
    '双钱品牌': 'Double Coin Brand',
    '双钱': 'Double Coin',
    '中策品牌': 'Zhongce Brand',
    '中策': 'Zhongce',
    '金宇品牌': 'Jinyu Brand',
    '金宇': 'Jinyu',
    '成山品牌': 'Chengshan Brand',
    '成山': 'Chengshan',

    # Wheels
    '铝合金轮辋': 'Aluminum Alloy Wheel Rims',
    '轮辋': 'Wheel Rims',
    '大偏置': 'Large Offset',
    '普通铝合金轮辋': 'Standard Aluminum Alloy Wheel Rims',
    '珀然': 'Poman',
    '美铝': 'Alcoa',
    '前轴轮辋装饰罩': 'Front Axle Wheel Rim Cover',
    '不锈钢轮辋装饰罩': 'Stainless Steel Wheel Rim Cover',
    '轮辋装饰罩': 'Wheel Rim Cover',

    # Axles & bridges
    '加宽桥': 'Wide Axle',
    '前轴': 'Front Axle',
    '后桥': 'Rear Axle',
    '驱动桥': 'Drive Axle',
    '单级桥': 'Single-reduction Axle',
    '双级桥': 'Double-reduction Axle',
    'HD': 'HD',
    '加强型前轴': 'Heavy-duty Front Axle',
    '后桥稳定杆': 'Rear Axle Stabilizer Bar',
    '稳定杆': 'Stabilizer Bar',
    '筒式减震器': 'Cylindrical Shock Absorber',
    '减震器': 'Shock Absorber',

    # Fuel tanks
    '铁油箱': 'Steel Fuel Tank',
    '铝合金油箱': 'Aluminum Alloy Fuel Tank',
    '不锈钢油箱': 'Stainless Steel Fuel Tank',
    '油箱': 'Fuel Tank',
    '双腔油箱': 'Dual-chamber Fuel Tank',
    '燃油粗滤器': 'Fuel Pre-filter',
    '世柏燃油粗滤器': 'SIBO Fuel Pre-filter',
    '长效粗滤器': 'Long-life Pre-filter',
    '普通粗滤': 'Standard Pre-filter',
    '燃油水寒宝': 'Fuel Water Separator Heater',
    '进回油口': 'Fuel Inlet/Return Port',

    # Transmission
    '变速箱': 'Transmission',
    '铁壳变速箱': 'Iron Housing Transmission',
    '铝壳变速箱': 'Aluminum Housing Transmission',
    '法士特变速箱': 'Fast Gear Transmission',
    '法士特': 'Fast Gear',
    '超速档': 'Overdrive',
    '不带超速档': 'Direct Drive',
    '缓速器': 'Retarder',
    'ZF缓速器': 'ZF Retarder',
    '福伊特缓速器': 'Voith Retarder',
    '法士特缓速器': 'Fast Gear Retarder',
    '换挡助力': 'Shift Assist',
    '柔性换挡': 'Soft Shift',

    # Clutch
    '离合器': 'Clutch',
    '国产离合器': 'Domestic Clutch',
    '伊顿离合器': 'Eaton Clutch',

    # PTO
    '取力器': 'PTO (Power Take-Off)',
    '法兰取力器': 'Flange PTO',
    '发动机PTO取力': 'Engine PTO',

    # Brakes
    '鼓式制动': 'Drum Brake',
    '盘式制动': 'Disc Brake',
    '盘式制动器': 'Disc Brake',
    '克诺尔品牌': 'Knorr-Bremse Brand',
    '克诺尔': 'Knorr-Bremse',
    'ABS': 'ABS',
    '四通道ABS': '4-channel ABS',
    '六通道ABS': '6-channel ABS',
    'WABCO四通道ABS': 'WABCO 4-channel ABS',
    'WABCO六通道ABS': 'WABCO 6-channel ABS',
    '电子制动系统EBS': 'Electronic Braking System (EBS)',
    'EBS': 'EBS',
    '紧急制动系统AEBS': 'Advanced Emergency Braking System (AEBS)',
    'AEBS': 'AEBS',
    '车身稳定系统ESC': 'Electronic Stability Control (ESC)',
    'ESC': 'ESC',
    '防侧滑系统ASR': 'Anti-Slip Regulation (ASR)',
    'ASR': 'ASR',
    'WABCO阀类': 'WABCO Valves',
    '全车WABCO阀类': 'Full Vehicle WABCO Valves',
    '自动间隙调整臂': 'Automatic Slack Adjuster',
    '持续式磨损报警': 'Continuous Wear Alert',

    # Safety systems
    '疲劳监控驾驶系统': 'Driver Fatigue Monitoring System',
    '车道偏离预警系统': 'Lane Departure Warning System',
    '防碰撞预警': 'Forward Collision Warning',
    '胎压监测装置': 'Tire Pressure Monitoring System (TPMS)',

    # Drivetrain
    '加强传动轴': 'Heavy-duty Drive Shaft',
    '传动轴': 'Drive Shaft',
    '传动轴保护架': 'Drive Shaft Guard',
    '轴距加长': 'Extended Wheelbase',
    '轴距': 'Wheelbase',

    # Chassis
    '车架后悬': 'Frame Rear Overhang',
    '车架': 'Frame',
    '底盘整喷聚脲': 'Full Chassis Polyurea Coating',
    '聚脲': 'Polyurea',
    '车架引桥': 'Frame Approach Bridge',
    '加大操作平台': 'Enlarged Operation Platform',
    '铝合金操作平台': 'Aluminum Alloy Operation Platform',
    '操作平台': 'Operation Platform',

    # Cold region
    '保温驾驶室': 'Insulated Cab',
    '加强暖风': 'Enhanced Heater',
    '风暖式独立暖风装置': 'Air-heating Independent Heater',
    '水暖独立暖风装置': 'Water-heating Independent Heater',
    '独立暖风装置': 'Independent Heater',
    '进口品牌': 'Imported Brand',
    '国产品牌': 'Domestic Brand',
    '低温管线': 'Low-temperature Piping',
    '低温蓄电池': 'Low-temperature Battery',
    '大厢底板加热排气管': 'Cargo Body Floor Heating Exhaust Pipe',

    # Hot region
    '高温管线': 'High-temperature Piping',

    # Multimedia & electronics
    '七寸多媒体显示屏': '7-inch Multimedia Display',
    '十寸多媒体显示屏': '10-inch Multimedia Display',
    '多媒体显示屏': 'Multimedia Display',
    '倒车影像': 'Reverse Camera',
    '倒车雷达': 'Reverse Parking Radar',
    '盲区监控': 'Blind Spot Monitoring',
    '360环视': '360 Surround View',
    '格罗纳斯系统': 'GLONASS System',
    'GLONASS紧急呼叫系统': 'GLONASS Emergency Call System',

    # Battery
    '免维护蓄电池': 'Maintenance-free Battery',
    '135Ah': '135Ah',
    '165Ah': '180Ah',
    '180Ah': '180Ah',
    '220Ah': '220Ah',
    '蓄电池': 'Battery',

    # Electronics & accessories
    '电子行驶记录仪': 'Electronic Driving Recorder',
    '行驶记录仪': 'Driving Recorder',
    '限速装置': 'Speed Limiter',
    '机械泵发动机': 'Mechanical Pump Engine',
    '电控发动机': 'Electronic Control Engine',
    '多功能方向盘': 'Multi-function Steering Wheel',
    '定速巡航': 'Cruise Control',
    'ETA断容器': 'ETA Circuit Breaker',
    '逆变电源接口': 'Power Inverter Outlet',
    '远程油门控制装置': 'Remote Throttle Control',
    '发动机车下启动装置': 'Engine Under-chassis Start Device',
    '电动电加热后视镜': 'Electric Heated Rearview Mirror',
    '后视镜': 'Rearview Mirror',
    '整体式后视镜': 'Integrated Rearview Mirror',
    '后梁照明灯': 'Rear Frame Work Light',
    'LED日间行车灯': 'LED Daytime Running Lights',
    '日间行车灯': 'Daytime Running Lights',
    '倒车蜂鸣器': 'Reverse Buzzer',
    'LED尾灯': 'LED Tail Lights',
    '尾灯': 'Tail Lights',
    'ADR系统': 'ADR System (Hazardous Goods)',

    # Safety equipment
    '三角警示牌': 'Warning Triangle',
    '危险警示灯': 'Hazard Warning Light',
    '全挂车电气路接口': 'Full Trailer Electrical/Pneumatic Interface',
    '灭火器': 'Fire Extinguisher',
    '静电拖带': 'Anti-static Ground Strap',
    '驻车楔块': 'Wheel Chock',

    # Towing & recovery
    '军用拖勾': 'Military Tow Hook',
    '军车后拖钩': 'Military Rear Tow Hook',
    '双前牵引销': 'Dual Front Tow Pin',
    '八字尾梁': 'Splayed Rear Crossmember',
    '千斤顶': 'Jack',
    '32T千斤顶': '32-ton Jack',
    '50T千斤顶': '50-ton Jack',

    # Protective equipment
    '水箱保护栅': 'Radiator Protection Grille',
    '油底壳保护栅': 'Oil Pan Protection Grille',
    '油底壳保护': 'Oil Pan Guard',
    '前后灯具保护栅': 'Front & Rear Light Protection Grilles',
    '灯具保护栅': 'Light Protection Grille',
    '后防护': 'Rear Under-run Protection',
    '前下部防护': 'Front Under-run Protection',
    '侧防护': 'Side Under-run Protection',
    '侧防护板': 'Side Guard Panel',

    # Anti-theft
    '电瓶箱防盗装置': 'Battery Box Anti-theft Lock',
    '油箱盖防盗装置': 'Fuel Tank Cap Anti-theft Lock',
    '燃油防盗报警': 'Fuel Anti-theft Alarm',
    '系统性燃油防盗': 'Systematic Fuel Anti-theft',

    # Other
    '铝合金储气筒': 'Aluminum Alloy Air Reservoir',
    '储气筒': 'Air Reservoir',
    '随车工具': 'Tool Kit',
    '经济版': 'Economy Version',
    '豪华版': 'Luxury Version',
    '出口车': 'Export Vehicle',
    '专用车': 'Special-purpose Vehicle',
    '载货车': 'Cargo Truck',
    '自卸车': 'Dump Truck',
    '牵引车': 'Tractor Truck',
    '搅拌车': 'Mixer Truck',
    '泵车': 'Concrete Pump Truck',
    '全驱车': 'AWD Vehicle',

    # Packages
    '超级版选装包一': 'Super Edition Package 1',
    '超级版选装包二': 'Super Edition Package 2',
    '选装包': 'Option Package',
    '加强板簧': 'Heavy-duty Leaf Spring',
    '钢板保险杠': 'Steel Bumper',

    # VOSS & fittings
    'VOSS接头': 'VOSS Connectors',
    '全车VOSS接头': 'Full Vehicle VOSS Connectors',

    # Additional
    '车架增加尾梁人字反光贴': 'Add Reflective Chevron Tape on Rear Crossmember',
    '人字反光贴': 'Reflective Chevron Tape',
    '同配置': 'Same-spec',
    '分动箱': 'Transfer Case',
    '分动器': 'Transfer Case',
    '铁马': 'Tiema',
    '株齿': 'Zhuchi',
    '驱动': 'Drive',
    '全驱': 'AWD',

    # Misc specific
    '预留行驶记录仪线束及接口': 'Pre-wired for Driving Recorder',
    '预留': 'Pre-wired for',
    '尿素': 'Urea/AdBlue',
}

# ── Category English names ──
CATEGORIES_EN = {
    'items': None,  # Will be filled per-item
}

# ── Full-item specific translations (for complex items that can't be pattern-matched) ──
# Key = Chinese description, Value = English translation
ITEM_TRANSLATIONS = {
    '加装康明斯Jacob制动': 'Add Cummins Jacobs Engine Brake',
    '换装防火型消声器（防火帽）': 'Upgrade to Fireproof Muffler (with Fire Cap)',
    '选装上排气/右排气（右上排气或右下排气）': 'Optional Upward/Right-side Exhaust (Right-upward or Right-downward)',
    '普通空滤换装中置空滤器': 'Replace Standard Air Filter with Center-mounted Air Filter',
    '普通空滤换装油浴式空滤器': 'Replace Standard Air Filter with Oil-bath Air Filter',
    '普通空滤换装分体式油浴': 'Replace Standard Air Filter with Split-type Oil-bath Filter',
    '普通空滤换装双级空滤器': 'Replace Standard Air Filter with Dual-stage Air Filter',
    '普通空滤换装沙漠式空滤器': 'Replace Standard Air Filter with Desert-type Air Filter',
    '选装复合式空气悬架（国产标配ECAS）': 'Optional Composite Air Suspension (Domestic, ECAS Standard)',
    '全气囊空气悬架（国产标配ECAS）': 'Full Airbag Suspension (Domestic, ECAS Standard)',
    '前后少片簧换前后多片簧两骑马螺栓': 'Replace Parabolic Leaf Springs with Multi-leaf Springs + 2 U-bolts (Front & Rear)',
    '两主片两骑马螺栓换装四主片四骑马螺栓': 'Upgrade from 2 Main Leaves + 2 U-bolts to 4 Main Leaves + 4 U-bolts',
    '德龙X3000加长平顶5驾驶室换装加长高顶4驾驶室': 'Delong X3000 Extended Flat-roof (Type 5) Cab → Extended High-roof (Type 4) Cab',
    '德龙X3000加长高顶4驾驶室换装加长平顶5驾驶室': 'Delong X3000 Extended High-roof (Type 4) Cab → Extended Flat-roof (Type 5) Cab',
    '德龙X3000加长高顶驾驶室加装顶侧导流罩': 'Delong X3000 Extended High-roof Cab: Add Roof & Side Deflectors',
    '德龙X3000驾驶室加装顶导流罩': 'Delong X3000 Cab: Add Roof Deflector',
    '德龙F3000加长平顶J驾驶室换装加长高顶N驾驶室': 'Delong F3000 Extended Flat-roof (J-type) Cab → Extended High-roof (N-type) Cab',
    '德龙F3000加长高顶N驾驶室换装加长平顶J驾驶室': 'Delong F3000 Extended High-roof (N-type) Cab → Extended Flat-roof (J-type) Cab',
    '德龙F3000加装顶导流罩': 'Delong F3000: Add Roof Deflector',
    '德龙F3000加长高顶驾驶室加装顶侧导流罩': 'Delong F3000 Extended High-roof Cab: Add Roof & Side Deflectors',
    '德龙H3000标准驾驶室（M）换装H3000加长半高顶驾驶室（H）': 'Delong H3000 Standard Cab (M-type) → H3000 Extended Semi High-roof Cab (H-type)',
    '德龙H3000加长半高顶驾驶室（H）换装新H3000标准驾驶室（M）': 'Delong H3000 Extended Semi High-roof (H-type) → New H3000 Standard Cab (M-type)',
    '德龙H3000半高顶驾驶室（H）换装高顶驾驶室（G）': 'Delong H3000 Semi High-roof Cab (H-type) → High-roof Cab (G-type)',
    '德龙H3000高顶驾驶室（G）换装半高顶驾驶室（H）': 'Delong H3000 High-roof Cab (G-type) → Semi High-roof Cab (H-type)',
    '德龙H3000高顶驾驶室（G）选装顶侧导流罩': 'Delong H3000 High-roof Cab (G-type): Optional Roof & Side Deflectors',
    '德龙H3000驾驶室选装顶导流罩': 'Delong H3000 Cab: Optional Roof Deflector',
    '德龙H3000换M3000同规格驾驶室': 'Delong H3000: Swap to M3000 Same-spec Cab',
    'L3000驾驶室选装导流罩': 'Delong L3000 Cab: Optional Deflector',
    '手动翻转选装驾驶室电动翻转装置': 'Manual Cab Tilt → Optional Electric Cab Tilt Device',
    '四点液压悬置换装四点空气悬置驾驶室': '4-point Hydraulic Cab Suspension → 4-point Air Cab Suspension',
    '加装进口驻车空调': 'Add Imported Parking A/C',
    '加装国产驻车空调': 'Add Domestic Parking A/C',
    '普通暖风换装电控自动恒温空调': 'Standard Heater → Electronic Automatic Climate Control',
    '电控自动恒温空调换装热区空调': 'Electronic Climate Control → Hot-region A/C',
    '普通暖风换装热区空调': 'Standard Heater → Hot-region A/C',
    '换装进口转向机': 'Upgrade to Imported Steering Gear',
    'F3000换装右置方向盘（国产转向机）': 'Delong F3000: Upgrade to RHD Steering (Domestic Steering Gear)',
    'X3000/X5000车型换装右置方向盘（国产转向机）': 'Delong X3000/X5000: Upgrade to RHD Steering (Domestic Steering Gear)',
    'H3000S车型换装右置方向盘（国产转向机）': 'Delong H3000S: Upgrade to RHD Steering (Domestic Steering Gear)',
    'H3000车型换装右置方向盘（国产转向机）': 'Delong H3000: Upgrade to RHD Steering (Domestic Steering Gear)',
    'L3000车型换装右置方向盘（国产转向机）': 'Delong L3000: Upgrade to RHD Steering (Domestic Steering Gear)',
    '偏置矿用自卸换装右置方向盘（国产转向机）': 'Offset Mining Dump Truck: Upgrade to RHD Steering (Domestic Steering Gear)',
    'L3000/F3000加装第三座椅': 'Delong L3000/F3000: Add Third Seat',
    'X3000/X5000液压主座椅换成空气主座椅': 'Delong X3000/X5000: Hydraulic Driver Seat → Air Driver Seat',
    'X3000/X5000空气主座椅换装通风加热空气主座椅': 'Delong X3000/X5000: Air Driver Seat → Ventilated & Heated Air Driver Seat',
    '液压主座椅换装空气主座椅': 'Hydraulic Driver Seat → Air Driver Seat',
    '固定副座椅换装液压副座椅': 'Fixed Passenger Seat → Hydraulic Passenger Seat',
    '固定副座椅换装空气副座椅': 'Fixed Passenger Seat → Air Passenger Seat',
    'X3000/X5000加装中控锁': 'Delong X3000/X5000: Add Central Locking',
    '加装中控锁': 'Add Central Locking',
    '加装X3000加宽卧铺': 'Delong X3000: Add Wide Sleeper Berth',
    '中间储物盒': 'Center Storage Box',
    '手动摇窗机换装电动摇窗机': 'Manual Window Crank → Power Windows',
    '保险杠状态变化（玻璃钢、金属保险杠互换）': 'Bumper Material Change (FRP ↔ Metal Bumper Swap)',
    '金属保险杠、玻璃钢保险杠换装工程保险杠': 'Metal/FRP Bumper → Heavy-duty Bumper',
    '加装第三级上车踏板': 'Add Third Step Board',
    '加装军用保护前围': 'Add Military Front Guard',
    '加装不锈钢前围': 'Add Stainless Steel Front Guard',
    '普通50鞍座换轻量化90型鞍座': 'Standard 50 Fifth Wheel → Lightweight 90-type Fifth Wheel',
    '普通50型鞍座换普通90型鞍座': 'Standard 50-type Fifth Wheel → Standard 90-type Fifth Wheel',
    '普通50鞍座换国产JSK37DV鞍座（铸造鞍座）': 'Standard 50 Fifth Wheel → Domestic JSK37DV Cast Fifth Wheel',
    '普通50鞍座换JOST 50鞍座(不带E标)': 'Standard 50 Fifth Wheel → JOST 50 Fifth Wheel (Non-E-marked)',
    '普通50鞍座换JOST 50鞍座(带E标)': 'Standard 50 Fifth Wheel → JOST 50 Fifth Wheel (E-marked)',
    '普通50鞍座换国产铸造50鞍座(L50)': 'Standard 50 Fifth Wheel → Domestic Cast 50 Fifth Wheel (L50)',
    '普通90鞍座换国产铸造90鞍座(L90)': 'Standard 90 Fifth Wheel → Domestic Cast 90 Fifth Wheel (L90)',
    '约斯特50鞍座（不带E标）换装约斯特国产C型铸造50鞍座（JSK37C)': 'JOST 50 Fifth Wheel (Non-E-marked) → JOST Domestic C-type Cast 50 Fifth Wheel (JSK37C)',
    '普通50型鞍座换装约斯特国产化加强50鞍座(JSK39DV1-28)': 'Standard 50 Fifth Wheel → JOST Domestic Heavy-duty 50 Fifth Wheel (JSK39DV1-28)',
    'JOST 50鞍座（不带E标）换装JOST轻量化90鞍座': 'JOST 50 Fifth Wheel (Non-E-marked) → JOST Lightweight 90 Fifth Wheel',
    '普通90鞍座换装JOST 90鞍座': 'Standard 90 Fifth Wheel → JOST 90 Fifth Wheel',
    '普通90鞍座换装加强型90鞍座': 'Standard 90 Fifth Wheel → Heavy-duty 90 Fifth Wheel',
    '普通90鞍座换装加强型JOST 90鞍座(JSK39DV1-35)': 'Standard 90 Fifth Wheel → Heavy-duty JOST 90 Fifth Wheel (JSK39DV1-35)',
    '加强型JOST 90鞍座(JSK39DV1-35)换装加强型JOST 90鞍座(JSK39DV1-46)': 'Heavy-duty JOST 90 Fifth Wheel (JSK39DV1-35) → Heavy-duty JOST 90 Fifth Wheel (JSK39DV1-46)',
    '加强型JOST 90鞍座(JSK39DV1-35)换装国产铸造90鞍座(G9038C-190)带E标': 'Heavy-duty JOST 90 Fifth Wheel (JSK39DV1-35) → Domestic Cast 90 Fifth Wheel (G9038C-190) E-marked',
    '加强型JOST 90鞍座(JSK39DV1-35)换装约斯特国产铸造90鞍座(JSK38C)带E标': 'Heavy-duty JOST 90 Fifth Wheel (JSK39DV1-35) → JOST Domestic Cast 90 Fifth Wheel (JSK38C) E-marked',
    '普通90鞍座换装90型普通双摆鞍座': 'Standard 90 Fifth Wheel → 90-type Standard Dual-oscillation Fifth Wheel',
    '加强型90型鞍座换装90型普通双摆鞍座': 'Heavy-duty 90-type Fifth Wheel → 90-type Standard Dual-oscillation Fifth Wheel',
    '加强型90鞍座换装JOST 50鞍座(不带E标)': 'Heavy-duty 90 Fifth Wheel → JOST 50 Fifth Wheel (Non-E-marked)',
    '自卸车加装临时鞍座': 'Dump Truck: Add Temporary Fifth Wheel',
    'JOST 50鞍座换装约斯特50双摆鞍座（JSK38G1-2）': 'JOST 50 Fifth Wheel → JOST 50 Dual-oscillation Fifth Wheel (JSK38G1-2)',

    # Tire swaps (non-brand)
    '10.00R20子午胎换装10R22.5真空胎': '10.00R20 Radial Tires → 10R22.5 Tubeless Tires',
    '10.00R20子午胎换装11.00R20子午胎': '10.00R20 Radial Tires → 11.00R20 Radial Tires',
    '11.00R20子午胎换装12.00R20子午胎': '11.00R20 Radial Tires → 12.00R20 Radial Tires',
    '12.00R20子午胎换装12.00R24子午胎': '12.00R20 Radial Tires → 12.00R24 Radial Tires',
    '12.00R20子午胎换装13R22.5真空胎': '12.00R20 Radial Tires → 13R22.5 Tubeless Tires',
    '12.00R20子午胎换装315/70R22.5真空胎': '12.00R20 Radial Tires → 315/70R22.5 Tubeless Tires',
    '12.00R20子午胎换装315/80R22.5真空胎': '12.00R20 Radial Tires → 315/80R22.5 Tubeless Tires',
    '12.00R20子午胎换装385/65R22.5真空胎': '12.00R20 Radial Tires → 385/65R22.5 Tubeless Tires',
    '12.00R20子午胎换装425/65R22.5（20PR）真空胎': '12.00R20 Radial Tires → 425/65R22.5 (20PR) Tubeless Tires',
    '11R22.5、12R22.5真空胎换装11.00R20子午胎、295/80R22.5真空胎': '11R22.5/12R22.5 Tubeless → 11.00R20 Radial / 295/80R22.5 Tubeless Tires',
    '12.00R20子午胎换装20-20沙漠轮胎': '12.00R20 Radial Tires → 20-20 Desert Tires (incl. rims)',
    '12.00R20子午胎换装15.5-20斜交轮胎': '12.00R20 Radial Tires → 15.5-20 Bias Tires (incl. rims)',

    # Tire patterns
    '11R22.5、12R22.5真空胎指定块状花纹': '11R22.5 & 12R22.5 Tubeless: Specify Block Pattern Tread',
    '295/80R22.5、315/80R22.5子午胎指定块状花纹': '295/80R22.5 & 315/80R22.5: Specify Block Pattern Tread',
    '315/70R22.5指定块状花纹': '315/70R22.5: Specify Block Pattern Tread',
    '13R22.5指定矿用花纹': '13R22.5: Specify Mining Pattern Tread',
    '315/80R22.5子午胎指定矿用花纹': '315/80R22.5: Specify Mining Pattern Tread',
    '12.00R24子午胎指定矿用花纹': '12.00R24: Specify Mining Pattern Tread',
    '12.00R20子午胎指定矿用/越野花纹': '12.00R20: Specify Mining/Off-road Pattern Tread',
    '14.00R20子午胎指定越野花纹': '14.00R20: Specify Off-road Pattern Tread',
    '315/80R22.5、12.00R24真空胎18层级换20层级': '315/80R22.5 & 12.00R24: 18PR → 20PR',
    '12.00R20子午胎18层级换20层级': '12.00R20 Radial: 18PR → 20PR',
    '单选加宽桥': 'Select Wide Axle Only',
    '加装胎压监测装置': 'Add Tire Pressure Monitoring System (TPMS)',
    '加一条12.00R20轮胎（含轮辋）': 'Add One 12.00R20 Tire (incl. Rim)',
    '加一条14.00R20轮胎（含轮辋）': 'Add One 14.00R20 Tire (incl. Rim)',

    # Brand-specific tires
    '11R22.5指定米其林品牌': '11R22.5: Specify Michelin Brand',
    '315/80R22.5指定米其林品牌': '315/80R22.5: Specify Michelin Brand',
    '295/80R22.5指定米其林品牌': '295/80R22.5: Specify Michelin Brand',
    '385/65R22.5指定米其林品牌': '385/65R22.5: Specify Michelin Brand',
    '12R22.5指定三角品牌': '12R22.5: Specify Triangle Brand',
    '12.00R20指定三角品牌': '12.00R20: Specify Triangle Brand',
    '295/80R22.5指定三角品牌': '295/80R22.5: Specify Triangle Brand',
    '315/70R22.5指定三角品牌': '315/70R22.5: Specify Triangle Brand',
    '315/80R22.5指定三角品牌': '315/80R22.5: Specify Triangle Brand',
    '13R22.5指定三角品牌': '13R22.5: Specify Triangle Brand',
    '12.00R24指定三角品牌': '12.00R24: Specify Triangle Brand',
    '14.00R20指定三角品牌': '14.00R20: Specify Triangle Brand',
    '385/65R22.5指定三角品牌': '385/65R22.5: Specify Triangle Brand',
    '295/80R22.5、315/70R22.5、12R22.5、12.00R20、315/80R22.5、13R22.5、12.00R24指定玲珑品牌': 'Multiple Sizes: Specify Linglong Brand (295/80, 315/70, 12R, 12.00R20, 315/80, 13R, 12.00R24)',
    '12R22.5指定双钱品牌': '12R22.5: Specify Double Coin Brand',
    '12.00R20指定双钱品牌': '12.00R20: Specify Double Coin Brand',
    '315/80R22.5指定双钱品牌': '315/80R22.5: Specify Double Coin Brand',
    '315/70R22.5指定双钱品牌': '315/70R22.5: Specify Double Coin Brand',
    '425/65R22.5指定双钱品牌': '425/65R22.5: Specify Double Coin Brand',
    '385/65R22.5、295/80R22.5指定双钱品牌': '385/65R22.5 & 295/80R22.5: Specify Double Coin Brand',
    '12R22.5指定中策品牌': '12R22.5: Specify Zhongce Brand',
    '12.00R20指定中策品牌': '12.00R20: Specify Zhongce Brand',
    '315/70R22.5指定中策品牌': '315/70R22.5: Specify Zhongce Brand',
    '315/80R22.5指定中策品牌': '315/80R22.5: Specify Zhongce Brand',
    '385/65R22.5指定中策品牌': '385/65R22.5: Specify Zhongce Brand',
    '295/80R22.5指定中策品牌': '295/80R22.5: Specify Zhongce Brand',
    '12.00R20子午胎指定金宇品牌': '12.00R20: Specify Jinyu Brand',
    '315/80R22.5指定金宇品牌': '315/80R22.5: Specify Jinyu Brand',
    '295/80R22.5指定金宇品牌': '295/80R22.5: Specify Jinyu Brand',
    '315/70R22.5指定金宇品牌': '315/70R22.5: Specify Jinyu Brand',
    '385/65R22.5指定金宇品牌': '385/65R22.5: Specify Jinyu Brand',
    '12.00R20指定成山品牌': '12.00R20: Specify Chengshan Brand',
    '315/70R22.5指定成山品牌': '315/70R22.5: Specify Chengshan Brand',
    '315/80R22.5指定成山品牌': '315/80R22.5: Specify Chengshan Brand',
    '385/65R22.5、12.00R24指定成山品牌': '385/65R22.5 & 12.00R24: Specify Chengshan Brand',
    '14.00R20指定成山品牌': '14.00R20: Specify Chengshan Brand',

    # Wheel rims
    '换装铝合金轮辋': 'Upgrade to Aluminum Alloy Wheel Rims',
    '换装铝合金轮辋（珀然）': 'Upgrade to Aluminum Alloy Wheel Rims (Poman Brand)',
    '换装铝合金轮辋（美铝）': 'Upgrade to Aluminum Alloy Wheel Rims (Alcoa Brand)',
    '换装大偏置普通铝合金轮辋': 'Upgrade to Large Offset Standard Aluminum Alloy Wheel Rims',
    '换装大偏置珀然铝合金轮辋': 'Upgrade to Large Offset Aluminum Alloy Wheel Rims (Poman Brand)',
    '换装大偏置美铝铝合金轮辋': 'Upgrade to Large Offset Aluminum Alloy Wheel Rims (Alcoa Brand)',

    # Fuel tanks
    '加装200L铁油箱': 'Add 200L Steel Fuel Tank',
    '加装300L铝合金油箱': 'Add 300L Aluminum Alloy Fuel Tank',
    '加装230L铝合金油箱': 'Add 230L Aluminum Alloy Fuel Tank',
    '230L铝合金油箱换260L铝合金油箱': '230L Aluminum Fuel Tank → 260L Aluminum Fuel Tank',
    '260L铝合金油箱换300铝合金油箱': '260L Aluminum Fuel Tank → 300L Aluminum Fuel Tank',
    '200L铁换300L铝合金油箱': '200L Steel Fuel Tank → 300L Aluminum Fuel Tank',
    '380L铁油箱换装400L铝合金油箱': '380L Steel Fuel Tank → 400L Aluminum Fuel Tank',
    '380L铁油箱换装400L不锈钢油箱': '380L Steel Fuel Tank → 400L Stainless Steel Fuel Tank',
    '300L铝合金油箱换装400L铝合金油箱': '300L Aluminum Fuel Tank → 400L Aluminum Fuel Tank',
    '400L铝合金油箱换装600L铝合金油箱': '400L Aluminum Fuel Tank → 600L Aluminum Fuel Tank',
    '500L铝合金油箱换装600L铝合金油箱': '500L Aluminum Fuel Tank → 600L Aluminum Fuel Tank',
    '600L铝合金油箱换装700L铝合金油箱': '600L Aluminum Fuel Tank → 700L Aluminum Fuel Tank',
    '700L铝合金油箱换双腔油箱': '700L Aluminum Fuel Tank → Dual-chamber Fuel Tank',
    '700L铝合金油箱换装（400L+300L）铝合金油箱': '700L Aluminum Fuel Tank → (400L+300L) Dual Aluminum Fuel Tanks',
    '400L铝合金油箱换800L铝合金油箱': '400L Aluminum Fuel Tank → 800L Aluminum Fuel Tank',
    '双腔油箱': 'Dual-chamber Fuel Tank',
    '增加一道世柏燃油粗滤器': 'Add One SIBO Fuel Pre-filter',
    '增加一道长效粗滤器': 'Add One Long-life Pre-filter',
    '增加一道普通粗滤': 'Add One Standard Pre-filter',
    '燃油水寒宝': 'Fuel Water Separator Heater',
    '油箱增加1组进回油口': 'Add 1 Set of Fuel Inlet/Return Ports to Fuel Tank',
    '油箱高配换至低配不减价': 'Fuel Tank: Downgrade (No Price Reduction)',

    # Transmission swaps
    '8JS85TM换8JS105': '8JS85TM → 8JS105 Transmission',
    '8JS85TM换8JS95TM': '8JS85TM → 8JS95TM Transmission',
    '8JS85TM换装8JS118': '8JS85TM → 8JS118 Transmission',
    '8JS85TM换装8JS125TB': '8JS85TM → 8JS125TB Transmission',
    '8JS118换装9JS119': '8JS118 → 9JS119 Transmission',
    '9JS119换装9JS135': '9JS119 → 9JS135 Transmission',
    '9JS135换装RTD11509C': '9JS135 → RTD11509C Transmission',
    'RTD11509C换装9JS150A': 'RTD11509C → 9JS150A Transmission',
    'RTD11509C换装9JS180/10JSD180': 'RTD11509C → 9JS180/10JSD180 Transmission',
    '10JSD180换装12JSD180T': '10JSD180 → 12JSD180T Transmission',
    '12JSD160T换装12JSD180T': '12JSD160T → 12JSD180T Transmission',
    '12JSD180T换装12JSD200T-B': '12JSD180T → 12JSD200T-B Transmission',
    '10JSD180换装12JSD200T-B': '10JSD180 → 12JSD200T-B Transmission',
    '12JSD200T-B换装12JSDX220T-B': '12JSD200T-B → 12JSDX220T-B Transmission',
    '12JSD200T-B换装12JSDX240T': '12JSD200T-B → 12JSDX240T Transmission',
    '12JSDX240T换装12JSDX240K': '12JSDX240T → 12JSDX240K Transmission',
    '12JSD200T-B换装16JSD200T': '12JSD200T-B → 16JSD200T Transmission',
    '12JSDX240T换装16JSDX240T': '12JSDX240T → 16JSDX240T Transmission',
    '同规格变速器带超速档和不带超速档变速箱同价': 'Same-spec Transmission: Overdrive vs Direct Drive (Same Price)',
    '12JSD200T-B换装SF16JZ240': '12JSD200T-B → SF16JZ240 AMT Transmission',
    'SF16JZ240换F16JZ260': 'SF16JZ240 → F16JZ260 AMT Transmission',
    'SF16JZ260换ZF12TX2620(不带缓速器）': 'SF16JZ260 → ZF12TX2620 Transmission (w/o Retarder)',
    '铁壳变速箱换装铝壳变速箱': 'Iron Housing → Aluminum Housing Transmission',
    '加装ZF缓速器、福伊特缓速器': 'Add ZF/Voith Retarder',
    '加装法士特缓速器': 'Add Fast Gear Retarder',
    '加装换挡助力（柔性换挡）': 'Add Shift Assist (Soft Shift)',
    '变速箱高换低减价为选换装×80%': 'Transmission Downgrade: Price ×80%',

    # Clutch & PTO
    '国产离合器换装伊顿离合器': 'Domestic Clutch → Eaton Clutch',
    '加装QH50取力器': 'Add QH50 PTO',
    '加装QH70取力器': 'Add QH70 PTO',
    '加装QF60取力器': 'Add QF60 PTO',
    '加装QQ60取力器(A/B)': 'Add QQ60 PTO (Type A/B)',
    '加装QQ90取力器': 'Add QQ90 PTO',
    '加装QQ130取力器(A)': 'Add QQ130 PTO (Type A)',
    '加装N200法兰取力器': 'Add N200 Flange PTO',
    '加装发动机PTO取力': 'Add Engine PTO',

    # Axles
    '4.8T前轴换4.8T加强型前轴': '4.8T Front Axle → 4.8T Heavy-duty Front Axle',
    '5.5吨HD前轴换装7.5吨HD前轴': '5.5T HD Front Axle → 7.5T HD Front Axle',
    '7.5吨HD前轴换装9.5吨HD前轴': '7.5T HD Front Axle → 9.5T HD Front Axle',
    '13吨HD技术双级桥与16吨HD技术双级桥': '13T HD Double-reduction Axle ↔ 16T HD Double-reduction Axle',
    '13吨HD技术单级桥换装13吨HD技术双级桥': '13T HD Single-reduction Axle → 13T HD Double-reduction Axle',
    '11.5吨HD技术单级桥换装13吨HD技术单级桥': '11.5T HD Single-reduction Axle → 13T HD Single-reduction Axle',
    '加装后桥筒式减震器': 'Add Rear Axle Cylindrical Shock Absorber',
    '前轴、后桥高配换低配不减钱': 'Front Axle/Rear Axle Downgrade (No Price Reduction)',

    # Brakes
    '鼓式制动换装盘式制动': 'Drum Brake → Disc Brake',
    '盘式制动器指定克诺尔品牌': 'Disc Brake: Specify Knorr-Bremse Brand',
    '选装前轴轮辋装饰罩': 'Optional Front Axle Wheel Rim Cover (Plastic)',
    '选装前轴不锈钢轮辋装饰罩': 'Optional Front Axle Stainless Steel Wheel Rim Cover',
    '后桥稳定杆': 'Rear Axle Stabilizer Bar',
    '换装加强传动轴': 'Upgrade to Heavy-duty Drive Shaft',
    '轴距加长': 'Extended Wheelbase',
    '底盘整喷聚脲': 'Full Chassis Polyurea Coating',
    '加装国产四通道ABS': 'Add Domestic 4-channel ABS',
    '加装国产六通道ABS': 'Add Domestic 6-channel ABS',
    '加装WABCO四通道ABS': 'Add WABCO 4-channel ABS',
    '加装WABCO六通道ABS': 'Add WABCO 6-channel ABS',
    '加装国产电子制动系统EBS': 'Add Domestic Electronic Braking System (EBS)',
    '加装国产紧急制动系统AEBS': 'Add Domestic Advanced Emergency Braking System (AEBS)',
    '加装WABCO紧急制动系统AEBS': 'Add WABCO Advanced Emergency Braking System (AEBS)',
    '加装车身稳定系统ESC': 'Add Electronic Stability Control (ESC)',
    '加装疲劳监控驾驶系统': 'Add Driver Fatigue Monitoring System',
    '加装车道偏离预警系统+防碰撞预警': 'Add Lane Departure Warning + Forward Collision Warning',
    '持续式磨损报警': 'Continuous Brake Wear Alert',
    '加装防侧滑系统系统ASR': 'Add Anti-Slip Regulation (ASR)',
    '换装全车WABCO阀类': 'Upgrade to Full Vehicle WABCO Valves',
    '全车VOSS接头': 'Full Vehicle VOSS Connectors',
    '自动间隙调整臂': 'Automatic Slack Adjuster',
    '车架后悬长度增加（300mm以上）': 'Frame Rear Overhang Extension (300mm+)',
    '6×4换装6×6': '6×4 → 6×6 AWD Conversion',
    '4×2换装4×4': '4×2 → 4×4 AWD Conversion',
    '同扭矩分动箱指定铁马/株齿品牌': 'Same-torque Transfer Case: Specify Tiema/Zhuchi Brand',
    'FDX-2500换到FDX-3200': 'FDX-2500 → FDX-3200 Transfer Case',
    '保温驾驶室': 'Insulated Cab',
    '加强暖风': 'Enhanced Heater',
    '加装风暖式独立暖风装置（进口品牌）': 'Add Air-heating Independent Heater (Imported Brand)',
    '加装风暖式独立暖风装置（国产品牌）': 'Add Air-heating Independent Heater (Domestic Brand)',
    '加装9KW水暖独立暖风装置': 'Add 9KW Water-heating Independent Heater',
    '低温管线': 'Low-temperature Piping',
    '加装大厢底板加热排气管（指底盘部分的加价）': 'Add Cargo Floor Heating Exhaust Pipe (Chassis Part)',
    '加装热区空调': 'Add Hot-region A/C',
    '换装高温管线': 'Upgrade to High-temperature Piping',
    '加装七寸多媒体显示屏': 'Add 7-inch Multimedia Display',
    '加装十寸多媒体显示屏': 'Add 10-inch Multimedia Display',
    '加装倒车影像': 'Add Reverse Camera',
    '加装倒车雷达': 'Add Reverse Parking Radar',
    '盲区监控': 'Blind Spot Monitoring System',
    'X5000加装360环视': 'Delong X5000: Add 360 Surround View',
    '加装格罗纳斯系统(GLONASS紧急呼叫系统)': 'Add GLONASS Emergency Call System',
    '135Ah免维护蓄电池换装165Ah免维护蓄电池': '135Ah Maintenance-free Battery → 165Ah Maintenance-free Battery',
    '165Ah免维护蓄电池换装180Ah免维护蓄电池': '165Ah Maintenance-free Battery → 180Ah Maintenance-free Battery',
    '180Ah免维护蓄电池换装220Ah免维护蓄电池': '180Ah Maintenance-free Battery → 220Ah Maintenance-free Battery',
    '180Ah低温蓄电池换装220Ah低温蓄电池': '180Ah Low-temperature Battery → 220Ah Low-temperature Battery',
    '180Ah免维护蓄电池换180Ah低温蓄电池': '180Ah Maintenance-free Battery → 180Ah Low-temperature Battery',
    '加装国产电子行驶记录仪': 'Add Domestic Electronic Driving Recorder',
    '加装进口电子行驶记录仪': 'Add Imported Electronic Driving Recorder',
    '预留行驶记录仪线束及接口': 'Pre-wired for Driving Recorder (Harness & Interface)',
    '机械泵发动机加装限速装置': 'Mechanical Pump Engine: Add Speed Limiter',
    '加装多功能方向盘（带定速巡航）': 'Add Multi-function Steering Wheel (with Cruise Control)',
    'ETA断容器': 'ETA Circuit Breaker',
    '逆变电源接口（300W）': 'Power Inverter Outlet (300W)',
    '逆变电源接口（1200W）': 'Power Inverter Outlet (1200W)',
    '专用车选装远程油门控制装置（包括油门专用线束、远程油门预留接口、远程油门控制器）': 'Special-purpose Vehicle: Optional Remote Throttle Control (incl. harness, interface, and controller)',
    '发动机车下启动装置': 'Engine Under-chassis Start Device',
    '加装电动电加热后视镜': 'Add Electric Heated Rearview Mirrors',
    '加装后梁照明灯': 'Add Rear Frame Work Light',
    'X3000加装LED日间行车灯': 'Delong X3000: Add LED Daytime Running Lights',
    '加装倒车蜂鸣器': 'Add Reverse Buzzer',
    '换装LED尾灯': 'Upgrade to LED Tail Lights',
    '加装ADR系统': 'Add ADR System (Hazardous Goods Compliance)',
    '三角警示牌': 'Warning Triangle',
    '加装危险警示灯': 'Add Hazard Warning Light',
    '全挂车电气路接口': 'Full Trailer Electrical & Pneumatic Interface',
    '牵引车增加车架引桥': 'Tractor Truck: Add Frame Approach Bridge',
    '加大操作平台': 'Add Enlarged Operation Platform',
    '增加一片铝合金操作平台': 'Add One Aluminum Alloy Operation Platform',
    '加装门下护板': 'Add Cab Door Lower Guards',
    '加装防飞溅翼子板': 'Add Anti-splash Fenders',
    '加装挡泥皮': 'Add Mud Flaps',
    '加装备胎架': 'Add Spare Tire Carrier',
    '加装军用拖勾+八字尾梁': 'Add Military Tow Hook + Splayed Rear Crossmember',
    '加装八字尾梁': 'Add Splayed Rear Crossmember',
    '选装驻车楔块': 'Optional Wheel Chocks (2 pcs + brackets)',
    '换装32T千斤顶': 'Upgrade to 32-ton Jack',
    '换装50T千斤顶': 'Upgrade to 50-ton Jack',
    '加装静电拖带': 'Add Anti-static Ground Strap',
    '加装灭火器（2KG）': 'Add Fire Extinguisher (2KG)',
    '加装灭火器（8KG）': 'Add Fire Extinguisher (8KG)',
    '选装军车后拖钩': 'Optional Military Rear Tow Hook',
    '选装双前牵引销': 'Optional Dual Front Tow Pins',
    '选装后牵引座': 'Optional Rear Towing Hitch',
    '约斯特球销式牵引装置': 'JOST Ball-type Towing Coupling',
    '整车加装大于10kg尿素': 'Vehicle: Add Urea/AdBlue (>10kg)',
    '出口车随车工具(经济版)': 'Export Vehicle Tool Kit (Economy Version)',
    '出口车随车工具(豪华版)': 'Export Vehicle Tool Kit (Luxury Version)',
    '加装传动轴保护架': 'Add Drive Shaft Guard',
    '水箱保护栅': 'Radiator Protection Grille',
    '油底壳保护栅': 'Oil Pan Protection Grille (Full-length, Intercooler to Oil Pan)',
    '前后灯具保护栅': 'Front & Rear Light Protection Grilles',
    '加装后防护': 'Add Rear Under-run Protection',
    '加装前下部防护': 'Add Front Under-run Protection',
    '加装侧防护': 'Add Side Under-run Protection',
    'X6000选装侧防护板': 'Delong X6000: Optional Side Guard Panel',
    '选装电瓶箱防盗装置': 'Optional Battery Box Anti-theft Lock',
    '选装油箱盖防盗装置': 'Optional Fuel Tank Cap Anti-theft Lock',
    '燃油防盗报警': 'Fuel Anti-theft Alarm (incl. siren, harness, sensor)',
    '系统性燃油防盗': 'Systematic Fuel Anti-theft (incl. tank cap lock)',
    '整体式后视镜': 'Integrated Rearview Mirrors',
    '加装卧铺挡帘+环形窗帘': 'Add Berth Curtain + Ring Curtains',
    '整车选装铝合金储气筒': 'Vehicle: Optional Aluminum Alloy Air Reservoirs',
    '同配置载货车用作专用车': 'Same-spec Cargo Truck Used as Special-purpose Vehicle',
    '换装金属挡泥板': 'Upgrade to Metal Mudguards',
    '车架增加尾梁人字反光贴': 'Add Reflective Chevron Tape on Rear Crossmember',
    '金属挡泥板换三段整体式挡泥板': 'Metal Mudguards → 3-piece Integrated Mudguards',
    '分体式挡泥板换装三段整体式挡泥板': 'Split-type Mudguards → 3-piece Integrated Mudguards',
    '分体式挡泥板换装轻量化三段式整体式挡泥板': 'Split-type Mudguards → Lightweight 3-piece Integrated Mudguards',
    '分体式挡泥板换轻量化整体式挡泥板': 'Split-type Mudguards → Lightweight Integrated Mudguards',
    '超级版选装包一（钢板保险杠、LED尾灯、加强板簧、尾灯保护栅）': 'Super Edition Package 1 (Steel Bumper, LED Tail Lights, Heavy-duty Leaf Springs, Tail Light Guards)',
    '超级版选装包二（钢板保险杠、加强板簧、长效粗滤、三拉带400L铁油箱+防护、LED尾灯、后桥稳定杆、油底壳防护、系统性燃油防盗、电瓶箱防盗、尾灯保护栅）': 'Super Edition Package 2 (Steel Bumper, Heavy-duty Leaf Springs, Long-life Pre-filter, 400L Steel Fuel Tank w/ Triple Straps & Guard, LED Tail Lights, Rear Axle Stabilizer, Oil Pan Guard, Systematic Fuel Anti-theft, Battery Box Lock, Tail Light Guards)',
}

# ── Generate English note for items with Chinese notes ──
NOTE_TRANSLATIONS = {
    '高配换低配不减钱': 'No price reduction for downgrade',
    '加强版牵引，载货，专用可选': 'Enhanced version for tractor, cargo, special vehicles',
    '5、6同价': 'Type 5 & 6: same price',
    'D、J同价': 'Type D & J: same price',
    '减价1500': 'Deduct ¥1,500 if removed',
    '减价1000（X3000/X5000牵引车不减价）': 'Deduct ¥1,000 if removed (not applicable for X3000/X5000 tractors)',
    '减价700（X3000/X5000牵引车不减价）': 'Deduct ¥700 if removed (not applicable for X3000/X5000 tractors)',
    '同价': 'Same price',
    '取消减750元': 'Deduct ¥750 if removed',
    '取消减500元': 'Deduct ¥500 if removed',
    '取消减700': 'Deduct ¥700 if removed',
    '取消减3500': 'Deduct ¥3,500 if removed',
    '取消减600': 'Deduct ¥600 if removed',
    '取消减500': 'Deduct ¥500 if removed',
    '取消减600元': 'Deduct ¥600 if removed',
    '仅X3000可选': 'Only available for X3000',
    'L3000不可选': 'Not available for L3000',
    '金属保险杠可选': 'Metal bumper required',
    'X3000牵引车玻璃钢保险杠可选': 'X3000 tractor with FRP bumper: optional',
    '减价500': 'Deduct ¥500 if removed',
    '取消顶侧导流罩减价1200': 'Deduct ¥1,200 if roof/side deflectors removed',
    '取消顶导流罩减价800': 'Deduct ¥800 if roof deflector removed',
    '除X3000/X5000以外平台可选': 'Available for platforms other than X3000/X5000',
    '减价300': 'Deduct ¥300 if removed',
    'X3000牵引车取消该项目不减价': 'No price reduction for X3000 tractors if removed',
    '标配车型取消该项目不减价': 'No price reduction for standard models if removed',
    'X3000牵引车增加和减少该配置均不加价不减价': 'No price change for X3000 tractors (add or remove)',
    '需选用加宽桥（轮胎选换装加价，加宽桥不加价）': 'Requires wide axle (tire swap has surcharge, axle upgrade free)',
    '含轮辋价格': 'Price includes wheel rims',
    '自卸车、搅拌车标配': 'Standard for dump trucks and mixer trucks',
    '载货车400mm/1000元': 'Cargo truck: ¥1,000 per 400mm extension',
    '牵引车、泵车无后牵引座，其余车型均标配': 'Standard on all models except tractors and pump trucks',
    '全挂车可选': 'Available for full trailers',
    '需与WABCO四通道/六通道ABS一起选用': 'Must be combined with WABCO 4/6-channel ABS',
    '仅适用于法士特变速箱': 'Fast Gear transmissions only',
    '12档变速箱加价500，仅适用于法士特变速箱': '12-speed transmission +¥500, Fast Gear only',
    'AMT变速箱仅潍柴共轨和康明斯发动机可选，必须带ABS': 'AMT only available with Weichai Common Rail or Cummins engine, ABS required',
    '驱动桥或轴均可选装（全驱车除外），说明计划中无特别说明默认是前后桥都更换': 'Available for drive axle/shaft (excl. AWD). Default: both front & rear if not specified',
    '500马力以下按此执行，500马力以上需考虑分动器差价': 'Applies to ≤500HP; >500HP requires transfer case price adjustment',
    '每根轴或桥加价2000，仅适合标载工况': '+¥2,000 per axle/shaft, standard load only',
    '电控发动机标配定速巡航功能 机械泵发动机不可匹配定速巡航功能': 'Cruise control standard on electronic engines; not available for mechanical pump engines',
    '需同时加装多媒体显示屏': 'Requires multimedia display',
    '简易备胎架加价100': 'Simple spare tire carrier: +¥100',
    '普通50鞍座与低位50鞍座同价，仅港口运输标柜车型可选': 'Same price as low-profile 50 FW; only for port transport standard container models',
    '9JS180与10JSD180同价': '9JS180 & 10JSD180: same price',
    'QH50、QHG50、QHG50B、QHG50C、QD40J同价': 'QH50, QHG50, QHG50B, QHG50C, QD40J: same price',
    'H3000S右舵车型仅体现H3000S外观': 'H3000S RHD models: H3000S exterior only',
    '车辆状态为F3000底盘加偏置驾驶室，非通力偏置矿用自卸车': 'F3000 chassis + offset cab configuration (non-Tongli mining dump)',
    '空气悬架、复合空气悬架可匹配': 'Compatible with air suspension and composite air suspension',
}


def translate_note(note_text):
    """Translate a Chinese note to English."""
    if not note_text:
        return ''
    # Check direct match
    if note_text in NOTE_TRANSLATIONS:
        return NOTE_TRANSLATIONS[note_text]
    return note_text  # Keep original as fallback


def main():
    # Load accessories
    with open(os.path.join(DATA_DIR, 'accessories.json'), 'r', encoding='utf-8') as f:
        accessories = json.load(f)

    translated = 0
    for cat_name, items in accessories.items():
        if not isinstance(items, list):
            continue
        for item in items:
            cn = item['description']
            # Use direct translation if available
            if cn in ITEM_TRANSLATIONS:
                item['description_en'] = ITEM_TRANSLATIONS[cn]
                translated += 1
            else:
                # Fallback: try term-by-term replacement
                en = cn
                # Replace known terms (longer first to avoid partial matches)
                sorted_terms = sorted(TERMS.keys(), key=len, reverse=True)
                for term in sorted_terms:
                    if term in en:
                        en = en.replace(term, TERMS[term])
                item['description_en'] = en

            # Translate note
            if item.get('note'):
                item['note_en'] = translate_note(item['note'])

    print(f'Translated {translated} items with direct mappings')

    # Save
    with open(os.path.join(DATA_DIR, 'accessories.json'), 'w', encoding='utf-8') as f:
        json.dump(accessories, f, ensure_ascii=False, indent=2)

    print(f'Saved {DATA_DIR}/accessories.json')

    # ── Also translate engine swaps ──
    engine_path = os.path.join(DATA_DIR, 'engine_swaps.json')
    with open(engine_path, 'r', encoding='utf-8') as f:
        engines = json.load(f)

    for rule in engines.get('rules', []):
        std = rule.get('standard', '')
        swp = rule.get('swap', '')

        # Translate engine names
        def translate_engine(name):
            if not name:
                return ''
            # Pattern: WP10.380E32
            en = name
            if 'WP' in en:
                en = en.replace('WP', 'Weichai WP')
            if 'ISM' in en:
                en = en.replace('ISM', 'Cummins ISM')
            if 'YC' in en:
                en = en.replace('YC', 'Yuchai YC')
            if 'Euro' in en:
                pass
            elif 'VI' in en:
                en = en + ''
            # Add HP
            for term, eng_term in TERMS.items():
                if term in en and len(term) > 2:
                    en = en.replace(term, eng_term)
            return en

        rule['standard_en'] = translate_engine(std)
        rule['swap_en'] = translate_engine(swp)

    with open(engine_path, 'w', encoding='utf-8') as f:
        json.dump(engines, f, ensure_ascii=False, indent=2)
    print(f'Saved {engine_path}')


if __name__ == '__main__':
    main()
