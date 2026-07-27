"""Fixup: titles and descriptions that weren't replaced due to global brand replace running first"""
import os, re
BASE = os.path.dirname(os.path.abspath(__file__))

fixes = {
    'about.html': {
        '<title>About Us-SAGMOTO</title>': '<title>About Us - SAGMOTO</title>',
        '<meta name="description" content="SAGMOTO About Us Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO is one of the top 10 commercial vehicle brands in China, headquartered in Baoji, Shaanxi. Authorized exporter: Shaanxi Fenghan Trading Co., Ltd. Contact us for factory-direct truck pricing, specifications, and export to Africa, Middle East, Latin America, and Southeast Asia."/>',
        '<meta property="og:title" content="About Us-SAGMOTO"/>': '<meta property="og:title" content="About Us - SAGMOTO"/>',
        '<meta property="og:description" content="SAGMOTO About Us Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO is one of the top 10 commercial vehicle brands in China, headquartered in Baoji, Shaanxi. Authorized exporter: Shaanxi Fenghan Trading Co., Ltd. Contact us for factory-direct truck pricing, specifications, and export to Africa, Middle East, Latin America, and Southeast Asia."/>',
        '<meta name="twitter:title" content="About Us-SAGMOTO"/>': '<meta name="twitter:title" content="About Us - SAGMOTO"/>',
        '<meta name="twitter:description" content="SAGMOTO About Us Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO is one of the top 10 commercial vehicle brands in China, headquartered in Baoji, Shaanxi. Authorized exporter: Shaanxi Fenghan Trading Co., Ltd. Contact us for factory-direct truck pricing, specifications, and export to Africa, Middle East, Latin America, and Southeast Asia."/>',
    },
    'service.html': {
        '<title>Service Policy-SAGMOTO</title>': '<title>Service Policy - SAGMOTO</title>',
        '<meta name="description" content="SAGMOTO Service Policy Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO service policy and after-sales support. Warranty coverage, spare parts supply, technical training, and maintenance services for SAGMOTO commercial vehicles exported worldwide. Authorized distributor: Shaanxi Fenghan Trading."/>',
        '<meta property="og:title" content="Service Policy-SAGMOTO"/>': '<meta property="og:title" content="Service Policy - SAGMOTO"/>',
        '<meta property="og:description" content="SAGMOTO Service Policy Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO service policy and after-sales support. Warranty coverage, spare parts supply, technical training, and maintenance services for SAGMOTO commercial vehicles exported worldwide. Authorized distributor: Shaanxi Fenghan Trading."/>',
        '<meta name="twitter:title" content="Service Policy-SAGMOTO"/>': '<meta name="twitter:title" content="Service Policy - SAGMOTO"/>',
        '<meta name="twitter:description" content="SAGMOTO Service Policy Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO service policy and after-sales support. Warranty coverage, spare parts supply, technical training, and maintenance services for SAGMOTO commercial vehicles exported worldwide. Authorized distributor: Shaanxi Fenghan Trading."/>',
    },
    'video_list.html': {
        '<title>Video Center-SAGMOTO</title>': '<title>Video Center - SAGMOTO</title>',
        '<meta name="description" content="SAGMOTO Video Center Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO video center featuring commercial vehicle product showcases, factory tours, off-road testing, customer testimonials, and industry exhibitions. Watch SAGMOTO trucks in action across global markets."/>',
        '<meta property="og:title" content="Video Center-SAGMOTO"/>': '<meta property="og:title" content="Video Center - SAGMOTO"/>',
        '<meta property="og:description" content="SAGMOTO Video Center Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO video center featuring commercial vehicle product showcases, factory tours, off-road testing, customer testimonials, and industry exhibitions. Watch SAGMOTO trucks in action across global markets."/>',
        '<meta name="twitter:title" content="Video Center-SAGMOTO"/>': '<meta name="twitter:title" content="Video Center - SAGMOTO"/>',
        '<meta name="twitter:description" content="SAGMOTO Video Center Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO video center featuring commercial vehicle product showcases, factory tours, off-road testing, customer testimonials, and industry exhibitions. Watch SAGMOTO trucks in action across global markets."/>',
    },
    'qyc.html': {
        '<title>Tractor-SAGMOTO</title>': '<title>SAGMOTO Tractor Trucks | Heavy-Duty Tractor Head for Export</title>',
        '<meta name="description" content="SAGMOTO Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO tractor trucks for long-haul logistics and heavy transport. Featuring E1st, Z3, X3s tractor heads with Cummins/Yuchai engines, 420-580HP. Factory-direct export pricing from Shaanxi Fenghan Trading to Africa, Middle East, Latin America, CIS."/>',
        '<meta property="og:title" content="Tractor-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Tractor Trucks | Heavy-Duty Tractor Head for Export"/>',
        '<meta property="og:description" content="SAGMOTO Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO tractor trucks for long-haul logistics and heavy transport. Featuring E1st, Z3, X3s tractor heads with Cummins/Yuchai engines, 420-580HP. Factory-direct export pricing from Shaanxi Fenghan Trading to Africa, Middle East, Latin America, CIS."/>',
        '<meta name="twitter:title" content="Tractor-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Tractor Trucks | Heavy-Duty Tractor Head for Export"/>',
        '<meta name="twitter:description" content="SAGMOTO Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO tractor trucks for long-haul logistics and heavy transport. Featuring E1st, Z3, X3s tractor heads with Cummins/Yuchai engines, 420-580HP. Factory-direct export pricing from Shaanxi Fenghan Trading to Africa, Middle East, Latin America, CIS."/>',
    },
    'zxc.html': {
        '<title>Dump truck-SAGMOTO</title>': '<title>SAGMOTO Dump Trucks | Construction & Mining Tipper Trucks</title>',
        '<meta name="description" content="SAGMOTO Dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO dump trucks (tipper trucks) for construction, mining, and earthmoving. Available in 6x4, 8x4 configurations, 25T-90T payload capacity. Models: X1s, X3s, X6, X9, E3. Factory-direct price from Shaanxi Fenghan Trading."/>',
        '<meta property="og:title" content="Dump truck-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Dump Trucks | Construction & Mining Tipper Trucks"/>',
        '<meta property="og:description" content="SAGMOTO Dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO dump trucks (tipper trucks) for construction, mining, and earthmoving. Available in 6x4, 8x4 configurations, 25T-90T payload capacity. Models: X1s, X3s, X6, X9, E3. Factory-direct price from Shaanxi Fenghan Trading."/>',
        '<meta name="twitter:title" content="Dump truck-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Dump Trucks | Construction & Mining Tipper Trucks"/>',
        '<meta name="twitter:description" content="SAGMOTO Dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO dump trucks (tipper trucks) for construction, mining, and earthmoving. Available in 6x4, 8x4 configurations, 25T-90T payload capacity. Models: X1s, X3s, X6, X9, E3. Factory-direct price from Shaanxi Fenghan Trading."/>',
    },
    'zhc.html': {
        '<title>Cargo truck-SAGMOTO</title>': '<title>SAGMOTO Cargo Trucks | Light & Heavy-Duty Freight Vehicles</title>',
        '<meta name="description" content="SAGMOTO Cargo truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO cargo trucks including van trucks, flatbed trucks, stake trucks, and refrigerated trucks. Covering light, medium, and heavy-duty segments. Models: E3, E6, E9, X5, X6, X7, X9. Factory-direct export from Shaanxi Fenghan Trading."/>',
        '<meta property="og:title" content="Cargo truck-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Cargo Trucks | Light & Heavy-Duty Freight Vehicles"/>',
        '<meta property="og:description" content="SAGMOTO Cargo truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO cargo trucks including van trucks, flatbed trucks, stake trucks, and refrigerated trucks. Covering light, medium, and heavy-duty segments. Models: E3, E6, E9, X5, X6, X7, X9. Factory-direct export from Shaanxi Fenghan Trading."/>',
        '<meta name="twitter:title" content="Cargo truck-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Cargo Trucks | Light & Heavy-Duty Freight Vehicles"/>',
        '<meta name="twitter:description" content="SAGMOTO Cargo truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO cargo trucks including van trucks, flatbed trucks, stake trucks, and refrigerated trucks. Covering light, medium, and heavy-duty segments. Models: E3, E6, E9, X5, X6, X7, X9. Factory-direct export from Shaanxi Fenghan Trading."/>',
    },
    'special.html': {
        '<title>Special vehicle-SAGMOTO</title>': '<title>SAGMOTO Special Vehicles | Fire Truck, Garbage Truck & More</title>',
        '<meta name="description" content="SAGMOTO Special vehicle Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO special purpose vehicles: fire trucks, garbage compactors, sewage suction trucks, road sweepers, water tankers, and concrete mixers. Built on proven SAGMOTO chassis. Factory-direct export pricing from Shaanxi Fenghan Trading."/>',
        '<meta property="og:title" content="Special vehicle-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Special Vehicles | Fire Truck, Garbage Truck & More"/>',
        '<meta property="og:description" content="SAGMOTO Special vehicle Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO special purpose vehicles: fire trucks, garbage compactors, sewage suction trucks, road sweepers, water tankers, and concrete mixers. Built on proven SAGMOTO chassis. Factory-direct export pricing from Shaanxi Fenghan Trading."/>',
        '<meta name="twitter:title" content="Special vehicle-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Special Vehicles | Fire Truck, Garbage Truck & More"/>',
        '<meta name="twitter:description" content="SAGMOTO Special vehicle Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO special purpose vehicles: fire trucks, garbage compactors, sewage suction trucks, road sweepers, water tankers, and concrete mixers. Built on proven SAGMOTO chassis. Factory-direct export pricing from Shaanxi Fenghan Trading."/>',
    },
    'tzc.html': {
        '<title>Off-road truck-SAGMOTO</title>': '<title>SAGMOTO Off-Road Trucks | 4x4 & All-Wheel Drive Vehicles</title>',
        '<meta name="description" content="SAGMOTO Off-road truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO off-road trucks built for extreme terrain: mining, oil fields, desert operations. 4x4 and 6x6 all-wheel drive configurations. Heavy-duty chassis with high ground clearance. Factory-direct export from Shaanxi Fenghan Trading to global markets."/>',
        '<meta property="og:title" content="Off-road truck-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Off-Road Trucks | 4x4 & All-Wheel Drive Vehicles"/>',
        '<meta property="og:description" content="SAGMOTO Off-road truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO off-road trucks built for extreme terrain: mining, oil fields, desert operations. 4x4 and 6x6 all-wheel drive configurations. Heavy-duty chassis with high ground clearance. Factory-direct export from Shaanxi Fenghan Trading to global markets."/>',
        '<meta name="twitter:title" content="Off-road truck-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Off-Road Trucks | 4x4 & All-Wheel Drive Vehicles"/>',
        '<meta name="twitter:description" content="SAGMOTO Off-road truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO off-road trucks built for extreme terrain: mining, oil fields, desert operations. 4x4 and 6x6 all-wheel drive configurations. Heavy-duty chassis with high ground clearance. Factory-direct export from Shaanxi Fenghan Trading to global markets."/>',
    },
    'pzkyzyc.html': {
        '<title>Off-road dump truck-SAGMOTO</title>': '<title>SAGMOTO Off-Road Mining Dump Trucks | Heavy-Duty Tipper</title>',
        '<meta name="description" content="SAGMOTO Off-road dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO off-road mining dump trucks for large-scale earthmoving and open-pit mining operations. Heavy-duty construction with reinforced chassis, high-torque powertrain. Available in multiple configurations. Factory-direct export pricing from Shaanxi Fenghan Trading."/>',
        '<meta property="og:title" content="Off-road dump truck-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Off-Road Mining Dump Trucks | Heavy-Duty Tipper"/>',
        '<meta property="og:description" content="SAGMOTO Off-road dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO off-road mining dump trucks for large-scale earthmoving and open-pit mining operations. Heavy-duty construction with reinforced chassis, high-torque powertrain. Available in multiple configurations. Factory-direct export pricing from Shaanxi Fenghan Trading."/>',
        '<meta name="twitter:title" content="Off-road dump truck-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Off-Road Mining Dump Trucks | Heavy-Duty Tipper"/>',
        '<meta name="twitter:description" content="SAGMOTO Off-road dump truck Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO off-road mining dump trucks for large-scale earthmoving and open-pit mining operations. Heavy-duty construction with reinforced chassis, high-torque powertrain. Available in multiple configurations. Factory-direct export pricing from Shaanxi Fenghan Trading."/>',
    },
    'pzmtc.html': {
        '<title>Off-road Tractor-SAGMOTO</title>': '<title>SAGMOTO Off-Road Tractor Trucks | Heavy Haul Transport</title>',
        '<meta name="description" content="SAGMOTO Off-road Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="description" content="SAGMOTO off-road tractor trucks for heavy-haul and extreme condition transport. Built for oil fields, mining sites, and infrastructure projects. High-power engines with heavy-duty drivetrain. Factory-direct export from Shaanxi Fenghan Trading."/>',
        '<meta property="og:title" content="Off-road Tractor-SAGMOTO"/>': '<meta property="og:title" content="SAGMOTO Off-Road Tractor Trucks | Heavy Haul Transport"/>',
        '<meta property="og:description" content="SAGMOTO Off-road Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta property="og:description" content="SAGMOTO off-road tractor trucks for heavy-haul and extreme condition transport. Built for oil fields, mining sites, and infrastructure projects. High-power engines with heavy-duty drivetrain. Factory-direct export from Shaanxi Fenghan Trading."/>',
        '<meta name="twitter:title" content="Off-road Tractor-SAGMOTO"/>': '<meta name="twitter:title" content="SAGMOTO Off-Road Tractor Trucks | Heavy Haul Transport"/>',
        '<meta name="twitter:description" content="SAGMOTO Off-road Tractor Founded in 1968, Shaanxi Automobile Holding Group Company currently employs 32,000 staff with total assets of 34.8 billion CNY. "/>':
        '<meta name="twitter:description" content="SAGMOTO off-road tractor trucks for heavy-haul and extreme condition transport. Built for oil fields, mining sites, and infrastructure projects. High-power engines with heavy-duty drivetrain. Factory-direct export from Shaanxi Fenghan Trading."/>',
    },
}

count = 0
for filename, replacements in fixes.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filename} not found")
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
        else:
            print(f"  [WARN] {filename}: '{old[:60]}...' not found")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [FIXED] {filename}")

print(f"\nTotal replacements: {count}")
