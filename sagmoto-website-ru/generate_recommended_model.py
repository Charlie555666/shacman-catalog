import json
import os

# Output path
output_dir = r"c:/Users/Administrator/WorkBuddy/20260605101515/shacman-catalog/sagmoto-website"

# Product data from original sagmoto.com HTML
tabs = [
    {
        "name": "Light Duty Truck",
        "products": [
            {
                "name": "X9 4X4 Dump Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3f35ad3a-2ea6-42cb-bb86-2af2c12a16e7.jpg",
                "desc": [
                    "4×4, All wheel drive, Leaf-springs suspension, main and sub-springs' structure, strong bearing capacity, simple structure, low maintenance cost.",
                    "The front and rear suspensions are strictly matched, supplemented by front and rear dampers to ensure loading capacity and improve comfort.",
                    "Extra-long service intervals for engine, gearbox and rear axle, halving the number of 'pit stop'."
                ]
            },
            {
                "name": "X9 Tow truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a2e376e5-bc63-4f1c-9379-cbef769fe0eb.jpg",
                "desc": [
                    "Maximum gradient of over 30%, easy to cope with the tough working conditions.",
                    "Easy to cope with the tough working conditions.",
                    ""
                ]
            },
            {
                "name": "X7 Flatbed Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/57b40134-f17a-4635-9862-4918881781b5.png",
                "desc": [
                    "Semi-floating cab + main driver's airbag shock-absorbing seat reduces driving fatigue and improves driving comfort.",
                    "The instrumentation adopts the design of pointer plus LCD display, which can read the vehicle driving data directly and clearly.",
                    "Fully wrapped airline seats, all-round fit for the lower back, cushion optimized sponge density, balancing soft and hard for more comfortable."
                ]
            },
            {
                "name": "9 Series Sweeper",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8cd0ebb8-92b2-4dcf-a200-ffbc21fffe71.jpg",
                "desc": [
                    "",
                    "",
                    ""
                ]
            }
        ]
    },
    {
        "name": "Medium Duty Truck",
        "products": [
            {
                "name": "X6 Dropside Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png",
                "desc": [
                    "Minimum ground clearance 314mm, approach angle greater than 25°.",
                    "Configured with airbag shock-absorbing main seat, the widest part of the lower sleeper reaches 85 cm.",
                    "Highly efficient optimization of the new transmission system + maintenance-free high-efficiency drive axles + special low-rolling resistance tires, result in lower fuel consumption for the whole vehicle."
                ]
            },
            {
                "name": "X6 AWD Cargo truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9b7254c2-82fe-49dc-b3de-36d66fc0bdd2.jpg",
                "desc": [
                    "4×4 All wheel drive",
                    "",
                    ""
                ]
            },
            {
                "name": "X6 Cement Mixers Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a9351ff3-e79c-44f1-b08f-a7bb8659d32f.png",
                "desc": [
                    "Flexible, Lightweight and Powerful",
                    "Short wheelbase design chassis, can be equipped with shortened axle, with smaller turning radius.",
                    "Modular weight reduction design, aluminum alloy, high-strength profiles."
                ]
            },
            {
                "name": "X6 Sprinkler Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/69a018d4-9ea8-4478-911c-d37afa898d10.png",
                "desc": [
                    "Lightweight design",
                    "Beautiful and practical M3000 cab, with a sedan-like interior",
                    "lightweight-design chassis, frame beam, suspension"
                ]
            }
        ]
    },
    {
        "name": "Heavy Duty Truck",
        "products": [
            {
                "name": "E1st Tractor",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a1ce2f36-8b3d-4d84-b199-0f997ac5b93f.jpg",
                "desc": [
                    "Cummins engine+Eaton AMT gearbox, Hande maintenance-free axle integrated exclusive power chain design, with a maximum output of 560 horsepower",
                    "Brand-new cab modeling design, optimization technology of vehicle external flow field (CFD), smooth adjustment of top air deflector, achieving optimal main+trailer matching, whole vehicle drag coefficient of 0.45, and fuel consumption of 26.97L per 100km.",
                    "The cab adopts the design concept of intelligent seat, with a flat floor design and an internal height of 2m 13, which provides ample space for drivers and passengers."
                ]
            },
            {
                "name": "Z3 Tractor Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/63331455-dd49-4dd2-8570-179c3127fc08.jpg",
                "desc": [
                    "The new powertrain, intelligent electronic system and driving environment provide customers with efficient, fast, and clean logistics experience.",
                    "The high-strength cab design complies with the latest European safety standards and provides strong protection for driver and passengers.",
                    "The flat-floor design and spacious interior make it possible to stand and walk in the cab without any obstacles."
                ]
            },
            {
                "name": "X3s Trailer Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/70f1e68f-95be-4336-9449-5dbe2e82e895.png",
                "desc": [
                    "",
                    "",
                    ""
                ]
            },
            {
                "name": "E3 Tractor Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/4ed9de22-91e5-4290-8c61-65f41329d720.jpg",
                "desc": [
                    "Equipped with dual warning system to ensure driving safety.",
                    "Efficient power chain, excellent chassis configuration for better operation.",
                    "The width of the berth reaches 850mm, and the distance between the upper and lower berths is 800mm for more comfortable rest."
                ]
            }
        ]
    },
    {
        "name": "Special Vehicle",
        "products": [
            {
                "name": "X9 Aerial Work Platform Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0c12b07d-79ed-4ed7-90af-72345564bbe7.jpg",
                "desc": [
                    "The truck has strong stability, convenient operation, flexible mobility, and is suitable for places with a wide range of work surfaces.",
                    "Adopting multi-level telescopic arms, with a large operating range and fast lifting speed.",
                    "Using high-strength materials and high-precision technology, the cab is equipped with multiple safety protection systems."
                ]
            },
            {
                "name": "X7 Concrete Mixer Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64a47e38-5f9e-4677-9389-1291e77e33e1.jpg",
                "desc": [
                    "High strength wear-resistant steel, reliable hydraulic system.",
                    "Reinforced multi-leaf springs, high strength and rigidity double-layer chassis, easy to cope with complex working conditions.",
                    "Main Rear View Mirror + Supplemental Blind Mirror to reduce the driver's visual blind spot."
                ]
            },
            {
                "name": "9 Series",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/62043e16-ed96-418e-b4c8-359b96e711f8.jpg",
                "desc": [
                    "Durability, high performance, and high load-bearing capacity.",
                    "Multiple of cabs are available for selection.",
                    "Convenient to adapt to all kinds of fuel tankers, sprinklers, dump trucks."
                ]
            },
            {
                "name": "7 Series",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/7b161d41-69b0-46c4-ad52-3a69558bcb0a.jpg",
                "desc": [
                    "Powerful engine, excellent maneuverability.",
                    "Reinforced oil pan protection grill.",
                    "Double-layer frame design."
                ]
            }
        ]
    },
    {
        "name": "Off-road Truck",
        "products": [
            {
                "name": "Off-road Dump Truck",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg",
                "desc": [
                    "Adopting 850 wide-chassis structure, stable performance and adaptable to poor road conditions.",
                    "Specialized rear suspension for mining, flattening load increased from 25.3T to 30.5T.",
                    "The exhaust tailpipe is designed to be directionally adjustable, effectively avoiding downward exhaust blowing up dust on the ground and affecting the driver's visibility."
                ]
            },
            {
                "name": "6 Series",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8065c0e4-5d81-4f00-97c1-6026bc4ef78c.jpg",
                "desc": [
                    "Strong Power and Efficient Transportation.",
                    "Reinforced Design, Iron bumper.",
                    "Customized Upper-body."
                ]
            },
            {
                "name": "X7 Mixer",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/c98399ce-d138-4d6d-b27c-bfddda9aa601.jpg",
                "desc": [
                    "High strength wear-resistant steel, reliable hydraulic system.",
                    "Reinforced multi-leaf springs, high strength and rigidity double-layer chassis.",
                    "Main Rear View Mirror + Supplemental Blind Mirror to reduce the driver's visual blind spot."
                ]
            },
            {
                "name": "X7 Special Vehicle",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a174fdcc-3ffd-4bc0-b84c-57b9499d20a7.jpg",
                "desc": [
                    "Powerful engine, excellent maneuverability.",
                    "Reinforced oil pan protection grill.",
                    "Double-layer frame design."
                ]
            }
        ]
    },
    {
        "name": "New Energy",
        "products": [
            {
                "name": "i9",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png",
                "desc": [
                    "Integrated electric drive axle, highly integrated structure, higher efficiency, increased in range.",
                    "Working range of 430km, support 120KW fast charging technology, 65 minutes to achieve fully charging.",
                    "Brake energy recovery technology, which reduces energy consumption by approximately 15%."
                ]
            },
            {
                "name": "i9 Lite",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2736f8a9-4674-4ae8-bda2-ff995e34c894.png",
                "desc": [
                    "Lightweight design, high energy density battery pack.",
                    "Efficient motor drive system, low energy consumption.",
                    "Smart energy management system, longer range."
                ]
            },
            {
                "name": "E9 Electric",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/3ca8f8b2-cf60-437e-999d-065aeae34090.png",
                "desc": [
                    "Zero emissions, green transportation.",
                    "High efficiency motor, lower operating cost.",
                    "Intelligent charging system, fast charging support."
                ]
            },
            {
                "name": "X9 Electric",
                "img": "https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/96c10ebb-4397-4a1f-844d-04c182f7dc46.png",
                "desc": [
                    "Pure electric drive, no emissions.",
                    "High capacity battery, long range.",
                    "Smart driving assistance system."
                ]
            }
        ]
    }
]

