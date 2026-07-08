#!/usr/bin/env python3
"""
俄语版网站全页面批量修复
扫描所有HTML/JS/JSON文件，修复遗漏的英文文本
"""

import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 通用替换 — 应用于所有HTML文件
# (old, new, replace_all)
GLOBAL_FIXES = [
    # === 导航下拉子菜单项 (所有页面内联导航) ===
    ('<li><a href="qyc.html">Port Transport</a></li>',
     '<li><a href="qyc.html">Портовые перевозки</a></li>', False),
    ('<li><a href="qyc.html#c_product_list_152-16902759283320">Hazardous Chemicals Transport</a></li>',
     '<li><a href="qyc.html#c_product_list_152-16902759283320">Перевозка опасных химикатов</a></li>', False),
    ('<li><a href="qyc.html#c_product_list_152-16902759511700">Coal Transport</a></li>',
     '<li><a href="qyc.html#c_product_list_152-16902759511700">Перевозка угля</a></li>', False),
    ('<li><a href="qyc.html#c_product_list_152-16902759295540">Sand And Gravel Transport</a></li>',
     '<li><a href="qyc.html#c_product_list_152-16902759295540">Перевозка песка и гравия</a></li>', False),
    ('<li><a href="zxc.html">Urban Construction</a></li>',
     '<li><a href="zxc.html">Городское строительство</a></li>', False),
    ('<li><a href="zxc.html#c_product_list_152-16902759962030">Mining</a></li>',
     '<li><a href="zxc.html#c_product_list_152-16902759962030">Горная добыча</a></li>', False),
    ('<li><a href="zhc.html">Express Delivery</a></li>',
     '<li><a href="zhc.html">Экспресс-доставка</a></li>', False),
    ('<li><a href="zhc.html#c_product_list_152-16902759962030">Intercity Logistics</a></li>',
     '<li><a href="zhc.html#c_product_list_152-16902759962030">Междугородняя логистика</a></li>', False),
    ('<li><a href="zhc.html#c_product_list_152-16915679157520">City Distribution</a></li>',
     '<li><a href="zhc.html#c_product_list_152-16915679157520">Городская дистрибуция</a></li>', False),
    ('<li><a href="special.html">City Transportation</a></li>',
     '<li><a href="special.html">Городской транспорт</a></li>', False),
    ('<li><a href="special.html#c_product_list_152-16889614330850">Smart Sanitation</a></li>',
     '<li><a href="special.html#c_product_list_152-16889614330850">Умная санитария</a></li>', False),
    ('<li><a href="special.html#c_product_list_152-16889616447540">Dangerous Goods Transportation</a></li>',
     '<li><a href="special.html#c_product_list_152-16889616447540">Перевозка опасных грузов</a></li>', False),
    ('<li><a href="special.html#c_product_list_152-16902780105800">Road Work &amp; Rescue</a></li>',
     '<li><a href="special.html#c_product_list_152-16902780105800">Дорожные работы и спасение</a></li>', False),

    # === Сервис 下拉 ===
    ('<li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>',
     '<li><a href="service_list/1674411748220751872.html">Напоминания о вождении</a></li>', False),

    # === Новости 下拉 ===
    ('<li><a href="news_list/1.html">News Center</a></li>',
     '<li><a href="news_list/1.html">Центр новостей</a></li>', False),

    # === О нас 下拉 ===
    ('<li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>',
     '<li><a href="about.html#c_category_427-16821721350130">Кто мы</a></li>', False),
    ('<li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>',
     '<li><a href="about.html#c_static_001-1682265886008">С чего мы начали</a></li>', False),
    ('<li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>',
     '<li><a href="about.html#c_static_001-16822977301490">Технологические инновации</a></li>', False),

    # === Contact Us (在各种位置的"Contact Us"链接) ===
    ('<li><a href="contact.html">Contact Us</a></li>',
     '<li><a href="contact.html">Свяжитесь с нами</a></li>', False),

    # === "Contact Us" 按钮文字 ===
    ('>Contact Us</a>', '>Свяжитесь с нами</a>', True),
    ('>Contact Us Today</a>', '>Свяжитесь с нами сегодня</a>', True),

    # === "Request a Quote" 按钮 ===
    ('>Request a Quote</a>', '>Запросить предложение</a>', True),
    ('>Request a Quote<', '>Запросить предложение<', True),

    # === "View Details" 按钮 ===
    ('>View Details</a>', '>Подробнее</a>', True),

    # === "MORE +" ===
    ('class="btn-link">MORE +</a>', 'class="btn-link">ПОДРОБНЕЕ +</a>', True),

    # === "Ready to Learn More?" ===
    ('<h2>Ready to Learn More?</h2>', '<h2>Готовы узнать больше?</h2>', True),

    # === "Technical Specifications" ===
    ('<h2>Technical Specifications</h2>', '<h2>Технические характеристики</h2>', True),

    # === "Available Variants" ===
    ('<h2>Available Variants</h2>', '<h2>Доступные варианты</h2>', True),

    # === "Key Features" ===
    ('<h2>Key Features</h2>', '<h2>Ключевые особенности</h2>', True),

    # === 产品变体名称 ===
    ('Stake Truck', 'Бортовой грузовик', True),
    ('Refrigerated Truck', 'Рефрижератор', True),
    ('Sprinkler Truck', 'Поливомоечная машина', True),
    ('Cement Mixer Truck', 'Автобетоносмеситель', True),
    ('Fuel Tanker Truck', 'Бензовоз', True),
    ('Fuel Tanker', 'Бензовоз', True),

    # === "Customer Service" ===
    ('<h2>Customer Service</h2>', '<h2>Обслуживание клиентов</h2>', True),
    ('<h3>Customer Service</h3>', '<h3>Обслуживание клиентов</h3>', True),

    # === "Service Hotline" ===
    ('<p class="hotline-label">Service Hotline</p>',
     '<p class="hotline-label">Горячая линия</p>', True),
    ('Service Hotline', 'Горячая линия', True),

    # === "Sales Service Hotline" ===
    ('Sales Service Hotline', 'Горячая линия продаж', True),

    # === "Long Warranty" ===
    ('<h3>Long Warranty</h3>', '<h3>Длительная гарантия</h3>', True),

    # === "Recommended Model" ===
    ('<h2 class="section-title">Recommended Model</h2>',
     '<h2 class="section-title">Рекомендуемые модели</h2>', True),

    # === Footer company info ===
    ('SAG Commercial Vehicle Company', 'SAGMOTO Коммерческий транспорт', True),
    ('Shaanxi Automobile Group Commercial Vehicle Co., Ltd.',
     'Shaanxi Automobile Group Commercial Vehicle Co., Ltd.', False),  # keep as is
    ('Shaanxi Automobile Holding Group Company',
     'Shaanxi Automobile Holding Group', False),  # reduce length

    # === Footer address ===
    ('Room 603A, Floor 6, Building B, Chanba Free Trade Center,',
     'Китай, провинция Шэньси, г. Сиань, район Чаньба,', False),
    ('No.777 Eurasia Avenue, Chanba Ecological District,',
     'Евразийский проспект, 777, Центр свободной торговли Чаньба,', False),
    ("Xi'an, Shaanxi, China", 'корпус B, этаж 6, офис 603A', False),

    # === "Add:" → "Адрес:" ===
    ('<p class="footer-addr">Add:', '<p class="footer-addr">Адрес:', True),

    # === "Tel:" / "E-mail:" / "Tel" / "E-mail" ===
    ('>Tel:</', '>Тел:</', True),
    ('>Tel<', '>Тел<', True),
    ('>E-mail:</', '>Эл. почта:</', True),
    ('>E-mail<', '>Эл. почта<', True),

    # === "Все rights reserved" ===
    ('Все rights reserved', 'Все права защищены', True),

    # === "Website Construction:" ===
    ('Website Construction: Power of Chinese Enterprises',
     'Сайт разработан: Power of Chinese Enterprises', True),

    # === "Business License" ===
    ('>Business License<', '>Бизнес-лицензия<', True),

    # === "SCROLL DOWN" ===
    ('<span>SCROLL DOWN</span>', '<span>ПРОКРУТИТЬ ВНИЗ</span>', True),

    # === "Making Favorite & Reliable Trucks." ===
    ('Making Favorite &amp; Reliable Trucks.',
     'Создаём любимые и надёжные грузовики.', True),
    ('Making Favorite & Reliable Trucks.',
     'Создаём любимые и надёжные грузовики.', True),

    # === "Marketing and Services" ===
    ('>Marketing and Services<', '>Маркетинг и услуги<', True),

    # === "Founded in 1968, Shaanxi Automobile..." in meta ===
    # These are too many variants. We'll handle meta separately.

    # === "language":"en" in tenant config ===
    ('"language":"en"', '"language":"ru"', True),

    # === Page object names with mixed RU/EN ===
    ('"Спецтехника vehicle"', '"Спецтехника"', True),
    ('"Внедорожные truck"', '"Внедорожные грузовики"', True),
    ('"Cargo truck"', '"Грузовики"', True),
    ('"Внедорожные dump truck"', '"Внедорожные самосвалы"', True),

    # === Working Hours ===
    ('Working Hours:', 'Часы работы:', True),
    ('Mon-Fri, 8:30 AM - 5:30 PM (GMT+8)',
     'Пн-Пт, 8:30 - 17:30 (GMT+8)', True),

    # === Headquarters / Contact Details ===
    ('<h3>Headquarters</h3>', '<h3>Штаб-квартира</h3>', True),
    ('<h3>International Trade Office</h3>', '<h3>Отдел международной торговли</h3>', True),
    ('<h3>Contact Details</h3>', '<h3>Контактная информация</h3>', True),

    # === Quality Management ===
    ('<h3>Quality Management</h3>', '<h3>Управление качеством</h3>', True),

    # === Product Certification ===
    ('<h3>Product Certification</h3>', '<h3>Сертификация продукции</h3>', True),

    # === Innovation-Driven ===
    ('Innovation-Приводn Positive Development Cycle',
     'Инновационный цикл позитивного развития', True),
]


def fix_file(filepath):
    """Apply all global fixes to a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    for old, new, replace_all in GLOBAL_FIXES:
        if old not in content:
            continue
        if replace_all:
            count = content.count(old)
            content = content.replace(old, new)
            changes += count
        else:
            content = content.replace(old, new, 1)
            changes += 1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes


def main():
    # 收集所有HTML文件
    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # 排除不需要的目录
        dirs[:] = [d for d in dirs if d not in ('.mirror_raw', '__pycache__', 'videos', '.git')]
        for f in files:
            if f.endswith('.html') or f.endswith('.js') or f.endswith('.json'):
                html_files.append(os.path.join(root, f))

    total_changes = 0
    changed_files = 0

    for fpath in sorted(html_files):
        relpath = os.path.relpath(fpath, BASE_DIR)
        changes = fix_file(fpath)
        if changes > 0:
            print(f"  ✅ {relpath}: {changes} замен(ы)")
            total_changes += changes
            changed_files += 1

    print(f"\n📊 Файлов изменено: {changed_files}")
    print(f"📊 ИТОГО замен: {total_changes}")


if __name__ == '__main__':
    main()
