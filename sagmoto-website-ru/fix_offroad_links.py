import os
import re
import glob

WEBSITE_DIR = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\sagmoto-website"

# Files to process (HTML only, not subdirectories)
html_files = glob.glob(os.path.join(WEBSITE_DIR, "*.html"))
# Also include service_list and news_list HTML files
html_files += glob.glob(os.path.join(WEBSITE_DIR, "service_list", "*.html"))
html_files += glob.glob(os.path.join(WEBSITE_DIR, "news_list", "*.html"))

changes_log = []

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    filename = os.path.basename(filepath)
    
    # 1. Fix APPLICATIONS dropdown group title: Off-road Truck -> tzc.html
    # Pattern: <li class="dropdown-group"><a class="dropdown-group-title" href="pzkyzyc.html">Off-road Truck</a>
    content = re.sub(
        r'(<li class="dropdown-group"><a class="dropdown-group-title" href=")pzkyzyc.html(">Off-road Truck</a>)',
        r'\1tzc.html\2',
        content
    )
    
    # 2. Fix footer APPLICATIONS: Off-road Truck -> tzc.html
    # Pattern: <li><a href="pzkyzyc.html">Off-road Truck</a></li>  (in footer context)
    # We need to be careful not to change the dropdown sub-item links
    # The footer links usually appear in <div class="footer-col"> section
    # Simple approach: replace <li><a href="pzkyzyc.html">Off-road Truck</a></li>
    content = re.sub(
        r'(<li><a href=")pzkyzyc.html(">Off-road Truck</a></li>)',
        r'\1tzc.html\2',
        content
    )
    
    # 3. Add New Energy to footer APPLICATIONS if not already present
    # Look for pattern: <li><a href="tzc.html">Off-road Truck</a></li>
    # and add <li><a href="new-energy.html">New Energy</a></li> after it if not present
    if '<li><a href="new-energy.html">New Energy</a></li>' not in content:
        content = re.sub(
            r'(<li><a href="tzc.html">Off-road Truck</a></li>)(\s*</ul>)',
            r'\1\n<li><a href="new-energy.html">New Energy</a></li>\2',
            content
        )
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        changes_log.append(filename)

print(f"Modified {len(changes_log)} files:")
for f in changes_log:
    print(f"  - {f}")
