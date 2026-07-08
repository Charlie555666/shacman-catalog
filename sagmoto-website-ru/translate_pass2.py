#!/usr/bin/env python3
"""
SAGMOTO RU - Second pass translation fix
Handles breadcrumbs, untranslated article content, page-specific text.
"""
import os, re

BASE = r'c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website-ru'

# Additional translations for content missed in first pass
FIXES = [
    # === Breadcrumb and navigation fixes ===
    ('<span>News</span>', '<span>Новости</span>'),
    ('<span>Article</span>', '<span>Статья</span>'),
    ('<span>About</span>', '<span>О нас</span>'),
    ('<span>Contact</span>', '<span>Контакты</span>'),
    ('<span>Products</span>', '<span>Продукция</span>'),
    ('<span>Videos</span>', '<span>Видео</span>'),
    
    # === Products.json "wheel drive" residual ===
    ('Все wheel drive', 'Полный привод'),
    
    # === html lang ===
    ('<html lang="en">', '<html lang="ru">'),
    
    # === Canonical URLs ===
    ('sagmoto-website/', 'sagmoto-website-ru/'),
    
    # === Meta OG ===
    ('property="og:title" content="Shaanxi Fenghan Trading', 
     'property="og:title" content="Shaanxi Fenghan Trading'),
    
    # === News detail titles ===
    ("Intelligent Production of Тяжёлые Trucks at Shaanxi Automobile", 
     "Интеллектуальное производство тяжёлых грузовиков на заводе Shaanxi Automobile"),
    ("Intelligent Production of Heavy Trucks at Shaanxi Automobile's Factory", 
     "Интеллектуальное производство тяжёлых грузовиков на заводе Shaanxi Automobile"),
    
    # === News detail alt text ===
    ('alt="Intelligent Production of Тяжёлые Trucks', 'alt="Интеллектуальное производство тяжёлых грузовиков'),
    
    # === News detail article bodies (key paragraphs only) ===
    ('The intelligent production facility for heavy trucks with alternative drive systems, operated by Shaanxi Automobile Holding Group Co., Ltd. in the Jingkai District of Xi',
     'Завод интеллектуального производства тяжёлых грузовиков с альтернативными системами привода, управляемый Shaanxi Automobile Holding Group Co., Ltd. в районе Цзинкай города Си'),
    ('is a prime example of advanced manufacturing expertise.',
     'является образцом передового производственного опыта.'),
    ('This production line can assemble multiple models simultaneously and has an annual capacity of 50,000 heavy truck chassis and 100,000 cabs,',
     'Эта производственная линия может одновременно собирать несколько моделей и имеет годовую мощность 50 000 шасси тяжёлых грузовиков и 100 000 кабин,'),
    ('explained Ji Xiang, deputy manager of Shaanxi Automobile',
     'пояснил Цзи Сян, заместитель директора сборочного завода Shaanxi Automobile'),
    
    # === Key words ===
    ('Key words:', 'Ключевые слова:'),
    ('Key words：', 'Ключевые слова:'),
    
    # === News "Previous / Next" if exists ===
    ('Previous', 'Предыдущая'),
    ('Next', 'Следующая'),
    ('Back to list', 'Вернуться к списку'),
    
    # === About page history headlines (translate key ones) ===
    ('The 135th Canton Fair was successfully concluded',
     '135-я Кантонская ярмарка успешно завершилась'),
    ('Shaanxi Automobile Commercial Vehicle Company released its E1st brand of heavy trucks',
     'Shaanxi Automobile Commercial Vehicle Company представила бренд тяжёлых грузовиков E1st'),
    ('SAGMOTO Participating China Import & Export Fair',
     'SAGMOTO участвует в Китайской ярмарке импорта и экспорта'),
    ('SAGMOTO Assist in engineering',
     'SAGMOTO помогает в инженерных проектах'),
    ('Make great efforts and work hard together',
     'Прилагать большие усилия и усердно работать вместе'),
    ('SAG Commercial Vehicle Company won the',
     'SAG Commercial Vehicle Company получила награду'),
    ('National Machinery Industry Quality Award',
     '«Национальная премия качества машиностроительной отрасли»'),
    
    # === Service page common phrases ===
    ('After-sales service', 'Послепродажное обслуживание'),
    ('Service commitment', 'Сервисные обязательства'),
    ('Warranty policy', 'Гарантийная политика'),
    ('Spare parts supply', 'Поставка запасных частей'),
    ('Technical support', 'Техническая поддержка'),
    ('Training service', 'Услуги обучения'),
    ('Service network', 'Сервисная сеть'),
    ('Maintenance', 'Техническое обслуживание'),
    ('Repair', 'Ремонт'),
    ('Quality assurance', 'Гарантия качества'),
    
    # === Application page common phrases ===
    ('Application scenarios', 'Сценарии применения'),
    ('Product features', 'Характеристики продукции'),
    ('Technical parameters', 'Технические параметры'),
    ('Product advantages', 'Преимущества продукции'),
    
    # === Tractor page ===
    ('Tractor series', 'Серия тягачей'),
    ('Tractor products', 'Продукция тягачей'),
    
    # === Dump truck page ===
    ('Dump truck series', 'Серия самосвалов'),
    
    # === Cargo truck page ===
    ('Cargo truck series', 'Серия грузовиков'),
    
    # === Special vehicle page ===
    ('Special vehicle series', 'Серия спецтехники'),
    
    # === Off-road pages ===
    ('Off-road truck series', 'Внедорожная серия'),
    ('Off-road dump truck series', 'Серия внедорожных самосвалов'),
    ('Off-road tractor series', 'Серия внедорожных тягачей'),
    
    # === About page history entries ===
    ('On November 5th, the nationally recognised enterprise technology centre and post-doctoral research station was established.',
     '5 ноября был создан национально признанный центр корпоративных технологий и постдокторская исследовательская станция.'),
    ('In September, Shaanxi Automobile Group Company has become the first enterprise that has the production and sale exceeding 10 billion CNY in',
     'В сентябре Shaanxi Automobile Group Company стала первым предприятием, объём производства и продаж которого превысил 10 млрд юаней в'),
    ('equipment manufacturing industry',
     'машиностроительной отрасли'),
    ('of Shaanxi Province.',
     'провинции Шэньси.'),
    ('Shaanxi Automobile Group Company and MAN(Germany) signed an agreement on the introduction of MAN heavy truck technology at the State Guest House in Beijing.',
     'Shaanxi Automobile Group Company и MAN (Германия) подписали соглашение о внедрении технологии тяжёлых грузовиков MAN в Государственной резиденции в Пекине.'),
    ('In September, Shaanxi Automobile Group Company has become the first enterprise',
     'В сентябре Shaanxi Automobile Group Company стала первым предприятием'),
    ('In September, Shaanxi Automobile Group Company has become the first enterprise in Shaanxi Province equipment manufacturing industry with production and sales exceeding 10 billion CNY.',
     'В сентябре Shaanxi Automobile Group Company стала первым предприятием машиностроительной отрасли провинции Шэньси с объёмом производства и продаж, превышающим 10 млрд юаней.'),
    
    # === Video center breadcrumb and other fixes ===
    ('Video Center-SAG Commercial Vehicle Company',
     'Видеоцентр — SAG Commercial Vehicle Company'),
    ('News Centre-SAG Commercial Vehicle Company',
     'Новостной центр — SAG Commercial Vehicle Company'),
    
    # === Timestamp display text ===
    ('Published', 'Опубликовано'),
    ('Date', 'Дата'),
    ('Read more', 'Читать далее'),
    ('View more', 'Смотреть ещё'),
    ('Learn more', 'Узнать больше'),
    
    # === Contact form labels (extra variants) ===
    ('Name', 'Имя'),
    ('Message', 'Сообщение'),
    ('Submit', 'Отправить'),
    
    # === Home page hero text if any remains ===
    ('Your Trusted Partner for Chinese Commercial Vehicles',
     'Ваш надёжный партнёр по коммерческим автомобилям из Китая'),
    ('Authorized SAGMOTO Exporter',
     'Авторизованный экспортёр SAGMOTO'),
    ('Serving 50+ Countries Worldwide',
     'Обслуживаем более 50 стран мира'),
    ('Explore Products',
     'Смотреть продукцию'),
    
    # === 404 or not found ===
    ('Page not found', 'Страница не найдена'),
    ('Back to Home', 'На главную'),
    
    # === Model series intro text ===
    ('Flagship Tractor Truck Series', 'Флагманская серия тягачей'),
    ('Heavy-Duty Tractor Series', 'Серия тяжёлых тягачей'),
    ('Medium-Duty Truck Series', 'Серия среднетоннажных грузовиков'),
    ('Light-Duty Truck Series', 'Серия лёгких грузовиков'),
    ('Electric Commercial Vehicle Series', 'Серия электрических коммерческих автомобилей'),
    ('Off-Road Truck Series', 'Внедорожная серия грузовиков'),
    
    # === SAGMOTO brand copy ===
    ('SAGMOTO is the commercial vehicle brand', 'SAGMOTO — бренд коммерческих автомобилей'),
    ('one of China', 'одного из'),
    ('leading commercial vehicle manufacturers', 'ведущих производителей коммерческого транспорта Китая'),
    ('With decades of engineering excellence, SAGMOTO delivers reliable, efficient, and innovative commercial vehicles to customers worldwide.',
     'Благодаря десятилетиям инженерного мастерства SAGMOTO поставляет надёжные, эффективные и инновационные коммерческие автомобили клиентам по всему миру.'),
]


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    for old, new in FIXES:
        if old in content:
            content = content.replace(old, new)
            changes += 1
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, 0


def main():
    total = 0
    files_changed = 0
    
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ('.mirror_raw', 'videos', '__pycache__', 'node_modules', 'admin')]
        for f in files:
            if f.endswith(('.html', '.js', '.json')):
                filepath = os.path.join(root, f)
                changed, count = fix_file(filepath)
                if changed:
                    files_changed += 1
                    total += count
                    print(f"  ✓ {os.path.relpath(filepath, BASE)} ({count} fixes)")
    
    print(f"\nSecond pass complete: {files_changed} files, {total} fixes")


if __name__ == '__main__':
    main()
