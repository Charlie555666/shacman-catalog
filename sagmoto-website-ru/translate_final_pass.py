#!/usr/bin/env python3
"""Final pass: Fix ALL remaining English strings across sagmoto-website-ru.
Handles: nav dropdown sub-items, breadcrumbs, back buttons, news body content."""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# GLOBAL REPLACEMENTS (apply to ALL .html files)
# ============================================================
GLOBAL_REPLACEMENTS = [
    # --- Navigation dropdown sub-items (APPLICATIONS menu) ---
    # 牵引车 sub-items
    (">Port Transport<", ">Портовые перевозки<"),
    (">Hazardous Chemicals Transport<", ">Перевозка опасных грузов<"),
    (">Coal Transport<", ">Перевозка угля<"),
    (">Sand And Gravel Transport<", ">Перевозка песка и гравия<"),
    # 自卸车 sub-items
    (">Urban Construction<", ">Городское строительство<"),
    (">Mining<", ">Горная добыча<"),
    # 载货车 sub-items
    (">Express Delivery<", ">Экспресс-доставка<"),
    (">Intercity Logistics<", ">Междугородняя логистика<"),
    (">City Distribution<", ">Городская дистрибуция<"),
    # 专用车 sub-items
    (">City Transportation<", ">Городские перевозки<"),
    (">Smart Sanitation<", ">Умная санитария<"),
    (">Dangerous Goods Transportation<", ">Перевозка опасных грузов<"),
    (">Road Work &amp; Rescue<", ">Дорожные работы и спасение<"),
    
    # --- Navigation dropdown sub-items (SERVICE menu) ---
    (">Driving Reminder<", ">Памятка водителю<"),
    
    # --- Navigation dropdown sub-items (NEWS menu) ---
    (">News Center<", ">Центр новостей<"),
    
    # --- Navigation dropdown sub-items (ABOUT menu) ---
    (">Who We Are<", ">Кто мы<"),
    (">When We Started<", ">С чего мы начали<"),
    (">Technological Innovation<", ">Технологические инновации<"),
    
    # --- Breadcrumb fixes ---
    ('">News</a>', '">Новости</a>'),
    
    # --- Back button fixes ---
    ('Назад к новостям Center', 'Назад к новостям'),
]

