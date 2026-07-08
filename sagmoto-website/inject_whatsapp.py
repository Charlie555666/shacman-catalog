"""Inject WhatsApp floating button <script> tag before </body> in all HTML files."""
import os, glob, re

SCRIPT_TAG = '<script src="js/whatsapp-float.js"></script>'
SCRIPT_TAG_PARENT = '<script src="../js/whatsapp-float.js"></script>'

def inject_file(filepath, tag):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already injected
    if 'whatsapp-float.js' in content:
        return False, 'already injected'
    
    # Skip if no </body>
    if '</body>' not in content:
        return False, 'no </body>'
    
    # Insert before </body>
    new_content = content.replace('</body>', f'{tag}\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, 'injected'

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    
    # English site
    en_dir = base
    count_en = 0
    
    # Top-level pages
    for f in sorted(glob.glob(os.path.join(en_dir, '*.html'))):
        ok, msg = inject_file(f, SCRIPT_TAG)
        if ok:
            count_en += 1
            rel = os.path.relpath(f, base)
            print(f'  [EN] {rel}')
    
    # Sub-directory pages
    for subdir in ['news_Detail', 'news_list', 'service_list']:
        sub = os.path.join(en_dir, subdir)
        if os.path.isdir(sub):
            for f in sorted(glob.glob(os.path.join(sub, '*.html'))):
                ok, msg = inject_file(f, SCRIPT_TAG_PARENT)
                if ok:
                    count_en += 1
                    rel = os.path.relpath(f, base)
                    print(f'  [EN] {rel}')
    
    # Russian site
    ru_dir = os.path.join(os.path.dirname(base), 'sagmoto-website-ru')
    count_ru = 0
    
    if os.path.isdir(ru_dir):
        for f in sorted(glob.glob(os.path.join(ru_dir, '*.html'))):
            ok, msg = inject_file(f, SCRIPT_TAG)
            if ok:
                count_ru += 1
                rel = os.path.relpath(f, ru_dir)
                print(f'  [RU] {rel}')
        
        for subdir in ['news_Detail', 'news_list', 'service_list']:
            sub = os.path.join(ru_dir, subdir)
            if os.path.isdir(sub):
                for f in sorted(glob.glob(os.path.join(sub, '*.html'))):
                    ok, msg = inject_file(f, SCRIPT_TAG_PARENT)
                    if ok:
                        count_ru += 1
                        rel = os.path.relpath(f, ru_dir)
                        print(f'  [RU] {rel}')
    
    print(f'\nDone! English: {count_en} files, Russian: {count_ru} files')

if __name__ == '__main__':
    main()
