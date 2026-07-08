#!/usr/bin/env python3
"""
俄语版网站第三轮精细化翻译修复
修复所有遗漏的英文文本：导航下拉子菜单、Hero大图标题、产品描述、section标题、按钮文字等
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# (old, new, replace_all)
# replace_all=True: 替换所有出现 (用于重复出现且意思相同的文本)
# replace_all=False: 仅替换第一个出现 (用于可能重复但上下文不同的文本)
FIXES = [
    # ===== 1. 导航 mega menu 右栏 =====
    ('<div class="mega-right-title">Marketing and Services</div>',
     '<div class="mega-right-title">Маркетинг и услуги</div>', False),
    ('<div class="mega-phone-label">Sales Service Hotline:</div>',
     '<div class="mega-phone-label">Горячая линия продаж:</div>', False),
    ('<a href="contact.html"><span>Request a Quote</span>',
     '<a href="contact.html"><span>Запросить предложение</span>', False),

    # ===== 2. 导航 ПРИМЕНЕНИЕ 下拉子菜单 =====
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

    # ===== 3. СЕРВИС / НОВОСТИ / О НАС 子项 =====
    ('<li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>',
     '<li><a href="service_list/1674411748220751872.html">Напоминания о вождении</a></li>', False),
    ('<li><a href="news_list/1.html">News Center</a></li>',
     '<li><a href="news_list/1.html">Центр новостей</a></li>', False),
    ('<li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>',
     '<li><a href="about.html#c_category_427-16821721350130">Кто мы</a></li>', False),
    ('<li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>',
     '<li><a href="about.html#c_static_001-1682265886008">С чего мы начали</a></li>', False),
    ('<li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>',
     '<li><a href="about.html#c_static_001-16822977301490">Технологические инновации</a></li>', False),
    ('<li><a href="contact.html">Contact Us</a></li>',
     '<li><a href="contact.html">Свяжитесь с нами</a></li>', False),

    # ===== 4. Hero 按钮和文字 =====
    ('class="btn-link">MORE +</a>', 'class="btn-link">ПОДРОБНЕЕ +</a>', True),
    ('<span>SCROLL DOWN</span>', '<span>ПРОКРУТИТЬ ВНИЗ</span>', False),

    # ===== 5. Hero大图标题 =====
    ('<h2>Hailar Extreme Cold Testing</h2>',
     '<h2>Экстремальные испытания на морозе в Хайларе</h2>', False),
    ('<h2>Z3 CONVENTIONAL TRACTOR</h2>',
     '<h2>Z3 КЛАССИЧЕСКИЙ ТЯГАЧ</h2>', False),
    ('<h2>Кабина strength meets the latest European ECER29-03 collision standard</h2>',
     '<h2>Прочность кабины соответствует новейшему европейскому стандарту ECER29-03</h2>', False),
    ('<p class="p_summary">Make Favorite &amp; Reliable Trucks</p>',
     '<p class="p_summary">Создаём любимые и надёжные грузовики</p>', True),
    ('<h2>Make Favorite &amp; Reliable Trucks</h2>',
     '<h2>Создаём любимые и надёжные грузовики</h2>', False),
    ('<p class="p_summary">A full range and digitalized commercial vehicle industrial base integrates product R&amp;D, manufacturing, testing and debugging, marketing, and after-sales service</p>',
     '<p class="p_summary">Полный спектр и цифровая промышленная база коммерческого транспорта, объединяющая НИОКР, производство, испытания, маркетинг и послепродажное обслуживание</p>', False),

    # ===== 6. Tagline =====
    ('<div class="tagline-text">Making Favorite &amp; Reliable Trucks.</div>',
     '<div class="tagline-text">Создаём любимые и надёжные грузовики.</div>', True),

    # ===== 7. Recommended Model section =====
    ('<h2 class="section-title">Recommended Model</h2>',
     '<h2 class="section-title">Рекомендуемые модели</h2>', False),

    # ===== 8. 产品描述残余英文 (tab0 Light) =====
    ("<p class=\"pg-desc\">4×4, Полный привод, Leaf-springs suspension, main and sub-springs' structure, strong bearing capacity, simple structure, low maintenance cost.</p>",
     '<p class="pg-desc">4×4, Полный привод, листовые рессоры с основной и дополнительной структурой, высокая несущая способность, простая конструкция, низкие затраты на обслуживание.</p>', False),
    ("<p class=\"pg-desc\">Extra-long service intervals for engine, gearbox and rear axle, halving the number of 'pit stop'.</p>",
     '<p class="pg-desc">Увеличенные интервалы обслуживания двигателя, коробки передач и заднего моста, сокращение числа остановок на ТО вдвое.</p>', False),

    # ===== 9. 产品描述残余英文 (tab1 Medium) =====
    ('<h4><a href="x6.html">X6 Cement Mixers Truck</a></h4>',
     '<h4><a href="x6.html">X6 Автобетоносмеситель</a></h4>', False),
    ('alt="X6 Cement Mixers Truck">',
     'alt="X6 Автобетоносмеситель">', False),
    ('<p class="pg-desc">lightweight-design chassis, frame beam, suspension</p>',
     '<p class="pg-desc">облегчённое шасси, рама, подвеска</p>', False),

    # ===== 10. 笔误修正 =====
    ('26,97 л/100 кмkm', '26,97 л/100 км', False),

    # ===== 11. 产品描述残余英文 (tab3 Special) =====
    ('alt="X9 Aerial Work Platform Truck">',
     'alt="X9 Автовышка">', False),
    ('<h4><a href="x9.html">X9 Aerial Work Platform Truck</a></h4>',
     '<h4><a href="x9.html">X9 Автовышка</a></h4>', False),
    ('<p class="pg-desc">The truck has strong stability, convenient operation, flexible mobility, and is suitable for places with a wide range of work surfaces.</p>',
     '<p class="pg-desc">Автомобиль обладает высокой устойчивостью, удобным управлением и гибкой мобильностью, подходит для мест с широким спектром рабочих поверхностей.</p>', True),

    # ===== 12. 新闻卡片alt和标题 =====
    ('alt="SAGMOTO X3s Debuts in Armenia"',
     'alt="SAGMOTO X3s дебютирует в Армении"', False),
    ('alt="SAGMOTO at Canton Fair"',
     'alt="SAGMOTO на Кантонской ярмарке"', False),
    ('alt="SAGMOTO Chinese New Year 2025"',
     'alt="SAGMOTO Китайский Новый год 2025"', False),
    ("Caucasus' New Jewel SAGMOTO X3s Тягачи Debuts in Armenia",
     'Новая жемчужина Кавказа — тягач SAGMOTO X3s дебютирует в Армении', False),

    # ===== 13. 视频区域 =====
    ('<h2>Video Centre</h2>', '<h2>Видеоцентр</h2>', False),
    ("на заводе Shaanxi Automobile's Factory",
     'на заводе Shaanxi Automobile', True),
    ('alt="Caucasus New Jewel SAGMOTO X3s">',
     'alt="Новая жемчужина Кавказа SAGMOTO X3s">', False),
    ('alt="SAGMOTO at Canton Fair">',
     'alt="SAGMOTO на Кантонской ярмарке">', False),
    ('alt="SAGMOTO Chinese New Year">',
     'alt="SAGMOTO Китайский Новый год">', False),
    ('<div class="video-title">Caucasus\' New Jewel SAGMOTO X3s Тягачи Debuts in Armenia</div>',
     '<div class="video-title">Новая жемчужина Кавказа — тягач SAGMOTO X3s дебютирует в Армении</div>', False),

    # ===== 14. Contact Section =====
    ('<h2>Contact Us</h2>', '<h2>Свяжитесь с нами</h2>', False),
    ('<p>If you would like to contact us, please dial our phone number or leave us with your information by email. We will get in touch with you as soon as possible, pleased with your co-operation.</p>',
     '<p>Если вы хотите связаться с нами, позвоните по телефону или оставьте информацию по электронной почте. Мы свяжемся с вами как можно скорее. Благодарим за сотрудничество.</p>', False),
    ('<a href="contact.html" class="btn-submit">Отправить Feedback</a>',
     '<a href="contact.html" class="btn-submit">Отправить сообщение</a>', False),

    # ===== 15. Footer =====
    ('<p class="hotline-label">Service Hotline</p>',
     '<p class="hotline-label">Горячая линия</p>', False),
    ('<p class="footer-addr">Add: Китай',
     '<p class="footer-addr">Адрес: Китай', False),
    ('<p>Все rights reserved',
     '<p>Все права защищены', False),

    # ===== 16. 注释修正 =====
    ('<!-- ===== LATEST НОВОСТИ (matching sagmoto.com "Последние новости") ===== -->',
     '<!-- ===== ПОСЛЕДНИЕ НОВОСТИ ===== -->', False),
]


def apply_fixes(file_path, fixes):
    """Apply (old, new, replace_all) replacements to a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    total_changes = 0

    for old, new, replace_all in fixes:
        if old not in content:
            print(f"  ⚠️ NOT FOUND: {old[:70]}...")
            continue
        if replace_all:
            count = content.count(old)
            content = content.replace(old, new)
            total_changes += count
            print(f"  ✅ x{count}: {old[:60]}...")
        else:
            content = content.replace(old, new, 1)
            total_changes += 1
            print(f"  ✅: {old[:60]}...")

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return total_changes


def main():
    index_path = os.path.join(BASE_DIR, 'index.html')
    print(f"\n📄 Обработка: {index_path}")
    t = apply_fixes(index_path, FIXES)
    print(f"\n📊 ИТОГО замен: {t}")


if __name__ == '__main__':
    main()
