#!/usr/bin/env python3
"""
Renumber LaTeX citations in thesis.tex by order of first appearance.
Supports placeholders like [T31], [T32] that will be renumbered.
Also supports multi-citations like [3,5,7].
"""
import re
import sys

THESIS = "d:/HealthAgent/docs/thesis.tex"

with open(THESIS, "r", encoding="utf-8") as f:
    text = f.read()

# Find all \textsuperscript{[...]} patterns and extract labels in order
cite_re = re.compile(r'\\textsuperscript\{\[([^\]]+)\]\}')
seen = {}  # label -> None (pending assignment)
order = []  # unique labels in first-appearance order

for m in cite_re.finditer(text):
    labels = [lbl.strip() for lbl in m.group(1).split(',')]
    for lbl in labels:
        if lbl not in seen:
            seen[lbl] = None
            order.append(lbl)

# Assign new numbers 1..N
for i, lbl in enumerate(order, 1):
    seen[lbl] = str(i)

print(f"Found {len(order)} unique citation labels", file=sys.stderr)
for lbl, num in seen.items():
    print(f"  {lbl} -> [{num}]", file=sys.stderr)

# Replace citations in body text
def replace_cite(m):
    labels = [lbl.strip() for lbl in m.group(1).split(',')]
    new_labels = [seen.get(lbl, lbl) for lbl in labels]
    return '\\textsuperscript{[' + ','.join(new_labels) + ']}'

new_text = cite_re.sub(replace_cite, text)

# Replace \item[Tnn] in bibliography
item_re = re.compile(r'\\item\s*\[([^\]]+)\]')
def replace_item(m):
    lbl = m.group(1).strip()
    if lbl in seen:
        return '\\item [' + seen[lbl] + ']'
    return m.group(0)

new_text = item_re.sub(replace_item, new_text)

with open(THESIS, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Done renumbering.", file=sys.stderr)