# Generate HTML for the product tabs section
html_parts = []

html_parts.append('<!-- ===== RECOMMENDED MODEL (tabs + 4-column grid) ===== -->')
html_parts.append('<div class="recommended-model" id="recommended">')
html_parts.append('    <h2 class="section-title">Recommended Model</h2>')
html_parts.append('    <div class="tab-wrapper">')
html_parts.append('        <div class="tab-list">')
for i, tab in enumerate(tabs):
    active = 'active' if i == 0 else ''
    html_parts.append(f'            <span class="tab-item {active}" data-tab="tab{i}">{tab["name"]}</span>')
html_parts.append('        </div>')
html_parts.append('        <div class="tab-content-wrapper">')
for i, tab in enumerate(tabs):
    active = 'active' if i == 0 else ''
    html_parts.append(f'        <div class="tab-content {active}" id="tab{i}">')
    html_parts.append('            <div class="product-grid-4">')
    for j, prod in enumerate(tab['products']):
        html_parts.append('                <div class="product-grid-item">')
        html_parts.append('                    <div class="pg-img">')
        html_parts.append(f'                        <a href="products.html"><img src="{prod["img"]}" alt="{prod["name"]}" onerror="this.style.display=\'none\'"></a>')
        html_parts.append('                    </div>')
        html_parts.append('                    <div class="pg-body">')
        html_parts.append(f'                        <h4><a href="products.html">{prod["name"]}</a></h4>')
        for k, d in enumerate(prod['desc']):
            if d.strip():
                html_parts.append(f'                        <p class="pg-desc pg-desc{k+1}">{d}</p>')
        html_parts.append('                        <a href="products.html" class="pg-plus">+</a>')
        html_parts.append('                    </div>')
        html_parts.append('                </div>')
    html_parts.append('            </div>')
    html_parts.append('        </div>')
html_parts.append('        </div>')
html_parts.append('    </div>')
html_parts.append('</div>')

html = '\n'.join(html_parts)

# Save to file
with open(os.path.join(output_dir, 'recommended_model_section.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated recommended_model_section.html")
print(f"Total tabs: {len(tabs)}, Total products: {sum(len(t['products']) for t in tabs)}")
print(f"Saved to: {os.path.join(output_dir, 'recommended_model_section.html')}")
