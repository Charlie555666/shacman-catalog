#!/usr/bin/env python3
"""
SAGMOTO Website - Full Russian Translation Script
Translates all HTML pages, JS files, and JSON data from English to Russian.
"""
import os, re, json

BASE = r'c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website-ru'

# ============================================================
# COMPREHENSIVE ENGLISH → RUSSIAN TRANSLATION MAP
# ============================================================

TRANSLATIONS = {
    # === NAVIGATION MENU ===
    "PRODUCTS": "ПРОДУКЦИЯ",
    "APPLICATIONS": "ПРИМЕНЕНИЕ",
    "SERVICES": "СЕРВИС",
    "NEWS": "НОВОСТИ",
    "ABOUT US": "О НАС",
    "CONTACT US": "КОНТАКТЫ",
    "Service Policy": "Сервисная политика",
    "Find Your Service Provider": "Найти поставщика услуг",
    "Maintenance Service": "Техническое обслуживание",
    "Driving reminder": "Памятка водителю",
    "Safe Driving": "Безопасное вождение",

    # === PRODUCT CATEGORIES ===
    "Light Duty Truck": "Лёгкие грузовики",
    "Medium Duty Truck": "Средние грузовики",
    "Heavy Duty Truck": "Тяжёлые грузовики",
    "Off-road Truck": "Внедорожные грузовики",
    "Off-road Dump": "Внедорожный самосвал",
    "Off-road Dump Truck": "Внедорожный самосвал",
    "Tractor": "Тягачи",
    "Dump Truck": "Самосвалы",
    "Cargo Truck": "Грузовики",
    "Special Vehicle": "Спецтехника",
    "New Energy": "Новая энергия",
    "Newenergy Truck": "Электрогрузовики",

    # === PAGE HEADERS & TITLES ===
    "Home": "Главная",
    "Products": "Продукция",
    "News Centre": "Новостной центр",
    "Video Center": "Видеоцентр",
    "OUR VIDEO CONTENT": "НАШИ ВИДЕОМАТЕРИАЛЫ",
    "About Us": "О нас",
    "Privacy Policy": "Политика конфиденциальности",
    "Terms of Use": "Условия использования",
    "Service Policy-SAG Commercial Vehicle Company": "Сервисная политика — SAG Commercial Vehicle Company",
    "Find your service provider": "Найти поставщика услуг",
    "Maintenance service": "Техническое обслуживание",
    "Driving reminder-SAG Commercial Vehicle Company": "Памятка водителю — SAG Commercial Vehicle Company",
    "Safe Driving-SAG Commercial Vehicle Company": "Безопасное вождение — SAG Commercial Vehicle Company",

    # === PAGE TITLES ===
    "Shaanxi Fenghan Trading — Authorized SAGMOTO Exporter": "Shaanxi Fenghan Trading — Авторизованный экспортёр SAGMOTO",
    "About Us-SAG Commercial Vehicle Company": "О нас — SAG Commercial Vehicle Company",
    "Contact Us - SAGMOTO": "Контакты — SAGMOTO",
    "Products - SAGMOTO": "Продукция — SAGMOTO",
    "News - SAGMOTO": "Новости — SAGMOTO",
    "New Energy - SAGMOTO": "Новая энергия — SAGMOTO",
    "Off-road 4x4 Series - SAGMOTO": "Внедорожная серия 4x4 — SAGMOTO",
    "E1st Flagship Tractor Truck - SAGMOTO": "Флагманский тягач E1st — SAGMOTO",
    "E3 Series - SAGMOTO": "Серия E3 — SAGMOTO",
    "E6 Series - SAGMOTO": "Серия E6 — SAGMOTO",
    "E9 Series - SAGMOTO": "Серия E9 — SAGMOTO",
    "i5 Series Electric Commercial Vehicle - SAGMOTO": "Электрогрузовик серии i5 — SAGMOTO",
    "i9 Series - SAGMOTO": "Серия i9 — SAGMOTO",
    "X3s Series - SAGMOTO": "Серия X3s — SAGMOTO",
    "X5 Series Medium Duty Truck - SAGMOTO": "Среднетоннажный грузовик серии X5 — SAGMOTO",
    "X6 Series - SAGMOTO": "Серия X6 — SAGMOTO",
    "X7 Series - SAGMOTO": "Серия X7 — SAGMOTO",
    "X9 Series - SAGMOTO": "Серия X9 — SAGMOTO",
    "Z3 Conventional Tractor Truck - SAGMOTO": "Классический тягач Z3 — SAGMOTO",
    "Tractor-SAG Commercial Vehicle Company": "Тягачи — SAG Commercial Vehicle Company",
    "Dump truck-SAG Commercial Vehicle Company": "Самосвалы — SAG Commercial Vehicle Company",
    "Cargo truck-SAG Commercial Vehicle Company": "Грузовики — SAG Commercial Vehicle Company",
    "Special vehicle-SAG Commercial Vehicle Company": "Спецтехника — SAG Commercial Vehicle Company",
    "Off-road truck-SAG Commercial Vehicle Company": "Внедорожные грузовики — SAG Commercial Vehicle Company",
    "Off-road dump truck -SAG Commercial Vehicle Company": "Внедорожный самосвал — SAG Commercial Vehicle Company",
    "Off-road Tractor-SAG Commercial Vehicle Company": "Внедорожный тягач — SAG Commercial Vehicle Company",
    "News-SAG Commercial Vehicle Company": "Новости — SAG Commercial Vehicle Company",

    # === Index Page ===
    "GET THE LATEST INFORMATION": "ПОСЛЕДНИЕ НОВОСТИ",
    "Discover what's happening at SAGMOTO — from product launches to industry insights.": "Узнайте, что происходит в SAGMOTO — от запуска продуктов до отраслевых новостей.",
    "Get the latest information": "Последние новости",
    "VIEW ALL NEWS": "ВСЕ НОВОСТИ",
    "VIDEO CENTRE": "ВИДЕОЦЕНТР",
    "OUR VIDEOS": "НАШИ ВИДЕО",
    "Watch SAGMOTO vehicles in action — real-world performance, product demos, and more.": "Смотрите автомобили SAGMOTO в действии — реальная производительность, демонстрации продуктов и многое другое.",
    "VIEW ALL VIDEOS": "ВСЕ ВИДЕО",
    "WATCH VIDEO": "СМОТРЕТЬ ВИДЕО",
    "Ready to discuss your fleet requirements?": "Готовы обсудить потребности вашего автопарка?",
    "Contact our sales team for a customized quotation and delivery timeline.": "Свяжитесь с нашим отделом продаж для индивидуального предложения и сроков поставки.",
    "GET IN TOUCH": "СВЯЗАТЬСЯ С НАМИ",
    "Explore Our Product Range": "Ознакомьтесь с нашей продукцией",
    "Recommended Models": "Рекомендуемые модели",

    # === Product Tab Categories ===
    "Tractor Truck": "Тягачи",
    "Dump Trucks": "Самосвалы",
    "Cargo Trucks": "Грузовики",
    "Special Purpose": "Спецтехника",
    "Off-Road Series": "Внедорожная серия",
    "New Energy": "Электромобили",

    # === Category Labels ===
    "All": "Все",
    "Light Duty": "Лёгкие",
    "Medium Duty": "Средние",
    "Heavy Duty": "Тяжёлые",
    "Off-road": "Внедорожные",
    "Special": "Спецтехника",

    # === Product Names (descriptive parts) ===
    "X9 4X4 Dump Truck": "X9 4×4 Самосвал",
    "X9 Tow truck": "X9 Эвакуатор",
    "X7 Flatbed Truck": "X7 Бортовой грузовик",
    "9 Series Sweeper": "9-я серия Подметальная машина",
    "X6 Dropside Truck": "X6 Бортовой грузовик",
    "X6 AWD Cargo truck": "X6 Полноприводный грузовик",
    "X6 Sprinkler Truck": "X6 Поливомоечная машина",
    "E1st Tractor": "E1st Тягач",
    "Z3 Tractor Truck": "Z3 Тягач",
    "X3s Trailer Truck": "X3s Тягач",
    "E3 Tractor Truck": "E3 Тягач",
    "X9 Aerial work platform truck": "X9 Автовышка",
    "X9 Tow truck": "X9 Эвакуатор",
    "X7 Concrete Mixer Truck": "X7 Автобетоносмеситель",
    "X3s Mixer trucks 8X4": "X3s Автобетоносмеситель 8×4",
    "9 series": "9-я серия",
    "7 Series": "7-я серия",
    "6 Series": "6-я серия",
    "Off-road Dump Truck": "Внедорожный самосвал",
    "i5 compressor car": "i5 Мусоровоз",

    # === Product Specs ===
    "4x4 All Wheel Drive": "4×4 Полный привод",
    "Recovery Vehicle": "Эвакуатор",
    "Flatbed": "Бортовой",
    "Dropside": "Бортовой с откидными бортами",
    "Municipal": "Коммунальный",
    "Water Sprinkler": "Поливомоечный",
    "Cummins Z14 560HP": "Cummins Z14 560 л.с.",
    "Cummins M13 520HP": "Cummins M13 520 л.с.",
    "Cummins ISME 420": "Cummins ISME 420 л.с.",
    "Yuchai 340-400HP": "Yuchai 340-400 л.с.",
    "Multi-Level Telescopic Arms": "Многосекционная телескопическая стрела",
    "Elevated Operations": "Высотные работы",
    "Heavy-Duty Winch": "Тяжёлая лебёдка",
    "High Strength Steel": "Высокопрочная сталь",
    "Reliable Hydraulic System": "Надёжная гидравлическая система",
    "Durability & High Performance": "Надёжность и высокая производительность",
    "Extreme Conditions": "Экстремальные условия",
    "Powerful Engine": "Мощный двигатель",
    "Excellent Maneuverability": "Отличная манёвренность",
    "Strong Power": "Высокая мощность",
    "Efficient Transportation": "Эффективная транспортировка",
    "All Wheel Drive": "Полный привод",

    # === Product specs truncated ===
    "4.5T<=GCW<=25T": "4,5Т≤ПММ≤25Т",
    "12T<=GCW<=60T": "12Т≤ПММ≤60Т",
    "18T<=GCW<=100T": "18Т≤ПММ≤100Т",

    # === Spec table labels ===
    "All Wheel drive": "Полный привод",
    "Leaf-springs suspension, main and sub-springs’structure, strong bearing capacity, simple structure, low maintenance cost.":
        "Рессорная подвеска, основная и дополнительная рессоры, высокая несущая способность, простая конструкция, низкие затраты на обслуживание.",
    "The front and rear suspensions are strictly matched, supplemented by front and rear dampers to ensure loading capacity and improve comfort.":
        "Передняя и задняя подвески строго согласованы, дополнены амортизаторами для обеспечения грузоподъёмности и повышения комфорта.",
    "Extra-long service intervals for engine, gearbox and rear axle, halving the number of \u2018pit stop\u2019.":
        "Увеличенные интервалы обслуживания двигателя, коробки передач и заднего моста, вдвое сокращающие количество заездов на техобслуживание.",
    "Maximum gradient of over 30%, easy to cope with the tough working conditions":
        "Максимальный уклон более 30%, легко справляется со сложными условиями эксплуатации",
    "Easy to cope with the tough working conditions":
        "Легко справляется со сложными условиями эксплуатации",
    "Semi-floating cab + main driver's airbag shock-absorbing seat reduces driving fatigue and improves driving comfort.":
        "Полуподвесная кабина + сиденье водителя с пневмоподвеской снижает утомляемость и повышает комфорт вождения.",
    "The instrumentation adopts the design of pointer plus LCD display, which can read the vehicle driving data directly and clearly.":
        "Приборная панель сочетает стрелочные указатели и ЖК-дисплей, обеспечивая прямое и чёткое считывание данных автомобиля.",
    "Fully wrapped airline seats, all-round fit for the lower back, cushion optimized sponge density, balancing soft and hard for more comfortable.":
        "Полностью охватывающие сиденья авиационного типа, полная поддержка поясницы, оптимизированная плотность подушки для баланса жёсткости и комфорта.",
    "Efficient street sweeper with high-capacity debris collection system. Designed for urban road maintenance with powerful sweeping and dust suppression capabilities. Smart sanitation solution for modern cities.":
        "Эффективная подметальная машина с системой сбора мусора большой ёмкости. Разработана для обслуживания городских дорог с мощными возможностями подметания и пылеподавления. Интеллектуальное решение для современных городов.",
    "Minimum ground clearance 314mm, approach angle greater than 25\u00b0.":
        "Минимальный дорожный просвет 314 мм, угол въезда более 25\u00b0.",
    "Highly efficient optimization of the new transmission system + maintenance-free high-efficiency drive axles + special low-rolling resistance tires, result in lower fuel consumption for the whole vehicle":
        "Высокоэффективная оптимизация новой трансмиссии + необслуживаемые ведущие мосты + специальные шины с низким сопротивлением качению обеспечивают низкий расход топлива",
    "Configured with airbag shock-absorbing main seat, the widest part of the lower sleeper reaches 85 cm.":
        "Сиденье водителя с пневмоподвеской, ширина нижнего спального места достигает 85 см.",
    "Flexible, Lightweight and Powerful":
        "Гибкий, лёгкий и мощный",
    "Modular weight reduction design, aluminum alloy, high-strength profiles":
        "Модульная конструкция снижения веса, алюминиевые сплавы, высокопрочные профили",
    "Short wheelbase design chassis, can be equipped with shortened axle, with smaller turning radius":
        "Шасси с короткой колёсной базой, может оснащаться укороченным мостом с меньшим радиусом разворота",
    "Lightweight design":
        "Облегчённая конструкция",
    "lightweight-design chassis,  frame beam, suspension":
        "облегчённое шасси, рама, подвеска",
    "Beautiful and practical M3000 cab, with a sedan-like interior":
        "Красивая и практичная кабина M3000 с интерьером легкового уровня",
    "Cummins engine+Eaton AMT gearbox, Hande maintenance-free axle integrated exclusive power chain design, with a maximum output of 560 horsepower":
        "Двигатель Cummins + АМТ Eaton, необслуживаемый мост Hande, эксклюзивная силовая цепь с максимальной мощностью 560 л.с.",
    "The cab adopts the design concept of intelligent seat, with a flat floor design and an internal height of 2m 13, which provides ample space for drivers and passengers":
        "Кабина с концепцией интеллектуального сиденья, ровный пол и внутренняя высота 2,13 м, обеспечивающая простор для водителя и пассажиров",
    "Brand-new cab modeling design, optimization technology of vehicle external flow field (CFD), smooth adjustment of top air deflector, achieving optimal main+trailer matching, whole vehicle drag coefficient of 0.45, and fuel consumption of 26.97L per 100":
        "Новый дизайн кабины, оптимизация внешней аэродинамики (CFD), регулируемый верхний спойлер, оптимальное сочетание тягача и прицепа, коэффициент лобового сопротивления 0,45, расход топлива 26,97 л/100 км",
    "The new powertrain, intelligent electronic system and driving environment provide customers with efficient, fast, and clean logistics experience.":
        "Новая силовая установка, интеллектуальная электронная система и среда вождения обеспечивают эффективную, быструю и экологичную логистику.",
    "The flat-floor design and spacious interior make it possible to stand and walk in the cab without any obstacles.":
        "Ровный пол и просторный интерьер позволяют стоять и передвигаться в кабине без препятствий.",
    "The high-strength cab design complies with the latest European safety standards and provides strong protection for driver and passengers.":
        "Высокопрочная конструкция кабины соответствует новейшим европейским стандартам безопасности и обеспечивает надёжную защиту водителя и пассажиров.",
    "Versatile heavy duty tractor with excellent power-to-weight ratio. Ideal for regional and inter-city transport with balanced performance, reliability, and operating economy.":
        "Универсальный тяжёлый тягач с отличным соотношением мощности к весу. Идеален для региональных и междугородних перевозок со сбалансированной производительностью, надёжностью и экономичностью.",
    "Cab strength meets the latest European ECER29-03 collision standard.":
        "Прочность кабины соответствует новейшему европейскому стандарту ECER29-03.",
    "Equipped with dual warning system to ensure driving safety.":
        "Оснащён двойной системой предупреждения для обеспечения безопасности вождения.",
    "The width of the berth reaches 850mm, and the distance between the upper and lower berths is 800mm for more comfortable rest.":
        "Ширина спального места достигает 850 мм, расстояние между верхним и нижним спальным местом — 800 мм для комфортного отдыха.",
    "Efficient power chain, excellent chassis configuration for better operation.":
        "Эффективная силовая цепь, отличная конфигурация шасси для лучшей эксплуатации.",
    "The truck has strong stability,convenient operation, flexible mobility, and is suitable for places with a wide range of work surfaces":
        "Автомобиль обладает высокой устойчивостью, удобным управлением, гибкой мобильностью и подходит для широкого спектра рабочих площадок",
    "Using high-strength materials and high-precision technology, the cab is equipped with multiple safety protection systems":
        "Использование высокопрочных материалов и высокоточных технологий, кабина оснащена множественными системами безопасности",
    "Adopting multi-level telescopic arms, with a large operating range and fast lifting speed":
        "Многосекционная телескопическая стрела с большим рабочим диапазоном и высокой скоростью подъёма",
    "High strength wear-resistant steel, reliable hydraulic system.":
        "Высокопрочная износостойкая сталь, надёжная гидравлическая система.",
    "Main Rear View Mirror + Supplemental Blind Mirror to reduce the driver's visual blind spot.":
        "Основное зеркало заднего вида + дополнительное зеркало слепых зон для уменьшения мёртвых зон водителя.",
    "Reinforced multi-leaf springs, high strength and rigidity double-layer chassis, easy to cope with complex working conditions.":
        "Усиленные многолистовые рессоры, двухслойное шасси высокой прочности и жёсткости, легко справляется со сложными условиями работы.",
    "durability, high performance, and high load-bearing capacity":
        "надёжность, высокая производительность и грузоподъёмность",
    "multiple of cabs are available for selection":
        "доступны различные варианты кабин",
    "Convenient to adapt to all kinds of fuel tankers, sprinklers, dump trucks":
        "Удобная адаптация для бензовозов, поливомоечных машин, самосвалов",
    "powerful engine, excellent maneuverability":
        "мощный двигатель, отличная манёвренность",
    "Reinforced oil pan protection grill":
        "Усиленная защитная решётка масляного поддона",
    "Double-layer frame design":
        "Двухслойная конструкция рамы",
    "Strong Power and Efficient Transportation":
        "Высокая мощность и эффективная транспортировка",
    "Reinforced Design, Iron bumper":
        "Усиленная конструкция, железный бампер",
    "Customized Upper-body":
        "Индивидуальная надстройка",
    "Adopting 850 wide-chassis structure, stable performance and adaptable to poor road conditions.":
        "Широкая рама 850 мм, стабильная работа и адаптация к плохим дорожным условиям.",
    "Specialized rear suspension for mining, flattening load increased from 25.3T to 30.5T.":
        "Специализированная задняя подвеска для горных работ, грузоподъёмность увеличена с 25,3Т до 30,5Т.",
    "The exhaust tailpipe is designed to be directionally adjustable, effectively avoiding downward exhaust blowing up dust on the ground and affecting the driver's visibility.":
        "Выхлопная труба с регулируемым направлением, эффективно предотвращает поднятие пыли выхлопными газами и ухудшение видимости водителя.",
    "Integrated electric drive axle, highly integrated structure, higher efficiency, increased in range.":
        "Интегрированный электрический ведущий мост, высокоинтегрированная конструкция, повышенная эффективность, увеличенный запас хода.",
    "Working range of 430km, support 120KW fast charging technology, 65 minutes to achieve fully charging.":
        "Запас хода 430 км, поддержка быстрой зарядки 120 кВт, полная зарядка за 65 минут.",
    "Brake energy recovery technology, which reduces energy consumption by approximately 15%.":
        "Технология рекуперации энергии торможения, снижающая энергопотребление примерно на 15%.",

    # === Footer ===
    "FOLLOW US": "ПОДПИСЫВАЙТЕСЬ",
    "Scan to visit our mobile site": "Отсканируйте для посещения мобильного сайта",
    "All Rights Reserved": "Все права защищены",
    "Sitemap": "Карта сайта",
    "Address:": "Адрес:",

    # === About page company name in footer copyright ===
    "SAGMOTO | 陕汽集团商用车有限公司": "SAGMOTO | Shaanxi Automobile Group Commercial Vehicle Co., Ltd.",

    # === Contact Form ===
    "Your Name": "Ваше имя",
    "Your Email": "Ваш email",
    "Phone Number": "Номер телефона",
    "Your Message": "Ваше сообщение",
    "SEND MESSAGE": "ОТПРАВИТЬ",
    "Send Message": "Отправить сообщение",
    "Get in Touch": "Свяжитесь с нами",
    "We'd Love to Hear from You": "Будем рады вашему обращению",
    "Have a question about our trucks? Fill out the form and our sales team will get back to you within 24 hours.":
        "Есть вопрос о наших грузовиках? Заполните форму, и наш отдел продаж свяжется с вами в течение 24 часов.",
    "Contact Information": "Контактная информация",
    "Phone": "Телефон",
    "Email": "Эл. почта",
    "Address": "Адрес",
    "Room 603A, Floor 6, Building B, Chanba Free Trade Center, No.777 Eurasia Avenue, Chanba Ecological District, Xi'an, Shaanxi, China":
        "Китай, провинция Шэньси, г. Сиань, район Чаньба, Евразийский проспект, 777, Центр свободной торговли Чаньба, корпус B, этаж 6, офис 603A",

    # === About Page ===
    "About SAGMOTO": "О компании SAGMOTO",
    "Our Story": "Наша история",
    "SAGMOTO is the commercial vehicle brand of Shaanxi Automobile Group, one of China's leading commercial vehicle manufacturers.":
        "SAGMOTO — бренд коммерческих автомобилей Shaanxi Automobile Group, одного из ведущих производителей коммерческого транспорта Китая.",
    "With decades of engineering excellence, SAGMOTO delivers reliable, efficient, and innovative commercial vehicles to customers worldwide.":
        "Благодаря десятилетиям инженерного мастерства, SAGMOTO поставляет надёжные, эффективные и инновационные коммерческие автомобили клиентам по всему миру.",

    # === News Detail Pages ===
    "Home / News / ": "Главная / Новости / ",
    "\u2190 Back to News": "\u2190 Назад к новостям",

    # === News Article Titles ===
    "Intelligent Production of Heavy Trucks at Shaanxi Automobile\u2019s Factory":
        "Интеллектуальное производство тяжёлых грузовиков на заводе Shaanxi Automobile",
    "Caucasus\u2019 New Jewel SAGMOTO X3s Tractor Debuts in Armenia":
        "Новая жемчужина Кавказа: тягач SAGMOTO X3s дебютирует в Армении",
    "SAGMOTO Brand Specialized Trucks at the 137th Canton Fair":
        "Специализированные грузовики SAGMOTO на 137-й Кантонской ярмарке",
    "SAGMOTO Chinese New Year Greeting 2025":
        "Поздравление SAGMOTO с Китайским Новым годом 2025",
    "Charting the Path of Courageous Advancement with the All-New X3s Heavy Truck to Realize a New Journey":
        "Прокладывая путь смелого прогресса с новым тяжёлым грузовиком X3s к новым горизонтам",

    # === Application Pages (qyc, zxc, zhc, special, tzc etc.) ===
    "Tractor Truck Products": "Продукция тягачей",
    "Dump Truck Products": "Продукция самосвалов",
    "Cargo Truck Products": "Продукция грузовиков",
    "Special Vehicle Products": "Продукция спецтехники",
    "Off-road Truck Products": "Продукция внедорожных грузовиков",

    # === Off-road sub pages ===
    "Off-road Dump Truck Products": "Продукция внедорожных самосвалов",
    "Off-road Tractor Products": "Продукция внедорожных тягачей",

    # === Service pages ===
    "Our Service Commitment": "Наши сервисные обязательства",
    "After-Sales Support": "Послепродажная поддержка",
    "Maintenance & Repair": "Техническое обслуживание и ремонт",
    "Genuine Parts": "Оригинальные запчасти",
    "Technical Training": "Техническое обучение",

    # === All Products label ===
    "ALL PRODUCTS": "ВСЯ ПРОДУКЦИЯ",

    # === Sort/search label ===
    "All Products": "Вся продукция",

    # === New Energy page ===
    "SAGMOTO New Energy": "SAGMOTO Новая энергия",
    "Driving the Future of Green Transportation": "Движение к будущему экологичного транспорта",
    "SAGMOTO New Energy Vehicles are engineered for zero-emission performance without compromising on power, reliability, or comfort.":
        "Электромобили SAGMOTO созданы для работы с нулевым уровнем выбросов без ущерба для мощности, надёжности и комфорта.",

    # === Off-road page ===
    "SAGMOTO Off-road Series": "Внедорожная серия SAGMOTO",
    "Built for the Toughest Terrains": "Созданы для самых сложных условий",
    "From mining sites to construction zones, SAGMOTO Off-road trucks deliver unmatched durability and performance.":
        "От горных карьеров до строительных площадок — внедорожные грузовики SAGMOTO обеспечивают непревзойдённую надёжность и производительность.",

    # === Video page titles ===
    "X6s Fuel Tanker": "X6s Бензовоз",
    "X3s | Shining!": "X3s | Сияние!",
    "SAGMOTO i9 electric light truck": "SAGMOTO i9 электрический лёгкий грузовик",
    "SAGMOTO X9 Cleaning sweeper truck": "SAGMOTO X9 Подметальная машина",
    "X9 2120 4X4 Dumper": "X9 2120 4×4 Самосвал",
    "X9 1995 Lorry": "X9 1995 Грузовик",
    "SAGMOTO Embracing World": "SAGMOTO Объединяя мир",
    "X3s 6x4 Stiff boom crane operating procedures & cautions": "X3s 6×4 Правила эксплуатации крана-манипулятора",

    # === Products page filters ===
    "All": "Все",
    "Light": "Лёгкие",
    "Medium": "Средние",
    "Heavy": "Тяжёлые",
    "Off-Road": "Внедорожные",
    "Special Purpose": "Спецтехника",

    # === JS hardcoded strings ===
    "Please fill in all required fields correctly.": "Пожалуйста, заполните все обязательные поля правильно.",
    "Sending...": "Отправка...",
    "Message Sent!": "Сообщение отправлено!",
    "Specifications not available": "Характеристики недоступны",
    "Key Features": "Ключевые особенности",
    "Category": "Категория",
    "Engine": "Двигатель",
    "Horsepower": "Мощность",
    "Torque": "Крутящий момент",
    "Transmission": "Трансмиссия",
    "Drive": "Привод",
    "GCW": "ПММ",
    "Wheelbase": "Колёсная база",
    "Cab": "Кабина",
    "Suspension": "Подвеска",
    "Range": "Запас хода",
    "Charging": "Зарядка",

    # === Product toggle feature titles ===
    "4x4 All-Wheel Drive System": "Система полного привода 4×4",
    "Heavy-Duty Leaf Spring Suspension": "Усиленная рессорная подвеска",
    "Powerful Yuchai 160HP Diesel Engine": "Мощный дизельный двигатель Yuchai 160 л.с.",
    "Recovery Capability": "Эвакуационные возможности",
    "Enhanced Maneuverability": "Повышенная манёвренность",
    "Rugged, Reliable Design": "Прочная, надёжная конструкция",
    "Ergonomic Cab with Airbag Seat": "Эргономичная кабина с пневмоподвеской сиденья",
    "Advanced Digital-LED Instrument Panel": "Современная цифровая светодиодная приборная панель",
    "Premium Comfort Seats": "Сиденья премиум-комфорта",
    "High-Efficiency Sweeping System": "Высокоэффективная подметальная система",
    "Dust Suppression Technology": "Технология пылеподавления",
    "Smart Sanitation Control": "Интеллектуальное управление уборкой",
    "Superior Ground Clearance": "Увеличенный дорожный просвет",
    "Optimized Fuel Efficiency": "Оптимизированная топливная эффективность",
    "Comfort Cabin": "Комфортная кабина",
    "All-Wheel Drive Traction": "Полноприводное сцепление",
    "Versatile Light-Duty Chassis": "Универсальное лёгкое шасси",
    "Flexible Lightweight Design": "Гибкая облегчённая конструкция",
    "Compact Turning Radius": "Компактный радиус разворота",
    "Efficient Municipal Design": "Эффективная коммунальная конструкция",
    "Eco Water Pump System": "Экологичная система водяного насоса",
    "Comfortable M3000 Cab": "Комфортная кабина M3000",
    "Flagship 560HP Powertrain": "Флагманская силовая установка 560 л.с.",
    "Spacious Flat-Floor Cab": "Просторная кабина с ровным полом",
    "Aerodynamic Optimization": "Аэродинамическая оптимизация",
    "Next-Gen Powertrain": "Силовая установка нового поколения",
    "European Safety Standard": "Европейский стандарт безопасности",
    "Spacious Interior": "Просторный интерьер",
    "Balanced Performance": "Сбалансированная производительность",
    "Advanced Safety Systems": "Современные системы безопасности",
    "Dual Warning System": "Двойная система предупреждения",
    "Spacious 850mm Berth": "Просторное спальное место 850 мм",
    "Reliable & Cost-Effective": "Надёжная и экономичная эксплуатация",
    "Multi-Level Telescopic Boom": "Многосекционная телескопическая стрела",
    "Advanced Safety Protection": "Современная защита безопасности",
    "High-Strength Construction": "Высокопрочная конструкция",
    "Wear-Resistant Steel": "Износостойкая сталь",
    "Enhanced Visibility Package": "Пакет улучшенной обзорности",
    "Reinforced Double-Layer Chassis": "Усиленное двухслойное шасси",
    "Strong & Stable Platform": "Прочная и стабильная платформа",
    "Multi-Purpose Adaptability": "Многоцелевая адаптивность",
    "Durable 850-Series Chassis": "Прочное шасси 850-й серии",
    "Mining-Ready Suspension": "Подвеска для горных работ",
    "Anti-Dust Exhaust Design": "Противопыльная конструкция выхлопа",
    "Integrated E-Axle Technology": "Интегрированная технология электромоста",
    "430km Range + 120kW Fast Charge": "Запас хода 430 км + быстрая зарядка 120 кВт",
    "15% Energy Recovery": "Рекуперация энергии 15%",

    # === Product feature descriptions in toggle ===
    "Engineered for tough terrain with full-time 4x4 all-wheel drive system, providing maximum traction in mud, sand, and steep grades.":
        "Разработан для сложного рельефа с постоянной системой полного привода 4×4, обеспечивающей максимальное сцепление на грязи, песке и крутых склонах.",
    "Engineered for the toughest terrains with full-time 4x4 drive, delivering maximum traction on mud, sand, and steep grades.":
        "Разработан для самых сложных условий с постоянным приводом 4×4, обеспечивающим максимальное сцепление на грязи, песке и крутых склонах.",
    "Built to handle maximum payloads with heavy-duty leaf springs featuring main and sub-spring structure. Offers high bearing capacity with simple, low-maintenance design.":
        "Создан для максимальных нагрузок с усиленными рессорами, включающими основные и дополнительные листы. Высокая несущая способность при простой конструкции с низкими затратами на обслуживание.",
    "Built to handle maximum payloads with multi-layer leaf springs and reinforced structural components. High load-bearing capacity with minimal maintenance.":
        "Создан для максимальных нагрузок с многолистовыми рессорами и усиленными элементами конструкции. Высокая несущая способность при минимальном обслуживании.",
    "Reliable Yuchai 160HP diesel engine delivers strong low-end torque for demanding work conditions, with proven durability in commercial applications.":
        "Надёжный дизельный двигатель Yuchai 160 л.с. обеспечивает высокий крутящий момент на низких оборотах для сложных условий работы, с проверенной надёжностью в коммерческой эксплуатации.",
    "Designed specifically for vehicle recovery operations with powerful winch system and reinforced chassis frame for heavy-duty towing tasks.":
        "Специально разработан для эвакуационных работ с мощной лебёдочной системой и усиленной рамой для тяжёлых буксировочных задач.",
    "Maximum gradient capability exceeding 30%, designed to handle tough working conditions with reliable performance and exceptional maneuverability.":
        "Способность преодолевать уклон более 30%, разработан для сложных условий работы с надёжной производительностью и исключительной манёвренностью.",
    "Built with reinforced chassis structure and heavy-duty components to withstand harsh environments and demanding commercial applications.":
        "Создан с усиленной конструкцией шасси и компонентами для тяжёлых условий эксплуатации и требовательных коммерческих применений.",
    "Semi-floating cab suspension with main driver airbag shock-absorbing seat reduces vibration and fatigue during long hauls for superior driver comfort.":
        "Полуподвесная кабина с пневмоподвеской сиденья водителя снижает вибрацию и утомляемость при длительных перевозках.",
    "Combination of analog gauges and LCD multi-function display provides clear, real-time vehicle data monitoring for better driving decisions.":
        "Сочетание аналоговых приборов и многофункционального ЖК-дисплея обеспечивает чёткий мониторинг данных автомобиля в реальном времени.",
    "Fully wrapped seat design with optimized cushion density and lumbar support, providing all-day comfort during extended driving sessions.":
        "Полностью охватывающая конструкция сиденья с оптимизированной плотностью подушки и поясничной поддержкой, обеспечивающая комфорт в течение всего дня.",
    "Advanced sweeping system with large-capacity debris collection and powerful suction for efficient urban street and highway maintenance.":
        "Современная подметальная система с большим объёмом сбора мусора и мощным всасыванием для эффективного обслуживания городских улиц и магистралей.",
    "Integrated water spray system effectively suppresses dust during operation, meeting environmental standards for urban sanitation work.":
        "Встроенная система водяного распыления эффективно подавляет пыль во время работы, соответствуя экологическим стандартам городской уборки.",
    "Intelligent control panel allows operators to adjust sweeping parameters on-the-fly for optimal cleaning performance across different road conditions.":
        "Интеллектуальная панель управления позволяет операторам регулировать параметры подметания на ходу для оптимальной очистки в различных дорожных условиях.",
    "314mm minimum ground clearance ensures obstacle clearance on rough terrain and construction sites, with approach angle exceeding 25 degrees.":
        "Минимальный дорожный просвет 314 мм обеспечивает преодоление препятствий на пересечённой местности и стройплощадках, с углом въезда более 25 градусов.",
    "New transmission system with maintenance-free drive axles and low rolling-resistance tires achieves best-in-class fuel economy for medium-duty operations.":
        "Новая трансмиссия с необслуживаемыми ведущими мостами и шинами с низким сопротивлением качению обеспечивает лучшую в классе топливную экономичность.",
    "Airbag-suspended driver seat and 850mm-wide lower sleeper berth provide exceptional comfort for overnight hauling and long-distance transport.":
        "Сиденье водителя с пневмоподвеской и нижнее спальное место шириной 850 мм обеспечивают исключительный комфорт при ночных и дальних перевозках.",
    "Full-time 4x4 all-wheel drive system delivers superior off-road traction and handling in challenging conditions including snow, mud, and loose surfaces.":
        "Постоянная система полного привода 4×4 обеспечивает превосходное внедорожное сцепление и управляемость в сложных условиях, включая снег, грязь и рыхлые поверхности.",
    "Modular weight-optimized design using aluminum alloy and high-strength steel reduces vehicle weight while maintaining structural integrity for maximum payload.":
        "Модульная конструкция с оптимизацией веса с использованием алюминиевых сплавов и высокопрочной стали снижает массу автомобиля при сохранении прочности конструкции.",
    "Short wheelbase configuration with optional shortened rear axle delivers tighter turning radius, ideal for urban delivery and confined-space operations.":
        "Конфигурация с короткой колёсной базой и укороченным задним мостом обеспечивает меньший радиус разворота, идеально для городских доставок и работы в ограниченном пространстве.",
    "Lightweight chassis with corrosion-resistant water tank and efficient pump system for municipal watering, dust control, and landscaping applications.":
        "Облегчённое шасси с коррозионностойким баком для воды и эффективной насосной системой для коммунального полива, пылеподавления и ландшафтных работ.",
    "M3000 cab provides sedan-like comfort with modern interior design, excellent noise insulation and ergonomic controls for productive long working days.":
        "Кабина M3000 обеспечивает комфорт легкового уровня с современным дизайном интерьера, отличной шумоизоляцией и эргономичным управлением.",
    "Cummins Z14 560HP engine paired with Eaton AMT transmission delivers exceptional power, seamless shifting, and maximum fuel efficiency for long-haul transport.":
        "Двигатель Cummins Z14 560 л.с. в паре с автоматизированной трансмиссией Eaton AMT обеспечивает исключительную мощность, плавное переключение и максимальную топливную эффективность.",
    "2.13m internal height with flat floor design allows the driver to stand upright and move freely inside the cab, enhancing living comfort during long journeys.":
        "Внутренняя высота 2,13 м с ровным полом позволяет водителю стоять и свободно передвигаться в кабине, повышая комфорт проживания в дальних поездках.",
    "CFD-optimized exterior with adjustable roof deflector achieves drag coefficient of 0.45, reducing fuel consumption to just 26.97L/100km with optimal trailer matching.":
        "Оптимизированный с помощью CFD экстерьер с регулируемым спойлером на крыше достигает коэффициента лобового сопротивления 0,45, снижая расход топлива до 26,97 л/100 км при оптимальном сочетании с прицепом.",
    "Cummins M13 engine with intelligent electronic management system delivers 520HP with exceptional fuel economy and lower emissions for sustainable transport.":
        "Двигатель Cummins M13 с интеллектуальной электронной системой управления выдаёт 520 л.с. с исключительной топливной экономичностью и низкими выбросами.",
    "High-strength cab meets latest ECE R29-03 European crash safety standards, combined with intelligent braking systems for comprehensive driver protection.":
        "Высокопрочная кабина соответствует новейшим европейским стандартам безопасности ECE R29-03 в сочетании с интеллектуальными тормозными системами.",
    "Flat-floor design creates spacious interior environment with standing room and obstacle-free movement, plus generous storage throughout the cabin.":
        "Ровный пол создаёт просторный интерьер с возможностью стоять и свободно передвигаться, а также с вместительными отсеками для хранения по всей кабине.",
    "Optimized engine-transmission matching delivers 420HP with smooth power delivery and excellent fuel efficiency for regional distribution and inter-city routes.":
        "Оптимизированное сочетание двигателя и трансмиссии обеспечивает 420 л.с. с плавной подачей мощности и отличной топливной эффективностью для региональных и междугородних маршрутов.",
    "Equipped with lane departure warning and forward collision alert systems, plus high-strength cab structure that meets ECE R29 crash safety standards.":
        "Оснащён системами предупреждения о выходе из полосы и фронтального столкновения, а также высокопрочной конструкцией кабины по стандартам безопасности ECE R29.",
    "Dual warning system with visual and audible alerts enhances operational safety. Combined with daytime running lights and enhanced mirror package for 360\u00b0 awareness.":
        "Двойная система предупреждения с визуальными и звуковыми сигналами повышает безопасность эксплуатации в сочетании с дневными ходовыми огнями и улучшенным пакетом зеркал.",
    "850mm-wide lower berth with 800mm vertical clearance between upper and lower bunks provides hotel-quality sleeping comfort during mandatory rest periods.":
        "Нижнее спальное место шириной 850 мм с вертикальным зазором 800 мм между верхней и нижней полками обеспечивает комфорт сна гостиничного уровня.",
    "Proven Yuchai powertrain with optimized chassis configuration delivers dependable daily operation with low total cost of ownership and easy maintenance access.":
        "Проверенная силовая установка Yuchai с оптимизированной конфигурацией шасси обеспечивает надёжную ежедневную эксплуатацию с низкой совокупной стоимостью владения.",
    "Multi-stage hydraulic telescopic boom with wide operating envelope, fast lift/lower speeds, and precision positioning for utility maintenance and construction work.":
        "Многоступенчатая гидравлическая телескопическая стрела с широкой рабочей зоной, высокой скоростью подъёма/опускания и точным позиционированием.",
    "Overload protection, emergency descent system, and stabilizer interlock ensure operator safety during elevated work at heights up to 20 meters.":
        "Защита от перегрузки, система аварийного спуска и блокировка стабилизаторов обеспечивают безопасность оператора при работе на высоте до 20 метров.",
    "High-tensile steel construction with reinforced outriggers provides exceptional stability during elevated operations, even in windy conditions.":
        "Конструкция из высокопрочной стали с усиленными аутригерами обеспечивает исключительную устойчивость при высотных работах, даже в ветреную погоду.",
    "High-strength wear-resistant steel drum and reliable hydraulic system ensure consistent concrete mixing quality and long service life in demanding conditions.":
        "Барабан из высокопрочной износостойкой стали и надёжная гидравлическая система обеспечивают стабильное качество смешивания бетона и длительный срок службы.",
    "Main rear-view mirror plus wide-angle blind spot mirror setup reduces driver blind zones, enhancing safety during urban maneuvering and job site navigation.":
        "Основное зеркало заднего вида и широкоугольное зеркало слепых зон уменьшают мёртвые зоны, повышая безопасность при городском маневрировании.",
    "Multi-leaf spring suspension with reinforced double-layer frame delivers exceptional rigidity and load-bearing capacity for challenging construction environments.":
        "Многолистовая рессорная подвеска с усиленной двухслойной рамой обеспечивает исключительную жёсткость и несущую способность для сложных строительных условий.",
    "Heavy-duty off-road chassis platform with reinforced frame and specialized mining application engineering for extreme terrain durability.":
        "Тяжёлая внедорожная платформа шасси с усиленной рамой и специализированной горной инженерией для работы в экстремальных условиях.",
    "Designed for mining operations with reinforced rear suspension that increases flattening load capacity from 25.3T to 30.5T for heavy ore transport.":
        "Разработан для горных работ с усиленной задней подвеской, увеличивающей грузоподъёмность с 25,3Т до 30,5Т для перевозки тяжёлой руды.",
    "Directionally adjustable exhaust tailpipe prevents ground dust from being blown up, maintaining clear visibility for the driver in dusty mining environments.":
        "Выхлопная труба с регулируемым направлением предотвращает поднятие пыли с земли, сохраняя чёткую видимость для водителя в пыльных горных условиях.",
    "Integrated electric drive axle with compact, highly-integrated design achieves higher efficiency and extended driving range compared to conventional e-powertrains.":
        "Интегрированный электрический ведущий мост с компактной высокоинтегрированной конструкцией обеспечивает более высокую эффективность и увеличенный запас хода.",
    "430km working range with 120kW DC fast charging capability achieves full charge in just 65 minutes, minimizing downtime for urban logistics operations.":
        "Запас хода 430 км с быстрой зарядкой постоянным током 120 кВт, полная зарядка всего за 65 минут, минимизируя время простоя для городских логистических операций.",
    "Advanced regenerative braking system recovers kinetic energy during deceleration, reducing overall energy consumption by approximately 15% for maximum efficiency.":
        "Усовершенствованная система рекуперативного торможения восстанавливает кинетическую энергию при замедлении, снижая общее энергопотребление примерно на 15%.",
    "Range": "Запас хода",  # already translated above but ensure
    "Charging": "Зарядка",  # already translated above but ensure

    # === Privacy Policy page ===
    "Last updated: July 2026": "Последнее обновление: июль 2026",
    "1. Information We Collect": "1. Какую информацию мы собираем",
    "2. How We Use Your Information": "2. Как мы используем вашу информацию",
    "3. Sharing of Information": "3. Передача информации",
    "4. Data Security": "4. Безопасность данных",
    "5. Your Rights": "5. Ваши права",
    "6. Cookies": "6. Файлы Cookie",
    "7. Contact Us": "7. Свяжитесь с нами",
    "We may collect the following types of information:": "Мы можем собирать следующие типы информации:",
    "Personal identification information (Name, email address, phone number, etc.)":
        "Персональные идентификационные данные (имя, адрес электронной почты, номер телефона и т.д.)",
    "Business information (Company name, industry, fleet size, etc.)":
        "Деловая информация (название компании, отрасль, размер автопарка и т.д.)",
    "Technical data (IP address, browser type, device information, etc.)":
        "Технические данные (IP-адрес, тип браузера, информация об устройстве и т.д.)",
    "Communication records (Inquiries, feedback, and correspondence with our team)":
        "Записи коммуникаций (запросы, отзывы и переписка с нашей командой)",
    "We use your information for the following purposes:": "Мы используем вашу информацию для следующих целей:",
    "To respond to your inquiries and provide customer support":
        "Для ответа на ваши запросы и предоставления поддержки клиентов",
    "To process and fulfill your orders and requests": "Для обработки и выполнения ваших заказов и запросов",
    "To send you product information, quotes, and promotional materials (with your consent)":
        "Для отправки вам информации о продукции, коммерческих предложений и рекламных материалов (с вашего согласия)",
    "To improve our products, services, and website experience":
        "Для улучшения нашей продукции, услуг и работы веб-сайта",
    "To comply with legal obligations and protect our rights":
        "Для соблюдения юридических обязательств и защиты наших прав",
    "We do not sell your personal information.": "Мы не продаём вашу личную информацию.",
    "We may share your information with:": "Мы можем передавать вашу информацию:",
    "Our authorized dealers and service partners to fulfill your requests":
        "Нашим авторизованным дилерам и сервисным партнёрам для выполнения ваших запросов",
    "Service providers who assist us in operating our business (IT, logistics, marketing)":
        "Поставщикам услуг, помогающим нам в ведении бизнеса (ИТ, логистика, маркетинг)",
    "Regulatory authorities when required by law":
        "Регулирующим органам, когда это требуется по закону",
    "We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.":
        "Мы применяем соответствующие технические и организационные меры для защиты вашей личной информации от несанкционированного доступа, изменения, раскрытия или уничтожения.",
    "However, no method of transmission over the Internet or electronic storage is 100% secure.":
        "Однако ни один метод передачи данных через Интернет или электронного хранения не является на 100% безопасным.",
    "You have the right to:": "Вы имеете право:",
    "Access the personal information we hold about you": "Получить доступ к вашей личной информации",
    "Request correction of inaccurate information": "Запросить исправление неточной информации",
    "Request deletion of your personal information": "Запросить удаление вашей личной информации",
    "Object to or restrict processing of your information": "Возразить против или ограничить обработку вашей информации",
    "Withdraw consent at any time (where processing is based on consent)":
        "Отозвать согласие в любое время (если обработка основана на согласии)",
    "We use cookies and similar technologies to enhance your browsing experience, analyze site traffic, and personalize content.":
        "Мы используем файлы cookie и аналогичные технологии для улучшения вашего опыта просмотра, анализа трафика сайта и персонализации контента.",
    "You can control cookie settings through your browser preferences.":
        "Вы можете управлять настройками cookie через параметры вашего браузера.",
    "If you have any questions about this Privacy Policy, please contact us at:":
        "Если у вас есть вопросы об этой Политике конфиденциальности, свяжитесь с нами:",
    "We will respond to your inquiry within 30 days.": "Мы ответим на ваш запрос в течение 30 дней.",

    # === Terms of Use page ===
    "Last updated: July 2026": "Последнее обновление: июль 2026",
    "1. Acceptance of Terms": "1. Принятие условий",
    "2. Use of the Website": "2. Использование веб-сайта",
    "3. Intellectual Property": "3. Интеллектуальная собственность",
    "4. Disclaimer of Warranties": "4. Отказ от гарантий",
    "5. Limitation of Liability": "5. Ограничение ответственности",
    "6. Governing Law": "6. Применимое право",
    "7. Changes to Terms": "7. Изменение условий",
    "By accessing and using this website, you agree to be bound by these Terms of Use.":
        "Получая доступ и используя этот веб-сайт, вы соглашаетесь соблюдать настоящие Условия использования.",
    "If you do not agree with any part of these terms, please do not use our website.":
        "Если вы не согласны с какой-либо частью этих условий, пожалуйста, не используйте наш веб-сайт.",
    "You agree to use this website only for lawful purposes.": "Вы соглашаетесь использовать этот веб-сайт только в законных целях.",
    "You agree not to:": "Вы соглашаетесь не:",
    "Use the website in any way that violates applicable laws or regulations":
        "Использовать веб-сайт способом, нарушающим применимые законы или правила",
    "Attempt to gain unauthorized access to any part of the website":
        "Пытаться получить несанкционированный доступ к любой части веб-сайта",
    "Interfere with or disrupt the website or servers": "Создавать помехи или нарушать работу веб-сайта или серверов",
    "Upload or transmit viruses or malicious code": "Загружать или передавать вирусы или вредоносный код",
    "All content on this website, including text, images, logos, and product information, is the property of SAGMOTO / Shaanxi Fenghan Trading Co., Ltd. and is protected by intellectual property laws.":
        "Весь контент на этом веб-сайте, включая текст, изображения, логотипы и информацию о продукции, является собственностью SAGMOTO / Shaanxi Fenghan Trading Co., Ltd. и защищён законами об интеллектуальной собственности.",
    "You may not reproduce, distribute, or create derivative works without our prior written consent.":
        "Вы не можете воспроизводить, распространять или создавать производные работы без нашего предварительного письменного согласия.",
    "This website is provided 'as is' without any representations or warranties, express or implied.":
        "Этот веб-сайт предоставляется «как есть» без каких-либо явных или подразумеваемых гарантий.",
    "We do not warrant that the website will be constantly available, or that the information on this website is complete, true, accurate, or non-misleading.":
        "Мы не гарантируем, что веб-сайт будет постоянно доступен или что информация на этом сайте является полной, достоверной, точной или не вводящей в заблуждение.",
    "To the fullest extent permitted by law, SAGMOTO / Shaanxi Fenghan Trading Co., Ltd. shall not be liable for any direct, indirect, incidental, or consequential damages arising from the use of this website.":
        "В максимальной степени, разрешённой законом, SAGMOTO / Shaanxi Fenghan Trading Co., Ltd. не несёт ответственности за любые прямые, косвенные, случайные или последующие убытки, возникающие в результате использования этого веб-сайта.",
    "These terms shall be governed by and construed in accordance with the laws of the People's Republic of China.":
        "Настоящие условия регулируются и толкуются в соответствии с законами Китайской Народной Республики.",
    "We reserve the right to modify these terms at any time. Changes will be effective immediately upon posting.":
        "Мы оставляем за собой право изменять эти условия в любое время. Изменения вступают в силу немедленно после публикации.",
    "Your continued use of the website after changes constitutes acceptance of the modified terms.":
        "Ваше дальнейшее использование веб-сайта после внесения изменений означает принятие изменённых условий.",

    # === Language selector ===
    # The EN should become RU on the Russian site
    # We handle this with a direct replacement in the script

    # === Page banner headings ===
    "PRODUCTS CATALOG": "КАТАЛОГ ПРОДУКЦИИ",
    "SAGMOTO PRODUCTS": "ПРОДУКЦИЯ SAGMOTO",
    "OUR PRODUCTS": "НАША ПРОДУКЦИЯ",
    "NEWS CENTER": "НОВОСТНОЙ ЦЕНТР",
    "CONTACT US PAGE": "СТРАНИЦА КОНТАКТОВ",
    "PRIVACY POLICY": "ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ",
    "TERMS OF USE": "УСЛОВИЯ ИСПОЛЬЗОВАНИЯ",
    "NEW ENERGY VEHICLES": "ЭЛЕКТРОМОБИЛИ",
    "OFF-ROAD SERIES": "ВНЕДОРОЖНАЯ СЕРИЯ",

    # === Breadcrumb ===
    "Home / Products": "Главная / Продукция",
    "Home / About": "Главная / О нас",
    "Home / Contact": "Главная / Контакты",
    "Home / News": "Главная / Новости",
    "Home / Privacy Policy": "Главная / Политика конфиденциальности",
    "Home / Terms of Use": "Главная / Условия использования",
    "Home / New Energy": "Главная / Новая энергия",
    "Home / Off-Road 4x4": "Главная / Внедорожные 4×4",

    # === Product series page descriptions ===
    "Discover the E1st flagship tractor truck series, engineered for premium long-haul transportation with 560HP Cummins power.":
        "Откройте для себя флагманскую серию тягачей E1st, созданную для премиальных дальних перевозок с двигателем Cummins 560 л.с.",
    "Explore the E3 series heavy-duty trucks, delivering reliable performance for demanding transport operations.":
        "Ознакомьтесь с серией тяжёлых грузовиков E3, обеспечивающих надёжную работу в сложных транспортных операциях.",
    "Browse the E6 series medium-duty trucks, offering versatile configurations for various commercial applications.":
        "Просмотрите серию среднетоннажных грузовиков E6 с универсальными конфигурациями для различных коммерческих применений.",
    "Check out the E9 series heavy-duty trucks, combining power and efficiency for modern logistics.":
        "Ознакомьтесь с серией тяжёлых грузовиков E9, сочетающих мощность и эффективность для современной логистики.",
    "Explore the i5 series electric commercial vehicles, leading the transition to zero-emission urban logistics.":
        "Откройте для себя серию электрических коммерческих автомобилей i5, ведущих переход к городской логистике с нулевым уровнем выбросов.",
    "Discover the i9 series, SAGMOTO's innovative electric light truck platform for sustainable urban transportation.":
        "Откройте для себя серию i9, инновационную платформу электрических лёгких грузовиков SAGMOTO для устойчивого городского транспорта.",
    "Browse the X3s series, rugged and reliable trucks built for challenging off-road and heavy-duty applications.":
        "Просмотрите серию X3s, прочные и надёжные грузовики для сложных внедорожных и тяжёлых условий эксплуатации.",
    "Explore the X5 series, versatile medium-duty trucks engineered for efficiency and everyday reliability.":
        "Откройте для себя серию X5, универсальные среднетоннажные грузовики, созданные для эффективности и повседневной надёжности.",
    "Check out the X6 series, powerful medium-duty trucks with premium configurations for demanding operations.":
        "Ознакомьтесь с серией X6, мощными среднетоннажными грузовиками с премиальными конфигурациями для сложных операций.",
    "Discover the X7 series, ultra-modern light-duty trucks with advanced features and exceptional comfort.":
        "Откройте для себя серию X7, ультрасовременные лёгкие грузовики с передовыми функциями и исключительным комфортом.",
    "Browse the X9 series, innovative light-duty trucks with flexible configurations for diverse commercial needs.":
        "Просмотрите серию X9, инновационные лёгкие грузовики с гибкими конфигурациями для различных коммерческих нужд.",
    "Explore the Z3 conventional tractor truck, a next-generation heavy-duty tractor with 520HP and advanced safety features.":
        "Откройте для себя классический тягач Z3, тяжёлый тягач нового поколения с мощностью 520 л.с. и передовыми системами безопасности.",
}


