#!/usr/bin/env python3
"""Update navigation in existing pages to match index.html (latest version)."""

from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent

# The correct navigation HTML (extracted from index.html's ul.main-nav)
NEW_NAV = '''<li class="has-dropdown">
                    <a href="products.html">PRODUCTS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <div class="dropdown-mega">
                        <div class="mega-inner">
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Light Duty Truck(4.5T&le;GCW&le;25T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/ef3451b4-d300-4c3d-92c5-dab5f29efb6f.png" alt="i9"> i9</a></li>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/175cc731-094c-4946-880b-90aa3a1a867e.png" alt="X9"> X9</a></li>
                                    <li><a href="products.html?cat=light-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0630693e-37e8-43be-98dd-acbdb49c70c9.png" alt="X7"> X7</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Medium Duty Truck(12T&le;GCW&le;60T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/64c3428c-c60f-4579-ac04-e561cbe8c772.png" alt="E6"> E6</a></li>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/8ae116ac-60cf-4da2-b2cb-ac4c80b04b92.png" alt="X6"> X6</a></li>
                                    <li><a href="products.html?cat=medium-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/d2bf1d4c-09c4-426a-895a-bd8f6aba5a63.jpg" alt="X5"> X5</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Heavy Duty Truck(18T&le;GCW&le;100T)</h4>
                                <ul>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/84912c76-6629-4d69-ad59-d8da5940fbb4.jpg" alt="E1st"> E1st</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/a32c4261-9dac-4e68-87f7-c037b5a56733.jpg" alt="Z3"> Z3</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/0d2ddb14-41e9-4f6c-b60a-1b53fa89e0f3.png" alt="E3"> E3</a></li>
                                    <li><a href="products.html?cat=heavy-duty"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/9aa95967-f314-494d-adbe-05935dee2d6c.png" alt="E9"> E9</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4 class="mega-cat-title">Off-road Truck</h4>
                                <ul>
                                    <li><a href="products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/fd557db0-8dc9-4c44-af5a-a0a89b608fc6.jpg" alt="Off-road"> Off-road Dump</a></li>
                                    <li><a href="products.html?cat=off-road"><img src="https://omo-oss-image.thefastimg.com/portal-saas/new2023032811535752050/cms/image/2f71c746-9325-462d-96c7-2f59c4c7503e.jpg" alt="X3s"> X3s</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>
                <li class="has-dropdown">
                    <a href="javascript:;">APPLICATIONS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu dropdown-wide">
                        <li class="dropdown-group"><a href="qyc.html" class="dropdown-group-title">Tractor</a>
                            <ul class="dropdown-sub">
                                <li><a href="qyc.html">Port Transport</a></li>
                                <li><a href="qyc.html#hazchem">Hazardous Chemicals Transport</a></li>
                                <li><a href="qyc.html#coal">Coal Transport</a></li>
                                <li><a href="qyc.html#sand">Sand And Gravel Transport</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="zxc.html" class="dropdown-group-title">Dump Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="zxc.html">Urban Construction</a></li>
                                <li><a href="zxc.html#mining">Mining</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="zhc.html" class="dropdown-group-title">Cargo Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="zhc.html">Express Delivery</a></li>
                                <li><a href="zhc.html#intercity">Intercity Logistics</a></li>
                                <li><a href="zhc.html#city-dist">City Distribution</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="special.html" class="dropdown-group-title">Special Vehicle</a>
                            <ul class="dropdown-sub">
                                <li><a href="special.html">City Transportation</a></li>
                                <li><a href="special.html#sanitation">Smart Sanitation</a></li>
                                <li><a href="special.html#dangerous-goods">Dangerous Goods Transportation</a></li>
                                <li><a href="special.html#rescue">Road Work &amp; Rescue</a></li>
                            </ul></li>
                        <li class="dropdown-group"><a href="pzkyzyc.html" class="dropdown-group-title">Off-road Truck</a>
                            <ul class="dropdown-sub">
                                <li><a href="pzkyzyc.html">Off-road Dump Truck</a></li>
                                <li><a href="pzmtc.html">Off-road Tractor</a></li>
                            </ul></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="service.html">SERVICES <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="service.html">Service Policy</a></li>
                        <li><a href="service_list/1674411714944516096.html">Find Your Service Provider</a></li>
                        <li><a href="service_list/1674411730417303552.html">Maintenance Service</a></li>
                        <li><a href="service_list/1674411748220751872.html">Driving Reminder</a></li>
                        <li><a href="service_list/1674411767427842048.html">Safe Driving</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="news_list/1.html">NEWS <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="news_list/1.html">News Center</a></li>
                        <li><a href="video_list.html">Video Center</a></li>
                    </ul>
                </li>
                <li class="has-dropdown">
                    <a href="about.html">ABOUT US <svg class="nav-arrow" viewBox="0 0 1024 1024" width="10" height="10"><path d="M761.056 532.128c.513-.993 1.344-1.823 1.792-2.849 8.8-18.304 5.92-40.703-9.664-55.424L399.936 139.744c-19.264-18.208-49.632-17.345-67.872 1.889-18.208 19.264-17.376 49.63 1.889 67.872l316.96 299.84L335.2 813.63c-19.072 18.4-19.648 48.768-1.247 67.872 9.407 9.792 21.984 14.69 34.56 14.69 12 0 24-4.48 33.312-13.44l350.048-337.376z" fill="currentColor"/></svg></a>
                    <ul class="dropdown-menu">
                        <li><a href="about.html#c_category_427-16821721350130">Who We Are</a></li>
                        <li><a href="about.html#c_static_001-1682265886008">When We Started</a></li>
                        <li><a href="about.html#c_static_001-16822977301490">Technological Innovation</a></li>
                        <li><a href="Contact.html">Contact Us</a></li>
                    </ul>
                </li>
                <li class="nav-search"><a href="#" onclick="event.preventDefault();"><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></a></li>'''


def update_nav_in_file(filepath):
    """Replace the ul.main-nav content in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    nav_ul = soup.find('ul', class_='main-nav')
    
    if not nav_ul:
        print(f"  SKIP: {filepath.name} (no ul.main-nav found)")
        return False
    
    # Clear current nav items
    nav_ul.clear()
    
    # Parse the new nav HTML and append to the ul
    new_nav_soup = BeautifulSoup(NEW_NAV, 'html.parser')
    for child in list(new_nav_soup.children):
        if hasattr(child, 'name'):  # skip NavigableStrings
            nav_ul.append(child)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  OK: {filepath.name}")
    return True


def main():
    pages = ['about.html', 'contact.html', 'products.html', 'news.html']
    
    ok = 0
    for page in pages:
        filepath = BASE_DIR / page
        if filepath.exists() and update_nav_in_file(filepath):
            ok += 1
    
    print(f"\nDone! Updated {ok}/{len(pages)} pages.")


if __name__ == '__main__':
    main()
