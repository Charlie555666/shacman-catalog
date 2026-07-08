#!/usr/bin/env python3
"""Replace old phone number 0086-029-86119719 with +86 15319431311 across all HTML/JS files."""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_NUM = "0086-029-86119719"
NEW_NUM = "+86 15319431311"
NEW_NUM_TEL = "+8615319431311"  # no spaces for tel: links

count = 0

for root, dirs, files in os.walk(BASE_DIR):
    # Skip subdirs that are not part of this site
    dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules'}]

    for fname in files:
        if not (fname.endswith('.html') or fname.endswith('.js')):
            continue

        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Replace tel: links first
        content = content.replace(f'href="tel:{OLD_NUM}"', f'href="tel:{NEW_NUM_TEL}"')
        content = content.replace(f"href='tel:{OLD_NUM}'", f"href='tel:{NEW_NUM_TEL}'")

        # Replace remaining display text occurrences
        content = content.replace(OLD_NUM, NEW_NUM)

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            n = original.count(OLD_NUM)
            print(f"  {fpath}: {n} replacements")
            count += n

print(f"\nTotal replacements: {count}")
