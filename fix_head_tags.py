#!/usr/bin/env python3
"""Fix missing </head> tags in main sagmoto-website pages."""
import os
import re

base = os.path.dirname(os.path.abspath(__file__))
sagmoto = os.path.join(base, "sagmoto-website")

pages = [
    "service.html", "qyc.html", "zxc.html", "zhc.html",
    "special.html", "pzkyzyc.html", "pzmtc.html", "tzc.html",
    "video_list.html"
]

fixed = 0
for page in pages:
    filepath = os.path.join(sagmoto, page)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if </head> is already present before <body>
    if "</head>" in content:
        print(f"  SKIP {page} - already has </head>")
        continue

    # Replace the pattern: <title>...</title>\n<body> with <title>...</title>\n</head>\n<body>
    new_content = re.sub(
        r'(</title>)\s*\n(<body>)',
        r'\1\n</head>\n\2',
        content
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  FIXED {page}")
        fixed += 1
    else:
        print(f"  WARN {page} - pattern not found")

print(f"\nTotal fixed: {fixed}/{len(pages)}")