# ============================================================
# FILE-SPECIFIC REPLACEMENTS
# ============================================================
FILE_SPECIFIC = {
    # 20.html - Canton Fair article body
    "news_Detail/20.html": [
        # Image alt
        ('alt="SAGMOTO brand specialized trucks makes an appearance in the 137th Canton Fair"', 
         'alt="Специализированные грузовики SAGMOTO на 137-й Кантонской ярмарке"'),
        # Body paragraphs
        ('The first phase of the 137th China Import and Export Fair concluded in Guangzhou on April 19. During the five-day exhibition, SAG INTL&nbsp;showcased its technological prowess in&nbsp;special&nbsp;purpose&nbsp;trucks. The highlights included the all-new i9pro electric truck, i9lec electric cargo truck, and X9 integrated sweeping vehicle, which covers&nbsp;both diesel and battery power sources. SAG demonstrates&nbsp;the company&#39;s comprehensive capabilities and confidence in global market expansion.',
         'Первая фаза 137-й Китайской ярмарки импорта и экспорта завершилась в Гуанчжоу 19 апреля. В течение пятидневной выставки SAG INTL&nbsp;продемонстрировала свои технологические возможности в области&nbsp;специализированных&nbsp;грузовиков. Среди экспонатов —全新的 i9pro 电动卡车、i9lec 电动载货车 и X9 集成清扫车，覆盖&nbsp;柴油和电动两种动力源. SAG демонстрирует&nbsp;комплексные возможности компании и уверенность в расширении глобального рынка.'),
        
        ('Adhering to its philosophy of &quot;Making favorite and reliable trucks&quot;, SAG INTL has developed a full range of commercial vehicle star products by precisely addressing customers&rsquo;&nbsp;needs, delivering high-quality, high-value&nbsp;and high-level service product solutions with premium services worldwide.',
         'Придерживаясь философии &quot;Создаём любимые и надёжные грузовики&quot;, SAG INTL разработала полный спектр коммерческих автомобилей — звёздных продуктов, точно отвечающих&nbsp;потребностям клиентов, предлагая высококачественные, высокоценные&nbsp;и высокоуровневые сервисные решения с премиальным обслуживанием по всему миру.'),
        
        ('The i9-я серия of electric trucks&nbsp;apply advanced technology such as large-capacity battery, electric drive axle, and power controller.',
         'Электрические грузовики&nbsp;серии i9&nbsp;используют передовые технологии, такие как аккумуляторы большой ёмкости, электрический ведущий мост и контроллер мощности.'),
        
        ('The following features make i9 stand out among its peers.',
         'Следующие особенности выделяют i9 среди аналогов.'),
        
        ('-400km comprehensive range enabled by high-capacity batteries',
         '-Комплексный запас хода 400 км благодаря аккумуляторам большой ёмкости'),
        
        ('-Optimized power output across scenarios through intelligent algorithm-controlled electric drive axles',
         '-Оптимизированная выходная мощность в различных сценариях благодаря интеллектуальным алгоритмам управления электрическими ведущими мостами'),
        
        ('-Advanced power management system ensuring stable performance',
         '-Передовая система управления питанием, обеспечивающая стабильную производительность'),
        
        ('Адресing traditional pain points in special&nbsp;purpose&nbsp;trucks like inconsistent modification standards and unstable performance, the company launched its branded special vehicle series featuring:',
         'Решая традиционные проблемы специализированных&nbsp;грузовиков, такие как несоответствие стандартов модификации и нестабильная производительность, компания запустила фирменную серию спецтехники, отличающуюся:'),
        
        ('-Dedicated chassis design with integrated&nbsp;upper body.',
         '-Специализированная конструкция шасси с интегрированной&nbsp;надстройкой.'),
        
        ('-Comprehensive CAE analysis and testing verification for&nbsp;both chassis and upper body, aiming at optimal system matching.',
         '-Комплексный CAE-анализ и тестовая верификация&nbsp;шасси и надстройки для оптимального согласования системы.'),
        
        ('The exhibited X9 integrated sweeper combines road cleaning and washing functions, adaptable to diverse operational requirements.',
         'Представленная интегрированная подметально-уборочная машина X9 сочетает функции очистки и мойки дорог, адаптируясь к разнообразным эксплуатационным требованиям.'),
        
        ('Looking ahead, SAG INTL&nbsp;will continue to focus on new energy and special&nbsp;purpose&nbsp;truck&nbsp;sectors, enriching product portfolios across segments while maintaining customer-centered&nbsp;innovation to provide globally favourite and reliable trucks.',
         'В перспективе SAG INTL&nbsp;продолжит фокусироваться на секторах новой энергетики и&nbsp;специализированных&nbsp;грузовиков, расширяя продуктовый портфель по всем сегментам, сохраняя клиентоориентированные&nbsp;инновации для поставки любимых и надёжных грузовиков по всему миру.'),
    ],
    
    # 21.html - Armenia debut article body
    "news_Detail/21.html": [
        # Image alt
        ('alt="Caucasus&#39; New Jewel SAGMOTO X3s Тягачи Debuts in Armenia"',
         'alt="Новая жемчужина Кавказа — тягач SAGMOTO X3s дебютирует в Армении"'),
        # Body paragraphs
        ('April 18-20, 2025, SAG INTL&nbsp;made a striking appearance at the Leasing Expo, a key machinery and equipment trade fair in the Caucasus region held in Armenia, showcasing its all-new X3s tractor and X9 cargo&nbsp;truck.',
         '18-20 апреля 2025 года SAG INTL&nbsp;ярко выступила на выставке Leasing Expo — ключевой торговой ярмарке машин и оборудования в Кавказском регионе, проходившей в Армении, представив全新 X3s тягач и X9 грузовой&nbsp;автомобиль.'),
        
        ('Situated in the southern South Caucasus with an average altitude of 2,000 meters, Armenia&rsquo;s rugged terrain features predominantly mountainous winding roads. How to stand out in a market saturated with European brands? SAG INTL prioritized the production. Through extensive customer research and bench&nbsp;marking against mainstream models, the company launched&nbsp;localized and customized&nbsp;model&nbsp;- the X3s tractor, tailored for Armenian conditions. Key adaptive configurations include:',
         'Расположенная в южной части Южного Кавказа на средней высоте 2000 метров, Армения отличается rugged рельефом с преимущественно горными извилистыми дорогами. Как выделиться на рынке, насыщенном европейскими брендами? SAG INTL приоритизировала производство. Проведя обширные исследования клиентов и&nbsp;бенчмаркинг основных моделей, компания запустила&nbsp;локализованную и адаптированную&nbsp;модель&nbsp;— тягач X3s, специально для армянских условий. Ключевые адаптивные конфигурации включают:'),
        
        ('- Cummins 490 high-power engine for robust performance.',
         '- Двигатель Cummins 490 высокой мощности для надёжной работы.'),
        
        ('- Eaton automatic transmission for smooth operation.',
         '- Автоматическая коробка передач Eaton для плавной работы.'),
        
        ('- Voith retarder&nbsp;for enhanced safety on steep slopes.',
         '- Ретардер Voith&nbsp;для повышенной безопасности на крутых склонах.'),
        
        ('This combination meets local demands for advanced configurations, load capacity, driving comfort, and smart features, attracting crowds of clients for test drives and inquiries during the exhibition.',
         'Это сочетание отвечает местным требованиям к передовым конфигурациям, грузоподъёмности, комфорту вождения и интеллектуальным функциям, привлекая толпы клиентов на тест-драйвы и консультации во время выставки.'),
        
        ('Consistently upholding its mission of &quot;Making favorite and reliable trucks&quot;. SAG INTL continues to deepen its understanding of user needs, drive technological innovation, and elevate product performance to deliver exceptional value for global customers.',
         'Последовательно придерживаясь миссии &quot;Создаём любимые и надёжные грузовики&quot;, SAG INTL продолжает углублять понимание потребностей пользователей, стимулировать технологические инновации и повышать производительность продукции для предоставления исключительной ценности клиентам по всему миру.'),
    ],
}


