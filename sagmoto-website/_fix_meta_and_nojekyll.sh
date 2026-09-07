#!/bin/bash
# Fix sagmoto site HTML meta tags and add .nojekyll
# Run from sagmoto repo root

echo "=== Fix 1: products.html - move meta inside head ==="
# Currently: line 18 is </head>, line 19 is <meta name="description">
# Need to move meta before </head>

echo "=== Fix 2: contact.html - move meta inside head ==="
# Same issue

echo "=== Fix 3: Add .nojekyll ==="
touch .nojekyll

echo "Done. Now: git add -A && git commit -m 'Fix meta tags and add .nojekyll' && git push"