def translate_file(filepath):
    """Apply all translations to a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    # Sort by key length descending to avoid partial matches
    for en, ru in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        if en in content:
            content = content.replace(en, ru)
            changes += 1

    # Special handling: language selector
    # Change EN (active) to RU (active)
    content = content.replace('class="active">RU</a>', 'class="active">RU</a>')  # no-op
    # If there's "EN" as active in the lang selector, swap to RU
    content = re.sub(r'(<a href="[^"]*"\s+class=")active(">EN</a>)', r'\1active">RU</a>', content)
    # Change other language links
    content = content.replace('>EN</a>', '>RU</a>')
    
    # Fix the lang selector to show Russian as default
    # Pattern: EN active, 中文, FR
    content = content.replace(
        '<a href="#" class="active">RU</a>\n                <a href="#">中文</a>\n                <a href="#">FR</a>',
        '<a href="#" class="active">RU</a>\n                <a href="#">EN</a>\n                <a href="#">中文</a>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, 0


def main():
    html_files = []
    js_files = []
    json_files = []

    for root, dirs, files in os.walk(BASE):
        # Skip directories we don't want to process
        dirs[:] = [d for d in dirs if d not in ('.mirror_raw', 'videos', '__pycache__', 'node_modules', 'admin')]
        
        for f in files:
            filepath = os.path.join(root, f)
            if f.endswith('.html'):
                html_files.append(filepath)
            elif f.endswith('.js') and 'mirror' not in root:
                js_files.append(filepath)
            elif f.endswith('.json'):
                json_files.append(filepath)

    total_changes = 0
    files_changed = 0

    print(f"Processing {len(html_files)} HTML files...")
    for fp in sorted(html_files):
        changed, count = translate_file(fp)
        if changed:
            files_changed += 1
            total_changes += count
            rel = os.path.relpath(fp, BASE)
            print(f"  ✓ {rel} ({count} replacements)")

    print(f"\nProcessing {len(js_files)} JS files...")
    for fp in sorted(js_files):
        changed, count = translate_file(fp)
        if changed:
            files_changed += 1
            total_changes += count
            rel = os.path.relpath(fp, BASE)
            print(f"  ✓ {rel} ({count} replacements)")

    print(f"\nProcessing {len(json_files)} JSON files...")
    for fp in sorted(json_files):
        changed, count = translate_file(fp)
        if changed:
            files_changed += 1
            total_changes += count
            rel = os.path.relpath(fp, BASE)
            print(f"  ✓ {rel} ({count} replacements)")

    print(f"\n{'='*60}")
    print(f"Translation complete!")
    print(f"Files changed: {files_changed}")
    print(f"Total replacements: {total_changes}")
    print(f"Translation dictionary size: {len(TRANSLATIONS)} entries")


if __name__ == '__main__':
    main()