def apply_global_replacements(filepath):
    """Apply global replacements to a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = 0
    for old, new in GLOBAL_REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            fixes += 1
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes
    return 0


def apply_file_specific(filepath, replacements):
    """Apply file-specific replacements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            fixes += 1
        else:
            print(f"  WARNING: Pattern not found: {old[:80]}...")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes
    return 0


def main():
    total_global = 0
    total_specific = 0
    files_modified = 0
    
    # Walk all HTML files
    for root, dirs, files in os.walk(BASE):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            relpath = os.path.relpath(fpath, BASE)
            
            # Apply global replacements
            gfixes = apply_global_replacements(fpath)
            if gfixes > 0:
                total_global += gfixes
                files_modified += 1
                print(f"  [GLOBAL] {relpath}: {gfixes} fixes")
            
            # Apply file-specific if available
            if relpath in FILE_SPECIFIC:
                sfixes = apply_file_specific(fpath, FILE_SPECIFIC[relpath])
                total_specific += sfixes
                print(f"  [SPECIFIC] {relpath}: {sfixes} fixes")
    
    print(f"\n=== FINAL PASS COMPLETE ===")
    print(f"Global fixes: {total_global} across {files_modified} files")
    print(f"File-specific fixes: {total_specific}")
    print(f"Total fixes: {total_global + total_specific}")


if __name__ == '__main__':
    main()
